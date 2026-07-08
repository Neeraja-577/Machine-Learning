import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration

st.set_page_config(
page_title="AI Sales Performance Dashboard",
page_icon="📊",
layout="wide"
)

st.title("📊 AI Sales Performance Dashboard")

# Upload File

uploaded_file = st.file_uploader(
"Upload Sales Dataset",
type=["csv", "xlsx"]
)

if uploaded_file is not None:

    try:
        # Read File
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file, encoding="latin-1")
        else:
            df = pd.read_excel(uploaded_file)

    # Convert Date
        df["Order Date"] = pd.to_datetime(
            df["Order Date"],
            errors="coerce"
        )

        st.success("Dataset Loaded Successfully")

    # ==========================
    # Sidebar Filters
    # ==========================

        st.sidebar.header("Filters")

        region_filter = st.sidebar.multiselect(
            "Select Region",
            df["Region"].unique(),
            default=df["Region"].unique()
        )

        category_filter = st.sidebar.multiselect(
            "Select Category",
            df["Category"].unique(),
            default=df["Category"].unique()
        )


        filtered_df = df[
            (df["Region"].isin(region_filter)) &
            (df["Category"].isin(category_filter)) 
       ]

    # ==========================
    # KPI Cards
    # ==========================

        total_sales = filtered_df["Sales"].sum()
        total_profit = filtered_df["Profit"].sum()
        total_orders = len(filtered_df)
        total_quantity = filtered_df["Quantity"].sum()

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "💰 Total Sales",
            f"${total_sales:,.0f}"
        )

        col2.metric(
            "📈 Total Profit",
            f"${total_profit:,.0f}"
        )

        col3.metric(
            "📦 Orders",
            total_orders
       )

        col4.metric(
            "🛒 Quantity",
            int(total_quantity)
        )

        st.markdown("---")

    # ==========================
    # Row 1 Charts
    # ==========================

        c1, c2 = st.columns(2)

        with c1:

            region_sales = filtered_df.groupby(
                "Region"
            )["Sales"].sum().reset_index()
 
            fig1 = px.bar(
                region_sales,
                x="Region",
                y="Sales",
                color="Region",
                title="Sales by Region"
           )

            st.plotly_chart(
                fig1,
                use_container_width=True
          )

        with c2:

            category_sales = filtered_df.groupby(
                "Category"
            )["Sales"].sum().reset_index()

            fig2 = px.pie(
                category_sales,
                names="Category",
                values="Sales",
                title="Sales by Category"
           )

            st.plotly_chart(
                fig2,
                use_container_width=True
            )

    # ==========================
    # Monthly Sales Trend
    # ==========================

        filtered_df["Month"] = (
            filtered_df["Order Date"].dt.month
        )

        monthly_sales = filtered_df.groupby(
            "Month"
        )["Sales"].sum().reset_index()

        fig3 = px.line(
            monthly_sales,
            x="Month",
            y="Sales",
            markers=True,
            title="Monthly Sales Trend"
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

    # ==========================
    # Yearly Sales Trend
    # ==========================

        filtered_df["Year"] = (
            filtered_df["Order Date"].dt.year
        )

        yearly_sales = filtered_df.groupby(
            "Year"
        )["Sales"].sum().reset_index()

        fig4 = px.bar(
            yearly_sales,
            x="Year",
            y="Sales",
            title="Yearly Sales Trend"
        )

        st.plotly_chart(
            fig4,
            use_container_width=True
        )

    # ==========================
    # Top 10 Products
    # ==========================

        st.subheader("🏆 Top 10 Products")

        top_products = (
            filtered_df.groupby(
                "Product Name"
            )["Sales"]
            .sum()
            .sort_values(
                ascending=False
            )
            .head(10)
            .reset_index()
        )

        fig5 = px.bar(
            top_products,
            x="Product Name",
            y="Sales",
            title="Top 10 Products"
        )

        st.plotly_chart(
            fig5,
            use_container_width=True
        )

    # ==========================
    # Dataset Preview
    # ==========================

        st.subheader("📋 Dataset Preview")

        st.dataframe(
            filtered_df.head(20)
        )

    except Exception as e:
        st.error(f"Error Loading File: {e}")

else:
    st.info("Please upload a CSV or Excel file.")