import streamlit as st
import requests
import pandas as pd
import re
import os
import streamlit_analytics
from collections import Counter

# ==========================================
# 1. KONFIGURASI & SECRETS
# ==========================================
YOUTUBE_API_KEY = st.secrets["YOUTUBE_API_KEY"]
SAFELINKU_API_KEY = st.secrets["SAFELINKU_API_KEY"]
logo_path = "nightflow-logo.png.png"

st.set_page_config(
    page_title="Nightflow PRO Researcher",
    page_icon=logo_path if os.path.exists(logo_path) else "🎸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. FUNGSI LOGIKA
# ==========================================
def get_safelink(long_url):
    api_url = f"https://api.safelinku.com/shorten?key={SAFELINKU_API_KEY}&url={long_url}"
    try:
        res = requests.get(api_url).json()
        if res.get("status") == "success":
            return res.get("shortenedUrl")
        return long_url
    except:
        return long_url

def clean_tags(tags, is_shorts=False):
    c = Counter(tags)
    top_tags = [f"#{t}" for t, _ in c.most_common(15)]
    if is_shorts:
        for s in ["#shorts", "#ytshorts"]:
            if s not in top_tags: top_tags.append(s)
    return " ".join(top_tags[:15])

# ==========================================
# 3. UI CLEANER (SANGAT AGRESIF)
# ==========================================
with streamlit_analytics.track():
    st.markdown("""
        <style>
        /* HILANGKAN TOTAL HEADER (Share, Star, GitHub, Menu) */
        header, [data-testid="stHeader"], .st-emotion-cache-zq5wms, .st-emotion-cache-18ni7ap {
            visibility: hidden !important;
            display: none !important;
            height: 0px !important;
        }
        
        /* HILANGKAN SIDEBAR & TOMBOL PANAH */
        [data-testid="stSidebar"], [data-testid="stSidebarNav"], 
        .st-emotion-cache-6qob1r, .st-emotion-cache-10o1hf7, 
        button[kind="header_button"] {
            display: none !important;
        }

        /* HILANGKAN FOOTER BAWAAN */
        footer { visibility: hidden !important; }

        /* RAPIKAN MARGIN ATAS */
        .stAppViewMain { margin-top: -120px; }

        /* TEMA GELAP UTAMA */
        .stApp { background: #0c0c0c; color: white; }
        
        /* JUDUL ATAS NEON */
        .neon-title { 
            color: white;
            text-shadow: 0 0 10px #d200ff, 0 0 20px #d200ff, 0 0 40px #d200ff; 
            text-align: center; 
            font-weight: 900; 
            font-size: 45px; 
            margin-bottom: 30px;
        }

        /* FOOTER NIGHTFLOW PRO (WARNA NEON UNGU-PINK UKURAN 40PX) */
        .nightflow-footer-neon {
            text-align: center;
            font-size: 40px; /* Ukuran disesuaikan menjadi 40px */
            font-weight: 900;
            color: white;
            text-shadow: 
                0 0 7px #fff,
                0 0 10px #fff,
                0 0 21px #d200ff,
                0 0 42px #d200ff,
                0 0 82px #d200ff;
            margin-top: 100px;
            padding-bottom: 80px;
            text-transform: uppercase;
            letter-spacing: 5px;
        }

        /* STYLING TOMBOL & INPUT */
        .stButton>button { 
            background: linear-gradient(90deg, #d200ff, #8a00ff) !important; 
            color: white !important; 
            border:none; width:100%; font-weight:bold; height: 55px; border-radius:15px; 
        }
        .sub-box { 
            background-color: #1e1e1e; padding: 25px; border-radius: 20px; 
            border: 2px solid #ff0000; text-align: center; margin-bottom: 25px; 
        }
        </style>
    """, unsafe_allow_html=True)

    # --- LOGO TENGAH ---
    if os.path.exists(logo_path):
        _, col_logo, _ = st.columns([1.5, 1, 1.5])
        with col_logo:
            st.image(logo_path, use_container_width=True)

    # --- JUDUL ---
    st.markdown('<h1 class="neon-title">Nightflow Keyword Researcher PRO</h1>', unsafe_allow_html=True)
    
    # --- SEARCH ---
    query = st.text_input("", placeholder="Masukkan keyword pencarian...")
    
    if st.button("START RESEARCH 🚀") and query:
        sub_link = "https://youtube.com/@nightflowpoppunk?sub_confirmation=1"
        st.markdown(f"""
            <div class="sub-box">
                <h2 style="color: #ff0000; margin-top: 0;">🔴 SUBSCRIBE REQUIRED</h2>
                <p>Silakan <b>Subscribe</b> channel Nightflow Pop Punk untuk melihat hasil riset.</p>
                <a href="{sub_link}" target="_blank">
                    <button style="background-color: #ff0000; color: white; border: none; padding: 12px 25px; border-radius: 8px; font-weight: bold; cursor: pointer;">
                        KLIK UNTUK SUBSCRIBE
                    </button>
                </a>
            </div>
        """, unsafe_allow_html=True)

        if st.checkbox("Saya sudah subscribe ✅"):
            with st.spinner("Sedang meriset YouTube..."):
                search_url = "https://www.googleapis.com/youtube/v3/search"
                s_params = {"part": "id", "q": query, "type": "video", "maxResults": 10, "key": YOUTUBE_API_KEY}
                res = requests.get(search_url, params=s_params).json()
                v_ids = [i["id"]["videoId"] for i in res.get("items", [])]

                if v_ids:
                    d_url = "https://www.googleapis.com/youtube/v3/videos"
                    d_params = {"part": "snippet,statistics", "id": ",".join(v_ids), "key": YOUTUBE_API_KEY}
                    items = requests.get(d_url, params=d_params).json().get("items", [])

                    results = []
                    all_tags = []
                    for item in items:
                        tags = re.findall(r"#(\w+)", item["snippet"].get("description", "").lower())
                        all_tags.extend(tags)
                        link_duit = get_safelink(f"https://youtube.com/watch?v={item['id']}")
                        results.append({
                            "Judul": item["snippet"]["title"],
                            "Views": f"{int(item['statistics'].get('viewCount', 0)):,}",
                            "LINK": link_duit
                        })

                    st.dataframe(pd.DataFrame(results), use_container_width=True)
                    
                    c1, c2 = st.columns(2)
                    with c1:
                        st.subheader("🏷️ Tag Video")
                        st.code(clean_tags(all_tags), language="text")
                    with c2:
                        st.subheader("📱 Tag Shorts")
                        st.code(clean_tags(all_tags, is_shorts=True), language="text")

    # --- FOOTER FINAL NEON 40PX ---
    st.markdown('<div class="nightflow-footer-neon">NIGHTFLOW PRO</div>', unsafe_allow_html=True)
