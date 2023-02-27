import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np
import os
import glob

###################    EXCEL IMPORT PART     #################
folder_path = 'C:\\Users\\jan_markvart\\Documents\\Python\\Projects\\Test1st\\data\\OutputData.xlsx'
#for filename in glob.glob(os.path.join(folder_path, '*.xlsm')):
dataServiceID = pd.read_excel(folder_path, 'receiptStock', dtype={'abno':'int'})
del dataServiceID["tel"]
del dataServiceID["adress"]
del dataServiceID["ico"]
del dataServiceID["mail"]
del dataServiceID["description"]
#rename columns
dataServiceID.rename(columns={'protocol_id': 'Číslo protokolu', "customer_id": "Č. zákazníka", "device": "Přístroj", "s_n": "S/N", "name": "Jméno", "status": "Status", "abno": "AB číslo"},inplace=True)

st.set_page_config(page_title="WB - Servis - Příjem",
                    page_icon=":bar_chart:",
                    layout="wide"
)

#@st.cache
def get_data_from_excel():
    df = pd.read_excel(
        io='dataHistory.xlsx',
        engine='openpyxl',
        sheet_name='data',
        usecols='A:C',
        nrows=3476,
    )
    return df
df = get_data_from_excel()

# ---- MAINPAGE -----
st.title("Wöhler Bohemia - Příjem")
st.markdown("##")

# TOK KPI's
st.markdown("---")

# SERVIS BY DEVICE [BAR CHART]
st.dataframe(dataServiceID)  # Same as st.write(df)
