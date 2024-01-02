import pandas as pd
import plotly.express as px
import streamlit as st
import pymongo

st.set_page_config(page_title="WB - Servis - Příjem přístrojů",
                    page_icon=":bar_chart:",
                    layout="wide"
)

# Initialize Mongodb connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return pymongo.MongoClient("mongodb+srv://honzamarkvart:LordTamis18@cluster0.ibdbn6l.mongodb.net/?retryWrites=true&w=majority")

client = init_connection()

@st.cache_data(ttl=600)
def get_data_DB():
    db = client["streamlit-db"]
    collection = db["protocols"]
    query11 = {}  # Define your query here if needed
    data = list(collection.find(query11))
    df = pd.DataFrame(data)
    df = df.drop(['_id'], axis=1)
    return df

df = get_data_DB()
df = df.drop(['adress', 'ico','mail'], axis=1)
df['date'] = df['date'].dt.date
#rename columns
df.rename(columns={'protocol_id': 'Číslo protokolu', "customer_id": "Č. zákazníka", "device": "Přístroj", "s_n": "S/N", "name": "Jméno", "status": "Status", "abno": "AB číslo", "tel":"Telefon", "date":"Příjem", "description":"Popis"},inplace=True)


# ---- MAINPAGE -----
st.title("Wöhler Bohemia - Příjem")
st.markdown("##")

# TOK KPI's
st.markdown("---")

# WRITE TABLE
st.dataframe(df)  # Same as st.write(df)
