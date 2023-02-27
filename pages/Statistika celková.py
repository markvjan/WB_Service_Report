import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import datetime as dt
import dateutil.relativedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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

#@st.cache
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
##This is grouped by Pristroj and Rok column and it is created column with count of Pristroj in specific year 
servis_by_device0 = (
    df_selection0.groupby(['Pristroj','Rok']).size().reset_index(name='counts')
)

##This creates group of Pristroj column according first string
servis_by_group = servis_by_device0
servis_by_group = (
    servis_by_group.groupby([servis_by_group.Pristroj.str[:1],'Rok']).sum().reset_index()
)
##Renamed column to specific name
servis_by_group.loc[servis_by_group['Pristroj'].str.contains('A'), 'Pristroj'] = 'Analyzátory'
servis_by_group.loc[servis_by_group['Pristroj'].str.contains('C'), 'Pristroj'] = 'CM'
servis_by_group.loc[servis_by_group['Pristroj'].str.contains('D'), 'Pristroj'] = 'DC/DM'
servis_by_group.loc[servis_by_group['Pristroj'].str.contains('E'), 'Pristroj'] = 'E98'
servis_by_group.loc[servis_by_group['Pristroj'].str.contains('G'), 'Pristroj'] = 'GS'
servis_by_group.loc[servis_by_group['Pristroj'].str.contains('V'), 'Pristroj'] = 'Kamery'

##Overall graph with each device
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
    xaxis_title="<b>Přístroj</b>",
    yaxis_title="<b>Počet</b>",
)

##Overall graph with group device
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
    xaxis_title="<b>Přístroj</b>",
    yaxis_title="<b>Počet</b>",
)

##New selection for pie chart for current year
df_pie_selection = servis_by_group.query(
    "Rok == @YearPrev0"
)

#Show charts
st.plotly_chart(fig_servis_device)
st.plotly_chart(fig_servis_group)
st.markdown("---")

##Section for show pie chart with select box
option = st.selectbox(
    'Vyberte rok pro porovnání koláčových grafů:',
    (YearPrev1, YearPrev2))
##New selection for pie chart for previous year
df_pie_selection_prev = servis_by_group.query(
    "Rok == @option"
)

# Create subplots: use 'domain' type for Pie subplot
fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
fig.add_trace(go.Pie(labels=df_pie_selection['Pristroj'], values=df_pie_selection['counts'], name="Rok 20"+YearPrev0, textinfo='label+percent',
                             insidetextorientation='radial'), 1, 1)
fig.add_trace(go.Pie(labels=df_pie_selection_prev['Pristroj'], values=df_pie_selection_prev['counts'], name="Rok 20"+YearPrev1, textinfo='label+percent',
                             insidetextorientation='radial'), 1, 2)

# Use `hole` to create a donut-like pie chart
fig.update_traces(hole=.4, hoverinfo="label+percent+name")

fig.update_layout(
    title_text="<b>Graf: Procentuální zastoupení opravených přístrojů - porovnání</b>",
    # Add annotations in the center of the donut pies.
    annotations=[dict(text='Rok 20'+YearPrev0, x=0.18, y=0.5, font_size=20, showarrow=False),
                 dict(text='Rok 20'+option, x=0.82, y=0.5, font_size=20, showarrow=False)])

#Show charts
st.plotly_chart(fig, use_container_width=True)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)