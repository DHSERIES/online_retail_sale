import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns
import plotly.express as px

dir = "/home/hoang/Local/work/online_furniture_retailer.csv"
# Load the dataset
if not os.path.exists(dir):
    st.error("Dataset not found. Please check the file path.")
else:
    data = pd.read_csv(dir)

df = pd.DataFrame(data)



import time
import numpy as np
import pandas as pd
import altair as alt
import streamlit as st

# --------- Page setup ---------
st.set_page_config(
    page_title=" online_furniture_retailer Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------- Sidebar (logo, nav, filters) ---------
with st.sidebar:
    st.markdown("### Adminty")
    nav = st.radio("Navigation", ["Dashboard", "Analytics", "Sales", "Settings"], index=0)
    st.markdown("---")
    
# --------- Top row KPI metrics ---------
st.markdown("### online furniture etailer 2025")
kpi_cols = st.columns([1,1,1,1], gap="large")
kpi_data = [
    ("Active Users", f"{len(df.customer_id.unique())}"),
    ("total_order", f"{len(df.order_id.unique())}"),
    ("sucessfully_delivered", f"{len(df[df.delivery_status == "Delivered"])}"),
    ("Total Revenue", f'{int(sum(df[df.delivery_status == "Delivered"].total_amount))}' + "$"),
]
for col, (label, value) in zip(kpi_cols, kpi_data):
    with col:
        st.metric(label=label, value=value)

st.markdown("")

# --------- Second row: charts (Traffic & Sales) ---------
left, right = st.columns([1, 1], gap="large")

with left:
    st.markdown('<div class="card"><h3> product_popularity  </h3>', unsafe_allow_html=True)
    # donut chart for product category
    product_category = df.groupby('product_category').size().reset_index(name='count')

    donut = alt.Chart(product_category).mark_arc(innerRadius=70).encode(
        theta=alt.Theta("count:Q"),
        color=alt.Color("product_category:N", legend=alt.Legend(title="Product Category")),
        tooltip=["product_category", "count"]
    ).properties(height=300)

    st.altair_chart(donut, use_container_width=True)
   

with right:
    st.markdown('<div class="card"><h3>product_subcategory</h3>', unsafe_allow_html=True)
    # barchart for product subcategory
    product_subcategory = df.groupby('product_subcategory').size().reset_index(name='count')
    bar = alt.Chart(product_subcategory).mark_bar().encode(
        x=alt.X('product_subcategory:N', title='Product Subcategory'),
        y=alt.Y('count:Q', title=''),
        color=alt.Color('product_subcategory:N', legend=None)
    ).properties(height=300)
    st.altair_chart(bar, use_container_width=True)

st.markdown("")

# --------- Third row: table + donut ---------
col1, col2 = st.columns([2,1], gap="large")

with col1:
    st.markdown('<div class="card"><h3> Orders</h3>', unsafe_allow_html=True)
    
with col2:
    st.markdown('<div class="card"><h3>Device Mix</h3><div class="subtle">Session share</div>', unsafe_allow_html=True)
    device = pd.DataFrame({
        "device": ["Desktop", "Mobile", "Tablet"],
        "share": [62, 30, 8],
    })
    donut = alt.Chart(device).mark_arc(innerRadius=60).encode(
        theta="share:Q",
        color=alt.Color("device:N", legend=alt.Legend(orient="bottom")),
        tooltip=["device","share"]
    ).properties(height=300)
    st.altair_chart(donut, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --------- Footer note ---------
st.caption("© 2025 Streamlit Demo • Replace demo data with your sources and wire up navigation callbacks.")
