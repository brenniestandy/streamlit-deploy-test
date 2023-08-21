import streamlit as st
import pandas as pd
import numpy as np

location_reference = {
    "library": [42.36056569, -71.08943549],
    "caffeteria": [42.37312483, -71.10085615],
    "main office": [42.36178193, -71.09631679],
    "resource facility": [42.36666569, -71.09903768],
    "tech department A": [42.34335434, -71.08819543],
    "tech department B": [42.36519256, -71.08819543],
    "tech department C": [42.3708027 , -71.09066592],
    "entrance security": [42.34762074, -71.09090888]
}

st.set_page_config(
    page_title="MIT Access Analytics",
    page_icon=":bar_chart:",
    layout="wide"
)

df = pd.read_excel(
    io='EXAMPLEDATA.xlsx',
    engine='openpyxl',
    # usecols='B'
)
total_accounts = len(df.value_counts())
st.title(f"MIT Access Analytics ({total_accounts} Account Holders)")


# ====== MEDIA TYPES ====== #
totals_mediatype = df['MEDIATYPE'].value_counts()
df_mediatype = pd.DataFrame(totals_mediatype.values, totals_mediatype.index, columns=["Total"])

st.header("Media Types")
st.bar_chart(df_mediatype, height=500)
# st.line_chart(new_df)


# ====== LAST ACCESSED (TOTALS) ====== #
last_access = df["LAST ACCESS"]
totals_last_access = last_access.value_counts()
df_last_access = pd.DataFrame(totals_last_access)

st.header("Last Accessed")
st.area_chart(df_last_access)


# ====== LAST ACCESSED (MAP) ====== #
# Compile locations into array
locations = []

for location in last_access:
    locations.append(location_reference[location])

df_locations = pd.DataFrame(
    np.random.randn(100, 2) / [150, 150] + [42.36, -71.09], # or locations var
    columns=['lat', 'lon'])

st.header("Location Access")
st.map(df_locations)


# ====== EXPIRED ACCOUNTS ====== #
start_dates = df["STARTDATE"]
end_dates = df["ENDDATE"]

total_enddates = start_dates.value_counts()

# Determine number of expired accounts based on end date
expired_count = 0
for date in end_dates:
    if date != "-":
        expired_count += 1


active_count = total_accounts - expired_count

df_expired_accounts = pd.DataFrame([expired_count], [active_count], columns=["Expired"])
st.header("Expired accounts")
st.bar_chart(df_expired_accounts)



# IMPORTANT: For celebrations only. DO NOT USE!
# st.balloons()
