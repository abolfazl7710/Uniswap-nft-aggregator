import streamlit as st

st.set_page_config(
    page_title="Home",
    layout= "wide",
    page_icon="🏠",
)
st.title("🏠 Home")
st.sidebar.success("🏠 Home")

st.write("""
 # ❓Uniswap NFT Aggregator #
 # Methodology #
 In this dashboard, I used python and streamlit library to display charts.
 The data used was obtained from shroomDk and Flipsidecrypto.
 All the codes of this web app can be seen in this link (Github). 
 
 https://github.com/abolfazl7710/Uniswap-nft-aggregator
"""
)
st.write("""
 # 📝 Introduction #

 NFTs and ERC-20 tokens have largely existed as two separate ecosystems within crypto, but both are essential to growing the digital economy. Launching NFTs on Uniswap is our first step in building more interoperable experiences between the two.To bring users the first-rate experience they've come to expect with Uniswap, we built the aggregator to deliver better prices, faster indexing, safer smart contracts, and efficient execution.With Uniswap, the NFT ecosystem can expect:More listings, at better prices.Aggregators deliver better prices by combining multiple marketplace listings into one interface. At launch, Uniswap will support OpenSea, X2Y2, LooksRare, Sudoswap, Larva Labs, X2Y2, Foundation, NFT20, and NFTX.More gas savings. Save up to 15 percent on gas costs compared to other NFT aggregators when purchasing across marketplaces. Powered by our new open-sourced Universal Router contract, Uniswap's aggregator can save tens of thousands of gas units over other marketplaces.Trustless and open source. Uniswap is committed to being trustless, transparent, and open source. We've brought those same design principles to NFTs and open-sourced all of our front-end code, making us the first major NFT platform to do so.

 """
 )

st.write("")
st.write("")
st.write("")
st.write("📓 Contact data")
c1, c2 = st.columns(2)
with c1:
    st.info('**Twitter: [@daryoshali](https://twitter.com/daryoshali)**')
with c2:
    st.info('**Data: [Github](https://github.com/abolfazl7710)**')

st.write("")
st.write("")
st.write("")
st.write("Thanks for MetricsDAO and flipsidecrypto team")
