import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Servis",
                    page_icon=":bar_chart:",
                    layout="wide"
)

@st.cache
def get_data_from_excel():
    df = pd.read_excel(
        io='OutputData.xlsx',
        engine='openpyxl',
        sheet_name='DataPy',
        usecols='A:D',
        nrows=50,
    )
    return df
df = get_data_from_excel()

# ---- SIDEBAR -----
st.sidebar.header("Filtr")
device = st.sidebar.multiselect(
    "Vyberte přístroj:",
    options=df["device"].unique(),
    default=df["device"].unique()
)

df_selection = df.query(
    "device == @device"
)
# ---- MAINPAGE -----
st.title(":bar_chart: Servis report")
st.markdown("##")

# TOK KPI's
total_device = int(df_selection["device"].count())

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Celkový počet přístrojů:")
    st.subheader(f"kusů: {total_device:,}")
with middle_column:
    st.subheader("Nevim")
    st.subheader(f"kusů: {total_device:,}")
with right_column:
    st.subheader("Nevim again")
    st.subheader(f"kusů: {total_device:,}")
    
st.markdown("---")

# SERVIS BY DEVICE [BAR CHART]
servis_by_device = (
    df_selection.groupby(by=["device"]).sum()[["repair_t"]].sort_values(by="repair_t")
)
fig_servis_device = px.bar(
    servis_by_device,
    x="repair_t",
    y=servis_by_device.index,
    orientation="h",
    title="<b>Počet minut strávených na přístroji podle typu</b>",
    color_discrete_sequence=["#0083B8"] * len(servis_by_device),
)
fig_servis_device.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
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