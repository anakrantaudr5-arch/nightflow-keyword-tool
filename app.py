import streamlit as st
import requests
import pandas as pd
import re
import os
import streamlit_analytics
from collections import Counter

# ==========================================
# 1. AMBIL DATA DARI SECRETS
# ==========================================
YOUTUBE_API_KEY = st.secrets["YOUTUBE_API_KEY"]
SAFELINKU_API_KEY = st.secrets["SAFELINKU_API_KEY"]

# Nama file logo di root GitHub
logo_path = "nightflow-logo.png.png"

st.set_page_config(
    page_title="Nightflow PRO Researcher",
    page_icon=logo_path if os.path.exists(logo_path) else "🎸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. FUNGSI LOGIKA (MONETISASI & HASHTAG)
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
# 3. TAMPILAN APLIKASI (UI) & ANALYTICS
# ==========================================
with streamlit_analytics.track():
    st.markdown("""
        <style>
        /* 1. MENGHILANGKAN SIDEBAR & TOMBOL NAVIGASI SECARA TOTAL */
        [data-testid="stSidebar"], 
        [data-testid="stSidebarNav"], 
        .st-emotion-cache-6qob1r, 
        .st-emotion-cache-10o1hf7,
        button[kind="header_button"] {
            display: none !important;
        }

        /* 2. MENGHILANGKAN JARAK KOSONG DI ATAS */
        .stAppViewMain {
            margin-top: -80px;
        }

        /* 3. TEMA GELAP & NEON */
        .stApp { background: #0c0c0c; color: white; }
        
        .neon-title { 
            color: #d200ff; 
            text-shadow: 0 0 15px #b700ff; 
            text-align: center; 
            font-weight: 900; 
            font-size: 45px; 
            margin-top: 10px;
            margin-bottom: 20px;
        }
        
        .stButton>button { 
            background: linear-gradient(90deg, #d200ff, #8a00ff) !important; 
            color: white !important; 
            border:none; 
            width:100%; 
            font-weight:bold; 
            height: 55px; 
            border-radius:15px; 
        }

        .sub-box { 
            background-color: #1e1e1e; 
            padding: 25px; 
            border-radius: 20px; 
            border: 2px solid #ff0000; 
            text-align: center; 
            margin-bottom: 25px; 
        }
        </style>
    """, unsafe_allow_html=True)

    # --- BAGIAN LOGO (TENGAH ATAS) ---
    # Menggunakan sistem kolom untuk memastikan logo di tengah
    if os.path.exists(logo_path):
        col_1, col_2, col_3 = st.columns([1.5, 1, 1.5])
        with col_2:
            st.image(logo_path, use_container_width=True)

    # --- JUDUL UTAMA ---
    st.markdown('<h1 class="neon-title">Nightflow Keyword Researcher PRO</h1>', unsafe_allow_html=True)
    
    # --- INPUT USER ---
    query = st.text_input("", placeholder="Masukkan keyword (contoh: pop punk guitar tutorial)")
    
    if st.button("START RESEARCH 🚀") and query:
        # TAMPILAN BOX SUBSCRIBE
        subscribe_link = "https://youtube.com/@nightflowpoppunk?sub_confirmation=1"
        st.markdown(f"""
            <div class="sub-box">
                <h2 style="color: #ff0000; margin-top: 0;">🔴 SUBSCRIBE UNTUK MEMBUKA DATA</h2>
                <p style="color: white;">Silakan <b>Subscribe</b> channel Nightflow Pop Punk agar hasil riset muncul di bawah.</p>
                <a href="{subscribe_link}" target="_blank" style="text-decoration: none;">
                    <button style="background-color: #ff0000; color: white; border: none; padding: 15px 30px; border-radius: 10px; font-weight: bold; cursor: pointer; font-size: 16px;">
                        KLIK UNTUK SUBSCRIBE
                    </button>
                </a>
            </div>
        """, unsafe_allow_html=True)

        # CHECKBOX KONFIRMASI
        if st.checkbox("Saya sudah klik subscribe ✅"):
            with st.spinner("Meriset YouTube & Memproses Link Berbayar..."):
                # YouTube Search API
                search_url = "https://www.googleapis.com/youtube/v3/search"
                s_params = {"part": "id", "q": query, "type": "video", "maxResults": 10, "key": YOUTUBE_API_KEY}
                search_res = requests.get(search_url, params=s_params).json()
                v_ids = [i["id"]["videoId"] for i in search_res.get("items", [])]

                if v_ids:
                    # Video Detail API
                    d_url = "https://www.googleapis.com/youtube/v3/videos"
                    d_params = {"part": "snippet,statistics", "id": ",".join(v_ids), "key": YOUTUBE_API_KEY}
                    items = requests.get(d_url, params=d_params).json().get("items", [])

                    final_data = []
                    all_tags = []

                    for item in items:
                        snip = item["snippet"]
                        stat = item["statistics"]
                        tags = re.findall(r"#(\w+)", snip.get("description", "").lower())
                        all_tags.extend(tags)
                        
                        link_yt = f"https://youtube.com/watch?v={item['id']}"
                        link_duit = get_safelink(link_yt)
                        
                        final_data.append({
                            "Judul Video": snip["title"],
                            "Views": f"{int(stat.get('viewCount', 0)):,}",
                            "AKSES VIDEO": link_duit
                        })

                    # TAMPILKAN HASIL
                    st.subheader("🎬 Hasil Riset")
                    st.dataframe(pd.DataFrame(final_data), use_container_width=True)

                    c1, c2 = st.columns(2)
                    with c1:
                        st.subheader("🏷️ Tag Long Video")
                        st.code(clean_tags(all_tags), language="text")
                    with c2:
                        st.subheader("📱 Tag Shorts")
                        st.code(clean_tags(all_tags, is_shorts=True), language="text")
                    st.balloons()
                else:
                    st.error("Data tidak ditemukan.")

    st.markdown("<br><br><hr>", unsafe_allow_html=True)
    st.caption("Nightflow PRO • Gunakan ?analytics=on untuk melihat log pengunjung.")
