from preparedata import align_datadf
import pandas as pd
import numpy as np
from preparedata import companies
from preparedata import rf_rate
from scipy.optimize import minimize

companies.remove("PLOPLN1M")
companies.remove("WIG20")

for company in companies:
    align_datadf[company] = pd.to_numeric(align_datadf[company], errors='coerce')

dailyreturns_df = align_datadf.set_index('Data')

# calculate daily returns
dailyreturns_df = dailyreturns_df.pct_change()
dailyreturns_df = dailyreturns_df.dropna()

# correlation
correl_m = dailyreturns_df.corr().round(4)
avgcorrel = (correl_m.apply(lambda x: x[x.index != x.name].mean(), axis=1).round(4)).sort_values()

# selection
companies_selected = avgcorrel.head(10).index.tolist()
dailyreturns_selection = dailyreturns_df[companies_selected]

# covariance
cov_m = dailyreturns_selection.cov()*252

################################################################################################################
def stdev(weights, cov_m):
    variance = np.dot(weights.T, np.dot(cov_m, weights))
    return np.sqrt(variance)

def expectedreturn(weights, dailyreturns_selection):
    weightedreturns = dailyreturns_selection.mean() *weights
    return np.sum(weightedreturns)*252

def sharpe(weights, dailyreturns_selection, cov_m, rf_rate):
    return (expectedreturn(weights, dailyreturns_selection) - rf_rate) / stdev(weights, cov_m)

def negsharpe(weights, dailyreturns_selection, cov_m, rf_rate):
    return - sharpe(weights, dailyreturns_selection, cov_m, rf_rate)

constraints = {'type':'eq','fun': lambda weights: np.sum(weights) - 1}
bounds = [(0, 0.3) for _ in range(len(companies_selected))]

# initial weights - equally weighted
weightsequal = np.array([1/len(companies_selected)] * len(companies_selected))

# optimization
resultoptimal = minimize(negsharpe, weightsequal, args=(dailyreturns_selection, cov_m, rf_rate), method='SLSQP', constraints=constraints, bounds=bounds)
weightsoptimal = resultoptimal.x
returnoptimal = expectedreturn(weightsoptimal, dailyreturns_selection)
riskoptimal = stdev(weightsoptimal, cov_m)
sharpeoptimal = sharpe(weightsoptimal, dailyreturns_selection, cov_m, rf_rate)

################################################################################################################
print(f"Optimal weights for the {len(companies_selected)} selected companies: ")
for cmp, weight in zip(companies_selected, weightsoptimal):
    print(f"{cmp}: {weight:.2f}")

print("\nPortfolio metrics in annualized terms: ")
print(f"Expected Return: {returnoptimal*100:.2f}%")
print(f"Risk: {riskoptimal*100:.2f}%")
print(f"Sharpe Ratio: {sharpeoptimal*100:.2f}%")

