"""
Outliers: finds outliers in the time series data using moving average approach

Requires: sys, matplotlib, pandas, datetime
Created on Sun May 13 18:13:01 CEST 2018

@author: Witkor
"""

import sys
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime


class outliers(object):

    def __init__(self,
                 data_frame,
                 window_size=28,
                 sigma=1.5,
                 start_date=None,
                 end_date=None):
            """
            Arguments:
                - 'data_frame' (pandas.DataFrame): df to look for the abnormal values
                    - first column has to be 'Date' (str, '%Y-%m-%d')
                    - second column contains nummeric values of interest (float)

                - 'window_size' (int): size of the rolling window (default: 28 periods/rows)
                It is assumed that rows corespond to days, therefore average over 4 weeks

                - 'sigma' (int): scaling parameter to the standard deviation to create
                upper and lower bound (expected range) to catch outliers

            self.arguments:
                - 'start/end': used for outlier range subseting, default use whole input range
                    - 'start': finds outliers by limiting start date
                    - 'end': finds outliers by limiting end date
                - 'data': vector of values which will be used to find outliers
                - 'date': time vector
            """

            # Error if data frame is empty
            if data_frame.empty:
                raise ValueError('Error: input data frame is empty')

            # Part necessary for outlier subsetting by date
            data_frame.columns = ['Date', 'Value']
            data_frame['Date'] = pd.to_datetime(data_frame['Date'])

            if (start_date and end_date) is not None:
                self.start = datetime.strptime(start_date, '%Y-%m-%d')
                self.end = datetime.strptime(end_date, '%Y-%m-%d')
            elif start_date is not None:
                self.start = datetime.strptime(start_date, '%Y-%m-%d')
                self.end = max(data_frame['Date'])
            elif end_date is not None:
                self.end = datetime.strptime(end_date, '%Y-%m-%d')
                self.start = min(data_frame['Date'])
            else:
                self.start = min(data_frame['Date'])
                self.end = max(data_frame['Date'])

            self.data = data_frame['Value']
            self.date = data_frame['Date']
            self.sigma = sigma
            self.N = window_size

            # Error if input data is too short
            if self.N > len(self.data):
                raise ValueError('Error: window_size is larger than input data')

    def find_outliers(self):
        """
        Function finds outliers in the data using moving average and rolling
        standard deviation
        Returns:
            'outliers' (pandas.DataFrame):
                - date
                - values from the input vector that
                fall out of the expected range bounds
                - upper and lower bounds of the expected range
        """
        # Calculate rolling mean, result is based on self.N past observation
        avg = self.data.rolling(window=self.N).mean()

        # Caluclate rolling variation in the data
        std = std = self.data.rolling(window=self.N).std()

        # Create upper and lower bound to create expected range of possible values
        upper_bound = avg + self.sigma * std
        lower_bound = avg - self.sigma * std

        # Filtering values that are fall out of the expected range,
        # returns list of date, value, upper and lower bound for each outlier
        outliers = [(date, value, lower, upper)
                    for date, value, upper, lower
                    in zip(self.date, self.data, upper_bound, lower_bound)
                    if (value < lower) or (value > upper)
                    ]

        if len(outliers) == 0:
            return []
        else:
            # Converting list of values into a data frame
            outliers = pd.DataFrame(outliers)
            outliers.columns = ['Date', 'Abnormal_values', 'Lower Bound', 'Upper Bound']

            return outliers

    def get_outliers(self):
            """
            Function to output the outliers analysis results
            Returns tuple:
                - Success\Failure
                - if Failure, 'DataFrame' with occurence dates, abnormal values
                and expected range bounds
            """
            outliers = self.find_outliers()

            if len(outliers) == 0:
                return 'Sucess', 'No anomalies found'
            else:
                # Filtering outliers based on input date range
                outliers = outliers[(outliers['Date'] >= self.start) &
                                    (outliers['Date'] <= self.end)]
                return 'Failure', outliers

    def plot_outliers(self):
        """
        Extra: Function plots outliers, moving_average and the actual data,
        just for visual validation
        """
        # Actual data plot
        plt.plot(self.date, self.data)

        # Moving average plot
        plt.plot(self.date, self.data.rolling(window=self.N).mean())

        # Anomalies Plot
        plt.plot(self.get_outliers()[1]['Date'],
                 self.get_outliers()[1]['Abnormal_values'],
                 color='orange',
                 linestyle='none',
                 marker='o',
                 alpha=0.5)

        plt.legend(['Actual Data', 'Moving average', 'Outliers'], loc='upper left')

        return plt.show()
