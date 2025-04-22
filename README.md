# Order Analysis Dashboard

A Streamlit dashboard for analyzing order data from Google Sheets.

## Requirements

- Python 3
- Streamlit
- Pandas

## Setup

1. Clone this repository:

   ```
   git clone https://github.com/dwimnofan/orderan-fabron.git
   cd https://github.com/dwimnofan/orderan-fabron.git
   ```

2. Create and activate a virtual environment:

   ```
   python3 -m venv .venv

   # On Windows:
   .venv\Scripts\activate

   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. Install required packages:
   ```
   pip install streamlit pandas
   ```

## Usage

1. Run the Streamlit app:

   ```
   streamlit run main.py
   ```

2. The app will open in your default web browser. If not, you can access it at:
   ```
   http://localhost:8501
   ```

## Data Source

The app fetches data from a Google Sheets document. The data should contain columns for price information, categories, brands, and stores. The app will automatically detect relevant columns.

## Customization

You can modify the Google Sheets source by changing the `sheet_id` and `gid` variables in `main.py`.
