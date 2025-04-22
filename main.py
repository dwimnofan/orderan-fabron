import pandas as pd
import streamlit as st

st.set_page_config(page_title="Order Analysis", layout="wide")
st.title("Order Analysis Dashboard")

# load data
with st.spinner('Loading data from Google Sheets...'):
    sheet_id = '1h0hifXG-WJTdAAklq_unX0wkMqYr6aeqg58aWLOeb8c'
    gid      = '0'
    url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}'

    df = pd.read_csv(url)

    # Show data null
    with st.expander("View data null information"):
        st.write("Null values in each column:")
        st.write(df.isnull().sum())

    # Process data
    df['Harga_num'] = (
        df['Harga']
          .str.replace('Rp','')
          .str.replace(r'\.','', regex=True)
          .astype(int)
    )

    # Calculate total per category
    total_per_catatan = (
        df
         .groupby('Catatan')['Harga_num']
         .sum()
         .reset_index(name='Harga_total')
    )

    # Format total price
    total_per_catatan['Total Harga'] = total_per_catatan['Harga_total'] \
        .apply(lambda x: 'Rp' + '{:,.0f}'.format(x).replace(',','.'))

    chart_data = total_per_catatan.copy()
    
    display_data = total_per_catatan[['Catatan','Total Harga']]

    # raw data
    st.subheader("Raw Data")
    st.dataframe(df)
    
    # total per category
    st.subheader("Total per Category")
    st.dataframe(display_data)
    
    # chart bar
    st.subheader("Category Analysis")
    st.bar_chart(chart_data.set_index('Catatan')['Harga_total'])