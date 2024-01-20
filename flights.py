import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px 


# Import the data - .csv's files


###  Treatment of each file separeted ###  

#print(df, "\n", (df.isnull().sum().sort_values(ascending=False)/len(df))*100)

@st.cache_data 


def load_data():
    ### Selecting Interesting Columns before the merge ###  
    ny  = pd.read_csv("nyc_flights.csv")
    airlines = pd.read_csv("nyc_airlines.csv")
    planes = pd.read_csv("nyc_planes.csv")
    weather = pd.read_csv("nyc_weather.csv")

    # nyc_fligts
    ny  = ny[['flight', 'carrier',"origin", 'dest', 'dep_delay', 'arr_delay',
          'time_hour', 'tailnum', 'distance', 'air_time']]

    #weather 
    weather = weather[['origin', 'temp', 'dewp', 'humid','wind_dir', 'wind_speed', 
                   'wind_gust', 'precip', 'pressure', 'visib', 'time_hour']]

    # Merging all the data
    df = pd.merge(ny, weather, how='left', left_on=['origin','time_hour'], 
              right_on = ['origin','time_hour'])
    df =pd.merge(df, planes, on = 'tailnum', how='left')
    df = pd.merge(df, airlines, on = 'carrier')

    del weather, planes, airlines 

    # df.drop([""])



    return df
df = load_data()
st.set_page_config(layout='wide')
st.title("Aircraft Accident Report") 
st.markdown(
    """
    This report has the goal to  **New York Airports**.   
    """
)
if st.sidebar.checkbox("Show table?"):
    st.header("Raw data")
    st.write(df)

st.sidebar.info("{} lines has been loaded".format(df.shape[0]))

st.subheader("Somenthing")
# df_chain = (
#     pd.read_csv('https://raw.githubusercontent.com/flyandlure/datasets/master/ecommerce_sales_by_date.csv')
#     .fillna('')
#     .sort_values(by='date', ascending=False)
#     .assign(
#         conversion_rate=(lambda x: ((x['transactions'] / x['sessions']) * 100).round(2)),
#         revenuePerTransaction=(lambda x: x['revenuePerTransaction'].round(2)),
#         transactionsPerSession=(lambda x: x['transactionsPerSession'].round(2))
#     )
#     .rename(columns={'date': 'Date', 
#                     'sessions': 'Sessions', 
#                     'transactions': 'Transactions', 
#                     'transactionRevenue': 'Revenue', 
#                     'transactionsPerSession': 'Transactions Per Session', 
#                     'revenuePerTransaction': 'AOV',
#                     'conversion_rate': 'CR'})        
#     .drop(columns=['Unnamed: 0', 'Transactions Per Session'])
#     .astype({'Date': 'datetime64[ns]'})  
# )
airports = pd.read_csv("nyc_airports.csv")

fig = px.scatter_mapbox(airports, lat=airports['lat'], lon=airports['lon'])

fig.update_layout(mapbox_style= 'open-street-map')
fig.update_layout(height=600, margin={'r': 0, 't':0, 'l':0, 'b':0})
st.plotly_chart(fig)