import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import datetime as dt
import dateutil.relativedelta

###################      DATE AND   TIME     #################
#get actual date and save it to variable as string in format year month day
actualMonth = dt.now()
MonthPrev1 = actualMonth + dateutil.relativedelta.relativedelta(months=-1)
MonthPrev2 = actualMonth + dateutil.relativedelta.relativedelta(months=-2)
MonthPrev0 = actualMonth.strftime('%m')
MonthPrev1 = MonthPrev1.strftime('%m')
MonthPrev2 = MonthPrev2.strftime('%m')
YearPrev0 = actualMonth.strftime('%y')
YearPrev1 = actualMonth + dateutil.relativedelta.relativedelta(years=-1)
YearPrev2 = actualMonth + dateutil.relativedelta.relativedelta(years=-2)
YearPrev1 = YearPrev1.strftime('%y')
YearPrev2 = YearPrev2.strftime('%y')

st.set_page_config(page_title="WB - Servis - Statistika",
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
st.sidebar.header("Filtrování graf")

yearId  = st.sidebar.selectbox(
    'Vyberte rok:',
    (YearPrev0, YearPrev1, YearPrev2))

monthId  = st.sidebar.selectbox(
    'Vyberte rok:',
    (MonthPrev0, MonthPrev1, MonthPrev2))

df_selection = df.query(
   "Mesic == @monthId & Rok == @yearId"
)
#TOTAL by YEAR
df_selectionYearPrev0 = df.query("Rok == @YearPrev0")
df_selectionYearPrev1 = df.query("Rok == @YearPrev1")
df_selectionYearPrev2 = df.query("Rok == @YearPrev2")
#TOTAL by YEAR0 and MONTH
df_selectionYearPrev0Month0 = df.query("Rok == @YearPrev0 & Mesic == @MonthPrev0")
df_selectionYearPrev0Month1 = df.query("Rok == @YearPrev0 & Mesic == @MonthPrev1")
df_selectionYearPrev0Month2 = df.query("Rok == @YearPrev0 & Mesic == @MonthPrev2")
#TOTAL by YEAR1 and MONTH
df_selectionYearPrev1Month0 = df.query("Rok == @YearPrev1 & Mesic == @MonthPrev0")
df_selectionYearPrev1Month1 = df.query("Rok == @YearPrev1 & Mesic == @MonthPrev1")
df_selectionYearPrev1Month2 = df.query("Rok == @YearPrev1 & Mesic == @MonthPrev2")
#TOTAL by YEAR2 and MONTH
df_selectionYearPrev2Month0 = df.query("Rok == @YearPrev2 & Mesic == @MonthPrev0")
df_selectionYearPrev2Month1 = df.query("Rok == @YearPrev2 & Mesic == @MonthPrev1")
df_selectionYearPrev2Month2 = df.query("Rok == @YearPrev2 & Mesic == @MonthPrev2")

# ---- MAINPAGE -----
st.title(":bar_chart: Wöhler Bohemia - Servisní report")
st.subheader(body="Statistika opravenených přístrojů")

# TOK KPI's
total_deviceYearPrev0 = int(df_selectionYearPrev0["Pristroj"].count())
total_deviceYearPrev1 = int(df_selectionYearPrev1["Pristroj"].count())
total_deviceYearPrev2 = int(df_selectionYearPrev2["Pristroj"].count())
total_deviceYear0Month0 = int(df_selectionYearPrev0Month0["Pristroj"].count())
total_deviceYear0Month1 = int(df_selectionYearPrev0Month1["Pristroj"].count())
total_deviceYear0Month2 = int(df_selectionYearPrev0Month2["Pristroj"].count())
total_deviceYear1Month0 = int(df_selectionYearPrev1Month0["Pristroj"].count())
total_deviceYear1Month1 = int(df_selectionYearPrev1Month1["Pristroj"].count())
total_deviceYear1Month2 = int(df_selectionYearPrev1Month2["Pristroj"].count())
total_deviceYear2Month0 = int(df_selectionYearPrev2Month0["Pristroj"].count())
total_deviceYear2Month1 = int(df_selectionYearPrev2Month1["Pristroj"].count())
total_deviceYear2Month2 = int(df_selectionYearPrev2Month2["Pristroj"].count())

left_column, month0_column, month1_column, month2_column, sum_column = st.columns(5)
with left_column:
    st.subheader("Rok")
    st.subheader(f"20{YearPrev0}")
    st.subheader(f"20{YearPrev1}")
    st.subheader(f"20{YearPrev2}")
with month0_column:
    st.subheader(f"Měsíc {MonthPrev0}:")
    st.subheader(f"{total_deviceYear0Month0:,}")
    st.subheader(f"{total_deviceYear1Month0:,}")
    st.subheader(f"{total_deviceYear2Month0:,}")
with month1_column:
    st.subheader(f"Měsíc {MonthPrev1}:")
    st.subheader(f"{total_deviceYear0Month1:,}")
    st.subheader(f"{total_deviceYear1Month1:,}")
    st.subheader(f"{total_deviceYear2Month1:,}")
with month2_column:
    st.subheader(f"Měsíc {MonthPrev2}:")
    st.subheader(f"{total_deviceYear0Month2:,}")
    st.subheader(f"{total_deviceYear1Month2:,}")
    st.subheader(f"{total_deviceYear2Month2:,}")
with sum_column:
    st.subheader("Celkem:")
    st.subheader(f"{total_deviceYearPrev0:,}")
    st.subheader(f"{total_deviceYearPrev1:,}")
    st.subheader(f"{total_deviceYearPrev2:,}")
    
st.markdown("---")

# SERVIS BY DEVICE [BAR CHART]
servis_by_device = (
    df_selection.groupby(by=["Pristroj"]).count()[["Rok"]].sort_values(by="Rok")
)
fig_servis_device = px.bar(
    servis_by_device,
    y="Rok",
    x=servis_by_device.index,
    
    title="<b>Graf:</b> Statistika opravených přístrojů v roce <b>20" + yearId + "</b> pro měsíc: <b>" + monthId +"</b>",
    color_discrete_sequence=["#0083B8"] * len(servis_by_device),
)
fig_servis_device.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis_title="Přístroj",
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