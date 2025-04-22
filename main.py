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
    
    # Display columns and sample data (temporary for development)
    st.write("DataFrame Columns:", df.columns.tolist())
    st.write("Sample Data (5 rows):", df.head())

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

    # Create filter sidebar
    st.sidebar.header("Filters")
    
    # Brand filter (selectbox)
    # Assuming there's a 'Brand' column - adjust if your column has a different name
    if 'Brand' in df.columns:
        brand_options = ['All'] + sorted(df['Brand'].unique().tolist())
        selected_brand = st.sidebar.selectbox("Select Brand:", brand_options)
    else:
        # Try to find a column that might contain brand information
        potential_brand_cols = [col for col in df.columns if 'brand' in col.lower() or 'merk' in col.lower()]
        if potential_brand_cols:
            brand_col = potential_brand_cols[0]
            brand_options = ['All'] + sorted(df[brand_col].unique().tolist())
            selected_brand = st.sidebar.selectbox(f"Select {brand_col}:", brand_options)
        else:
            st.sidebar.warning("No brand column found. Please adjust the code.")
            selected_brand = 'All'
    
    # Toko filter (checkbox)
    # Assuming there's a 'Toko' column - adjust if your column has a different name
    if 'Toko' in df.columns:
        toko_options = sorted(df['Toko'].unique().tolist())
        selected_toko = st.sidebar.multiselect("Select Toko:", toko_options, default=toko_options)
    else:
        # Try to find a column that might contain store information
        potential_toko_cols = [col for col in df.columns if 'toko' in col.lower() or 'store' in col.lower()]
        if potential_toko_cols:
            toko_col = potential_toko_cols[0]
            toko_options = sorted(df[toko_col].unique().tolist())
            selected_toko = st.sidebar.multiselect(f"Select {toko_col}:", toko_options, default=toko_options)
        else:
            st.sidebar.warning("No toko column found. Please adjust the code.")
            selected_toko = []
    
    # Apply filters to dataframe
    filtered_df = df.copy()
    
    # Apply brand filter if 'All' is not selected
    if selected_brand != 'All':
        if 'Brand' in df.columns:
            filtered_df = filtered_df[filtered_df['Brand'] == selected_brand]
        elif potential_brand_cols:
            filtered_df = filtered_df[filtered_df[brand_col] == selected_brand]
    
    # Apply toko filter if any selections are made
    if selected_toko:
        if 'Toko' in df.columns:
            filtered_df = filtered_df[filtered_df['Toko'].isin(selected_toko)]
        elif potential_toko_cols:
            filtered_df = filtered_df[filtered_df[toko_col].isin(selected_toko)]
    
    # Use filtered DataFrame for analysis
    # Calculate total per category using filtered data
    total_per_catatan = (
        filtered_df
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
    st.dataframe(filtered_df)
    
    # total per category
    st.subheader("Total per Category")
    st.dataframe(display_data)
    
    # chart bar
    st.subheader("Category Analysis")
    st.bar_chart(chart_data.set_index('Catatan')['Harga_total'])