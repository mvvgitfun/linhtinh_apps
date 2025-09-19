import streamlit as st
import pandas as pd
import json
from google.cloud import bigquery
from google.oauth2 import service_account
from io import BytesIO
from collections import Counter
import re

# optional translation lib
try:
    from googletrans import Translator
    TRANSLATOR_AVAILABLE = True
except Exception:
    TRANSLATOR_AVAILABLE = False

# ================== CONFIG ==================
st.set_page_config(page_title="📊 Game Review Analytics", layout="wide")

st.markdown(
    "<h1 style='text-align: center;'>📊 Game Review Analytics Dashboard 🎮</h1>",
    unsafe_allow_html=True,
)

# ================== BIGQUERY CONNECT ==================
# Lấy credentials từ Streamlit secrets (st.secrets["bigquery"] should be the JSON structure)
try:
    sa_info = st.secrets["bigquery"]
    creds = service_account.Credentials.from_service_account_info(sa_info)
    client = bigquery.Client(credentials=creds, project=creds.project_id)
except Exception as e:
    st.error("❌ Không tìm thấy hoặc không đọc được `st.secrets['bigquery']`. Vui lòng kiểm tra lại.")
    st.stop()

# ================== LOAD DATA ==================
@st.cache_data(ttl=600)
def load_data():
    try:
        query = """
            SELECT
                Package_Name AS package_name,
                App_Version_Name AS app_version,
                Reviewer_Language AS reviewer_lang,
                Device AS device,
                Review_Submit_Date_and_Time AS review_time,
                SAFE_CAST(Star_Rating AS INT64) AS star_rating,
                Review_Title AS review_title,
                Review_Text AS review_text,
                Developer_Reply_Text AS dev_reply
            FROM `mps-data-139.gpc_reviews_viz.reviews`
            WHERE Package_Name IS NOT NULL
        """
        return client.query(query).to_dataframe()
    except Exception as e:
        st.error(f"❌ BigQuery error: {e}")
        return pd.DataFrame()

df = load_data()
if df.empty:
    st.warning("⚠️ Không có dữ liệu trả về từ BigQuery.")
    st.stop()

# Normalize columns
df["review_text"] = df["review_text"].astype("string")
df["review_time"] = pd.to_datetime(df["review_time"], errors="coerce")
df["date"] = df["review_time"].dt.date

# ================== SIDEBAR CONTROLS ==================
st.sidebar.header("Filters & Options")
apps = df["package_name"].dropna().unique().tolist()
selected_app = st.sidebar.selectbox("🎮 Chọn game (package name)", apps)

# Version filter
df_app_all = df[df["package_name"] == selected_app].copy()
versions = ["Tất cả"] + sorted(df_app_all["app_version"].dropna().unique().tolist())
selected_version = st.sidebar.selectbox("🛠 Chọn phiên bản", versions)

# Translation option
translate_enable = st.sidebar.checkbox("🌐 Dịch review sang tiếng Anh (Translate to English)", value=False)
if translate_enable and not TRANSLATOR_AVAILABLE:
    st.sidebar.error("Module `googletrans` chưa cài. Chạy: pip install googletrans==4.0.0-rc1")
    translate_enable = False

# Analysis options
use_translated_for_analysis = st.sidebar.checkbox("🔎 Dùng tiếng Anh để phân tích (nếu có)", value=True)
min_word_count = st.sidebar.number_input("Min words to consider review text", min_value=0, max_value=500, value=1)

# ================== SELECT DATA SLICE ==================
df_app = df_app_all.copy()
if selected_version != "Tất cả":
    df_app = df_app[df_app["app_version"] == selected_version].copy()

# ================== TRANSLATION HELPERS ==================
@st.cache_data(ttl=3600)
def translate_texts_batch(texts, dest="en"):
    if not TRANSLATOR_AVAILABLE:
        return texts
    translator = Translator()
    translated = []
    CHUNK = 50
    for i in range(0, len(texts), CHUNK):
        chunk = texts[i:i+CHUNK]
        strs = ["" if (t is None or str(t).strip() == "") else str(t) for t in chunk]
        try:
            res = translator.translate(strs, dest=dest)
            if isinstance(res, list):
                translated.extend([r.text if getattr(r, "text", None) is not None else "" for r in res])
            else:
                translated.append(res.text if getattr(res, "text", None) is not None else "")
        except Exception:
            translated.extend(strs)
    return translated

if translate_enable:
    st.info("Đang dịch review sang tiếng Anh (caching để giảm requests)...")
    texts = df_app["review_text"].fillna("").astype(str).tolist()
    translated_list = translate_texts_batch(texts, dest="en")
    df_app["review_text_en"] = translated_list
else:
    df_app["review_text_en"] = df_app["review_text"]

if use_translated_for_analysis:
    analysis_text_col = "review_text_en"
else:
    analysis_text_col = "review_text"

# ================== METRICS ==================
st.subheader(f"📦 Đang xem: {selected_app}  —  Phiên bản: {selected_version}")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("👥 Tổng số review", df_app.shape[0])
with col2:
    st.metric("💬 Có review text", int(df_app["review_text"].astype(bool).sum()))
with col3:
    avg_rating = df_app["star_rating"].dropna()
    st.metric("⭐ Điểm trung bình", round(avg_rating.mean(), 2) if not avg_rating.empty else "N/A")

# ================== DISTRIBUTIONS ==================
st.subheader("⭐ Phân bố Rating")
rating_counts = df_app["star_rating"].value_counts().sort_index()
st.bar_chart(rating_counts)

st.subheader("⏱ Review theo thời gian (số lượng / ngày)")
time_series = df_app.groupby("date").size().rename("count")
st.line_chart(time_series)

# ================== ISSUE ANALYSIS ==================
st.subheader("🔍 Phân tích lý do rating thấp (1-2 sao)")
low_reviews = df_app[(df_app["star_rating"] <= 2) & (df_app[analysis_text_col].notna())].copy()
low_reviews["analysis_text"] = low_reviews[analysis_text_col].astype(str)

issues_keywords = {
    r"\blag\b": "Lag / Slow",
    r"\bslow\b": "Lag / Slow",
    r"\bcrash\b": "Crash",
    r"\bforce close\b": "Crash",
    r"\bad(s)?\b": "Too Many Ads",
    r"\bads\b": "Too Many Ads",
    r"\bcontrol(s)?\b": "Control Issues",
    r"\bbug\b": "Bug",
    r"\berror\b": "Error",
    r"\bpay(ment)?\b": "Monetization / Payment",
    r"\binstall\b": "Install / Update Issues",
    r"\bconnect(ion)?\b": "Connection / Network",
}

def detect_issue_from_text(text):
    if not text or text.strip() == "":
        return None
    t = text.lower()
    for pattern, label in issues_keywords.items():
        if re.search(pattern, t):
            return label
    return None

if not low_reviews.empty:
    low_reviews["detected_issue"] = low_reviews["analysis_text"].apply(detect_issue_from_text)
    issue_counts = low_reviews["detected_issue"].value_counts(dropna=True)
    if not issue_counts.empty:
        st.bar_chart(issue_counts)
    else:
        st.info("Không phát hiện keyword issue nào phổ biến — bạn có thể mở rộng danh sách `issues_keywords`.")
    st.subheader("📋 Một số review 1-2★ (kèm bản dịch nếu bật)")
    show_cols = ["star_rating", "reviewer_lang", "analysis_text", "detected_issue"]
    st.dataframe(low_reviews[show_cols].rename(columns={"analysis_text": "Review (analysis text)"}).head(50))
else:
    st.info("Không có review 1-2★ để phân tích trong tập dữ liệu đã chọn.")

# ================== WORDCLOUD ==================
st.subheader("☁️ WordCloud từ review text (dùng text phân tích)")
all_text = " ".join(df_app[analysis_text_col].dropna().astype(str).tolist())
if all_text.strip():
    try:
        from wordcloud import WordCloud
        import matplotlib.pyplot as plt
        from wordcloud import STOPWORDS
        stopwords = set(STOPWORDS)
        extra_stops = {"game", "play", "one", "like", "good", "dont", "the", "and"}
        stopwords.update(extra_stops)

        wc = WordCloud(width=800, height=400, background_color="white", stopwords=stopwords, max_words=200).generate(all_text)

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.imshow(wc, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)
    except Exception as e:
        st.error("WordCloud không thể tạo (thiếu package?). Cài: pip install wordcloud matplotlib")
else:
    st.info("Không có review text để tạo WordCloud.")

# ================== RAW DATA ==================
st.subheader("📜 Dữ liệu gốc (có cột bản dịch khi bật)")
display_cols = ["review_time", "star_rating", "reviewer_lang", "device", "review_text"]
if translate_enable:
    display_cols += ["review_text_en"]
st.dataframe(df_app[display_cols].sort_values(by="review_time", ascending=False).reset_index(drop=True), height=400)

# ================== DOWNLOAD ==================
def to_excel_bytes(df_export: pd.DataFrame) -> bytes:
    with BytesIO() as buffer:
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df_export.to_excel(writer, index=False, sheet_name="Reviews")
        return buffer.getvalue()

st.download_button(
    "⬇️ Tải dữ liệu (.xlsx)",
    to_excel_bytes(df_app),
    file_name=f"{selected_app}_reviews.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)

# ================== NOTES ==================
st.markdown("""
**Ghi chú**
- Dịch dùng package `googletrans`; có thể bị rate-limit hoặc không hoàn hảo — nếu gặp lỗi, tắt option translate.
- `st.secrets["bigquery"]` phải chứa JSON của service account (copy nguyên file service_account.json vào Streamlit secrets).
- Nếu muốn cải thiện phân loại issue, mở rộng `issues_keywords`.
""")
