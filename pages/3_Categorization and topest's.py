import streamlit as st
from shroomdk import ShroomDK
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="🔥 categorization and topest's",
    layout= "wide",
    page_icon="🔥 ",
)
st.title("🔥 categorization and topest's")
st.sidebar.success("🔥 categorization and topest's")

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
#categorize by count 
df_query="""
with main as(select
DISTINCT seller_address as seller,
'Uniswap' as aggregator,
count(DISTINCT tx_hash) as "sales count",
sum(price_usd) as "sales volume (USD)"
from ethereum.core.ez_nft_sales 
where ORIGIN_TO_ADDRESS = lower('0xef1c6e67703c7bd7107eed8303fbe6ec2554bf6b')
group by 1,2
union 
select
DISTINCT seller_address as seller,
'Gem' as aggregator,
count(DISTINCT tx_hash) as "sales count",
sum(price_usd) as "sales volume (USD)"
from ethereum.core.ez_nft_sales 
where AGGREGATOR_NAME = 'Gem'
and block_timestamp >= '2022-11-29'
group by 1,2
union 
select
DISTINCT seller_address as seller,
'Blur' as aggregator,
count(DISTINCT tx_hash) as "sales count",
sum(price_usd) as "sales volume (USD)"
from ethereum.core.ez_nft_sales 
where AGGREGATOR_NAME = 'Blur'
and block_timestamp >= '2022-11-29'
group by 1,2
  )
select
case 
when "sales count" = 1 then 'Sale just one time'
when "sales count" between 2 and 5 then 'Sale 2 - 5 time'
when "sales count" between 6 and 10 then 'Sale 6 - 10 time'
when "sales count" between 11 and 20 then 'Sale 11 - 20 time'
when "sales count" between 21 and 50 then 'Sale 21 - 50 time'
when "sales count" between 51 and 100 then 'Sale 51 - 100 time'
when "sales count" between 101 and 200 then 'Sale 101 - 200 time'
when "sales count" between 201 and 500 then 'Sale 201 - 500 time'
when "sales count" between 501 and 1000 then 'Sale 501 - 1000 time'
else 'Sale more than 1000 time'
end as sales_count,
aggregator,
count(seller) as sellers_count
from main
group by 1,2
"""

df = querying_pagination(df_query)

#categorize by volume 
df1_query="""
with main as(select
DISTINCT seller_address as seller,
'Uniswap' as aggregator,
count(DISTINCT tx_hash) as "sales count",
sum(price_usd) as "sales volume (USD)"
from ethereum.core.ez_nft_sales 
where ORIGIN_TO_ADDRESS = lower('0xef1c6e67703c7bd7107eed8303fbe6ec2554bf6b')
group by 1,2
union 
select
DISTINCT seller_address as seller,
'Gem' as aggregator,
count(DISTINCT tx_hash) as "sales count",
sum(price_usd) as "sales volume (USD)"
from ethereum.core.ez_nft_sales 
where AGGREGATOR_NAME = 'Gem'
and block_timestamp >= '2022-11-29'
group by 1,2
union 
select
DISTINCT seller_address as seller,
'Blur' as aggregator,
count(DISTINCT tx_hash) as "sales count",
sum(price_usd) as "sales volume (USD)"
from ethereum.core.ez_nft_sales 
where AGGREGATOR_NAME = 'Blur'
and block_timestamp >= '2022-11-29'
group by 1,2
  )
select
case 
when "sales volume (USD)" < 100 then 'Sale less than 100 USD'
when "sales volume (USD)" between 100 and 499.99 then 'Sale 100 - 500 USD'
when "sales volume (USD)" between 5000 and 9999.99 then 'Sale 500 - 1 K USD'
when "sales volume (USD)" between 10000 and 24999.99 then 'Sale 1 K - 2.5 K USD'
when "sales volume (USD)" between 25000 and 49999.99 then 'Sale 2.5 K - 5 K USD'
when "sales volume (USD)" between 50000 and 99999.99 then 'Sale 5 K - 10 K USD'
when "sales volume (USD)" between 100000 and 199999.99 then 'Sale 10 K - 20 K USD'
when "sales volume (USD)" between 200000 and 499999.99 then 'Sale 20 K - 50 K USD'
when "sales volume (USD)" between 500000 and 999999.99 then 'Sale 50 K - 100 K USD'
else 'Sale more than 100 K USD'
end as Sale_volume,
aggregator,
count(seller) as count_sellers
from main
group by 1,2
"""

df1 = querying_pagination(df1_query)

#top 10 collection
df2_query="""
with main as(select
DISTINCT project_name as collection,
'Uniswap' as aggregator,
count(DISTINCT tx_hash) as sales_count
from ethereum.core.ez_nft_sales 
where ORIGIN_TO_ADDRESS = lower('0xef1c6e67703c7bd7107eed8303fbe6ec2554bf6b')
group by 1,2
union 
select
DISTINCT project_name as collection,
'Gem' as aggregator,
count(DISTINCT tx_hash) as sales_count
from ethereum.core.ez_nft_sales 
where AGGREGATOR_NAME = 'Gem'
and block_timestamp >= '2022-11-29'
group by 1,2
union 
select
DISTINCT project_name as collection,
'Blur' as aggregator,
count(DISTINCT tx_hash) as sales_count
from ethereum.core.ez_nft_sales 
where AGGREGATOR_NAME = 'Blur'
and block_timestamp >= '2022-11-29'
group by 1,2)
select 
*
from main
group by 1,2,3
order by 3 desc
limit 10
"""

df2 = querying_pagination(df2_query)

#top 10 collection by volume
df3_query="""
with main as(select
DISTINCT project_name as collection,
'Uniswap' as aggregator,
sum(price_usd) as sales_vol
from ethereum.core.ez_nft_sales 
where ORIGIN_TO_ADDRESS = lower('0xef1c6e67703c7bd7107eed8303fbe6ec2554bf6b')
group by 1,2
union 
select
DISTINCT project_name as collection,
'Gem' as aggregator,
sum(price_usd) as sales_vol
from ethereum.core.ez_nft_sales 
where AGGREGATOR_NAME = 'Gem'
and block_timestamp >= '2022-11-29'
group by 1,2
union 
select
DISTINCT project_name as collection,
'Blur' as aggregator,
sum(price_usd) as sales_vol
from ethereum.core.ez_nft_sales 
where AGGREGATOR_NAME = 'Blur'
and block_timestamp >= '2022-11-29'
group by 1,2)
select 
*
from main
group by 1,2,3
order by 3 desc
limit 10
"""

df3 = querying_pagination(df3_query)

#top 10 user
df4_query="""
with main as(select
DISTINCT seller_address as seller,
'Uniswap' as aggregator,
count(DISTINCT tx_hash) as sales_count
from ethereum.core.ez_nft_sales 
where ORIGIN_TO_ADDRESS = lower('0xef1c6e67703c7bd7107eed8303fbe6ec2554bf6b')
group by 1,2
union 
select
DISTINCT seller_address as seller,
'Gem' as aggregator,
count(DISTINCT tx_hash) as sales_count
from ethereum.core.ez_nft_sales 
where AGGREGATOR_NAME = 'Gem'
and block_timestamp >= '2022-11-29'
group by 1,2
union 
select
DISTINCT seller_address as seller,
'Blur' as aggregator,
count(DISTINCT tx_hash) as sales_count
from ethereum.core.ez_nft_sales 
where AGGREGATOR_NAME = 'Blur'
and block_timestamp >= '2022-11-29'
group by 1,2)
select 
*
from main
group by 1,2,3
order by 3 desc
limit 10
"""

df4 = querying_pagination(df4_query)

#top 10 user by volume
df5_query="""
with main as(select
DISTINCT seller_address as seller,
'Uniswap' as aggregator,
sum(price_usd) as sales_volume
from ethereum.core.ez_nft_sales 
where ORIGIN_TO_ADDRESS = lower('0xef1c6e67703c7bd7107eed8303fbe6ec2554bf6b')
and price_usd is not null
group by 1,2
union 
select
DISTINCT seller_address as seller,
'Gem' as aggregator,
sum(price_usd) as sales_volume
from ethereum.core.ez_nft_sales 
where AGGREGATOR_NAME = 'Gem'
and block_timestamp >= '2022-11-29'
and price_usd is not null
group by 1,2
union 
select
DISTINCT seller_address as seller,
'Blur' as aggregator,
sum(price_usd) as sales_volume
from ethereum.core.ez_nft_sales 
where AGGREGATOR_NAME = 'Blur'
and block_timestamp >= '2022-11-29'
and price_usd is not null
group by 1,2)
select 
*
from main
group by 1,2,3
order by 3 desc
limit 10
"""

df5 = querying_pagination(df5_query)

options = st.multiselect(
    '**Select your desired aggregator:**',
    options=df['aggregator'].unique(),
    default=df['aggregator'].unique(),
    key='collection'
)

if len(options) > 0:
 st.subheader('Aggregator transaction count')
 df = df.query("aggregator == @options")
 df1 = df1.query("aggregator == @options")
 df2 = df2.query("aggregator == @options")
 df3 = df3.query("aggregator == @options")
 df4 = df4.query("aggregator == @options")
 df5 = df5.query("aggregator == @options")

 st.subheader('User categorize by count of sales')
 cc1, cc2= st.columns([1, 1])
 with cc1:
  fig = px.bar(df, y='sellers_count', x='sales_count', color='aggregator', title='User categorize by count of sales')
  fig.update_layout(legend_title=None, legend_y=0.5)
  st.plotly_chart(fig, use_container_width=True, theme='streamlit')
 with cc2:
  fig = px.pie(df, values='sellers_count', names='sales_count', title='User categorize by count of sales')
  fig.update_layout(legend_title=None, legend_y=0.5)
  fig.update_traces(textinfo='percent+label', textposition='inside')
  st.plotly_chart(fig, use_container_width=True, theme='streamlit')

 st.subheader('User categorize by volume(USD) of sales')
 cc1, cc2= st.columns([1, 1])
 with cc1:
  fig = px.bar(df1, y='count_sellers', x='sale_volume', color='aggregator', title='User categorize by volume(USD) of sales')
  fig.update_layout(legend_title=None, legend_y=0.5)
  st.plotly_chart(fig, use_container_width=True, theme='streamlit')
 with cc2:
  fig = px.pie(df1, values='count_sellers', names='sale_volume', title='User categorize by volume(USD) of sales')
  fig.update_layout(legend_title=None, legend_y=0.5)
  fig.update_traces(textinfo='percent+label', textposition='inside')
  st.plotly_chart(fig, use_container_width=True, theme='streamlit')

 st.subheader('Top 10 collection by count of sale')
 cc1, cc2= st.columns([1, 1])
 with cc1:
  fig = px.bar(df2, y='sales_count', x='collection', color='aggregator', title='Top 10 collection by count of sale')
  fig.update_layout(legend_title=None, legend_y=0.5)
  st.plotly_chart(fig, use_container_width=True, theme='streamlit')
 with cc2:
  fig = px.pie(df2, values='sales_count', names='collection', title='Top 10 collection by count of sale')
  fig.update_layout(legend_title=None, legend_y=0.5)
  fig.update_traces(textinfo='percent+label', textposition='inside')
  st.plotly_chart(fig, use_container_width=True, theme='streamlit')

 st.subheader('Top 10 collection by volume(USD) of sale')
 cc1, cc2= st.columns([1, 1])
 with cc1:
  fig = px.bar(df3, y='sales_vol', x='collection', color='aggregator', title='Top 10 collection by volume(USD) of sale')
  fig.update_layout(legend_title=None, legend_y=0.5)
  st.plotly_chart(fig, use_container_width=True, theme='streamlit')
 with cc2:
  fig = px.pie(df3, values='sales_vol', names='collection', title='Top 10 collection by volume(USD) of sale')
  fig.update_layout(legend_title=None, legend_y=0.5)
  fig.update_traces(textinfo='percent+label', textposition='inside')
  st.plotly_chart(fig, use_container_width=True, theme='streamlit')

 st.subheader('Top 10 user by count of sale')
 cc1, cc2= st.columns([1, 1])
 with cc1:
  st.caption('Top 10 user by count of sale')
  st.bar_chart(df4, x='seller', y = 'sales_count', width = 400, height = 400)
 with cc2:
  fig = px.pie(df4, values='sales_count', names='seller', title='Top 10 user by count of sale')
  fig.update_layout(legend_title=None, legend_y=0.5)
  fig.update_traces(textinfo='percent+label', textposition='inside')
  st.plotly_chart(fig, use_container_width=True, theme='streamlit')

 st.subheader('Top 10 user by volume(USD) of sale')
 cc1, cc2= st.columns([1, 1])
 with cc1:
  st.caption('Top 10 user by volume(USD) of sale')
  st.bar_chart(df5, x='seller', y = 'sales_volume', width = 400, height = 400)
 with cc2:
  fig = px.pie(df5, values='sales_volume', names='seller', title='Top 10 user by volume(USD) of sale')
  fig.update_layout(legend_title=None, legend_y=0.5)
  fig.update_traces(textinfo='percent+label', textposition='inside')
  st.plotly_chart(fig, use_container_width=True, theme='streamlit')
