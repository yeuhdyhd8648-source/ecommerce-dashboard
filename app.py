# -*- coding: utf-8 -*-
"""
Executive E-Commerce Dashboard & Strategic Intelligence Report
================================================================
لوحة تحكم تنفيذية لتحليل أداء التجارة الإلكترونية على مستوى كبار المستشارين.

المصدر: Ecommerce_Master_Summary.csv
تشغيل:  streamlit run app.py
"""

import io
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# =====================================================================================
# 1) إعداد الصفحة العام (PAGE CONFIG)
# =====================================================================================
st.set_page_config(
    page_title="Executive E-Commerce Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

DEFAULT_FILE = Path(__file__).parent / "Ecommerce_Master_Summary.csv"
CURRENCY = "$"

# أسماء الأعمدة الحقيقية في ملف المصدر (لا يحتوي الملف على صف رأس - Header)
RAW_COLUMNS = [
    "Category",
    "Total_Customers",
    "Total_Revenue",
    "Reported_AOV",
    "Churned_Customers",
    "Churn_Rate_Pct_Source",
    "Reserved_Metric_1",
    "Reserved_Metric_2",
    "Reserved_Metric_3",
]

PALETTE = {
    "navy": "#0B1F3A",
    "navy_light": "#132C4F",
    "ivory": "#F6F4EF",
    "gold": "#C6A15B",
    "gold_dark": "#9C7C3E",
    "slate": "#5B6B79",
    "red": "#B33A3A",
    "amber": "#C68A2E",
    "green": "#1E8A6E",
    "line": "#E3DFD3",
}

CATEGORY_COLOR_SEQUENCE = ["#0B1F3A", "#C6A15B", "#1E8A6E", "#B33A3A", "#5B6B79", "#7D5BA6", "#2E7DA6"]

# =====================================================================================
# 2) التنسيق المخصص (CUSTOM CSS) — هوية بصرية استشارية داكنة/ذهبية
# =====================================================================================
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}

    .block-container {{
        padding-top: 1.6rem;
        padding-bottom: 3rem;
        max-width: 1360px;
    }}

    /* ------- عنوان الصفحة الرئيسي ------- */
    .exec-header {{
        background: linear-gradient(120deg, {PALETTE['navy']} 0%, {PALETTE['navy_light']} 100%);
        border-radius: 6px;
        padding: 34px 40px;
        margin-bottom: 22px;
        border: 1px solid {PALETTE['gold_dark']};
        direction: rtl;
        text-align: right;
    }}
    .exec-header .eyebrow {{
        color: {PALETTE['gold']};
        font-family: 'JetBrains Mono', monospace;
        font-size: 12.5px;
        letter-spacing: 1px;
        margin-bottom: 10px;
    }}
    .exec-header h1 {{
        font-family: 'Sora', sans-serif;
        color: {PALETTE['ivory']};
        font-size: 30px;
        font-weight: 700;
        margin: 0 0 8px 0;
        line-height: 1.35;
    }}
    .exec-header p {{
        color: #C9D2DC;
        font-size: 14.5px;
        margin: 0;
        max-width: 760px;
        margin-right: 0;
        margin-left: auto;
    }}

    /* ------- كروت KPI ------- */
    .kpi-card {{
        background: #FFFFFF;
        border: 1px solid {PALETTE['line']};
        border-right: 4px solid {PALETTE['navy']};
        border-radius: 4px;
        padding: 16px 18px;
        height: 128px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        direction: rtl;
        text-align: right;
    }}
    .kpi-card.risk {{ border-right-color: {PALETTE['red']}; }}
    .kpi-card.good {{ border-right-color: {PALETTE['green']}; }}
    .kpi-card.gold {{ border-right-color: {PALETTE['gold_dark']}; }}
    .kpi-label {{
        font-size: 12.5px;
        color: {PALETTE['slate']};
        font-weight: 600;
        letter-spacing: 0.2px;
    }}
    .kpi-value {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 25px;
        font-weight: 700;
        color: {PALETTE['navy']};
        margin: 2px 0;
    }}
    .kpi-sub {{
        font-size: 12px;
        font-weight: 600;
    }}
    .kpi-sub.up {{ color: {PALETTE['green']}; }}
    .kpi-sub.down {{ color: {PALETTE['red']}; }}
    .kpi-sub.flat {{ color: {PALETTE['slate']}; }}

    /* ------- عناوين الأقسام ------- */
    .section-title {{
        font-family: 'Sora', sans-serif;
        font-size: 19px;
        font-weight: 700;
        color: {PALETTE['navy']};
        border-right: 4px solid {PALETTE['gold']};
        padding-right: 10px;
        margin: 26px 0 12px 0;
        direction: rtl;
        text-align: right;
    }}
    .section-caption {{
        direction: rtl; text-align: right; color: {PALETTE['slate']};
        font-size: 13px; margin-top: -8px; margin-bottom: 14px;
    }}

    .rtl-block {{ direction: rtl; text-align: right; }}

    .insight-card {{
        background: {PALETTE['ivory']};
        border: 1px solid {PALETTE['line']};
        border-radius: 4px;
        padding: 16px 18px;
        margin-bottom: 10px;
        direction: rtl;
        text-align: right;
    }}
    .insight-card h4 {{
        font-family: 'Sora', sans-serif;
        margin: 0 0 6px 0;
        color: {PALETTE['navy']};
        font-size: 15.5px;
    }}
    .insight-card p {{
        margin: 0;
        font-size: 13.5px;
        color: #333;
        line-height: 1.7;
    }}
    .tag {{
        display: inline-block;
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        padding: 2px 8px;
        border-radius: 3px;
        margin-left: 6px;
        color: white;
    }}
    .tag-high {{ background: {PALETTE['red']}; }}
    .tag-med {{ background: {PALETTE['amber']}; }}
    .tag-low {{ background: {PALETTE['green']}; }}

    .stTabs [data-baseweb="tab-list"] {{ gap: 6px; }}
    .stTabs [data-baseweb="tab"] {{
        background-color: {PALETTE['ivory']};
        border-radius: 4px 4px 0 0;
        padding: 10px 16px;
        font-weight: 600;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: {PALETTE['navy']} !important;
        color: white !important;
    }}

    footer {{visibility: hidden;}}
    #MainMenu {{visibility: hidden;}}
    </style>
    """,
    unsafe_allow_html=True,
)


# =====================================================================================
# 3) طبقة تحميل وتنظيف البيانات (DATA LOADING & CLEANING LAYER)
# =====================================================================================
@st.cache_data(show_spinner=False)
def load_and_clean_data(file_bytes: bytes):
    """يقرأ الملف الخام، ينظفه، ويحسب كافة المؤشرات المالية المشتقة بدقة."""
    processing_log = []

    bom_detected = file_bytes[:3] == b"\xef\xbb\xbf"
    processing_log.append(
        f"{'تم رصد' if bom_detected else 'لم يتم رصد'} بادئة UTF-8 BOM في بداية الملف — "
        f"{'تمت إزالتها تلقائيًا عبر ترميز utf-8-sig.' if bom_detected else 'الترميز نظيف.'}"
    )

    raw_df = pd.read_csv(io.BytesIO(file_bytes), header=None, encoding="utf-8-sig", engine="python")
    processing_log.append(f"تمت قراءة {raw_df.shape[0]} صفًا و {raw_df.shape[1]} عمودًا من الملف الخام.")

    if raw_df.shape[1] == len(RAW_COLUMNS):
        raw_df.columns = RAW_COLUMNS
        processing_log.append("تم التحقق من مطابقة عدد الأعمدة (9) وتم إسناد أسماء الحقول القياسية.")
    else:
        raw_df.columns = [f"Field_{i+1}" for i in range(raw_df.shape[1])]
        processing_log.append("⚠️ عدد الأعمدة غير مطابق للبنية المتوقعة — تم استخدام أسماء عامة كإجراء احترازي.")

    nulls_before = raw_df.isnull().sum()
    duplicate_rows = int(raw_df.duplicated().sum())

    df = raw_df.copy()
    df["Category"] = df["Category"].astype(str).str.strip()

    numeric_cols = [c for c in df.columns if c != "Category"]
    for c in numeric_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    coerced_nulls = int(df[numeric_cols].isnull().sum().sum())
    if coerced_nulls > 0:
        processing_log.append(f"⚠️ تم اكتشاف {coerced_nulls} قيمة غير رقمية تم تحويلها إلى NaN أثناء التنظيف.")
        df[numeric_cols] = df[numeric_cols].fillna(0)
        processing_log.append("تم تعويض القيم المفقودة بالصفر لضمان استقرار الحسابات (سياسة تحفّظية).")
    else:
        processing_log.append("لا توجد قيم مفقودة (Null) في الأعمدة الرقمية بعد التحويل.")

    # ---- المعادلات المالية والتحليلية الدقيقة ----
    safe_customers = df["Total_Customers"].replace(0, np.nan)
    df["Active_Customers"] = df["Total_Customers"] - df["Churned_Customers"]
    df["Precise_AOV"] = df["Total_Revenue"] / safe_customers
    df["Precise_Churn_Rate_Pct"] = (df["Churned_Customers"] / safe_customers) * 100
    df["Retention_Rate_Pct"] = 100 - df["Precise_Churn_Rate_Pct"]
    safe_churn = (df["Precise_Churn_Rate_Pct"] / 100).replace(0, np.nan)
    df["Estimated_CLV"] = df["Precise_AOV"] / safe_churn
    df[["Precise_AOV", "Precise_Churn_Rate_Pct", "Retention_Rate_Pct", "Estimated_CLV"]] = df[
        ["Precise_AOV", "Precise_Churn_Rate_Pct", "Retention_Rate_Pct", "Estimated_CLV"]
    ].fillna(0)

    total_rev = df["Total_Revenue"].sum()
    total_cust = df["Total_Customers"].sum()
    df["Revenue_Share_Pct"] = (df["Total_Revenue"] / total_rev * 100) if total_rev else 0
    df["Customer_Share_Pct"] = (df["Total_Customers"] / total_cust * 100) if total_cust else 0

    rank_pct = df["Precise_Churn_Rate_Pct"].rank(pct=True, method="average")
    df["Risk_Tier"] = np.select(
        [rank_pct >= 0.66, rank_pct >= 0.33],
        ["مرتفعة الخطورة", "متوسطة الخطورة"],
        default="منخفضة الخطورة",
    )
    processing_log.append("تم احتساب Precise_AOV و Precise_Churn_Rate_Pct و Retention Rate و CLV التقديرية بدقة كاملة.")
    processing_log.append("تم تصنيف كل فئة إلى شريحة مخاطر (مرتفعة / متوسطة / منخفضة) بالاعتماد على الترتيب النسبي لمعدل المغادرة.")

    # ---- كشف القيم الشاذة (Outliers) بطريقة IQR ----
    outlier_cols = ["Total_Revenue", "Total_Customers", "Precise_Churn_Rate_Pct", "Precise_AOV"]
    outlier_report = {}
    for c in outlier_cols:
        q1, q3 = df[c].quantile(0.25), df[c].quantile(0.75)
        iqr = q3 - q1
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        flags = (df[c] < lower) | (df[c] > upper)
        outlier_report[c] = {"count": int(flags.sum()), "categories": df.loc[flags, "Category"].tolist()}
    processing_log.append("تم تنفيذ فحص القيم الشاذة (IQR Method) على الحقول المالية والتشغيلية الأساسية.")

    quality_report = {
        "bom_detected": bom_detected,
        "rows_processed": int(len(df)),
        "columns_processed": int(df.shape[1]),
        "duplicate_rows": duplicate_rows,
        "nulls_before": nulls_before.to_dict(),
        "coerced_nulls": coerced_nulls,
        "outliers": outlier_report,
        "encoding_used": "utf-8-sig",
    }

    return df, processing_log, quality_report


def fmt_money(x: float) -> str:
    return f"{CURRENCY}{x:,.0f}"


def fmt_num(x: float) -> str:
    return f"{x:,.0f}"


def fmt_pct(x: float) -> str:
    return f"{x:,.2f}%"


def kpi_card(label: str, value: str, sub_text: str, tone: str = "") -> str:
    tone_class = {"risk": "risk", "good": "good", "gold": "gold"}.get(tone, "")
    sub_tone = {"risk": "down", "good": "up", "gold": "flat"}.get(tone, "flat")
    return f"""
    <div class="kpi-card {tone_class}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-sub {sub_tone}">{sub_text}</div>
    </div>
    """


# =====================================================================================
# 4) الشريط الجانبي — تحميل الملف والفلاتر
# =====================================================================================
with st.sidebar:
    st.markdown(
        f"""<div style="direction:rtl;text-align:right;">
        <div style="font-family:'Sora',sans-serif;font-weight:700;font-size:18px;color:{PALETTE['navy']};">
        📊 مركز التحكم التنفيذي</div>
        <div style="font-size:12.5px;color:{PALETTE['slate']};margin-top:2px;">
        Strategic Intelligence Console</div></div>""",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    uploaded_file = st.file_uploader("رفع ملف بيانات بديل (CSV)", type=["csv"])

    if uploaded_file is not None:
        file_bytes = uploaded_file.getvalue()
        source_label = uploaded_file.name
    elif DEFAULT_FILE.exists():
        file_bytes = DEFAULT_FILE.read_bytes()
        source_label = DEFAULT_FILE.name
    else:
        file_bytes = None
        source_label = None

if file_bytes is None:
    st.error("⚠️ لم يتم العثور على ملف البيانات. الرجاء رفع ملف Ecommerce_Master_Summary.csv من الشريط الجانبي.")
    st.stop()

try:
    df, processing_log, quality = load_and_clean_data(file_bytes)
except Exception as exc:  # حماية شاملة ضد أي عطل في القراءة
    st.error(f"❌ تعذّرت معالجة الملف المرفوع. تفاصيل الخطأ: {exc}")
    st.stop()

with st.sidebar:
    st.caption(f"📁 مصدر البيانات الحالي: **{source_label}**")
    st.markdown("#### 🔎 فلاتر العرض")
    all_categories = df["Category"].tolist()
    selected_categories = st.multiselect("اختر الفئات", options=all_categories, default=all_categories)

    max_churn = float(df["Precise_Churn_Rate_Pct"].max()) if len(df) else 0.0
    churn_ceiling = st.slider(
        "استبعاد الفئات ذات معدل مغادرة أعلى من (%)",
        min_value=0.0,
        max_value=max(round(max_churn, 1) + 1, 1.0),
        value=max(round(max_churn, 1) + 1, 1.0),
        step=0.5,
    )
    st.markdown("---")
    st.caption(f"🕓 آخر تحديث للتقرير: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

if not selected_categories:
    st.warning("الرجاء اختيار فئة واحدة على الأقل من الشريط الجانبي لعرض التقرير.")
    st.stop()

view = df[df["Category"].isin(selected_categories) & (df["Precise_Churn_Rate_Pct"] <= churn_ceiling)].copy()
if view.empty:
    st.warning("لا توجد بيانات مطابقة للفلاتر المختارة حاليًا.")
    st.stop()

view = view.sort_values("Total_Revenue", ascending=False).reset_index(drop=True)

# =====================================================================================
# 5) الترويسة التنفيذية
# =====================================================================================
st.markdown(
    f"""
    <div class="exec-header">
        <div class="eyebrow">EXECUTIVE INTELLIGENCE REPORT · E-COMMERCE DIVISION</div>
        <h1>لوحة التحكم التنفيذية لأداء التجارة الإلكترونية والتقرير الاستراتيجي</h1>
        <p>تحليل شامل لأداء الإيرادات، سلوك العملاء، ومخاطر المغادرة عبر {len(view)} من {len(df)} فئة تشغيلية،
        مُعدّ لدعم قرارات مجلس الإدارة وفرق النمو والاحتفاظ بالعملاء.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# =====================================================================================
# 6) قسم فحص وتشخيص جودة البيانات
# =====================================================================================
with st.expander("🔍 فحص وتشخيص جودة البيانات التلقائي (Automated Data Quality & Error Audit)", expanded=False):
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("عدد الصفوف المعالجة", quality["rows_processed"])
    c2.metric("عدد الأعمدة", quality["columns_processed"])
    c3.metric("الصفوف المكررة", quality["duplicate_rows"])
    c4.metric("قيم غير رقمية مُحوَّلة", quality["coerced_nulls"])

    qa_col1, qa_col2 = st.columns(2)
    with qa_col1:
        st.markdown('<div class="rtl-block"><b>📋 فحص القيم المفقودة (قبل التنظيف)</b></div>', unsafe_allow_html=True)
        nulls_df = pd.DataFrame(
            {"العمود": list(quality["nulls_before"].keys()), "قيم مفقودة": list(quality["nulls_before"].values())}
        )
        st.dataframe(nulls_df, hide_index=True, use_container_width=True)

    with qa_col2:
        st.markdown('<div class="rtl-block"><b>📈 كشف القيم الشاذة (IQR Method)</b></div>', unsafe_allow_html=True)
        out_rows = []
        for col, info in quality["outliers"].items():
            out_rows.append(
                {
                    "المؤشر": col,
                    "عدد الشواذ": info["count"],
                    "الفئات المتأثرة": ", ".join(info["categories"]) if info["categories"] else "—",
                }
            )
        st.dataframe(pd.DataFrame(out_rows), hide_index=True, use_container_width=True)

    st.markdown(
        '<div class="rtl-block"><b>🧹 تقرير تنظيف الترميز (Encoding & BOM)</b></div>', unsafe_allow_html=True
    )
    bom_msg = "تم اكتشاف وإزالة بادئة UTF-8 BOM من بداية الملف." if quality["bom_detected"] else "لم يتم رصد أي بادئة BOM؛ الملف نظيف من هذه الناحية."
    st.info(f"الترميز المستخدم للقراءة: `{quality['encoding_used']}` — {bom_msg}")

    st.markdown('<div class="rtl-block"><b>🛠️ سجل خطوات المعالجة البرمجية</b></div>', unsafe_allow_html=True)
    for i, step in enumerate(processing_log, start=1):
        st.markdown(f"<div class='rtl-block'>{i}. {step}</div>", unsafe_allow_html=True)

# =====================================================================================
# 7) شريط مؤشرات الأداء التنفيذية (KPI GRID)
# =====================================================================================
st.markdown('<div class="section-title">⚡ مؤشرات الأداء التنفيذية الرئيسية</div>', unsafe_allow_html=True)

total_revenue = view["Total_Revenue"].sum()
total_customers = view["Total_Customers"].sum()
total_churned = view["Churned_Customers"].sum()
overall_churn = (total_churned / total_customers * 100) if total_customers else 0
overall_aov = (total_revenue / total_customers) if total_customers else 0
overall_retention = 100 - overall_churn
overall_clv = (overall_aov / (overall_churn / 100)) if overall_churn else 0

top_revenue_cat = view.loc[view["Total_Revenue"].idxmax(), "Category"]
top_risk_cat = view.loc[view["Precise_Churn_Rate_Pct"].idxmax(), "Category"]
best_retention_cat = view.loc[view["Retention_Rate_Pct"].idxmax(), "Category"]

k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.markdown(kpi_card("إجمالي الإيرادات", fmt_money(total_revenue), f"🏆 الأعلى: {top_revenue_cat}", "gold"), unsafe_allow_html=True)
with k2:
    st.markdown(kpi_card("إجمالي قاعدة العملاء", fmt_num(total_customers), f"نشطون: {fmt_num(total_customers - total_churned)}", "good"), unsafe_allow_html=True)
with k3:
    st.markdown(kpi_card("إجمالي العملاء المغادرين", fmt_num(total_churned), f"⚠️ الأعلى خطورة: {top_risk_cat}", "risk"), unsafe_allow_html=True)
with k4:
    st.markdown(kpi_card("معدل المغادرة العام (Churn)", fmt_pct(overall_churn), "نسبة من إجمالي قاعدة العملاء", "risk"), unsafe_allow_html=True)
with k5:
    st.markdown(kpi_card("متوسط قيمة الطلب (AOV)", fmt_money(overall_aov), "الإيراد ÷ عدد العملاء", "gold"), unsafe_allow_html=True)

st.write("")
k6, k7, k8 = st.columns(3)
with k6:
    st.markdown(kpi_card("معدل الاحتفاظ بالعملاء (Retention)", fmt_pct(overall_retention), f"✅ الأفضل: {best_retention_cat}", "good"), unsafe_allow_html=True)
with k7:
    st.markdown(kpi_card("القيمة التقديرية لعمر العميل (CLV)", fmt_money(overall_clv), "AOV ÷ معدل المغادرة (تقدير مبسّط)", "gold"), unsafe_allow_html=True)
with k8:
    healthiest = view.loc[view["Estimated_CLV"].idxmax(), "Category"]
    st.markdown(kpi_card("عدد الفئات التشغيلية المعروضة", f"{len(view)}", f"⭐ أعلى قيمة عميل: {healthiest}", "gold"), unsafe_allow_html=True)

st.caption("⚠️ ملاحظة منهجية: القيمة الدالة على عمر العميل (CLV) هنا تقدير مبسّط (AOV ÷ معدل المغادرة) لغياب بيانات هامش الربح وتكرار الشراء الفعلي، وتُستخدم لأغراض التخطيط الاسترشادي فقط وليست تقييمًا ماليًا نهائيًا.")

# =====================================================================================
# 8) الرسوم البيانية التفاعلية المتقدمة
# =====================================================================================
st.markdown('<div class="section-title">📊 التحليل البصري التفاعلي</div>', unsafe_allow_html=True)

PLOTLY_LAYOUT = dict(
    font=dict(family="Inter, sans-serif", color=PALETTE["navy"], size=13),
    paper_bgcolor="white",
    plot_bgcolor="white",
    margin=dict(l=10, r=10, t=50, b=10),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)

row1_c1, row1_c2 = st.columns(2)

with row1_c1:
    fig_rev = px.bar(
        view.sort_values("Total_Revenue"),
        x="Total_Revenue",
        y="Category",
        orientation="h",
        text="Total_Revenue",
        color="Category",
        color_discrete_sequence=CATEGORY_COLOR_SEQUENCE,
        title="مقارنة الإيرادات الإجمالية حسب الفئة",
    )
    fig_rev.update_traces(texttemplate="%{text:,.0f}", textposition="outside", cliponaxis=False)
    fig_rev.update_layout(**PLOTLY_LAYOUT, showlegend=False, xaxis_title="الإيرادات", yaxis_title="")
    st.plotly_chart(fig_rev, use_container_width=True)

with row1_c2:
    stacked = view.melt(
        id_vars="Category",
        value_vars=["Active_Customers", "Churned_Customers"],
        var_name="الحالة",
        value_name="عدد العملاء",
    )
    stacked["الحالة"] = stacked["الحالة"].map({"Active_Customers": "نشطون", "Churned_Customers": "مغادرون"})
    fig_cust = px.bar(
        stacked,
        x="Category",
        y="عدد العملاء",
        color="الحالة",
        barmode="stack",
        color_discrete_map={"نشطون": PALETTE["green"], "مغادرون": PALETTE["red"]},
        title="توزيع العملاء: النشطون مقابل المغادرون",
    )
    fig_cust.update_layout(**PLOTLY_LAYOUT, xaxis_title="", yaxis_title="عدد العملاء")
    st.plotly_chart(fig_cust, use_container_width=True)

row2_c1, row2_c2 = st.columns(2)

with row2_c1:
    risk_sorted = view.sort_values("Precise_Churn_Rate_Pct")
    fig_churn = px.bar(
        risk_sorted,
        x="Precise_Churn_Rate_Pct",
        y="Category",
        orientation="h",
        color="Precise_Churn_Rate_Pct",
        color_continuous_scale=["#1E8A6E", "#C68A2E", "#B33A3A"],
        text="Precise_Churn_Rate_Pct",
        title="تحليل مخاطر مغادرة العملاء حسب الفئة (Churn Risk)",
    )
    fig_churn.update_traces(texttemplate="%{text:.2f}%", textposition="outside", cliponaxis=False)
    fig_churn.update_layout(**PLOTLY_LAYOUT, xaxis_title="معدل المغادرة (%)", yaxis_title="", coloraxis_showscale=False)
    st.plotly_chart(fig_churn, use_container_width=True)

with row2_c2:
    fig_bubble = px.scatter(
        view,
        x="Precise_Churn_Rate_Pct",
        y="Precise_AOV",
        size="Total_Revenue",
        color="Category",
        color_discrete_sequence=CATEGORY_COLOR_SEQUENCE,
        hover_name="Category",
        size_max=55,
        title="العلاقة بين قيمة الطلب ومعدل المغادرة وحجم الإيراد",
    )
    fig_bubble.update_layout(**PLOTLY_LAYOUT, xaxis_title="معدل المغادرة (%)", yaxis_title="متوسط قيمة الطلب (AOV)")
    st.plotly_chart(fig_bubble, use_container_width=True)

row3_c1, row3_c2 = st.columns(2)
with row3_c1:
    fig_donut_rev = px.pie(
        view, names="Category", values="Total_Revenue", hole=0.55,
        color="Category", color_discrete_sequence=CATEGORY_COLOR_SEQUENCE,
        title="حصة كل فئة من إجمالي الإيرادات",
    )
    fig_donut_rev.update_traces(textinfo="percent+label")
    fig_donut_rev.update_layout(**PLOTLY_LAYOUT)
    st.plotly_chart(fig_donut_rev, use_container_width=True)

with row3_c2:
    fig_clv = px.bar(
        view.sort_values("Estimated_CLV"),
        x="Estimated_CLV", y="Category", orientation="h",
        color="Category", color_discrete_sequence=CATEGORY_COLOR_SEQUENCE,
        text="Estimated_CLV",
        title="القيمة التقديرية لعمر العميل (Estimated CLV) حسب الفئة",
    )
    fig_clv.update_traces(texttemplate="%{text:,.0f}", textposition="outside", cliponaxis=False)
    fig_clv.update_layout(**PLOTLY_LAYOUT, showlegend=False, xaxis_title="CLV التقديرية", yaxis_title="")
    st.plotly_chart(fig_clv, use_container_width=True)

# =====================================================================================
# 9) التبويبات الاستراتيجية التنفيذية
# =====================================================================================
st.markdown('<div class="section-title">🧭 التقرير الاستراتيجي العميق</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "🏆 الأداء المالي والربحية",
        "⚠️ تشخيص أزمة المغادرة",
        "💡 التوصيات وإعادة الاستهداف",
        "📈 توقعات النمو المستقبلي",
    ]
)

# --- التبويب 1: الأداء المالي ---
with tab1:
    best_cat = view.loc[view["Total_Revenue"].idxmax()]
    worst_cat = view.loc[view["Total_Revenue"].idxmin()]
    aov_leader = view.loc[view["Precise_AOV"].idxmax()]

    m1, m2, m3 = st.columns(3)
    m1.markdown(kpi_card("الفئة الأعلى إيرادًا", best_cat["Category"], fmt_money(best_cat["Total_Revenue"]), "gold"), unsafe_allow_html=True)
    m2.markdown(kpi_card("الفئة الأقل إيرادًا", worst_cat["Category"], fmt_money(worst_cat["Total_Revenue"]), "risk"), unsafe_allow_html=True)
    m3.markdown(kpi_card("الفئة الأعلى بقيمة الطلب", aov_leader["Category"], fmt_money(aov_leader["Precise_AOV"]), "good"), unsafe_allow_html=True)

    st.write("")
    revenue_gap = (best_cat["Total_Revenue"] - worst_cat["Total_Revenue"]) / worst_cat["Total_Revenue"] * 100 if worst_cat["Total_Revenue"] else 0
    st.markdown(
        f"""
        <div class="insight-card">
            <h4>الفجوة التنافسية بين الفئات <span class="tag tag-med">تحليل</span></h4>
            <p>تتصدر فئة <b>{best_cat['Category']}</b> ترتيب الإيرادات بإجمالي {fmt_money(best_cat['Total_Revenue'])}،
            بفارق {revenue_gap:.1f}% عن الفئة الأقل أداءً <b>{worst_cat['Category']}</b>
            ({fmt_money(worst_cat['Total_Revenue'])}). هذا التقارب النسبي في الأداء المالي بين الفئات
            يشير إلى توازن تشغيلي جيد، لكنه يفتح فرصة لإعادة توزيع الميزانية التسويقية نحو
            الفئات ذات قيمة الطلب الأعلى مثل <b>{aov_leader['Category']}</b> لتعظيم العائد على كل عميل جديد.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="rtl-block"><b>جدول الربحية التفصيلي</b></div>', unsafe_allow_html=True)
    profitability_table = view[["Category", "Total_Revenue", "Total_Customers", "Precise_AOV", "Revenue_Share_Pct"]].copy()
    profitability_table.columns = ["الفئة", "إجمالي الإيرادات", "عدد العملاء", "متوسط قيمة الطلب", "حصة الإيراد %"]
    st.dataframe(
        profitability_table.style.format(
            {"إجمالي الإيرادات": "{:,.0f}", "عدد العملاء": "{:,.0f}", "متوسط قيمة الطلب": "{:,.2f}", "حصة الإيراد %": "{:,.2f}%"}
        ),
        hide_index=True,
        use_container_width=True,
    )

# --- التبويب 2: تشخيص المغادرة ---
with tab2:
    risk_counts = view["Risk_Tier"].value_counts()
    r1, r2, r3 = st.columns(3)
    r1.markdown(kpi_card("فئات مرتفعة الخطورة", str(int(risk_counts.get("مرتفعة الخطورة", 0))), "تتطلب تدخلاً فوريًا", "risk"), unsafe_allow_html=True)
    r2.markdown(kpi_card("فئات متوسطة الخطورة", str(int(risk_counts.get("متوسطة الخطورة", 0))), "تحتاج متابعة دورية", "gold"), unsafe_allow_html=True)
    r3.markdown(kpi_card("فئات منخفضة الخطورة", str(int(risk_counts.get("منخفضة الخطورة", 0))), "أداء مستقر", "good"), unsafe_allow_html=True)

    st.write("")
    for _, row in view.sort_values("Precise_Churn_Rate_Pct", ascending=False).iterrows():
        tag_class = {"مرتفعة الخطورة": "tag-high", "متوسطة الخطورة": "tag-med", "منخفضة الخطورة": "tag-low"}[row["Risk_Tier"]]
        st.markdown(
            f"""
            <div class="insight-card">
                <h4>{row['Category']} <span class="tag {tag_class}">{row['Risk_Tier']}</span></h4>
                <p>معدل المغادرة الدقيق: <b>{row['Precise_Churn_Rate_Pct']:.2f}%</b> — أي ما يعادل
                {fmt_num(row['Churned_Customers'])} عميل مغادر من إجمالي {fmt_num(row['Total_Customers'])}.
                معدل الاحتفاظ الحالي: <b>{row['Retention_Rate_Pct']:.2f}%</b>. الأثر المالي التقديري
                للمغادرة على هذه الفئة يُقدَّر بـ {fmt_money(row['Churned_Customers'] * row['Precise_AOV'])}
                من الإيرادات المحتملة الضائعة سنويًا (بافتراض استمرار متوسط قيمة الطلب الحالي).</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    fig_risk_heat = px.imshow(
        view.set_index("Category")[["Precise_Churn_Rate_Pct", "Retention_Rate_Pct"]].T,
        text_auto=".1f",
        color_continuous_scale=["#1E8A6E", "#C68A2E", "#B33A3A"],
        aspect="auto",
        title="خريطة حرارية لمعدلات المغادرة والاحتفاظ عبر الفئات",
    )
    fig_risk_heat.update_layout(**PLOTLY_LAYOUT, coloraxis_showscale=True)
    st.plotly_chart(fig_risk_heat, use_container_width=True)

# --- التبويب 3: التوصيات الاستراتيجية ---
with tab3:
    st.markdown('<div class="rtl-block">استراتيجيات استهداف عكسي (Retargeting) مخصصة لكل شريحة مخاطر:</div>', unsafe_allow_html=True)
    st.write("")
    recs = {
        "مرتفعة الخطورة": (
            "🔴",
            "تفعيل حملات استرجاع فورية (Win-back) خلال 48 ساعة من علامات عدم النشاط، مع عروض خصم مخصصة "
            "تعادل 15–20% من متوسط قيمة الطلب، إلى جانب مسح استقصائي سريع لأسباب المغادرة.",
        ),
        "متوسطة الخطورة": (
            "🟡",
            "برنامج ولاء تدريجي (نقاط/مكافآت) وتذكيرات بريدية مخصصة بناءً على سلوك الشراء السابق، "
            "مع تحسين تجربة ما بعد البيع لمنع الانزلاق نحو الفئة المرتفعة الخطورة.",
        ),
        "منخفضة الخطورة": (
            "🟢",
            "التركيز على البيع المتقاطع (Cross-sell) والبيع الإضافي (Upsell) لرفع متوسط قيمة الطلب، "
            "مع الاستفادة من هذه الشريحة كنموذج مرجعي لتوسيع الحصة السوقية.",
        ),
    }
    for tier, (icon, text) in recs.items():
        cats_in_tier = view.loc[view["Risk_Tier"] == tier, "Category"].tolist()
        if not cats_in_tier:
            continue
        tag_class = {"مرتفعة الخطورة": "tag-high", "متوسطة الخطورة": "tag-med", "منخفضة الخطورة": "tag-low"}[tier]
        st.markdown(
            f"""
            <div class="insight-card">
                <h4>{icon} {tier} <span class="tag {tag_class}">{', '.join(cats_in_tier)}</span></h4>
                <p>{text}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    st.markdown('<div class="section-caption">أولوية الاستثمار التسويقي المقترحة (وفق الأثر المالي المتوقع لكل فئة)</div>', unsafe_allow_html=True)
    impact = view.copy()
    impact["الأثر المالي المحتمل"] = impact["Churned_Customers"] * impact["Precise_AOV"]
    fig_priority = px.bar(
        impact.sort_values("الأثر المالي المحتمل"),
        x="الأثر المالي المحتمل", y="Category", orientation="h",
        color="Risk_Tier",
        color_discrete_map={"مرتفعة الخطورة": PALETTE["red"], "متوسطة الخطورة": PALETTE["amber"], "منخفضة الخطورة": PALETTE["green"]},
        title="ترتيب أولوية الاستهداف العكسي حسب الإيراد المهدد",
    )
    fig_priority.update_layout(**PLOTLY_LAYOUT, xaxis_title="الإيراد المهدد", yaxis_title="")
    st.plotly_chart(fig_priority, use_container_width=True)

# --- التبويب 4: توقعات النمو ---
with tab4:
    st.markdown('<div class="rtl-block">محاكاة تفاعلية لأثر خفض معدل المغادرة على الإيرادات المستقبلية:</div>', unsafe_allow_html=True)

    sim_c1, sim_c2 = st.columns(2)
    with sim_c1:
        churn_reduction = st.slider("نسبة خفض معدل المغادرة المستهدفة (نقطة مئوية)", 0.0, min(15.0, overall_churn), 3.0, 0.5)
    with sim_c2:
        growth_assumption = st.slider("افتراض نمو قاعدة العملاء الجديدة سنويًا (%)", 0.0, 20.0, 5.0, 0.5)

    years = np.arange(0, 6)
    base_customers = total_customers
    base_churn = overall_churn / 100
    new_churn = max(base_churn - churn_reduction / 100, 0.001)
    g = growth_assumption / 100

    projected_customers_base, projected_customers_improved = [base_customers], [base_customers]
    for _ in years[1:]:
        prev_b = projected_customers_base[-1]
        prev_i = projected_customers_improved[-1]
        projected_customers_base.append(prev_b * (1 + g) * (1 - base_churn))
        projected_customers_improved.append(prev_i * (1 + g) * (1 - new_churn))

    projected_revenue_base = np.array(projected_customers_base) * overall_aov
    projected_revenue_improved = np.array(projected_customers_improved) * overall_aov

    forecast_df = pd.DataFrame(
        {
            "السنة": [f"سنة {y}" for y in years],
            "السيناريو الحالي": projected_revenue_base,
            "سيناريو خفض المغادرة": projected_revenue_improved,
        }
    ).melt(id_vars="السنة", var_name="السيناريو", value_name="الإيراد المتوقع")

    fig_forecast = px.line(
        forecast_df, x="السنة", y="الإيراد المتوقع", color="السيناريو",
        markers=True,
        color_discrete_map={"السيناريو الحالي": PALETTE["slate"], "سيناريو خفض المغادرة": PALETTE["green"]},
        title="توقعات نمو الإيرادات على مدى 5 سنوات (نموذج ما‑الذي‑لو What-If)",
    )
    fig_forecast.update_layout(**PLOTLY_LAYOUT, xaxis_title="", yaxis_title="الإيراد المتوقع")
    st.plotly_chart(fig_forecast, use_container_width=True)

    incremental_value = projected_revenue_improved[-1] - projected_revenue_base[-1]
    st.markdown(
        f"""
        <div class="insight-card">
            <h4>الأثر التراكمي للسيناريو التحسيني <span class="tag tag-low">توقع</span></h4>
            <p>في حال نجاح خفض معدل المغادرة بمقدار {churn_reduction:.1f} نقطة مئوية والحفاظ على نمو سنوي
            بنسبة {growth_assumption:.1f}% في قاعدة العملاء، فإن الإيراد المتوقع بنهاية السنة الخامسة
            يرتفع إلى {fmt_money(projected_revenue_improved[-1])} مقابل {fmt_money(projected_revenue_base[-1])}
            في السيناريو الحالي — بفارق تراكمي إيجابي قدره {fmt_money(incremental_value)}.
            هذا النموذج تقديري مبسّط لأغراض التخطيط الاستراتيجي ولا يُغني عن نموذج مالي تفصيلي كامل.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# =====================================================================================
# 10) الجدول الرئيسي النظيف مع خيارات البحث والتصدير
# =====================================================================================
st.markdown('<div class="section-title">🗂️ الجدول الرئيسي للبيانات المعالجة</div>', unsafe_allow_html=True)

search_col, sort_col = st.columns([3, 1])
with search_col:
    search_term = st.text_input("🔎 بحث سريع باسم الفئة", "")
with sort_col:
    sort_field = st.selectbox("ترتيب حسب", ["Total_Revenue", "Precise_Churn_Rate_Pct", "Precise_AOV", "Estimated_CLV"])

display_df = view.copy()
if search_term.strip():
    display_df = display_df[display_df["Category"].str.contains(search_term.strip(), case=False, na=False)]
display_df = display_df.sort_values(sort_field, ascending=False)

final_cols = [
    "Category", "Total_Customers", "Active_Customers", "Churned_Customers",
    "Total_Revenue", "Precise_AOV", "Precise_Churn_Rate_Pct", "Retention_Rate_Pct",
    "Estimated_CLV", "Revenue_Share_Pct", "Customer_Share_Pct", "Risk_Tier",
]
display_labels = [
    "الفئة", "إجمالي العملاء", "عملاء نشطون", "عملاء مغادرون",
    "إجمالي الإيرادات", "متوسط قيمة الطلب", "معدل المغادرة %", "معدل الاحتفاظ %",
    "CLV التقديرية", "حصة الإيراد %", "حصة العملاء %", "شريحة المخاطر",
]
clean_table = display_df[final_cols].copy()
clean_table.columns = display_labels

st.dataframe(
    clean_table.style.format(
        {
            "إجمالي العملاء": "{:,.0f}", "عملاء نشطون": "{:,.0f}", "عملاء مغادرون": "{:,.0f}",
            "إجمالي الإيرادات": "{:,.0f}", "متوسط قيمة الطلب": "{:,.2f}",
            "معدل المغادرة %": "{:,.2f}%", "معدل الاحتفاظ %": "{:,.2f}%",
            "CLV التقديرية": "{:,.2f}", "حصة الإيراد %": "{:,.2f}%", "حصة العملاء %": "{:,.2f}%",
        }
    ),
    hide_index=True,
    use_container_width=True,
    height=min(60 + 40 * len(clean_table), 420),
)

download_col1, download_col2 = st.columns(2)
with download_col1:
    st.download_button(
        "⬇️ تحميل الجدول المعالج (CSV)",
        data=clean_table.to_csv(index=False).encode("utf-8-sig"),
        file_name="Ecommerce_Master_Summary_Processed.csv",
        mime="text/csv",
        use_container_width=True,
    )
with download_col2:
    st.download_button(
        "⬇️ تحميل جدول البيانات الخام الكامل (CSV)",
        data=view.to_csv(index=False).encode("utf-8-sig"),
        file_name="Ecommerce_Master_Summary_Full.csv",
        mime="text/csv",
        use_container_width=True,
    )

st.markdown(
    f"""
    <div style="direction:rtl;text-align:right;color:{PALETTE['slate']};font-size:12px;margin-top:28px;
    border-top:1px solid {PALETTE['line']};padding-top:12px;">
    تم إعداد هذا التقرير آليًا بواسطة منصة الذكاء الاستراتيجي التنفيذي · للاستخدام الداخلي في دعم القرار فقط.
    </div>
    """,
    unsafe_allow_html=True,
)
# زود السطر ده عشان تخفي القائمة العلوية وشعار ستريمليت
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)