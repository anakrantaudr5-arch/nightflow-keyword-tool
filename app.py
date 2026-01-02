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
# 3. UI STYLING (CLEAN & NEON)
# ==========================================
st.markdown("""
    <style>
    /* Hapus Header & Sidebar */
    header, [data-testid="stHeader"], .st-emotion-cache-zq5wms, .st-emotion-cache-18ni7ap {
        visibility: hidden !important; display: none !important; height: 0px !important;
    }
    [data-testid="stSidebar"], [data-testid="stSidebarNav"], .st-emotion-cache-6qob1r, .st-emotion-cache-10o1hf7 {
        display: none !important;
    }
    footer { visibility: hidden !important; }

    /* Tema Gelap */
    .stApp { background: #0c0c0c; color: white; margin-top: -80px; }
    
    .neon-title { 
        color: white;
        text-shadow: 0 0 10px #d200ff, 0 0 20px #d200ff; 
        text-align: center; font-weight: 900; font-size: 45px; margin-bottom: 30px;
    }

    /* Tombol */
    .stButton>button { 
        background: linear-gradient(90deg, #d200ff, #8a00ff) !important; 
        color: white !important; border:none; width:100%; font-weight:bold; height: 55px; border-radius:15px; 
    }

    /* Footer Nightflow PRO (Jarak 300px) */
    .nightflow-footer-container {
        margin-top: 300px;
        padding-bottom: 100px;
        text-align: center;
    }
    .nightflow-footer-neon {
        font-size: 40px; font-weight: 900; color: white;
        text-shadow: 0 0 10px #d200ff, 0 0 20px #d200ff;
        text-transform: uppercase; letter-spacing: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# --- LOGO & JUDUL ---
if os.path.exists(logo_path):
    _, col_logo, _ = st.columns([1.5, 1, 1.5])
    with col_logo:
        st.image(logo_path, use_container_width=True)

st.markdown('<h1 class="neon-title">Nightflow Keyword Researcher PRO</h1>', unsafe_allow_html=True)

# --- INPUT ---
query = st.text_input("", placeholder="Masukkan keyword pencarian...")

if st.button("START RESEARCH 🚀") and query:
    with st.spinner("Sedang mengambil data riset..."):
        try:
            # 1. Ambil data YouTube
            search_url = "https://www.googleapis.com/youtube/v3/search"
            s_params = {"part": "id", "q": query, "type": "video", "maxResults": 10, "key": YOUTUBE_API_KEY}
            search_res = requests.get(search_url, params=s_params).json()

            if "error" in search_res:
                st.error(f"YouTube API Error: {search_res['error']['message']}")
            else:
                v_ids = [i["id"]["videoId"] for i in search_res.get("items", [])]

                if v_ids:
                    # 2. Ambil detail video
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
                            "Judul Video": item["snippet"]["title"],
                            "Views": f"{int(item['statistics'].get('viewCount', 0)):,}",
                            "AKSES VIDEO": link_duit
                        })

                    # Tampilkan Hasil
                    st.subheader("🎬 Hasil Riset")
                    st.dataframe(pd.DataFrame(results), use_container_width=True)

                    c1, c2 = st.columns(2)
                    with c1:
                        st.subheader("🏷️ Tag Long Video")
                        st.code(clean_tags(all_tags), language="text")
                    with c2:
                        st.subheader("📱 Tag Shorts")
                        st.code(clean_tags(all_tags, is_shorts=True), language="text")
                else:
                    st.warning("Data tidak ditemukan. Coba kata kunci lain.")
        
        except Exception as e:
            st.error(f"Terjadi kesalahan teknis: {e}")

# --- FOOTER ---
st.markdown("""
    <div class="nightflow-footer-container">
        <div class="nightflow-footer-neon">NIGHTFLOW PRO</div>
    </div>
""", unsafe_allow_html=True)

    if st.checkbox("Saya sudah subscribe ✅"):
        with st.spinner("Sedang meriset YouTube..."):
            try:
                # 1. API YouTube Search
                search_url = "https://www.googleapis.com/youtube/v3/search"
                s_params = {"part": "id", "q": query, "type": "video", "maxResults": 10, "key": YOUTUBE_API_KEY}
                search_res = requests.get(search_url, params=s_params).json()

                if "error" in search_res:
                    st.error(f"YouTube API Error: {search_res['error']['message']}")
                else:
                    v_ids = [i["id"]["videoId"] for i in search_res.get("items", [])]

                    if v_ids:
                        # 2. API Detail Video
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
                                "Judul Video": item["snippet"]["title"],
                                "Views": f"{int(item['statistics'].get('viewCount', 0)):,}",
                                "AKSES VIDEO": link_duit
                            })

                        st.subheader("🎬 Hasil Riset")
                        st.dataframe(pd.DataFrame(results), use_container_width=True)

                        c1, c2 = st.columns(2)
                        with c1:
                            st.subheader("🏷️ Tag Long Video")
                            st.code(clean_tags(all_tags), language="text")
                        with c2:
                            st.subheader("📱 Tag Shorts")
                            st.code(clean_tags(all_tags, is_shorts=True), language="text")
                    else:
                        st.warning("Data tidak ditemukan.")
            
            except Exception as e:
                st.error(f"Kesalahan: {e}")

# --- BAGIAN FOOTER (Tetap di bawah) ---
st.markdown("""
    <div class="nightflow-footer-container">
        <div class="nightflow-footer-neon">NIGHTFLOW PRO</div>
    </div>
""", unsafe_allow_html=True)
            <h2 style="color: #ff0000; margin-top: 0;">🔴 SUBSCRIBE REQUIRED</h2>
            <p>Subscribe channel Nightflow Pop Punk untuk membuka hasil riset.</p>
            <a href="{sub_link}" target="_blank">
                <button style="background-color: #ff0000; color: white; border: none; padding: 12px 25px; border-radius: 8px; font-weight: bold; cursor: pointer;">
                    KLIK UNTUK SUBSCRIBE
                </button>
            </a>
        </div>
    """, unsafe_allow_html=True)

    if st.checkbox("Saya sudah subscribe ✅"):
        with st.spinner("Sedang meriset YouTube..."):
            try:
                # 1. Ambil data pencarian YouTube
                search_url = "https://www.googleapis.com/youtube/v3/search"
                s_params = {"part": "id", "q": query, "type": "video", "maxResults": 10, "key": YOUTUBE_API_KEY}
                search_res = requests.get(search_url, params=s_params).json()

                if "error" in search_res:
                    st.error(f"YouTube API Error: {search_res['error']['message']}")
                else:
                    v_ids = [i["id"]["videoId"] for i in search_res.get("items", [])]

                    if v_ids:
                        # 2. Ambil detail video (views & tags)
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
                                "Judul Video": item["snippet"]["title"],
                                "Views": f"{int(item['statistics'].get('viewCount', 0)):,}",
                                "AKSES VIDEO": link_duit
                            })

                        st.subheader("🎬 Hasil Riset")
                        st.dataframe(pd.DataFrame(results), use_container_width=True)

                        c1, c2 = st.columns(2)
                        with c1:
                            st.subheader("🏷️ Tag Long Video")
                            st.code(clean_tags(all_tags), language="text")
                        with c2:
                            st.subheader("📱 Tag Shorts")
                            st.code(clean_tags(all_tags, is_shorts=True), language="text")
                    else:
                        st.warning("Data tidak ditemukan. Coba kata kunci lain.")
            
            except Exception as e:
                st.error(f"Terjadi kesalahan teknis: {e}")

# --- BAGIAN FOOTER (Tetap tampil di bawah) ---
st.markdown("""
    <div class="nightflow-footer-container">
        <div class="nightflow-footer-neon">NIGHTFLOW PRO</div>
    </div>
""", unsafe_allow_html=True)
                <button style="background-color: #ff0000; color: white; border: none; padding: 12px 25px; border-radius: 8px; font-weight: bold; cursor: pointer;">
                    KLIK UNTUK SUBSCRIBE
                </button>
            </a>
        </div>
    """, unsafe_allow_html=True)

    if st.checkbox("Saya sudah subscribe ✅"):
        with st.spinner("Sedang meriset YouTube..."):
            try:
                # 1. SEARCH API
                search_url = "https://www.googleapis.com/youtube/v3/search"
                s_params = {"part": "id", "q": query, "type": "video", "maxResults": 10, "key": YOUTUBE_API_KEY}
                search_res = requests.get(search_url, params=s_params).json()

                if "error" in search_res:
                    st.error(f"YouTube API Error: {search_res['error']['message']}")
                    if "quota" in search_res['error']['message'].lower():
                        st.warning("Kuota API harian Anda habis. Silakan ganti API Key di Secrets atau tunggu besok.")
                else:
                    v_ids = [i["id"]["videoId"] for i in search_res.get("items", [])]

                    if v_ids:
                        # 2. DETAIL VIDEO API
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
                                "Judul Video": item["snippet"]["title"],
                                "Views": f"{int(item['statistics'].get('viewCount', 0)):,}",
                                "AKSES VIDEO": link_duit
                            })

                        st.subheader("🎬 Hasil Riset")
                        st.dataframe(pd.DataFrame(results), use_container_width=True)

                        c1, c2 = st.columns(2)
                        with c1:
                            st.subheader("🏷️ Tag Long Video")
                            st.code(clean_tags(all_tags), language="text")
                        with c2:
                            st.subheader("📱 Tag Shorts")
                            st.code(clean_tags(all_tags, is_shorts=True), language="text")
                    else:
                        st.warning("Tidak ada video yang ditemukan untuk keyword tersebut.")
            
            except Exception as e:
                st.error(f"Terjadi kesalahan koneksi: {e}")

# --- FOOTER ---
st.markdown("""
    <div class="nightflow-footer-container">
        <div class="nightflow-footer-neon">NIGHTFLOW PRO</div>
    </div>
""", unsafe_allow_html=True)
            <h2 style="color: #ff0000; margin-top: 0;">🔴 SUBSCRIBE REQUIRED</h2>
            <p>Subscribe channel Nightflow Pop Punk untuk membuka hasil riset.</p>
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
                        "Judul Video": item["snippet"]["title"],
                        "Views": f"{int(item['statistics'].get('viewCount', 0)):,}",
                        "AKSES VIDEO": link_duit
                    })

                st.subheader("🎬 Hasil Riset")
                st.dataframe(pd.DataFrame(results), use_container_width=True)

                c1, c2 = st.columns(2)
                with c1:
                    st.subheader("🏷️ Tag Long Video")
                    st.code(clean_tags(all_tags), language="text")
                with c2:
                    st.subheader("📱 Tag Shorts")
                    st.code(clean_tags(all_tags, is_shorts=True), language="text")
            else:
                st.error("Data tidak ditemukan.")

# --- FOOTER ---
st.markdown("""
    <div class="nightflow-footer-container">
        <div class="nightflow-footer-neon">NIGHTFLOW PRO</div>
    </div>
""", unsafe_allow_html=True)




