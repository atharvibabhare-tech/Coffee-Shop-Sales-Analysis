import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Brew & Co. — Sales Dashboard",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  GLOBAL STYLES  (warm espresso palette)
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Palette tokens ── */
:root {
    --espresso:  #1C0A00;
    --roast:     #3B1F0A;
    --caramel:   #C68642;
    --cream:     #FAF3E8;
    --latte:     #E8D5B7;
    --mist:      #F4EDE0;
    --accent:    #D4501A;
    --text:      #2D1B0E;
    --muted:     #7A5C3E;
}

/* ── Base canvas ── */
html, body, [data-testid="stAppViewContainer"] {
    background: var(--cream) !important;
    font-family: 'DM Sans', sans-serif;
    color: var(--text);
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--roast) !important;
    border-right: none !important;
}
[data-testid="stSidebar"] * {
    color: var(--latte) !important;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: var(--caramel) !important;
    font-family: 'Playfair Display', serif !important;
    letter-spacing: .03em;
}
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: var(--espresso) !important;
    border: 1px solid var(--caramel) !important;
    border-radius: 8px !important;
    color: var(--latte) !important;
}

/* ── Main top padding ── */
[data-testid="stMain"] > div:first-child {
    padding-top: 1.5rem;
}

/* ── Hero header ── */
.hero {
    background: linear-gradient(135deg, var(--espresso) 0%, var(--roast) 60%, #5C2D0A 100%);
    border-radius: 20px;
    padding: 2.8rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '☕';
    position: absolute;
    right: 2.5rem;
    top: 50%;
    transform: translateY(-50%);
    font-size: 7rem;
    opacity: .08;
}
.hero h1 {
    font-family: 'Playfair Display', serif;
    font-size: 2.8rem;
    font-weight: 900;
    color: var(--caramel) !important;
    margin: 0 0 .4rem;
    letter-spacing: -.01em;
    line-height: 1.15;
}
.hero p {
    font-family: 'DM Sans', sans-serif;
    font-size: 1rem;
    color: var(--latte) !important;
    margin: 0;
    font-weight: 300;
    letter-spacing: .04em;
}

/* ── KPI cards ── */
.kpi-card {
    background: white;
    border-radius: 16px;
    padding: 1.5rem 1.8rem;
    border-left: 5px solid var(--caramel);
    box-shadow: 0 4px 20px rgba(60,30,10,.08);
    height: 100%;
}
.kpi-card .label {
    font-size: .78rem;
    font-weight: 500;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: .5rem;
}
.kpi-card .value {
    font-family: 'Playfair Display', serif;
    font-size: 2.2rem;
    font-weight: 700;
    color: var(--espresso);
    line-height: 1;
}
.kpi-card .delta {
    font-size: .82rem;
    color: #27A060;
    margin-top: .4rem;
    font-weight: 500;
}
.kpi-card.accent { border-left-color: var(--accent); }
.kpi-card.dark   { border-left-color: var(--espresso); }

/* ── Section titles ── */
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--espresso);
    margin: 1.8rem 0 1rem;
    border-bottom: 2px solid var(--latte);
    padding-bottom: .5rem;
}

/* ── Tabs ── */
[data-testid="stTabs"] [role="tablist"] {
    gap: .5rem;
    border-bottom: 2px solid var(--latte);
}
[data-testid="stTabs"] [role="tab"] {
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    font-size: .9rem;
    letter-spacing: .03em;
    border-radius: 8px 8px 0 0 !important;
    color: var(--muted) !important;
    padding: .55rem 1.2rem !important;
    transition: all .2s;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    background: var(--roast) !important;
    color: var(--caramel) !important;
    border-bottom: 2px solid var(--roast) !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid var(--latte);
}

/* ── Metric overrides (native) ── */
[data-testid="metric-container"] {
    background: white;
    border-radius: 14px;
    padding: 1rem 1.4rem;
    border: 1px solid var(--latte);
    box-shadow: 0 2px 12px rgba(60,30,10,.05);
}
[data-testid="metric-container"] label {
    font-size: .78rem !important;
    letter-spacing: .1em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
    font-weight: 500 !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: 'Playfair Display', serif !important;
    font-size: 2rem !important;
    color: var(--espresso) !important;
}

/* ── Divider ── */
hr {
    border-color: var(--latte) !important;
    margin: 1.5rem 0 !important;
}

/* ── Footer ── */
.footer {
    text-align: center;
    color: var(--muted);
    font-size: .8rem;
    padding: 2rem 0 1rem;
    letter-spacing: .05em;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  MATPLOTLIB THEME
# ─────────────────────────────────────────────
ESPRESSO  = "#1C0A00"
CARAMEL   = "#C68642"
ACCENT    = "#D4501A"
LATTE     = "#E8D5B7"
MUTED     = "#7A5C3E"
CREAM     = "#FAF3E8"

PALETTE = [CARAMEL, ACCENT, "#6B3A2A", "#A0522D", "#8B6914",
           "#D2691E", "#CD853F", "#DEB887", "#F4A460", "#BC8F5F"]

plt.rcParams.update({
    "figure.facecolor":  CREAM,
    "axes.facecolor":    CREAM,
    "axes.edgecolor":    LATTE,
    "axes.labelcolor":   ESPRESSO,
    "axes.titlecolor":   ESPRESSO,
    "xtick.color":       MUTED,
    "ytick.color":       MUTED,
    "grid.color":        LATTE,
    "grid.linestyle":    "--",
    "grid.alpha":        0.6,
    "text.color":        ESPRESSO,
    "font.family":       "sans-serif",
    "axes.spines.top":   False,
    "axes.spines.right": False,
})

# ─────────────────────────────────────────────
#  LOAD & PREP DATA
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("CoffeeShopSales-cleaned.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0 1.5rem;'>
        <div style='font-size:3rem;'>☕</div>
        <div style='font-family:"Playfair Display",serif; font-size:1.3rem;
                    color:#C68642; font-weight:700; letter-spacing:.02em;'>Brew & Co.</div>
        <div style='font-size:.75rem; color:#C0A070; letter-spacing:.1em; margin-top:.2rem;'>
            SALES DASHBOARD
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Filters")

    product_list = ["All"] + sorted(df["product_category"].dropna().unique().tolist())
    selected_product = st.selectbox("☕ Product Category", product_list)

    store_list = ["All"] + sorted(df["store_location"].dropna().unique().tolist())
    selected_store = st.selectbox("📍 Store Location", store_list)

    st.markdown("---")
    st.markdown(
        "<div style='font-size:.75rem; color:#907060; text-align:center; line-height:1.6;'>"
        "Data refreshes daily.<br>Showing all available records."
        "</div>",
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────
#  FILTER
# ─────────────────────────────────────────────
filtered_df = df.copy()
if selected_product != "All":
    filtered_df = filtered_df[filtered_df["product_category"] == selected_product]
if selected_store != "All":
    filtered_df = filtered_df[filtered_df["store_location"] == selected_store]

# ─────────────────────────────────────────────
#  HERO
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>Brew & Co. Sales Dashboard</h1>
    <p>Interactive analysis of coffee shop sales, revenue, and customer trends</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  KPIs
# ─────────────────────────────────────────────
total_sales   = int(filtered_df["transaction_qty"].sum())
total_revenue = filtered_df["transaction_amt"].sum()
total_orders  = filtered_df["transaction_id"].nunique()
avg_order_val = total_revenue / total_orders if total_orders else 0

k1, k2, k3, k4 = st.columns(4)

def kpi(col, icon, label, value, extra_class=""):
    col.markdown(f"""
    <div class="kpi-card {extra_class}">
        <div class="label">{icon} {label}</div>
        <div class="value">{value}</div>
    </div>
    """, unsafe_allow_html=True)

kpi(k1, "🛒", "Total Orders",    f"{total_orders:,}")
kpi(k2, "💰", "Total Revenue",   f"₹{total_revenue:,.0f}", "accent")
kpi(k3, "☕", "Products Sold",   f"{total_sales:,}", "dark")
kpi(k4, "📊", "Avg. Order Value", f"₹{avg_order_val:,.2f}")

st.markdown("<div style='margin-top:2rem;'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📈  Sales Analysis", "🏆  Top Products", "📄  Raw Data"])

# ════════════════════════════════════════════
#  TAB 1 — SALES ANALYSIS
# ════════════════════════════════════════════
with tab1:
    col_a, col_b = st.columns([3, 2], gap="large")

    # ── Monthly Revenue Trend ──
    with col_a:
        st.markdown('<div class="section-title">Monthly Revenue Trend</div>', unsafe_allow_html=True)

        monthly = (
            filtered_df
            .groupby(filtered_df["date"].dt.to_period("M"))["transaction_amt"]
            .sum()
            .reset_index()
        )
        monthly["date"] = monthly["date"].dt.to_timestamp()
        monthly = monthly.sort_values("date")

        fig, ax = plt.subplots(figsize=(8, 3.6))
        ax.fill_between(monthly["date"], monthly["transaction_amt"],
                        alpha=0.18, color=CARAMEL)
        ax.plot(monthly["date"], monthly["transaction_amt"],
                color=CARAMEL, linewidth=2.5, marker="o",
                markersize=5, markerfacecolor=ACCENT, markeredgecolor=ACCENT)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"₹{x/1000:.0f}K"))
        ax.set_xlabel("")
        ax.set_ylabel("Revenue", fontsize=9, color=MUTED)
        ax.tick_params(axis="x", rotation=30, labelsize=8)
        ax.tick_params(axis="y", labelsize=8)
        ax.grid(axis="y")
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    # ── Revenue by Store ──
    with col_b:
        st.markdown('<div class="section-title">Revenue by Store</div>', unsafe_allow_html=True)

        store_rev = (
            filtered_df
            .groupby("store_location")["transaction_amt"]
            .sum()
            .sort_values(ascending=True)
        )

        fig, ax = plt.subplots(figsize=(4.5, 3.6))
        bars = ax.barh(store_rev.index, store_rev.values,
                       color=PALETTE[:len(store_rev)], height=0.55, edgecolor="none")
        for bar in bars:
            w = bar.get_width()
            ax.text(w * 1.01, bar.get_y() + bar.get_height() / 2,
                    f"₹{w/1000:.1f}K", va="center", fontsize=8, color=ESPRESSO)
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"₹{x/1000:.0f}K"))
        ax.tick_params(labelsize=8)
        ax.set_xlim(0, store_rev.max() * 1.18)
        ax.grid(axis="x")
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    # ── Revenue by Product Category ──
    st.markdown('<div class="section-title">Revenue by Product Category</div>', unsafe_allow_html=True)

    cat_sales = (
        filtered_df
        .groupby("product_category")["transaction_amt"]
        .sum()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(10, 3.8))
    bars = ax.bar(cat_sales.index, cat_sales.values,
                  color=PALETTE[:len(cat_sales)], width=0.6, edgecolor="none",
                  linewidth=0)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + cat_sales.max() * .012,
                f"₹{h/1000:.1f}K", ha="center", va="bottom", fontsize=8.5, color=ESPRESSO)
    ax.set_ylim(0, cat_sales.max() * 1.18)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"₹{x/1000:.0f}K"))
    ax.tick_params(axis="x", rotation=25, labelsize=9)
    ax.tick_params(axis="y", labelsize=8)
    ax.grid(axis="y")
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

# ════════════════════════════════════════════
#  TAB 2 — TOP PRODUCTS
# ════════════════════════════════════════════
with tab2:
    col_c, col_d = st.columns([3, 2], gap="large")

    # ── Top 10 bar ──
    with col_c:
        st.markdown('<div class="section-title">Top 10 Best-Selling Products</div>', unsafe_allow_html=True)

        top_products = (
            filtered_df
            .groupby("product_type")["transaction_qty"]
            .sum()
            .sort_values(ascending=True)
            .tail(10)
        )

        colors = [CARAMEL if i == len(top_products) - 1 else PALETTE[2]
                  for i in range(len(top_products))]

        fig, ax = plt.subplots(figsize=(7.5, 4.5))
        bars = ax.barh(top_products.index, top_products.values,
                       color=colors, height=0.6, edgecolor="none")
        for bar in bars:
            w = bar.get_width()
            ax.text(w + top_products.max() * .01, bar.get_y() + bar.get_height() / 2,
                    f"{int(w):,}", va="center", fontsize=8.5, color=ESPRESSO)
        ax.set_xlim(0, top_products.max() * 1.15)
        ax.tick_params(labelsize=9)
        ax.grid(axis="x")
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    # ── Category share donut ──
    with col_d:
        st.markdown('<div class="section-title">Category Share</div>', unsafe_allow_html=True)

        cat_qty = (
            filtered_df
            .groupby("product_category")["transaction_qty"]
            .sum()
            .sort_values(ascending=False)
        )

        fig, ax = plt.subplots(figsize=(4, 4.5))
        wedges, texts, autotexts = ax.pie(
            cat_qty.values,
            labels=cat_qty.index,
            autopct="%1.0f%%",
            startangle=90,
            colors=PALETTE[:len(cat_qty)],
            wedgeprops=dict(width=0.55, edgecolor=CREAM, linewidth=2),
            pctdistance=0.78,
        )
        for t in texts:
            t.set_fontsize(8)
            t.set_color(ESPRESSO)
        for at in autotexts:
            at.set_fontsize(7.5)
            at.set_color("white")
            at.set_fontweight("bold")
        ax.set_aspect("equal")
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    # ── Table ──
    st.markdown('<div class="section-title">Top 10 Products Table</div>', unsafe_allow_html=True)
    top_table = (
        filtered_df
        .groupby("product_type")["transaction_qty"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
        .rename(columns={"product_type": "Product", "transaction_qty": "Units Sold"})
    )
    top_table.index = top_table.index + 1
    top_table["Units Sold"] = top_table["Units Sold"].map("{:,}".format)
    st.dataframe(
        top_table,
        use_container_width=True,
        column_config={
            "Product":    st.column_config.TextColumn("☕ Product"),
            "Units Sold": st.column_config.TextColumn("🛒 Units Sold"),
        }
    )

# ════════════════════════════════════════════
#  TAB 3 — RAW DATA
# ════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-title">Transaction Records</div>', unsafe_allow_html=True)

    search = st.text_input("🔍 Search product or location", placeholder="e.g. Latte, Astoria …")
    display_df = filtered_df.copy()
    if search:
        mask = display_df.apply(
            lambda col: col.astype(str).str.contains(search, case=False, na=False)
        ).any(axis=1)
        display_df = display_df[mask]

    st.caption(f"Showing {len(display_df):,} records")
    st.dataframe(display_df, use_container_width=True, height=420)

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown('<hr>', unsafe_allow_html=True)
st.markdown(
    '<div class="footer">Brew & Co. Sales Dashboard &nbsp;·&nbsp; '
    'Built with ❤️ using Streamlit &nbsp;·&nbsp; ☕</div>',
    unsafe_allow_html=True,
)
