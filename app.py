import streamlit as st
import pandas as pd

# Fetch data
@st.cache_data(ttl=600)
def load_data(sheets_url: str):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    return pd.read_csv(csv_url, on_bad_lines="skip")

df = load_data("https://docs.google.com/spreadsheets/d/195xHzIOLpvVYWc_pNXhqTC_DNYn15xnv_aQ7F0BhNfg/edit#gid=855163300")

crpyto_name = []
crypto_symbol = []
crypto_price = []

for row in df.itertuples():
    crpyto_name.append(row.Name)
    crypto_price.append(row.PriceUsd)
    crypto_symbol.append(row.Symbol)

crypto = pd.DataFrame({"Name" : crpyto_name, "Symbol" : crypto_symbol, 'Price per unit (USD)': crypto_price})

# Ui Render
st.header("Cryptocurrencies price")

currency_search = st.text_input("Search currency")

# Search currency
if currency_search:
    found = 0
    result_name = []
    result_symbol = []
    result_price = []

    for i in range(len(crpyto_name)):
        if currency_search.lower() in crpyto_name[i].lower():
            result_name.append(crpyto_name[i])
            result_symbol.append(crypto_symbol[i])
            result_price.append(crypto_price[i])
            found += 1
    
    if found > 0:
        result = pd.DataFrame({"Name" : result_name, "Symbol" : result_symbol, 'Price per unit (USD)': result_price})
        if found > 5:
            with st.expander("Search Result"): 
                st.table(result)
        else:
            st.table(result)

st.table(crypto)

st.sidebar.subheader("Data taken from Kaggle")
st.sidebar.markdown("[Cryptocurrency Prices Dataset](https://www.kaggle.com/datasets/jahaidulislam/cryptocurrency-prices-dataset)")
