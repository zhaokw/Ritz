import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas.tseries.offsets import MonthBegin

def plot3Sigma(sc: pd.DataFrame, col: str):
    df = sc[['Date2','Occupancy', col]]
    df['p'] = df[col]/df['Occupancy']
    mu = df[col].sum()/df['Occupancy'].sum()
    df['sigma'] = df.apply(lambda r: (mu*(1-mu)/r['Occupancy'])**.5 , axis=1)
    df['UCL'] = 3*df['sigma'] + mu
    df['LCL'] = -3*df['sigma'] + mu

    plt.figure()
    plt.rcParams['figure.figsize'] = (16,8)
    plt.plot(df['Date2'],df['p'])
    plt.plot(df['Date2'],df['UCL'])
    plt.plot(df['Date2'],df['LCL'])
    plt.xlabel('Day')
    plt.ylabel(col+ ' Complaint Ratio')
    plt.title(col + ' Day-by-Day P-Chart');
    
    return df

def plot3SigmaByMo(sc: pd.DataFrame, col: str):
    sc['DM'] = pd.to_datetime(sc['Date2']) - MonthBegin(1)
    scm = sc.groupby('DM').agg('sum').reset_index()
    scm['p'] = scm[col]/scm['Occupancy']
    scm['sigma'] = scm.apply(lambda r: (mu*(1-mu)/r['Occupancy'])**.5 , axis=1)

    plt.figure()
    plt.plot(scm['DM'],scm['p'])
    plt.plot(scm['DM'],3*scm['sigma']+scm['p'])
    plt.plot(scm['DM'],-3*scm['sigma']+scm['p'])
    plt.xlabel('Month')
    plt.ylabel(col + ' Complaint Ratio')
    plt.title(col + ' Month-by-Month P-Chart');
    
    return df