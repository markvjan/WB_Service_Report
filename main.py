import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="WB - Servis",
                    page_icon=":bar_chart:",
                    layout="wide"
)

@st.cache
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

# ---- SIDEBAR -----
st.sidebar.header("Filtrování")

yearId = st.sidebar.multiselect(
    "Vyberte rok:",
    options=df["Rok"].unique(),
    default=df["Rok"].unique()
)

monthId = st.sidebar.multiselect(
    "Vyberte měsíc:",
    options=df["Mesic"].unique(),
    default=df["Mesic"].unique()
)

device = st.sidebar.multiselect(
    "Vyberte přístroj:",
    options=df["Pristroj"].unique(),
    default=df["Pristroj"].unique()
)

df_selection = df.query(
    "Pristroj == @device & Mesic == @monthId & Rok == @yearId"
)
df_selection22 = df.query(
    "Pristroj == @device & Mesic == @monthId & Rok == 22"
)
df_selection21 = df.query(
    "Pristroj == @device & Mesic == @monthId & Rok == 21"
)
df_selection20 = df.query(
    "Pristroj == @device & Mesic == @monthId & Rok == 20"
)
# ---- MAINPAGE -----
st.title(":bar_chart: Wöhler Bohemia - Servisní report")
st.markdown("##")

# TOK KPI's
total_device = int(df_selection["Pristroj"].count())
total_device22 = int(df_selection22["Pristroj"].count())
total_device21 = int(df_selection21["Pristroj"].count())
total_device20 = int(df_selection20["Pristroj"].count())

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Opravených přístrojů 2022:")
    st.subheader(f"kusů: {total_device22:,}")
with middle_column:
    st.subheader("Opravených přístrojů 2021:")
    st.subheader(f"kusů: {total_device21:,}")
with right_column:
    st.subheader("Opravených přístrojů 2020:")
    st.subheader(f"kusů: {total_device20:,}")
    
st.markdown("---")

# SERVIS BY DEVICE [BAR CHART]
servis_by_device = (
    df_selection.groupby(by=["Pristroj"]).count()[["Rok"]].sort_values(by="Rok")
)
fig_servis_device = px.bar(
    servis_by_device,
    y="Rok",
    x=servis_by_device.index,
    
    title="<b>Počet opravených přístrojů podle zvoleného filtru</b>",
    color_discrete_sequence=["#0083B8"] * len(servis_by_device),
)
fig_servis_device.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis_title="Typ",
    yaxis_title="Počet",
)

st.plotly_chart(fig_servis_device)
# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)