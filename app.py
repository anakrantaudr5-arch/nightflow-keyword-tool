import streamlit as st
import requests
import pandas as pd
import re
from datetime import datetime, timedelta
from collections import Counter
import os

# ==========================================
# 1. SETUP & KONFIGURASI UTAMA
# ==========================================
YOUTUBE_API_KEY = st.secrets["YOUTUBE_API_KEY"]

# Nama file sesuai Screenshot (94): nightflow-logo.png.png
logo_path = "nightflow-logo.png.png"

st.set_page_config(
    page_title="Nightflow PRO Researcher",
    page_icon=logo_path if os.path.exists(logo_path) else "🎸",
    layout="wide"
)

# ==========================================
# 2. CSS CUSTOM (NEON PURPLE METAL UI)
# ==========================================
st.markdown(f"""
<style>
    .stApp {{
        background: #0c0c0c;
        background-image: linear-gradient(135deg, #0c0c0c 0%, #1a0014 40%, #0c0010 100%);
        color: white;
    }}
    
    /* Judul Hero */
    .hero-title {{
        font-size: 54px !important;
        font-weight: 900 !important;
        text-align: center !important;
        margin-top: 20px !important;
        color: #d200ff !important;
        text-shadow: 0 0 35px #b700ff, 0 0 60px #8a00ff;
    }}
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {{
        background-color: rgba(10,10,10,0.95) !important;
        border-right: 1px solid #3b0050 !important;
    }}
    
    /* Input Styling */
    .stTextInput input {{
        text-align: center !important;
        background-color: #1a1a1a !important;
        color: white !important;
        border: 1px solid #d200ff !important;
        border-radius: 10px !important;
    }}
    
    /* Button Neon */
    .stButton>button {{
        width: 100%;
        background: linear-gradient(90deg, #d200ff, #8a00ff) !important;
        border: none !important;
        color: white !important;
        font-weight: bold !important;
        padding: 10px !important;
        border-radius: 12px !important;
        box-shadow: 0 0 20px rgba(210, 0, 255, 0.4);
    }}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. SIDEBAR (LOGO & INFO)
# ==========================================
with st.sidebar:
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    else:
        st.warning("⚠️ Logo tidak ditemukan di folder assets")
    
    st.title("Nightflow Studio")
    st.caption("v1.0 Pro Edition • Real-time Data")
    st.divider()
    st.markdown("### Fitur Utama:")
    st.markdown("- 🎥 Video Real YouTube\n- 🏷️ Hashtag Asli Deskripsi\n- 📱 Strategi Shorts vs Long")

# ==========================================
# 4. FUNGSI LOGIKA (API & CLEANER)
# ==========================================
def get_youtube_data(query):
    try:
        # Search Videos
        search_url = "https://www.googleapis.com/youtube/v3/search"
        params = {"part": "id", "q": query, "type": "video", "maxResults": 15, "key": YOUTUBE_API_KEY}
        video_ids = [item["id"]["videoId"] for item in requests.get(search_url, params=params).json().get("items", [])]
        
        if not video_ids: return pd.DataFrame(), []

        # Get Video Details
        details_url = "https://www.googleapis.com/youtube/v3/videos"
        params = {"part": "snippet,statistics,contentDetails", "id": ",".join(video_ids), "key": YOUTUBE_API_KEY}
        items = requests.get(details_url, params=params).json().get("items", [])
        
        results, tags_list = [], []
        for item in items:
            snip = item["snippet"]
            stat = item["statistics"]
            desc = snip.get("description", "")
            
            # Perbaikan Regex Hashtag
            found_tags = re.findall(r"#(\w+)", desc.lower())
            tags_list.extend(found_tags)
            
            results.append({
                "Judul": snip["title"],
                "Channel": snip["channelTitle"],
                "Views": int(stat.get("viewCount", 0)),
                "Hashtags": " ".join([f"#{t}" for t in dict.fromkeys(found_tags)]),
                "Link": f"https://youtube.com/watch?v={item['id']}"
            })
        return pd.DataFrame(results), tags_list
    except:
        return pd.DataFrame(), []

def clean_tags_output(tags, is_shorts=False):
    c = Counter(tags)
    top_tags = [f"#{t}" for t, _ in c.most_common(15)]
    if is_shorts:
        for s in ["#shorts", "#ytshorts", "#shortsvideo"]:
            if s not in top_tags: top_tags.append(s)
    return " ".join(top_tags[:15])

# ==========================================
# 5. HALAMAN UTAMA (USER INTERFACE)
# ==========================================
st.markdown('<h1 class="hero-title">Nightflow Keyword Researcher PRO</h1>', unsafe_allow_html=True)

query = st.text_input("", placeholder="Masukkan keyword (misal: pop punk 2000s)")
col_a, col_b, col_c = st.columns([1,2,1])
with col_b:
    btn = st.button("Start Research 🚀")

if btn and query:
    with st.spinner("Menarik data dari YouTube..."):
        df, all_tags = get_youtube_data(query)
        
        if not df.empty:
            st.subheader("🎬 Video Real YouTube + Hashtag ASLI")
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            st.divider()
            st.subheader("🏷️ HASHTAG FINAL (TINGGAL COPY)")
            
            col1, col2 = st.columns(2)
            with col1:
                st.info("📺 **LONG VIDEO**")
                st.code(clean_tags_output(all_tags), language="text")
            with col2:
                st.success("📱 **SHORTS**")
                st.code(clean_tags_output(all_tags, is_shorts=True), language="text")
        else:
            st.error("Data tidak ditemukan. Cek keyword atau API Key anda.")


st.markdown("<br><hr><center>Nightflow PRO • Final Fixed Version</center>", unsafe_allow_html=True)

