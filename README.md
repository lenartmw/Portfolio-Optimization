# Portfolio-Optimization
Creating a diversified portfolio of 19 selected stocks from WSE 

# Dataset #
The stock returns between 4/1/10 and 29/12/23 were obtained from [Stooq](https://stooq.pl/). The dates are located in _Data_ columns and adjusted closing prices under _Zamkniecie_

# Data Preparation #
The dataset had to be cleaned first due to multiple inconsistencies. Some stocks had missing dates and corresponding prices, so those dates had to be removed to ensure data consistency. The size of the sample was narrowed down from 3526 rows of data to 3164 after removing inconsistent observations. 

# Portfolio #
For the risk-free rate, monthly WIBOR was used. <br>
The 10 stocks that were selected for the portfolio were the ones with the lowest correlation to eliminate specific risk. To maximize the risk-adjusted return, the minimize function with the SLSQP method from the SciPy library was used. Under the assumption that short sales aren't allowed, the minimum weight within the optimal portfolio had to be at least 0. 







