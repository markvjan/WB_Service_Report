import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import datetime as dt
import dateutil.relativedelta

###################      DATE AND   TIME     #################
#get actual date and save it to variable as string in format year month day
actualMonth = dt.now()
YearPrev0 = actualMonth.strftime('%y')
YearPrev1 = actualMonth + dateutil.relativedelta.relativedelta(years=-1)
YearPrev2 = actualMonth + dateutil.relativedelta.relativedelta(years=-2)
YearPrev1 = YearPrev1.strftime('%y')
YearPrev2 = YearPrev2.strftime('%y')

st.set_page_config(page_title="WB - Servis - Statistika celková",
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
        dtype={'Rok':'str', 'Mesic':'str'}
    )
    return df
df = get_data_from_excel()
# ---- SIDEBAR ------
st.sidebar.header("Filtrování")

device = st.sidebar.multiselect(
    "Vyberte přístroj:",
    options=df["Pristroj"].unique(),
    default=df["Pristroj"].unique()
)

df_selection0 = df.query(
    "Pristroj == @device & (Rok == @YearPrev0 | Rok == @YearPrev1 | Rok == @YearPrev2)"
)

# ---- MAINPAGE -----
st.title(":bar_chart: Wöhler Bohemia - Servisní report celkový")


st.markdown("---")

# SERVIS BY DEVICE [BAR CHART]
servis_by_device0 = (
    df_selection0.groupby(['Pristroj','Rok']).size().reset_index(name='counts')
)

servis_by_group = servis_by_device0
servis_by_group = (
    servis_by_group.groupby([servis_by_group.Pristroj.str[:1],'Rok']).sum().reset_index()
)
servis_by_group.loc[servis_by_group['Pristroj'].str.contains('A'), 'Pristroj'] = 'Analyzátory'
servis_by_group.loc[servis_by_group['Pristroj'].str.contains('C'), 'Pristroj'] = 'CM'
servis_by_group.loc[servis_by_group['Pristroj'].str.contains('D'), 'Pristroj'] = 'DC/DM'
servis_by_group.loc[servis_by_group['Pristroj'].str.contains('E'), 'Pristroj'] = 'E98'
servis_by_group.loc[servis_by_group['Pristroj'].str.contains('G'), 'Pristroj'] = 'GS'
servis_by_group.loc[servis_by_group['Pristroj'].str.contains('V'), 'Pristroj'] = 'Kamery'
print(servis_by_group)

fig_servis_device = px.bar(
    servis_by_device0,
    y="counts",
    x="Pristroj",
    color='Rok',
    barmode='group',
    title="<b>Graf: Přehled opravených přístrojů, porovnání posledních 3 let</b>",
    #color_discrete_sequence=["#0083B8"] * len(servis_by_device0),
)

fig_servis_device.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis_title="Přístroj",
    yaxis_title="Počet",
)
  
fig_servis_group = px.bar(
    servis_by_group,
    y="counts",
    x="Pristroj",
    color='Rok',
    barmode='group',
    title="<b>Graf: Přehled opravených přístrojů, porovnání posledních 3 let podle skupin přístrojů</b>",
    #color_discrete_sequence=["#0083B8"] * len(servis_by_device0),
)

fig_servis_group.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis_title="Přístroj",
    yaxis_title="Počet",
)

st.plotly_chart(fig_servis_device)
st.plotly_chart(fig_servis_group)
# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)