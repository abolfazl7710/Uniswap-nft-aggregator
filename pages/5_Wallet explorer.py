import streamlit as st
from shroomdk import ShroomDK
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="🔍 Wallet explorer",
    layout= "wide",
    page_icon="🔍 ",
)
st.title("🔍 Wallet explorer")
st.write("""
Due to the large amount of data, the search may take some time. Please wait...
""")
st.sidebar.success("🔍 Wallet explorer")

@st.cache(ttl=10000)
def querying_pagination(query_string):
    sdk = ShroomDK('8c37dc3a-fcf4-42a1-a860-337fa9931a2a')
    result_list = []
    for i in range(1,11): 
        data=sdk.query(query_string,page_size=100000,page_number=i)
        if data.run_stats.record_count == 0:  
            break
        else:
            result_list.append(data.records)
  
    result_df=pd.DataFrame()
    for idx, each_list in enumerate(result_list):
        if idx == 0:
            result_df=pd.json_normalize(each_list)
        else:
            result_df=pd.concat([result_df, pd.json_normalize(each_list)])

    return result_df
#daily 
df_query="""
select
DISTINCT seller_address as user,
block_timestamp::date as date,
'Uniswap' as aggregator,
PLATFORM_NAME as marketplace,
count(DISTINCT tx_hash) as count_tx,
sum(price) as vol_eth, 
sum(price_usd) as vol_usd
from ethereum.core.ez_nft_sales 
where ORIGIN_TO_ADDRESS = lower('0xef1c6e67703c7bd7107eed8303fbe6ec2554bf6b')
group by 1,2,3,4
union 
select
DISTINCT seller_address as user,
block_timestamp::date as date,
'Uniswap' as aggregator,
PLATFORM_NAME as marketplace,
count(DISTINCT tx_hash) as count_tx,
sum(price) as vol_eth, 
sum(price_usd) as vol_usd
from ethereum.core.ez_nft_sales 
where AGGREGATOR_NAME = 'Gem'
and block_timestamp >= '2022-11-29'
group by 1,2,3,4
union 
select
DISTINCT seller_address as user,
block_timestamp::date as date,
'Uniswap' as aggregator,
PLATFORM_NAME as marketplace,
count(DISTINCT tx_hash) as count_tx,
sum(price) as vol_eth, 
sum(price_usd) as vol_usd
from ethereum.core.ez_nft_sales 
where AGGREGATOR_NAME = 'Blur'
and block_timestamp >= '2022-11-29'
group by 1,2,3,4
"""

df = querying_pagination(df_query)

#total 
df1_query="""
select
DISTINCT seller_address as user,
'Uniswap' as aggregator,
PLATFORM_NAME as marketplace,
count(DISTINCT tx_hash) as count_tx,
sum(price) as vol_eth, 
sum(price_usd) as vol_usd
from ethereum.core.ez_nft_sales 
where ORIGIN_TO_ADDRESS = lower('0xef1c6e67703c7bd7107eed8303fbe6ec2554bf6b')
group by 1,2,3
union 
select
DISTINCT seller_address as user,
'Gem' as aggregator,
PLATFORM_NAME as marketplace,
count(DISTINCT tx_hash) as count_tx,
sum(price) as vol_eth, 
sum(price_usd) as vol_usd
from ethereum.core.ez_nft_sales 
where AGGREGATOR_NAME = 'Gem'
and block_timestamp >= '2022-11-29'
group by 1,2,3
union 
select
DISTINCT seller_address as user,
'Blur' as aggregator,
PLATFORM_NAME as marketplace,
count(DISTINCT tx_hash) as count_tx,
sum(price) as vol_eth, 
sum(price_usd) as vol_usd
from ethereum.core.ez_nft_sales 
where AGGREGATOR_NAME = 'Blur'
and block_timestamp >= '2022-11-29'
group by 1,2,3
"""

df1 = querying_pagination(df1_query)

user = st.text_input('Import your wallet address!')
user=str(user)
df=df[df['user'].str.contains(user)]
df1=df1[df1['user'].str.contains(user)]

if len(user) > 0:

 st.subheader('Aggregator transaction count')
 st.write("""
 Here you can see total and daily transactions count at each Aggregator.
 """)
 cc1, cc2= st.columns([1, 1])

 with cc1:
  st.caption('Total number of transaction at each aggregator')
  st.bar_chart(df1, x='aggregator', y = 'count_tx', width = 400, height = 400)
 with cc2:
  fig = px.pie(df1, values='count_tx', names='aggregator', title='Total number of transaction at each aggregator')
  fig.update_layout(legend_title=None, legend_y=0.5)
  fig.update_traces(textinfo='percent+label', textposition='inside')
  st.plotly_chart(fig, use_container_width=True, theme='streamlit')

 fig = px.bar(df, x='date', y='count_tx',color='aggregator', title='Daily number of transaction at each aggregator')
 fig.update_layout(legend_title=None, legend_y=0.5)
 st.plotly_chart(fig, use_container_width=True, theme='streamlit')

 st.subheader('Aggregator transaction volume(ETH)')
 st.write("""
 Here you can see total and daily transaction volume(ETH) at each Aggregator.
 """)
 cc1, cc2= st.columns([1, 1])

 with cc1:
  st.caption('Total volume (ETH) of transaction at each aggregator')
  st.bar_chart(df1, x='aggregator', y = 'vol_eth', width = 400, height = 400)
 with cc2:
  fig = px.pie(df1, values='vol_eth', names='aggregator', title='Total volume (ETH) of transaction at each aggregator')
  fig.update_layout(legend_title=None, legend_y=0.5)
  fig.update_traces(textinfo='percent+label', textposition='inside')
  st.plotly_chart(fig, use_container_width=True, theme='streamlit')

 fig = px.bar(df, x='date', y='vol_eth',color='aggregator', title='Daily volume (ETH) of transaction at each aggregator')
 fig.update_layout(legend_title=None, legend_y=0.5)
 st.plotly_chart(fig, use_container_width=True, theme='streamlit')
 st.subheader('Aggregator transaction volume(USD)')
 st.write("""
 Here you can see total and daily transaction volume(USD) at each Aggregator.
 """)
 cc1, cc2= st.columns([1, 1])

 with cc1:
  st.caption('Total volume (USD) of transaction at each aggregator')
  st.bar_chart(df1, x='aggregator', y = 'vol_usd', width = 400, height = 400)
 with cc2:
  fig = px.pie(df1, values='vol_usd', names='aggregator', title='Total volume (USD) of transaction at each aggregator')
  fig.update_layout(legend_title=None, legend_y=0.5)
  fig.update_traces(textinfo='percent+label', textposition='inside')
  st.plotly_chart(fig, use_container_width=True, theme='streamlit')

 fig = px.bar(df, x='date', y='vol_usd',color='aggregator', title='Daily volume (USD) of transaction at each aggregator')
 fig.update_layout(legend_title=None, legend_y=0.5)
 st.plotly_chart(fig, use_container_width=True, theme='streamlit')
 st.subheader('Aggregator transaction count at each marketplace')
 st.write("""
 Here you can see total and daily Aggregator transaction count at each marketplace.
 """)
 cc1, cc2= st.columns([1, 1])

 with cc1:
  st.caption('Total number of aggregator transaction at each marketplace')
  st.bar_chart(df1, x='marketplace', y = 'count_tx', width = 400, height = 400)
 with cc2:
  fig = px.pie(df1, values='count_tx', names='marketplace', title='Total number of aggregator transaction at each marketplace')
  fig.update_layout(legend_title=None, legend_y=0.5)
  fig.update_traces(textinfo='percent+label', textposition='inside')
  st.plotly_chart(fig, use_container_width=True, theme='streamlit')

 fig = px.bar(df, x='date', y='count_tx',color='marketplace', title='Daily number of aggregator transaction at each marketplace')
 fig.update_layout(legend_title=None, legend_y=0.5)
 st.plotly_chart(fig, use_container_width=True, theme='streamlit')
 st.subheader('Aggregator transaction volume(ETH) at each marketplace')
 st.write("""
 Here you can see total and daily Aggregator transaction volume(ETH) at each marketplace.
 """)
 cc1, cc2= st.columns([1, 1])

 with cc1:
  st.caption('Total volume (ETH) of aggregator transaction at each marketplace')
  st.bar_chart(df1, x='marketplace', y = 'vol_eth', width = 400, height = 400)
 with cc2:
  fig = px.pie(df1, values='vol_eth', names='marketplace', title='Total volume (ETH) of aggregator transaction at each marketplace')
  fig.update_layout(legend_title=None, legend_y=0.5)
  fig.update_traces(textinfo='percent+label', textposition='inside')
  st.plotly_chart(fig, use_container_width=True, theme='streamlit')

 fig = px.bar(df, x='date', y='vol_eth',color='marketplace', title='Daily volume (ETH) of aggregator transaction at each marketplace')
 fig.update_layout(legend_title=None, legend_y=0.5)
 st.plotly_chart(fig, use_container_width=True, theme='streamlit')
 st.subheader('Aggregator transaction volume(USD) at each marketplace')
 st.write("""
 Here you can see total and daily Aggregator transaction volume(USD) at each marketplace.
 """)
 cc1, cc2= st.columns([1, 1])

 with cc1:
  st.caption('Total volume (USD) of aggregator transaction at each marketplace')
  st.bar_chart(df1, x='marketplace', y = 'vol_usd', width = 400, height = 400)
 with cc2:
  fig = px.pie(df1, values='vol_usd', names='marketplace', title='Total volume (USD) of aggregator transaction at each marketplace')
  fig.update_layout(legend_title=None, legend_y=0.5)
  fig.update_traces(textinfo='percent+label', textposition='inside')
  st.plotly_chart(fig, use_container_width=True, theme='streamlit')

 fig = px.bar(df, x='date', y='vol_usd',color='marketplace', title='Daily volume (USD) of aggregator transaction at each marketplace')
 fig.update_layout(legend_title=None, legend_y=0.5)
 st.plotly_chart(fig, use_container_width=True, theme='streamlit')
