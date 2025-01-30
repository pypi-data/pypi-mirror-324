# MIT License
#
# Copyright (c) 2024 Chronulus AI Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import base64
import json
import pickle
import time
from datetime import datetime
from typing import Tuple, TypeVar, Type, Optional

import requests
from pydantic import BaseModel
from chronulus_core.types.response import QueuePredictionResponse, PredictionGetByIdResponse

from ..prediction import Forecast
from ..session import Session
from .base import Estimator, BaseModelSubclass, EstimatorCreationRequest


class NormalizedForecaster(Estimator):
    """
   A forecasting estimator that normalizes input data for time series predictions.

   This estimator handles the creation, queuing, and retrieval of normalized time series
   forecasts through the API. It supports various time horizons and can generate both
   numerical predictions and explanatory notes.

   Parameters
   ----------
   session : Session
       Active session instance for API communication.
   input_type : Type[BaseModelSubclass]
       Pydantic model class that defines the expected input data structure.

   Attributes
   ----------
   estimator_name : str
       Name identifier for the estimator. Set to "NormalizedForecaster".
   estimator_version : str
       Version string for the estimator. Set to "1".
   prediction_version : str
       Version string for the prediction. Set to "1".
   estimator_id : str or None
       Unique identifier assigned by the API after creation.

   """

    estimator_name = "NormalizedForecaster"
    estimator_version = "1"
    prediction_version = "1"

    def __init__(self, session: Session, input_type: Type[BaseModelSubclass]):
        super().__init__(session, input_type)
        self.create()

    def create(self):
        """
        Initialize the forecaster instance with the API.

        Creates a new forecaster instance on the API side with the specified input schema.
        The schema is serialized and base64 encoded before transmission.

        Raises
        ------
        ValueError
            If the API fails to create the estimator or returns an invalid response.
        """

        fields = pickle.dumps(self.input_type.model_fields)
        fields_b64 = base64.b64encode(fields).decode()

        request_data = EstimatorCreationRequest(
            estimator_name=self.estimator_name,
            session_id=self.session.session_id,
            input_item_schema_b64=fields_b64,
        )

        resp = requests.post(
            url=f"{self.session.env.API_URI}/estimators/{self.get_route_prefix()}/create",
            headers=self.session.headers,
            json=request_data.model_dump()
        )

        response_json = resp.json()

        if 'estimator_id' in response_json:
            self.estimator_id = response_json['estimator_id']
            print(f"Estimator created with estimator_id: {response_json['estimator_id']}")
        else:
            print(resp.status_code)
            print(resp.text)
            raise ValueError("There was an error creating the estimator. Please try again.")

    def queue(
            self,
            item: BaseModelSubclass,
            start_dt: datetime,
            weeks: int = None,
            days: int = None,
            hours: int = None,
            note_length: Tuple[int, int] = (3, 5),
    ):
        """
        Queue a prediction request for processing.

        Parameters
        ----------
        item : BaseModelSubclass
            The input data conforming to the specified input_type schema.
        start_dt : datetime
            The starting datetime for the forecast.
        weeks : int, optional
            Number of weeks to forecast.
        days : int, optional
            Number of days to forecast.
        hours : int, optional
            Number of hours to forecast.
        note_length : tuple[int, int], optional
            Desired length range (number of sentences) for explanatory notes (min, max), by default (3, 5).

        Returns
        -------
        QueuePredictionResponse
            Response object containing the request status and ID.

        Raises
        ------
        TypeError
            If the provided item doesn't match the expected input_type.
        """

        if not isinstance(item, self.input_type):
            raise TypeError(f"Expect item to be an instance of {self.input_type}, but item has type {type(item)}")

        data = dict(
            estimator_id=self.estimator_id,
            item_data=item.model_dump(),
            start_dt=start_dt.timestamp(),
            weeks=weeks,
            days=days,
            hours=hours,
            note_length=note_length,
        )
        resp = requests.post(
            url=f"{self.session.env.API_URI}/estimators/{self.get_route_prefix()}/queue-predict",
            headers=self.session.headers,
            json=data,
        )

        if resp.status_code == 200:
            return QueuePredictionResponse(**resp.json())
        else:
            return QueuePredictionResponse(
                success=False,
                request_id='',
                message=f'Queuing failed with status code {resp.status_code}: {resp.text}',
            )

    def get_predictions(self, request_id: str, try_every: int = 3, max_tries: int = 20):
        """
        Retrieve predictions for a queued request.

        Parameters
        ----------
        request_id : str
            The ID of the queued prediction request.
        try_every : int, optional
            Seconds to wait between retry attempts, by default 3.
        max_tries : int, optional
            Maximum number of retry attempts, by default 20.

        Returns
        -------
        list[Forecast] or dict
            List of Forecast objects if successful, or error dictionary if failed.

        Raises
        ------
        Exception
            If the maximum retry limit is exceeded or if an API error occurs.
        """

        retries = 0

        while retries < max_tries:

            resp = requests.post(
                url=f"{self.session.env.API_URI}/predictions/{self.prediction_version}/check-by-request-id",
                headers=self.session.headers,
                json=dict(request_id=request_id),
            )

            if resp.status_code != 200:
                print(resp)
                raise Exception(f"An error occurred")

            else:
                response_json = resp.json()

                if response_json['status'] == 'ERROR':
                    return response_json

                if response_json['status'] == 'SUCCESS':
                    print(f'{response_json["status"]}. {response_json["message"]}. Fetching predictions.')
                    prediction_ids = response_json.get('prediction_ids', [])
                    return [self.get_prediction(prediction_id) for prediction_id in prediction_ids]

                if response_json['status'] in ['PENDING', 'NOT_FOUND']:
                    print(f'{response_json["status"]}. {response_json["message"]}. Trying again in {try_every} seconds...')
                    time.sleep(try_every)

                retries += 1

        if retries >= max_tries:
            raise Exception(f"Retry limit exceeded max_tries of {max_tries}")

    def get_prediction(self, prediction_id: str) -> Optional[Forecast]:

        """
        Retrieve a single prediction by its ID.

        Parameters
        ----------
        prediction_id : str
            Unique identifier for the prediction.

        Returns
        -------
        Forecast or None
            Forecast object containing the forecast results and notes if successful,
            None if the prediction couldn't be retrieved.
        """

        resp = requests.post(
            url=f"{self.session.env.API_URI}/predictions/{self.prediction_version}/get-by-prediction-id",
            headers=self.session.headers,
            json=dict(prediction_id=prediction_id),
        )

        if resp.status_code == 200:
            response_json = resp.json()
            pred_response = PredictionGetByIdResponse(**response_json)
            if pred_response.success:
                estimator_response = pred_response.response
                prediction = Forecast(
                    _id=prediction_id,
                    text=estimator_response['notes'],
                    data=estimator_response['json_split_format_dict'],
                )
                return prediction
            else:
                print(f"The prediction could not be retrieved for prediction_id '{prediction_id}'")
                print(pred_response.message)

        else:
            print(f"The prediction could not be retrieved for prediction_id '{prediction_id}'")
            print(resp.status_code)
            print(resp.text)

    def predict(
            self,
            item: BaseModelSubclass,
            start_dt: datetime = None,
            weeks: int = None,
            days: int = None,
            hours: int = None,
            note_length: Tuple[int, int] = (3, 5),
       ) -> Forecast:
        """
        Convenience method to queue and retrieve predictions in a single call.

        This method combines the queue and get_predictions steps into a single operation,
        waiting for the prediction to complete before returning.

        Parameters
        ----------
        item : BaseModelSubclass
            The input data conforming to the specified input_type schema.
        start_dt : datetime, optional
            The starting datetime for the forecast.
        weeks : int, optional
            Number of weeks to forecast.
        days : int, optional
            Number of days to forecast.
        hours : int, optional
            Number of hours to forecast.
        note_length : tuple[int, int], optional
            Desired length range for explanatory notes (min, max), by default (3, 5).

        Returns
        -------
        Prediction or None
            The completed prediction if successful, None otherwise.
        """
        req = self.queue(item, start_dt, weeks, days, hours, note_length)
        predictions = self.get_predictions(req['request_id'])
        return predictions[0] if predictions else None
