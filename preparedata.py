import pandas as pd
import numpy as np
from datetime import datetime

df = pd.read_csv('companies.csv')

companies = list(df.columns[::2])
companiesdata = {company: {'Data': [], 'Zamkniecie': []} for company in companies}

for company in companies:
    dates = df.iloc[:, df.columns.get_loc(company)].tolist()[1:]
    prices = df.iloc[:, df.columns.get_loc(company)+1].tolist()[1:]

    companiesdata[company]['Data'].extend(dates)
    companiesdata[company]['Zamkniecie'].extend(prices)

alldates = [x['Data'] for x in companiesdata.values()]
alldateslist = [item for sublist in alldates for item in sublist if not pd.isnull(item)]
uniquedates = set(alldateslist)
sorteddates = sorted(uniquedates, key=lambda x: datetime.strptime(str(x), '%d/%m/%y'), reverse=True)
align_data = pd.DataFrame({'Data': sorteddates})

for company in companies:
    prices = []
    company_dates = companiesdata[company]['Data']
    company_prices = companiesdata[company]['Zamkniecie']

    for date in sorteddates:
        if date in company_dates:
            index = company_dates.index(date)
            prices.append(company_prices[index])
        else:
            prices.append(float('nan'))

    align_data[company] = prices

align_data = align_data.dropna()
align_datadf = pd.DataFrame(align_data)

# calculate rf rate
rf_ratedata = align_datadf.loc[:, 'PLOPLN1M']
rf_ratedata = pd.to_numeric(rf_ratedata, errors='coerce')
rf_ratedata = rf_ratedata.div(100)
rf_rate = (rf_ratedata.mean() * 252)/100

align_datadf = align_datadf.drop(columns=['PLOPLN1M'])
align_datadf = align_datadf.drop(columns=['WIG20'])
