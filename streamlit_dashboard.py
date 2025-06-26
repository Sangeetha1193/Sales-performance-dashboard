
import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Northwind Sales Dashboard",
    layout="wide"
)


@st.cache_data
def load_data():
    conn = sqlite3.connect('northwind.db')
    
    sales_data = pd.read_csv('sales_overview.csv')
    product_data = pd.read_csv('product_performance.csv')
    customer_data = pd.read_csv('customer_analysis.csv')
    employee_data = pd.read_csv('employee_performance.csv')
    
    return sales_data, product_data, customer_data, employee_data


def main():
    st.title(" Northwind Sales Performance Dashboard")
    
    
    sales_data, product_data, customer_data, employee_data = load_data()
    
   
    st.sidebar.title("Dashboard Navigation")
    page = st.sidebar.selectbox("Select Page", 
                               ["Executive Summary", "Sales Analysis", 
                                "Product Performance", "Customer Analysis"])
    
    if page == "Executive Summary":
        st.header("Executive Summary")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Revenue", f"${sales_data['total_revenue'].sum():,.2f}")
        with col2:
            st.metric("Total Orders", f"{sales_data['total_orders'].sum():,}")
        with col3:
            st.metric("Active Customers", f"{len(customer_data):,}")
        with col4:
            st.metric("Avg Order Value", f"${sales_data['avg_order_value'].mean():.2f}")
        
        fig = px.line(sales_data, x='order_month', y='total_revenue', 
                      title='Monthly Revenue Trend')
        st.plotly_chart(fig, use_container_width=True)
        
    elif page == "Sales Analysis":
        st.header("Sales Analysis")
        st.write("This page will contain detailed sales analysis charts and tables.")
        fig = px.bar(sales_data, x='order_month', y='total_orders', title='Monthly Orders')
        st.plotly_chart(fig, use_container_width=True)
    
    elif page == "Product Performance":
        st.header("Product Performance")
        # st.write("This page will show insights on product performance.")
        top_products = product_data.sort_values('total_revenue', ascending=False).head(10)
        fig = px.bar(top_products, x='ProductName', y='total_revenue', title='Top 10 Products by revenue')
        st.plotly_chart(fig, use_container_width=True)
    
    elif page == "Customer Analysis":
        st.header("Customer Analysis")
        # st.write("This page will provide analysis on customers.")
        if 'value_segment' in customer_data.columns:
            segment_counts = customer_data['value_segment'].value_counts()
            fig = px.pie(values=segment_counts.values, names=segment_counts.index, title='Customer Value Segments')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("Customer value segment data not available.")



if __name__ == "__main__":
    main()
