"""
Class to preprocessing data
"""

# pylint: disable=too-many-instance-attributes

import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import StandardScaler


class DataTransformer:
    """
    A class for preprocessing numerical data with various transformation methods.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame containing data to be transformed
    sqrt_col : list, optional
        Columns for square root transformation (requires non-negative values)
    log_default : list, optional
        Columns for logarithmic transformation with added constant 0.01
    ihs : list, optional
        Columns for inverse hyperbolic sine transformation
    extensive_log : list, optional
        Columns for extensive logarithmic transformation
    neglog : list, optional
        Columns for logarithmic transformation with negative values handling
    boxcox_zero : list, optional
        Columns for Box-Cox transformation with zero handling
    log_x_divide_2 : list, optional
        Columns for logarithmic transformation with half minimum non-zero value
    """

    def __init__(
        self,
        data,
        sqrt_col=[],
        log_default=[],
        ihs=[],
        extensive_log=[],
        neglog=[],
        boxcox_zero=[],
        log_x_divide_2=[],
    ):

        self.transform_data = data.copy()
        self.sqrt_col = sqrt_col
        self.log_default = log_default
        self.ihs = ihs
        self.extensive_log = extensive_log
        self.neglog = neglog
        self.boxcox_zero = boxcox_zero
        self.log_x_divide_2 = log_x_divide_2

    def sqrt_transformation(self, column):
        """Sqrt transformation

        Parameters
        ----------
        column : list
            List of column to transform.
        """
        if (self.transform_data[column] < 0).any():
            raise ValueError(f"Column {column} contains negative values")
        self.transform_data[column] = np.sqrt(self.transform_data[column])

    def log_default_transformation(self, column, value_add):
        """Log transformation

        Parameters
        ----------
        column : str
            Name of the column to transform.
        value_add : float
            Constant added before logarithmic transformation.
        """
        self.transform_data[column] = np.log(self.transform_data[column] + value_add)

    def ihs_transformation(self, column):
        """IHS transformation

        Parameters
        ----------
        column : list
            List of column to transform.
        """
        self.transform_data[column] = np.arcsinh(self.transform_data[column])

    def extensive_log_transformation(self, column, value=None):
        """Extensive log transformation

        Parameters
        ----------
        column : list
            List of column to transform.
        """
        min_data = value if value is not None else self.transform_data[column].min()
        self.transform_data[column] = self.transform_data[column].clip(lower=min_data)

        shift = min_data - 1
        
        if (self.transform_data[column] - shift <= 0).any():
            raise ValueError(f"Column {column} contains negative values")
        
        self.transform_data[column] = np.log(self.transform_data[column] - shift)
        
        if value is None:
            print(f'For column {column} min_value is: {min_data}')

    def neglog_transformation(self, column):
        """Neglog transformation

        Parameters
        ----------
        column : list
            List of column to transform.
        """
        self.transform_data[column] = self.transform_data[column].apply(
            lambda x: np.sign(x) * np.log(abs(x) + 1)
        )

    def log_x_divide_2_transformation(self, column, value=None):
        """Log transformation

        Parameters
        ----------
        column : list
            List of column to transform.
        value : float, optional
            Minimum df value
        """
        min_non_zero = value if value is not None else self.transform_data[self.transform_data[column] > 0][column].min()

        shift = min_non_zero / 2

        if (self.transform_data[column] + shift <= 0).any():
            raise ValueError(f"Column {column} contains negative values")
        self.transform_data[column] = np.log(self.transform_data[column] + shift)

        if value is None:
            print(f'For column {column} min_value is: {min_non_zero}')

    def func_transform_data(self, parameters=None):
        """Function to transform all data with optional parameters for each transformation.
        
        Parameters
        ----------
        parameters : dict, optional
            Dictionary containing parameters for transformations and columns in format:
            {
                'transformation_name': {
                    'column_name': parameter_value
                }
            }
            Example:
            {
                'log_x_divide_2': {
                    'column1': 0.5, 
                    'column2': 1.0
                },
                'extensive_log': {
                    'column3': 2.0
                }
            }
            If not provided, default parameters will be used for transformations.

        Returns
        -------
        pd.DataFrame
            Transformed DataFrame.
        """
        parameters = parameters or {}
        
        transformations = {
            "log_default": (self.log_default, self.log_default_transformation, 0.01),
            "sqrt": (self.sqrt_col, self.sqrt_transformation),
            "ihs": (self.ihs, self.ihs_transformation),
            "extensive_log": (self.extensive_log, self.extensive_log_transformation),
            "neglog": (self.neglog, self.neglog_transformation),
            "log_x_divide_2": (self.log_x_divide_2, self.log_x_divide_2_transformation),
        }

        for transform_name, transform_info in transformations.items():
            columns = transform_info[0]  # columns list
            transform_func = transform_info[1]  # transformation function
            
            # Get parameters for current transformation if they exist
            transform_params = parameters.get(transform_name, {})

            for column in columns:
                if column in self.transform_data.columns:
                    if len(transform_info) == 3:  # if default parameter exists (for log_default)
                        transform_func(column, transform_info[2])
                    else:
                        # Check if parameter exists for this column
                        if column in transform_params:
                            transform_func(column, transform_params[column])
                        else:
                            transform_func(column)
                else:
                    raise ValueError(f"Column {column} not in dataframe")
                                   
        return self.transform_data
