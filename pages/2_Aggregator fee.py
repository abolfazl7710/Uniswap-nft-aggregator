import streamlit as st
from shroomdk import ShroomDK
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="💲 Aggregator fee",
    layout= "wide",
    page_icon="💲 ",
)
st.title("💲 Aggregator fee")
st.sidebar.success("💲 Aggregator fee")

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
with table1 as(select
block_timestamp::date as date,
'Uniswap' as aggregator,
TX_FEE,
TX_FEE_USD,
count(DISTINCT TOKENID) as transaction_count
from ethereum.core.ez_nft_sales
where ORIGIN_TO_ADDRESS = lower('0xef1c6e67703c7bd7107eed8303fbe6ec2554bf6b')
and PROJECT_NAME is not null
and price_usd is not null
group by 1,2,3,4
union 
select
block_timestamp::date as date,
'Gem' as aggregator,
TX_FEE,
TX_FEE_USD,
count(DISTINCT TOKENID) as transaction_count
from ethereum.core.ez_nft_sales 
where AGGREGATOR_NAME = 'Gem'
and block_timestamp >= '2022-11-29'
and PROJECT_NAME is not null
and price_usd is not null
group by 1,2,3,4
union 
select
block_timestamp::date as date,
'Blur' as aggregator,
TX_FEE,
TX_FEE_USD,
count(DISTINCT TOKENID) as transaction_count
from ethereum.core.ez_nft_sales 
where AGGREGATOR_NAME = 'Blur'
and block_timestamp >= '2022-11-29'
and PROJECT_NAME is not null
and price_usd is not null
group by 1,2,3,4
  ), main as(select
date,
aggregator,
TX_FEE / transaction_count as daily_tx_fee_eth,
TX_FEE_USD / transaction_count as daily_tx_fee_usd
from table1 
group by 1,2,3,4
  )
select 
date,
aggregator,
avg(daily_tx_fee_eth) as avg_fee_eth,
avg(daily_tx_fee_usd) as avg_fee_usd
from main 
group by 1,2
"""

df = querying_pagination(df_query)

#total 
df1_query="""
with table1 as(select
'Uniswap' as aggregator,
TX_FEE,
TX_FEE_USD,
count(DISTINCT TOKENID) as transaction_count
from ethereum.core.ez_nft_sales
where ORIGIN_TO_ADDRESS = lower('0xef1c6e67703c7bd7107eed8303fbe6ec2554bf6b')
and PROJECT_NAME is not null
and price_usd is not null
group by 1,2,3
union 
select
'Gem' as aggregator,
TX_FEE,
TX_FEE_USD,
count(DISTINCT TOKENID) as transaction_count
from ethereum.core.ez_nft_sales 
where AGGREGATOR_NAME = 'Gem'
and block_timestamp >= '2022-11-29'
and PROJECT_NAME is not null
and price_usd is not null
group by 1,2,3
union 
select
'Blur' as aggregator,
TX_FEE,
TX_FEE_USD,
count(DISTINCT TOKENID) as transaction_count
from ethereum.core.ez_nft_sales 
where AGGREGATOR_NAME = 'Blur'
and block_timestamp >= '2022-11-29'
and PROJECT_NAME is not null
and price_usd is not null
group by 1,2,3
  ), main as(select
aggregator,
TX_FEE / transaction_count as daily_tx_fee_eth,
TX_FEE_USD / transaction_count as daily_tx_fee_usd
from table1 
group by 1,2,3
  )
select 
aggregator,
avg(daily_tx_fee_eth) as avg_fee_eth,
avg(daily_tx_fee_usd) as avg_fee_usd
from main 
group by 1
"""

df1 = querying_pagination(df1_query)

options = st.multiselect(
    '**Select your desired aggregator:**',
    options=df['aggregator'].unique(),
    default=df['aggregator'].unique(),
    key='collection'
)

if len(options) > 0:
 
 df = df.query("aggregator == @options")
 df1 = df1.query("aggregator == @options")

 st.subheader('Aggregator transaction fee')
 st.write("""
 Here you can see total and daily transactions fee at each Aggregator.
 """)
 st.subheader('Aggregator transaction fee(ETH)')
 cc1, cc2= st.columns([1, 1])
 
 with cc1:
  fig = px.area(df, x='date', y='avg_fee_eth',color='aggregator', title='Daily average transaction fee(ETH) at each aggregator')
  fig.update_layout(legend_title=None, legend_y=0.5)
  st.plotly_chart(fig, use_container_width=True, theme='streamlit')
 with cc2:
  st.caption('Average transaction fee(ETH) at each aggregator')
  st.bar_chart(df1, x='aggregator', y = 'avg_fee_eth', width = 400, height = 400)

 st.subheader('Aggregator transaction fee(USD)')
 cc1, cc2= st.columns([1, 1])
 
 with cc1:
  fig = px.area(df, x='date', y='avg_fee_usd',color='aggregator', title='Daily average transaction fee(USD) at each aggregator')
  fig.update_layout(legend_title=None, legend_y=0.5)
  st.plotly_chart(fig, use_container_width=True, theme='streamlit')
 with cc2:
  st.caption('Average transaction fee(USD) at each aggregator')
  st.bar_chart(df1, x='aggregator', y = 'avg_fee_usd', width = 400, height = 400)
