import streamlit as st
import requests
import pandas as pd
import re
import os
from collections import Counter

# ==========================================
# 1. KONFIGURASI & SECRETS
# ==========================================
YOUTUBE_API_KEY = st.secrets["YOUTUBE_API_KEY"]
SAFELINKU_API_KEY = st.secrets["SAFELINKU_API_KEY"]

logo_path = "assets/nightflow-logo.png"

st.set_page_config(
    page_title="Nightflow PRO Researcher",
    page_icon="🎸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. FUNGSI LOGIKA
# ==========================================
def get_safelink(long_url):
    api_url = f"https://api.safelinku.com/shorten?key={SAFELINKU_API_KEY}&url={long_url}"
    try:
        res = requests.get(api_url, timeout=10).json()
        if res.get("status") == "success":
            return res.get("shortenedUrl")
        return long_url
    except Exception:
        return long_url


def clean_tags(tags, is_shorts=False):
    c = Counter(tags)
    top_tags = [f"#{t}" for t, _ in c.most_common(15)]
    if is_shorts:
        for s in ["#shorts", "#ytshorts"]:
            if s not in top_tags:
                top_tags.append(s)
    return " ".join(top_tags[:15])

# ==========================================
# 3. UI STYLING (FULL REPLACE)
# ==========================================
st.markdown("""
<style>
/* Hilangkan header, sidebar, footer Streamlit */
header, footer, [data-testid="stHeader"], [data-testid="stSidebar"] {
    display: none !important;
}

/* Background utama */
.stApp {
    background: radial-gradient(circle at top, #1a001f 0%, #0c0c0c 45%, #050505 100%);
    color: white;
    margin-top: -80px;
}

/* Judul Neon */
.neon-title {
    text-align: center;
    font-size: 46px;
    font-weight: 900;
    color: #ffffff;
    text-shadow:
        0 0 10px #d200ff,
        0 0 25px #b000ff,
        0 0 45px #7a00ff;
    margin-bottom: 30px;
}

/* Input */
input {
    text-align: center !important;
    font-size: 18px !important;
    border-radius: 10px !important;
}

/* Tombol */
.stButton>button {
    background: linear-gradient(90deg, #d200ff, #8a00ff) !important;
    color: white !important;
    border: none;
    width: 100%;
    height: 55px;
    font-size: 18px;
    font-weight: bold;
    border-radius: 14px;
    box-shadow: 0 0 25px rgba(210,0,255,0.6);
}

.stButton>button:hover {
    transform: scale(1.05);
    background: linear-gradient(90deg, #e600ff, #a100ff) !important;
}

/* Footer */
.nightflow-footer-container {
    margin-top: 300px;
    padding-bottom: 100px;
    text-align: center;
}

.nightflow-footer-neon {
    font-size: 40px;
    font-weight: 900;
    letter-spacing: 5px;
    color: white;
    text-shadow:
        0 0 10px #d200ff,
        0 0 30px #a100ff;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. HERO LOGO + TITLE
# ==========================================
if os.path.exists(logo_path):
    _, col_logo, _ = st.columns([1.5, 1, 1.5])
    with col_logo:
        st.image(logo_path, use_container_width=True)

st.markdown(
    '<h1 class="neon-title">Nightflow Keyword Researcher PRO</h1>',
    unsafe_allow_html=True
)

# ==========================================
# 5. INPUT
# ==========================================
query = st.text_input("", placeholder="Masukkan keyword pencarian YouTube...")

start = st.button("START RESEARCH 🚀")

# ==========================================
# 6. MAIN LOGIC
# ==========================================
if start and query:
    with st.spinner("🔎 Mengambil data YouTube..."):
        try:
            search_url = "https://www.googleapis.com/youtube/v3/search"
            search_params = {
                "part": "id",
                "q": query,
                "type": "video",
                "maxResults": 10,
                "key": YOUTUBE_API_KEY
            }

            search_res = requests.get(search_url, params=search_params, timeout=10).json()

            if "error" in search_res:
                st.error(search_res["error"]["message"])
            else:
                video_ids = [i["id"]["videoId"] for i in search_res.get("items", [])]

                if not video_ids:
                    st.warning("Tidak ada video ditemukan.")
                else:
                    detail_url = "https://www.googleapis.com/youtube/v3/videos"
                    detail_params = {
                        "part": "snippet,statistics",
                        "id": ",".join(video_ids),
                        "key": YOUTUBE_API_KEY
                    }

                    items = requests.get(detail_url, params=detail_params, timeout=10).json().get("items", [])

                    rows = []
                    all_tags = []

                    for item in items:
                        desc = item["snippet"].get("description", "").lower()
                        tags = re.findall(r"#(\w+)", desc)
                        all_tags.extend(tags)

                        rows.append({
                            "Judul Video": item["snippet"]["title"],
                            "Views": f"{int(item['statistics'].get('viewCount', 0)):,}",
                            "Link": get_safelink(f"https://youtube.com/watch?v={item['id']}")
                        })

                    st.subheader("🎬 Hasil Riset YouTube")
                    st.dataframe(pd.DataFrame(rows), use_container_width=True)

                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("🏷️ Hashtag Long Video")
                        st.code(clean_tags(all_tags), language="text")
                    with col2:
                        st.subheader("📱 Hashtag Shorts")
                        st.code(clean_tags(all_tags, is_shorts=True), language="text")

        except Exception as e:
            st.error(f"Terjadi kesalahan teknis: {e}")

# ==========================================
# 7. FOOTER
# ==========================================
st.markdown("""
<div class="nightflow-footer-container">
    <div class="nightflow-footer-neon">NIGHTFLOW PRO</div>
</div>
""", unsafe_allow_html=True)
