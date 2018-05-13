# Finding Outliers (in-progress)

This project is a Python exercise. It aims to present various methods that can be used in abnormalities detection.

#### Current methods:
- Moving average
- Z-score (to be added)
- Proximity method (k-means)

### Moving Average:

Using daily opening prices of the S&P 500 `moving_average` function allows to calculate **4 weeks moving average** and detect outliers that are above confidence interval ($1.5\sigma + \mu$).

![S&P500][sp500_plot]

[sp500_plot]: ./figures/S&P500.png 
