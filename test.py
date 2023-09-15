import streamlit as st
import pandas as pd
import plotly.express as px
import aws_lambda
import asyncio
from datetime import datetime

st.set_page_config(
    page_title="MIT Access Analytics",
    page_icon=":bar_chart:",
    layout="wide"
)

SERVER_TYPE = "lambda"
# SERVER_TYPE = "websocket"

result_data = None

media_type_ref = {
    "090": "Physical Card",
    "501": "iPhone",
    "502": "iWatch",
    "503": "Android"
}

btn_col1, btn_col2, btn_col3, btn_col4, btn_col5, btn_col6, btn_col7, btn_col8,  = st.columns(8)
with btn_col1:
    option = st.selectbox('Display:', ('All', 'Students', 'Affiliates', 'Employees'))

with btn_col8:
    st.button("Refresh", type="primary")

result_data = asyncio.run(aws_lambda.fetch(option))
# print(result_data)
media_types = result_data["MEDIATYPE"]
# creation_dates = pd.DataFrame(result_data[0][1])

total_accounts = len(media_types.values)
st.title(f"MIT Access Analytics (Currently based on {total_accounts} {'Account Holders' if option == 'All' else option})")
# st.title(f"MIT Access Analytics (Based on 1000 Account Holders)")
st.text("")
st.text("")
a_col1, a_col2 = st.columns(2)
b_col1, b_col2 = st.columns(2)
# ====== MEDIATYPES (donut) ====== #
type_storage = {
    "Types": ["Physical Card", "iPhone", "iWatch", "Android", "Other"],
    "Values": [0, 0, 0, 0, 0]
}

for item in media_types:
    if item in media_type_ref:
        index = type_storage["Types"].index(media_type_ref[item])
        type_storage["Values"][index] += 1
    else:
        type_storage["Values"][4] += 1

df_mediatypes = pd.DataFrame(type_storage)

fig_mediatypes = px.pie(df_mediatypes, names="Types",
                        values="Values", hole=0.5)
with a_col1:
    st.header("Media Type Ratios")
    st.plotly_chart(fig_mediatypes)

# ====== MEDIATYPES-BAR (all) ====== #
with a_col2:
    df_all_media = pd.DataFrame(
        type_storage["Values"],
        type_storage["Types"],
        columns=["Totals"]
    )
    st.header("Media Type Totals")
    st.bar_chart(df_all_media)

# ====== MEDIATYPES-BAR (watch vs phone) ====== #
watch_phone = {
    "Types": ["iPhone", "iWatch"],
    "Values": [type_storage["Values"][1], type_storage["Values"][2]]
}
with b_col1:
    df_watch_phone = pd.DataFrame(
        watch_phone["Values"],
        watch_phone["Types"],
        columns=["Totals"]
    )
    st.header(f"iWatch vs iPhone (Total: {df_watch_phone.sum().sum()})")
    st.bar_chart(df_watch_phone)

# ====== MEDIATYPES-BAR (mobile vs physical) ====== #
watch_phone = {
    "Types": ["Mobile", "Physical"],
    "Values": [type_storage["Values"][1]+type_storage["Values"][2]+type_storage["Values"][3], type_storage["Values"][0]]
}
with b_col2:
    df_mobile_physical = pd.DataFrame(watch_phone)
    fig_mediatypes = px.pie(df_mobile_physical, names="Types",
                        values="Values")
    st.header(f"Mobile vs Physical (Total: {df_mobile_physical.values[0][1] + df_mobile_physical.values[1][1]})")
    st.plotly_chart(fig_mediatypes)

# ====== No. of Credentials by Date (created?) ======
if option == "All":
    date_data = asyncio.run(aws_lambda.fetch("Dates"))

    dates = {
        "Counts": [],
        "Dates": []
    }

    dbtn_col1, dbtn_col2, dbtn_col3, dbtn_col4 = st.columns(4)

    with dbtn_col1:
        date_option = st.selectbox('Show:', ('Year by year', 'Month by month', 'Day by day'))


    year_totals = {}
    month_totals = {}
    day_totals = {}

    for index, row in date_data.iterrows():
        count = row['Count(KRB_NAME_CREATE_DATE)']
        date = row['KRB_NAME_CREATE_DATE']
        destructured_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
        curr_year = str(destructured_date.year)
        curr_month = str(destructured_date.month)
        curr_day = destructured_date.day

        # Skip the 27 October 2001 baby boom (16k records created on 1 day?) and also the 6 records created on 1989 (just for better display sake)
        # if curr_year == 2001 and curr_month == 10 and curr_day == 27 or curr_year == 1989:
        #     continue
        
        if date_option == "Year by year":
            if curr_year not in year_totals:
                year_totals[curr_year] = 0
            else:
                year_totals[curr_year] += count

        if date_option == "Month by month":
            if curr_month not in month_totals:
                month_totals[curr_month] = 0
            else:
                month_totals[curr_month] += count

        if date_option == "Day by day":
            if curr_day not in day_totals:
                day_totals[curr_day] = 0
            else:
                day_totals[curr_day] += count
            

    if date_option == "Year by year":
        for year in year_totals:
            dates["Counts"].append(year_totals[year])
            dates["Dates"].append(year)

    if date_option == "Month by month":
        month_ref = {
            "1": "January",
            "2": "February",
            "3": "March",
            "4": "April",
            "5": "May",
            "6": "June",
            "7": "July",
            "8": "August",
            "9": "September",
            "10": "October",
            "11": "November",
            "12": "December"
        }
        for month in month_totals:
            dates["Counts"].append(month_totals[month])
            dates["Dates"].append(month_ref[month])
        
    if date_option == "Day by day":
        for day in day_totals:
            dates["Counts"].append(day_totals[day])
            dates["Dates"].append(day)

    df_dates = pd.DataFrame(
        dates["Counts"],
        dates["Dates"],
        columns=["Total Devices per Date"]
    )

    date_text_ref = {
        'Year by year': "Year",
        'Month by month': "Month",
        'Day by day': "Day of the month"
    }

    st.header(f"No. of Credentials Created by {date_text_ref[date_option]} (Work in progress)")
    st.line_chart(df_dates)

# ====== Expirations ====== #

# expiration_storage = {
#     "Category": ["Expired", "Valid"],
#     "Values": [0, 0]
# }

# expiration_dates = result_data["EXPIRATIONDATE"]


# for date in expiration_dates:

#     if type(date) == str:
#         # Convert to epoch
#         date_object = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

#         date = date_object.timestamp()

#     if not math.isnan(date):
#         try:
#             today = datetime.now()
#             date_reformatted = int(date / 1000)
#             date_to_compare = datetime.fromtimestamp(date_reformatted)
#             if date_to_compare < today:
#                 expiration_storage["Values"][0] += 1
#             else:
#                 expiration_storage["Values"][1] += 1

#         except Exception as e:
#             print(e)

# df_expiration_dates = pd.DataFrame(expiration_storage)

# figure_expirations = px.pie(
#     df_expiration_dates, names="Category", values="Values", title="Account Expirations")

# with col1:
#     st.header("Expired Accounts")
#     st.plotly_chart(figure_expirations)



# # ====== Classifications ====== #


# # ====== TYPES ====== #
# totals_types = result_data["TYPE"].value_counts()
# df_types = pd.DataFrame(
#     totals_types.values,
#     totals_types.index,
#     columns=["Total"]
# )

# st.header("Member Types")
# st.bar_chart(df_types, height=500)


# # ====== LAST ACCESSED (TOTALS) ====== #
# last_access = df["LAST ACCESS"]
# totals_last_access = last_access.value_counts()
# df_last_access = pd.DataFrame(totals_last_access)

# st.header("Last Accessed")
# st.area_chart(df_last_access)


# # ====== LAST ACCESSED (MAP) ====== #
# # Compile locations into array

# location_reference = {
#     "library": [42.36056569, -71.08943549],
#     "caffeteria": [42.37312483, -71.10085615],
#     "main office": [42.36178193, -71.09631679],
#     "resource facility": [42.36666569, -71.09903768],
#     "tech department A": [42.34335434, -71.08819543],
#     "tech department B": [42.36519256, -71.08819543],
#     "tech department C": [42.3708027 , -71.09066592],
#     "entrance security": [42.34762074, -71.09090888]
# }

# locations = []

# for location in last_access:
#     locations.append(location_reference[location])

# df_locations = pd.DataFrame(
#     np.random.randn(100, 2) / [150, 150] + [42.36, -71.09], # or locations var
#     columns=['lat', 'lon'])

# st.header("Location Access")
# st.map(df_locations)


# # ====== EXPIRED ACCOUNTS ====== #
# start_dates = df["STARTDATE"]
# end_dates = df["ENDDATE"]

# total_enddates = start_dates.value_counts()

# # Determine number of expired accounts based on end date
# expired_count = 0
# for date in end_dates:
#     if date != "-":
#         expired_count += 1


# active_count = total_accounts - expired_count

# df_expired_accounts = pd.DataFrame([expired_count], [active_count], columns=["Expired"])
# st.header("Expired accounts")
# st.bar_chart(df_expired_accounts)


# IMPORTANT: For celebrations only. DO NOT USE!
# st.balloons()
