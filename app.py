import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Sales Forecasting Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

/* ---------------- MAIN APP ---------------- */

[data-testid="stAppViewContainer"]{
    background-color:#0F172A;
}

/* ---------------- SIDEBAR ---------------- */

[data-testid="stSidebar"]{
    background-color:#1E293B;
}

[data-testid="stSidebar"] *{
    color:white !important;
}
          

/* ---------------- HEADINGS ---------------- */

h1,h2,h3,h4{
    color:white;
}

p{
    color:#E5E7EB;
}

/* ---------------- BUTTON ---------------- */

.stButton>button{
    background:#2563EB;
    color:white;
    border-radius:8px;
    border:none;
}

/* ---------------- SELECTBOX ---------------- */

label{
    color:white !important;
    font-size:16px;
    font-weight:600;
}

div[data-baseweb="select"]{
    background:white !important;
    border-radius:10px !important;
}

div[data-baseweb="select"] *{
    color:black !important;
}

/* ---------------- TABLE ---------------- */

[data-testid="stDataFrame"]{
    background:white;
    border-radius:10px;
}

/* ---------------- HORIZONTAL LINE ---------------- */

hr{
    border:1px solid #334155;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# LOAD DATA
# ==========================================================

df = pd.read_csv("train.csv")

forecast_df = pd.read_csv("forecast_results_new.csv")

df["Order Date"] = pd.to_datetime(df["Order Date"])

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.image(
    "https://img.icons8.com/color/96/combo-chart.png",
    width=90
)

st.sidebar.title("📊 Sales Forecasting Dashboard")


st.sidebar.markdown("""
Explore different dashboard sections:

- 📊 Sales Overview
- 🔮 Forecast Explorer
- 🚨 Anomaly Report
- 📦 Demand Segments
""")

page = st.sidebar.radio(
    "Navigation",
    [
        "Sales Overview",
        "Forecast Explorer",
        "Anomaly Report",
        "Demand Segments"
    ]
)


# ==========================================================
# PAGE 1
# ==========================================================

if page == "Sales Overview":
    sns.set_style("whitegrid")

    # ==========================================================
    # PAGE TITLE
    # ==========================================================

    st.markdown(
        "<h1 style='color:white;'>📊 Sales Overview Dashboard</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='color:#CBD5E1;font-size:18px;'>"
        "Interactive Sales Analytics Dashboard"
        "</p>",
        unsafe_allow_html=True
    )

    st.markdown("""
    <hr style="
    height:2px;
    border:none;
    background:#334155;
    margin-top:20px;
    margin-bottom:20px;">
    """, unsafe_allow_html=True)

    st.write("""
Analyze historical sales performance across years, regions, categories,
and monthly trends using interactive visualizations.

Use interactive filters to explore the dataset, compare sales performance,
identify patterns, and gain actionable business insights.
""")

    st.markdown("""
    <hr style="
    height:2px;
    border:none;
    background:#334155;
    margin-top:20px;
    margin-bottom:20px;">
    """, unsafe_allow_html=True)

    # ==========================================================
    # TOTAL SALES BY YEAR & MONTHLY SALES TREND
    # ==========================================================

    col1, col2 = st.columns(2, gap="large")

    # ----------------------------------------------------------
    # TOTAL SALES BY YEAR
    # ----------------------------------------------------------

    with col1:

        st.markdown("""
        <h2 style="
        color:white;
        font-size:30px;
        font-weight:700;
        margin-bottom:15px;">
        📅 Total Sales by Year
        </h2>
        """, unsafe_allow_html=True)

        yearly_sales = (
            df.groupby("Year")["Sales"]
            .sum()
            .reset_index()
        )

        fig, ax = plt.subplots(
            figsize=(7, 5),
            constrained_layout=True
        )

        fig.patch.set_facecolor("white")
        ax.set_facecolor("#F8F9FA")

        bars = ax.bar(
            yearly_sales["Year"].astype(str),
            yearly_sales["Sales"],
            color="#4C72B0",
            edgecolor="black",
            linewidth=1
        )

        ax.set_title(
            "Year-wise Sales",
            fontsize=15,
            fontweight="bold",
            color="#003366"
        )

        ax.set_xlabel("Year")
        ax.set_ylabel("Sales")

        ax.grid(
            axis="y",
            linestyle="--",
            alpha=0.35
        )

        for bar in bars:

            height = bar.get_height()

            ax.text(
                bar.get_x() + bar.get_width()/2,
                height,
                f"{height:,.0f}",
                ha="center",
                va="bottom",
                fontsize=8
            )

        st.pyplot(fig, width="stretch")
        plt.close(fig)

    # ----------------------------------------------------------
    # MONTHLY SALES TREND
    # ----------------------------------------------------------

    with col2:

        st.markdown("""
        <h2 style="
        color:white;
        font-size:30px;
        font-weight:700;
        margin-bottom:15px;">
        📈 Monthly Sales Trend
        </h2>
        """, unsafe_allow_html=True)

        monthly_sales = (
            df.groupby(
                pd.Grouper(
                    key="Order Date",
                    freq="ME"
                )
            )["Sales"]
            .sum()
            .reset_index()
        )

        fig, ax = plt.subplots(
            figsize=(7, 5),
            constrained_layout=True
        )

        fig.patch.set_facecolor("white")
        ax.set_facecolor("#F8F9FA")

        ax.plot(
            monthly_sales["Order Date"],
            monthly_sales["Sales"],
            color="#2E8B57",
            linewidth=3,
            marker="o",
            markersize=4
        )

        ax.fill_between(
            monthly_sales["Order Date"],
            monthly_sales["Sales"],
            color="#2E8B57",
            alpha=0.20
        )

        ax.set_title(
            "Monthly Sales Trend",
            fontsize=15,
            fontweight="bold",
            color="#003366"
        )

        ax.set_xlabel("Month")
        ax.set_ylabel("Sales")

        ax.tick_params(
            axis="x",
            rotation=45
        )

        ax.grid(
            linestyle="--",
            alpha=0.35
        )

        st.pyplot(fig, width="stretch")
        plt.close(fig)

    st.markdown("""
    <hr style="
    height:2px;
    border:none;
    background:#334155;
    margin-top:20px;
    margin-bottom:20px;">
    """, unsafe_allow_html=True)

        # ==========================================================
    # FILTERS
    # ==========================================================

    st.markdown("""
    <h2 style="
    color:white;
    font-size:30px;
    font-weight:700;
    margin-bottom:5px;">
    🎯 Sales by Region and Category
    </h2>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style="
    color:#CBD5E1;
    font-size:17px;
    margin-bottom:20px;">
    Filter the sales records by Region and Category to explore performance
    across different business segments.
    </p>
    """, unsafe_allow_html=True)

    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:
        region = st.selectbox(
            "🌍 Select Region",
            ["All"] + sorted(df["Region"].unique()),
            key="region_filter"
        )

    with filter_col2:
        category = st.selectbox(
            "📦 Select Category",
            ["All"] + sorted(df["Category"].unique()),
            key="category_filter"
        )

    # ----------------------------------------------------------
    # APPLY FILTERS
    # ----------------------------------------------------------

    filtered_df = df.copy()

    if region != "All":
        filtered_df = filtered_df[
            filtered_df["Region"] == region
        ]

    if category != "All":
        filtered_df = filtered_df[
            filtered_df["Category"] == category
        ]

    st.markdown("""
    <hr style="
    height:2px;
    border:none;
    background:#334155;
    margin-top:20px;
    margin-bottom:20px;">
    """, unsafe_allow_html=True)

    # ==========================================================
    # FILTERED SALES TABLE
    # ==========================================================

    st.markdown("""
    <h2 style="
    color:white;
    font-size:30px;
    font-weight:700;
    margin-bottom:5px;">
    📄 Filtered Sales Data
    </h2>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style="
    color:#CBD5E1;
    font-size:17px;
    margin-bottom:20px;">
    View the sales records based on the selected filters.
    </p>
    """, unsafe_allow_html=True)

    display_df = filtered_df[
        [
            "Order Date",
            "Region",
            "Category",
            "Sub-Category",
            "Sales"
        ]
    ].copy()

    display_df["Order Date"] = display_df["Order Date"].dt.strftime("%d-%m-%Y")

    display_df["Sales"] = display_df["Sales"].apply(
        lambda x: f"${x:,.2f}"
    )

    st.dataframe(
        display_df,
        width="stretch",
        height=420
    )

    st.markdown("""
    <hr style="
    height:2px;
    border:none;
    background:#334155;
    margin-top:20px;
    margin-bottom:20px;">
    """, unsafe_allow_html=True)

    # ==========================================================
    # SALES BY CATEGORY
    # ==========================================================

    st.markdown("""
    <h2 style="
    color:white;
    font-size:30px;
    font-weight:700;
    margin-bottom:5px;">
    📊 Sales by Category
    </h2>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style="
    color:#CBD5E1;
    font-size:17px;
    margin-bottom:20px;">
    Compare total sales across product categories after applying the filters.
    </p>
    """, unsafe_allow_html=True)

    category_sales = (
        filtered_df
        .groupby("Category")["Sales"]
        .sum()
        .reset_index()
    )

    fig, ax = plt.subplots(
        figsize=(8,5),
        constrained_layout=True
    )

    fig.patch.set_facecolor("white")
    ax.set_facecolor("#F8F9FA")

    colors = [
        "#4C72B0",
        "#55A868",
        "#C44E52",
        "#8172B2",
        "#CCB974"
    ]

    bars = ax.bar(
        category_sales["Category"],
        category_sales["Sales"],
        color=colors[:len(category_sales)],
        edgecolor="black",
        linewidth=1
    )

    ax.set_title(
        "Sales by Category",
        fontsize=15,
        fontweight="bold",
        color="#003366"
    )

    ax.set_xlabel("Category")
    ax.set_ylabel("Total Sales")

    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.35
    )

    for bar in bars:

        height = bar.get_height()

        ax.text(
            bar.get_x() + bar.get_width()/2,
            height,
            f"{height:,.0f}",
            ha="center",
            va="bottom",
            fontsize=9
        )

    st.pyplot(fig, width="stretch")
    plt.close(fig)

    st.markdown("""
    <hr style="
    height:2px;
    border:none;
    background:#334155;
    margin-top:20px;
    margin-bottom:20px;">
    """, unsafe_allow_html=True)


elif page == "Forecast Explorer":
        # ==========================================================
    # FORECAST EXPLORER
    # ==========================================================

    st.markdown(
        "<h1 style='color:white;'>🔮 Forecast Explorer</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='color:#CBD5E1;font-size:18px;'>"
        "Interactive Sales Forecasting Dashboard"
        "</p>",
        unsafe_allow_html=True
    )

    st.markdown("""
    <hr style="
    height:2px;
    border:none;
    background:#334155;
    margin-top:20px;
    margin-bottom:20px;">
    """, unsafe_allow_html=True)

    st.write("""
Explore future sales forecasts using the best-performing **XGBoost** model.

Choose a Region or Category, select the forecasting horizon, and visualize
future sales predictions along with model performance metrics.
""")

    st.markdown("""
    <hr style="
    height:2px;
    border:none;
    background:#334155;
    margin-top:20px;
    margin-bottom:20px;">
    """, unsafe_allow_html=True)

    # ==========================================================
    # FORECAST SETTINGS
    # ==========================================================

    st.markdown("""
    <h2 style="
    color:white;
    font-size:30px;
    font-weight:700;
    margin-bottom:5px;">
    📌 Forecast Settings
    </h2>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style="
    color:#CBD5E1;
    font-size:17px;
    margin-bottom:20px;">
    Configure the forecasting options before generating predictions.
    </p>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:

        forecast_by = st.selectbox(
            "Forecast By",
            ["Category", "Region"]
        )

        if forecast_by == "Category":

            selected_value = st.selectbox(
                "Select Category",
                sorted(df["Category"].unique())
            )

        else:

            selected_value = st.selectbox(
                "Select Region",
                ["East", "West"]
            )

    with col2:

        horizon = st.slider(
            "Forecast Horizon (Months)",
            min_value=1,
            max_value=3,
            value=1
        )

    st.markdown("""
    <hr style="
    height:2px;
    border:none;
    background:#334155;
    margin-top:20px;
    margin-bottom:20px;">
    """, unsafe_allow_html=True)


    # ==========================================================
    # FORECAST OUTPUT
    # ==========================================================

    months = ["Month 1", "Month 2", "Month 3"][:horizon]

    if forecast_by == "Category":
        
        row = forecast_df[
            (forecast_df["Type"] == "Category") &
            (forecast_df["Segment"] == selected_value)
        ].iloc[0]

    else:
        
        row = forecast_df[
            (forecast_df["Type"] == "Region") &
            (forecast_df["Segment"] == selected_value)
        ].iloc[0]

    forecast_plot = [
    row["Month1"],
    row["Month2"],
    row["Month3"]
    ][:horizon]

    st.markdown("""
    <h2 style="
    color:white;
    font-size:30px;
    font-weight:700;
    margin-bottom:5px;">
    📈 Forecast Output
    </h2>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style="
    color:#CBD5E1;
    font-size:17px;
    margin-bottom:20px;">
    Visualize the predicted sales for the next three months using the
    best-performing XGBoost forecasting model.
    </p>
    """, unsafe_allow_html=True)

    fig, ax = plt.subplots(
        figsize=(10,5),
        constrained_layout=True
    )

    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#F8F9FA")

    ax.plot(
        months,
        forecast_plot,
        color="#2563EB",
        linewidth=3,
        marker="o",
        markersize=8
    )

    ax.fill_between(
        months,
        forecast_plot,
        color="#2563EB",
        alpha=0.20
    )

    ax.set_title(
        "XGBoost Sales Forecast",
        fontsize=15,
        fontweight="bold",
        color="#003366"
    )

    ax.set_xlabel("Forecast Horizon")
    ax.set_ylabel("Predicted Sales")

    ax.grid(
        linestyle="--",
        alpha=0.35
    )

    for i, value in enumerate(forecast_plot):
        
        ax.text(
            i,
            value + 1200,
            f"{value:,.0f}",
            ha="center",
            fontsize=9
        )

    st.pyplot(fig, width="stretch")

    # =====================================================
    # MODEL PERFORMANCE
    # =====================================================

    st.markdown("""
    <h2 style="
    color:white;
    font-size:30px;
    font-weight:700;
    margin-bottom:5px;">
    📊 Model Performance (XGBoost)
    </h2>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style="
    color:#CBD5E1;
    font-size:17px;
    margin-bottom:20px;">
    Visualize the performance metrics of the best-performing XGBoost forecasting model.
    </p>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.metric("MAE", "14,763.81")

    with col2:
        st.metric("RMSE", "18,337.41")


    selected_prediction = forecast_plot[horizon - 1]

    st.success(
        f"✅ Predicted Sales for the next {horizon} month(s): "
        f"${selected_prediction:,.2f}"
    )

    st.markdown("""
    <hr style="
    height:2px;
    border:none;
    background:#334155;
    margin-top:25px;
    margin-bottom:25px;">
    """, unsafe_allow_html=True)

# ==========================================================
# PAGE 3 — ANOMALY REPORT
# ==========================================================

elif page == "Anomaly Report":

    st.markdown("""
    <h1 style="
    color:white;
    font-size:42px;
    font-weight:700;">
    🚨 Anomaly Report
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style="
    color:#CBD5E1;
    font-size:19px;">
    Explore unusual sales spikes and drops detected using anomaly detection techniques.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("""
    <hr style="
    height:2px;
    border:none;
    background:#334155;
    margin-top:20px;
    margin-bottom:25px;">
    """, unsafe_allow_html=True)

    # =====================================================
    # WEEKLY SALES
    # =====================================================

    weekly_sales = (
        df.groupby(pd.Grouper(key="Order Date", freq="W"))["Sales"]
        .sum()
        .reset_index()
    )

    # =====================================================
    # ISOLATION FOREST
    # =====================================================

    from sklearn.ensemble import IsolationForest

    iso_model = IsolationForest(
        contamination=0.05,
        random_state=42
    )

    weekly_sales["Anomaly"] = iso_model.fit_predict(
        weekly_sales[["Sales"]]
    )

    anomalies = weekly_sales[
        weekly_sales["Anomaly"] == -1
    ]

    # =====================================================
    # Z-SCORE
    # =====================================================

    weekly_sales["Rolling_Mean"] = (
        weekly_sales["Sales"].rolling(8).mean()
    )


    weekly_sales["Rolling_STD"] = (
        weekly_sales["Sales"].rolling(8).std()
    )

    weekly_sales["Z_Score"] = (
        (weekly_sales["Sales"] - weekly_sales["Rolling_Mean"])
        /
        weekly_sales["Rolling_STD"]
    )

    weekly_sales["Z_Anomaly"] = (
        weekly_sales["Z_Score"].abs() > 2
    )

    z_anomalies = weekly_sales[
        weekly_sales["Z_Anomaly"]
    ]

    # =====================================================
    # CHARTS
    # =====================================================

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
        <h3 style="
        color:white;
        font-size:28px;
        font-weight:700;">
        🔴 Isolation Forest
        </h3>
        """, unsafe_allow_html=True)

        fig, ax = plt.subplots(figsize=(7,5))

        fig.patch.set_facecolor("#FFFFFF")
        ax.set_facecolor("#F8F9FA")

        ax.plot(
            weekly_sales["Order Date"],
            weekly_sales["Sales"],
            color="#2563EB",
            linewidth=2,
            label="Weekly Sales"
        )

        ax.scatter(
            anomalies["Order Date"],
            anomalies["Sales"],
            color="red",
            s=70,
            label="Anomaly"
        )

        ax.set_title(
            "Isolation Forest Anomalies",
            fontsize=14,
            fontweight="bold"
        )

        ax.grid(True, linestyle="--", alpha=0.3)

        ax.legend()

        st.pyplot(fig, width="stretch")

    with col2:
        st.markdown("""
        <h3 style="
        color:white;
        font-size:28px;
        font-weight:700;">
        🟢 Z-Score Detection
        </h3>
        """, unsafe_allow_html=True)

        fig, ax = plt.subplots(figsize=(7,5))

        fig.patch.set_facecolor("#FFFFFF")
        ax.set_facecolor("#F8F9FA")

        ax.plot(
            weekly_sales["Order Date"],
            weekly_sales["Sales"],
            color="#2563EB",
            linewidth=2,
            label="Weekly Sales"
        )

        ax.scatter(
            z_anomalies["Order Date"],
            z_anomalies["Sales"],
            color="green",
            s=70,
            label="Anomaly"
        )

        ax.set_title(
            "Z-Score Anomalies",
            fontsize=14,
            fontweight="bold"
        )

        ax.grid(True, linestyle="--", alpha=0.3)

        ax.legend()

        st.pyplot(fig, width="stretch")

    st.markdown("""
    <hr style="
    height:2px;
    border:none;
    background:#334155;
    margin-top:25px;
    margin-bottom:25px;">
    """, unsafe_allow_html=True)

    st.markdown("""
    <h2 style="
    color:white;
    font-size:30px;
    font-weight:700;">
    📄 Detected Anomalies
    </h2>
    """, unsafe_allow_html=True)
        
    tab1, tab2 = st.tabs([
    "Isolation Forest",
    "Z-Score"
    ])

    with tab1:
        
        iso_table = anomalies[
            ["Order Date", "Sales"]
        ].copy()

        iso_table["Sales"] = iso_table["Sales"].map(
            "${:,.2f}".format
        )

        st.dataframe(
            iso_table,
            width="stretch",
            height=300
        )

    with tab2:
        
        z_table = z_anomalies[
            ["Order Date", "Sales"]
        ].copy()

        z_table["Sales"] = z_table["Sales"].map(
            "${:,.2f}".format
        )

        st.dataframe(
            z_table,
            width="stretch",
            height=300
        )

elif page == "Demand Segments":
    
    st.markdown("""
    <h1 style="
    color:white;
    font-size:42px;
    font-weight:700;">
    📦 Product Demand Segments
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style="
    color:#CBD5E1;
    font-size:18px;">
    Analyze product demand segments using K-Means clustering based on
    Sales, Growth Rate, Volatility and Average Order Value.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("""
    <hr style="
    height:2px;
    border:none;
    background:#334155;
    margin-top:20px;
    margin-bottom:25px;">
    """, unsafe_allow_html=True)

    # ----------------------------------------------------
    # Feature Engineering
    # ----------------------------------------------------

    cluster_data = df.copy()

    cluster_data["Order Date"] = pd.to_datetime(cluster_data["Order Date"])
    cluster_data["Year"] = cluster_data["Order Date"].dt.year

    total_sales = (
        cluster_data.groupby("Sub-Category")["Sales"]
        .sum()
    )

    yearly_sales = (
        cluster_data.groupby(
            ["Sub-Category","Year"]
        )["Sales"]
        .sum()
        .reset_index()
    )

    growth = yearly_sales.pivot(
        index="Sub-Category",
        columns="Year",
        values="Sales"
    )

    growth_rate = (
        (growth[2018]-growth[2017])
        / growth[2017]
    ) * 100

    monthly_sales = (
        cluster_data.groupby(
            [
                "Sub-Category",
                pd.Grouper(
                    key="Order Date",
                    freq="ME"
                )
            ]
        )["Sales"]
    .sum()
    .reset_index()
    )

    volatility = (
        monthly_sales.groupby("Sub-Category")["Sales"]
        .std()
    )

    average_order = (
        cluster_data.groupby("Sub-Category")["Sales"]
        .mean()
    )

    cluster_df = pd.DataFrame({
        "Total Sales": total_sales,
        "Growth Rate": growth_rate,
        "Volatility": volatility,
        "Average Order Value": average_order
    })

    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans
    from sklearn.decomposition import PCA

    scaler = StandardScaler()

    scaled = scaler.fit_transform(cluster_df)

    kmeans = KMeans(
        n_clusters=4,
        random_state=42,
        n_init=10
    )

    cluster_df["Cluster"] = kmeans.fit_predict(scaled)

    cluster_names = {
        0: "High Value, High Volatility",
        1: "Low Volume, Stable Demand",
        2: "Growing Demand",
        3: "High Volume, Stable Demand"
    }

    cluster_df["Demand Segment"] = (
        cluster_df["Cluster"]
        .map(cluster_names)
    )

    # =====================================================
    # PCA CLUSTER VISUALIZATION
    # =====================================================

    pca = PCA(n_components=2)

    pca_features = pca.fit_transform(scaled)

    pca_df = pd.DataFrame({
        "PCA1": pca_features[:, 0],
        "PCA2": pca_features[:, 1],
        "Cluster": cluster_df["Cluster"],
        "Sub-Category": cluster_df.index
    })

    st.markdown("""
    <h2 style="
    color:white;
    font-size:30px;
    font-weight:700;">
    📊 Product Demand Cluster Visualization
    </h2>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style="
    color:#CBD5E1;
    font-size:17px;">
    Each point represents a product sub-category grouped according to
    its sales behavior using K-Means clustering.
    </p>
    """, unsafe_allow_html=True)

    fig, ax = plt.subplots(figsize=(10, 6))

    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#F8F9FA")

    scatter = ax.scatter(
        pca_df["PCA1"],
        pca_df["PCA2"],
        c=pca_df["Cluster"],
        cmap="viridis",
        s=180,
        edgecolor="black",
        linewidth=0.8
    )

    # Show sub-category names beside each point
    for i in range(len(pca_df)):
        ax.text(
            pca_df.iloc[i]["PCA1"] + 0.05,
            pca_df.iloc[i]["PCA2"] + 0.05,
            pca_df.iloc[i]["Sub-Category"],
            fontsize=8
        )

    ax.set_title(
        "K-Means Product Demand Segmentation",
        fontsize=16,
        fontweight="bold",
        color="#003366"
    )

    ax.set_xlabel("Principal Component 1")
    ax.set_ylabel("Principal Component 2")

    ax.grid(
        linestyle="--",
        alpha=0.35
    )


    plt.colorbar(
        scatter,
        label="Cluster"
    )

    st.pyplot(fig, width="stretch")

    st.markdown("""
    <hr style="
    height:2px;
    border:none;
    background:#334155;
    margin-top:25px;
    margin-bottom:25px;">
    """, unsafe_allow_html=True)

    # =====================================================
    # DEMAND SEGMENT TABLE
    # =====================================================

    st.markdown("""
    <h2 style="
    color:white;
    font-size:30px;
    font-weight:700;">
    📄 Product Demand Segments
    </h2>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style="
    color:#CBD5E1;
    font-size:17px;">
    The table below shows the demand segment assigned to each product
    sub-category based on K-Means clustering.
    </p>
    """, unsafe_allow_html=True)

    display_cluster = (
        cluster_df
        .reset_index()
        .rename(columns={"index": "Sub-Category"})
    )

    display_cluster = display_cluster[
        [
            "Sub-Category",
            "Demand Segment",
            "Cluster",
            "Total Sales",
            "Growth Rate",
            "Average Order Value"
        ]
    ]

    display_cluster["Total Sales"] = (
        display_cluster["Total Sales"]
        .map("${:,.2f}".format)
    )

    display_cluster["Growth Rate"] = (
        display_cluster["Growth Rate"]
        .map("{:.2f}%".format)
    )

    display_cluster["Average Order Value"] = (
        display_cluster["Average Order Value"]
        .map("${:,.2f}".format)
    )

    st.dataframe(
        display_cluster,
        width="stretch",
        height=520
    )

    st.markdown("""
    <hr style="
    height:2px;
    border:none;
    background:#334155;
    margin-top:25px;
    margin-bottom:25px;">
    """, unsafe_allow_html=True)

    # =====================================================
    # SUMMARY METRICS
    # =====================================================

    st.markdown("""
    <h2 style="
    color:white;
    font-size:30px;
    font-weight:700;">
    📌 Cluster Summary
    </h2>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Products",
        len(display_cluster)
    )

    c2.metric(
        "Clusters",
        display_cluster["Cluster"].nunique()
    )

    c3.metric(
        "Highest Sales",
        display_cluster["Total Sales"].iloc[
            display_cluster["Total Sales"].str.replace("$","",regex=False)
            .str.replace(",","")
            .astype(float)
            .idxmax()
        ]
    )


    c4.metric(
        "Growing Segments",
        len(
            display_cluster[
                display_cluster["Demand Segment"] == "Growing Demand"
            ]
        )
    )
