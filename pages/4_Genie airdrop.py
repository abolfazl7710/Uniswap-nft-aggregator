import streamlit as st
from shroomdk import ShroomDK
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="💠 Genie airdrop",
    layout= "wide",
    page_icon="💠 ",
)
st.title("💠 Genie airdrop")
st.sidebar.success("💠 Genie airdrop")

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
BLOCK_TIMESTAMP::date as date,
'1sd tier' as type,
count(DISTINCT tx_hash) as claimed_count,
(count(DISTINCT tx_hash) * 300) as claimed_volume
from ethereum.core.fact_event_logs
where CONTRACT_ADDRESS='0x8b799381ac40b838bba4131ffb26197c432afe78'
and EVENT_INPUTS:amount = '300000000'
group by 1,2
union
select
BLOCK_TIMESTAMP::date as date, 
'2nd tier' as type,
count(DISTINCT tx_hash) as claimed_count,
(count(DISTINCT tx_hash) * 1000) as claimed_volume
from ethereum.core.fact_event_logs
where CONTRACT_ADDRESS='0x8b799381ac40b838bba4131ffb26197c432afe78'
and EVENT_INPUTS:amount = '1000000000'
group by 1,2
union 
select
BLOCK_TIMESTAMP::date as date,
'3rd tier' as type,
count(DISTINCT tx_hash) as claimed_count,
(count(DISTINCT tx_hash) * 1300) as claimed_volume
from ethereum.core.fact_event_logs
where CONTRACT_ADDRESS='0x8b799381ac40b838bba4131ffb26197c432afe78'
and EVENT_INPUTS:amount = '1300000000'
group by 1,2
"""

df = querying_pagination(df_query)

#total 
df1_query="""
select
'1sd tier' as type,
count(DISTINCT tx_hash) as claimed_count,
(count(DISTINCT tx_hash) * 300) as claimed_volume
from ethereum.core.fact_event_logs
where CONTRACT_ADDRESS='0x8b799381ac40b838bba4131ffb26197c432afe78'
and EVENT_INPUTS:amount = '300000000'
group by 1
union
select
'2nd tier' as type,
count(DISTINCT tx_hash) as claimed_count,
(count(DISTINCT tx_hash) * 1000) as claimed_volume
from ethereum.core.fact_event_logs
where CONTRACT_ADDRESS='0x8b799381ac40b838bba4131ffb26197c432afe78'
and EVENT_INPUTS:amount = '1000000000'
group by 1
union 
select
'3rd tier' as type,
count(DISTINCT tx_hash) as claimed_count,
(count(DISTINCT tx_hash) * 1300) as claimed_volume
from ethereum.core.fact_event_logs
where CONTRACT_ADDRESS='0x8b799381ac40b838bba4131ffb26197c432afe78'
and EVENT_INPUTS:amount = '1300000000'
group by 1
"""

df1 = querying_pagination(df1_query)

st.subheader('Genie airdrop')
st.write("""
 
 With the launch Uniswap NFT Aggregator on the Ethereum Mainnet announced that it will distribute 5 million USDC to historical users of the Genie aggregator. The snapshot was taken on April 15, 2022 at 00:00 UTC. According to the announcement, those that included airdrops were categorized into three tires. The first tier was the users who had done the transaction before the snapshot, each of which included 300 USDC. The second tier was the users who were Genesis Genie NFT holders at the time of the snapshot, and each included 1000 USDC. And the third tier were users who were both in tier one and in tier two, each of whom received 1,300 USDC.
 """)
st.subheader('Genie airdrop calim count')
cc1, cc2= st.columns([1, 1])
 
with cc1:
  fig = px.bar(df, x='date', y='claimed_count',color='type', title='Daily genie airdrop calim count at each tier')
  fig.update_layout(legend_title=None, legend_y=0.5)
  st.plotly_chart(fig, use_container_width=True, theme='streamlit')
with cc2:
  st.caption('Genie airdrop calim count at each tier')
  st.bar_chart(df1, x='type', y = 'claimed_count', width = 400, height = 400)

st.subheader('Aggregator transaction fee(USD)')
cc1, cc2= st.columns([1, 1])
 
with cc1:
  fig = px.bar(df, x='date', y='claimed_volume',color='type', title='Daily genie airdrop calim volume at each tier')
  fig.update_layout(legend_title=None, legend_y=0.5)
  st.plotly_chart(fig, use_container_width=True, theme='streamlit')
with cc2:
  st.caption('Genie airdrop calim volume at each tier')
  st.bar_chart(df1, x='type', y = 'claimed_volume', width = 400, height = 400)
