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

import json
from io import StringIO
from datetime import datetime

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    import warnings


class Prediction:
    """
   A class representing the output of a prediction request

   Parameters
   ----------
   _id : str
       Unique identifier for the prediction.

   Attributes
   ----------
   id : str
       Unique identifier for the prediction.
   """

    def __init__(self, _id: str):
        self.id = _id


class Forecast(Prediction):
    """
   A class representing the output of a prediction request, containing both numerical results and explanatory text.

   This class encapsulates the prediction results returned from the chronulus API,
   including a unique identifier, descriptive text, and the numerical predictions in
   a pandas DataFrame format.

   Parameters
   ----------
   _id : str
       Unique identifier for the prediction.
   text : str
       Descriptive text or notes explaining the prediction results.
   data : dict
       JSON-Split formatted dictionary containing the prediction results.

   Attributes
   ----------
   id : str
       Unique identifier for the prediction.
   text : str
       Explanatory text describing the prediction results.
   data : dict
       JSON-Split formatted dictionary containing the prediction results.
   """

    def __init__(self, _id: str, text: str, data: dict):
        super().__init__(_id)
        self.text = text
        self.data = data

    def to_json(self, orient='columns'):
        """
        Convert the forecast data to JSON format with specified orientation.

        Parameters
        ----------
        orient : str, optional
            Data orientation for the JSON output. Options are:

            - 'split': Original JSON-split format
            - 'rows': List of dictionaries, each representing a row
            - 'columns': Dictionary of lists, each representing a column
            Default is 'columns'.

        Returns
        -------
        dict or list
            Forecast data in the specified JSON format:

            - For 'split': Original JSON-split dictionary
            - For 'rows': List of row dictionaries
            - For 'columns': Dictionary of column arrays

        Examples
        --------
        >>> # Get data in columns format
        >>> json_cols = forecast.to_json(orient='columns')
        >>> # Get data in rows format
        >>> json_rows = forecast.to_json(orient='rows')
        """

        if orient == 'split':
            return self.data

        elif orient == 'rows':
            columns = self.data.get('columns')
            rows = list()
            for row in self.data.get('data'):
                _row = {columns[j]: val for j, val in enumerate(row)}
                rows.append(_row)
            return rows

        else:
            col_names = self.data.get('columns')
            columns = {k: list() for k in col_names}

            for row in self.data.get('data'):
                for j, val in enumerate(row):
                    columns[col_names[j]].append(val)

            return columns

    def to_pandas(self) -> pd.DataFrame:
        """
        Convert the forecast data to a pandas DataFrame.

        The first column is automatically set as the index of the resulting DataFrame.
        Typically, this is a timestamp or date column.

        Returns
        -------
        pd.DataFrame
            DataFrame containing the forecast data with the first column as index.

        Raises
        ------
        UserWarning
            If pandas is not installed in the environment.

        Examples
        --------
        >>> df = forecast.to_pandas()
        >>> print(df.head())
                   y_hat
        date
        2025-01-01   .12345
        2025-01-02   .67890
        """
        if not PANDAS_AVAILABLE:
            warnings.warn(
                "pandas is not installed but his method requires pandas."
                "Please install pandas using `pip install pandas` and then try again.",
                UserWarning
            )
        else:
            json_str = json.dumps(self.data)
            df = pd.read_json(StringIO(json_str), orient='split')
            return df.set_index(self.data.get('columns')[0], drop=True)

