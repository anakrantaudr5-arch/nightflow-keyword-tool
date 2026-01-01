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
    layout="wide"
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
# 3. TAMPILAN APLIKASI (UI)
# ==========================================
with streamlit_analytics.track():
    st.markdown("""
        <style>
        .stApp { background: #0c0c0c; color: white; }
        /* Sembunyikan Sidebar secara total */
        [data-testid="stSidebar"] { display: none; }
        [data-testid="stSidebarNav"] { display: none; }
        
        .neon-title { color: #d200ff; text-shadow: 0 0 15px #b700ff; text-align: center; font-weight: 900; font-size: 45px; margin-top: 10px; }
        .stButton>button { background: linear-gradient(90deg, #d200ff, #8a00ff) !important; color: white !important; border:none; width:100%; font-weight:bold; height: 50px; border-radius:15px; }
        .sub-box { background-color: #1e1e1e; padding: 20px; border-radius: 15px; border: 1px solid #ff0000; text-align: center; margin-bottom: 20px; }
        </style>
    """, unsafe_allow_html=True)

    # --- BAGIAN LOGO & JUDUL UTAMA (TENGAH) ---
    if os.path.exists(logo_path):
        col_logo_1, col_logo_2, col_logo_3 = st.columns([2, 1, 2])
        with col_logo_2:
            st.image(logo_path, use_container_width=True)

    st.markdown('<h1 class="neon-title">Nightflow Keyword Researcher PRO</h1>', unsafe_allow_html=True)
    
    # --- INPUT USER ---
    query = st.text_input("", placeholder="Masukkan keyword (contoh: pop punk guitar tutorial)")
    
    if st.button("START RESEARCH 🚀") and query:
        subscribe_link = "https://youtube.com/@nightflowpoppunk?sub_confirmation=1"
        st.markdown(f"""
            <div class="sub-box">
                <h3 style="color: white; margin-top: 0;">📢 Langkah Terakhir!</h3>
                <p style="color: #cccccc;">Silakan <b>Subscribe</b> channel Nightflow Pop Punk untuk membuka hasil riset.</p>
                <a href="{subscribe_link}" target="_blank" style="text-decoration: none;">
                    <button style="background-color: #ff0000; color: white; border: none; padding: 12px 25px; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 16px;">
                        🔴 KLIK UNTUK SUBSCRIBE
                    </button>
                </a>
            </div>
        """, unsafe_allow_html=True)

        if st.checkbox("Saya sudah subscribe (Centang untuk melihat data) ✅"):
            with st.spinner("Sedang meriset YouTube..."):
                search_url = "https://www.googleapis.com/youtube/v3/search"
                s_params = {"part": "id", "q": query, "type": "video", "maxResults": 10, "key": YOUTUBE_API_KEY}
                search_res = requests.get(search_url, params=s_params).json()
                v_ids = [i["id"]["videoId"] for i in search_res.get("items", [])]

                if v_ids:
                    d_url = "https://www.googleapis.com/youtube/v3/videos"
                    d_params = {"part": "snippet,statistics", "id": ",".join(v_ids), "key": YOUTUBE_API_KEY}
                    items = requests.get(d_url, params=d_params).json().get("items", [])

                    final_data = []
                    all_tags = []

                    for item in items:
                        snip = item["snippet"]
                        stat = item["statistics"]
                        desc = snip.get("description", "")
                        tags = re.findall(r"#(\w+)", desc.lower())
                        all_tags.extend(tags)
                        
                        link_yt = f"https://youtube.com/watch?v={item['id']}"
                        link_berbayar = get_safelink(link_yt)
                        
                        final_data.append({
                            "Judul Video": snip["title"],
                            "Views": f"{int(stat.get('viewCount', 0)):,}",
                            "AKSES VIDEO": link_berbayar
                        })

                    st.subheader("🎬 Hasil Riset (Link Berbayar)")
                    st.dataframe(pd.DataFrame(final_data), use_container_width=True)

                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("🏷️ Tag Long Video")
                        st.code(clean_tags(all_tags), language="text")
                    with col2:
                        st.subheader("📱 Tag Shorts")
                        st.code(clean_tags(all_tags, is_shorts=True), language="text")
                    st.balloons()
                else:
                    st.error("Data tidak ditemukan.")

    st.markdown("---")
    st.caption("Nightflow PRO • Gunakan ?analytics=on di URL untuk melihat catatan pengunjung.")
