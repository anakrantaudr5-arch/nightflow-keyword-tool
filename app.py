import streamlit as st
import requests
import pandas as pd
import re
import os
import streamlit_analytics  # Pastikan baris ini ada!
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
# 2. UI CLEANER & STYLING (JARAK FOOTER DIATUR)
# ==========================================
with streamlit_analytics.track():
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
        .stAppViewMain { margin-top: -120px; }

        .stApp { background: #0c0c0c; color: white; }
        
        .neon-title { 
            color: white;
            text-shadow: 0 0 10px #d200ff, 0 0 20px #d200ff, 0 0 40px #d200ff; 
            text-align: center; font-weight: 900; font-size: 45px; margin-bottom: 30px;
        }

        /* --- FOOTER DENGAN JARAK JAUH KE BAWAH --- */
        .nightflow-footer-container {
            margin-top: 250px; /* Jarak jauh ke bawah sesuai permintaan */
            padding-bottom: 80px; 
            text-align: center;
        }

        .nightflow-footer-neon {
            font-size: 40px; /* Ukuran 40px sesuai permintaan */
            font-weight: 900;
            color: white;
            text-shadow: 0 0 7px #fff, 0 0 15px #d200ff, 0 0 30px #d200ff;
            text-transform: uppercase;
            letter-spacing: 5px;
            display: inline-block;
        }

        .stButton>button { 
            background: linear-gradient(90deg, #d200ff, #8a00ff) !important; 
            color: white !important; 
            border:none; width:100%; font-weight:bold; height: 55px; border-radius:15px; 
        }
        </style>
    """, unsafe_allow_html=True)

    # ... (Gunakan logika pencarian yang sudah ada sebelumnya) ...
    # Masukkan input_text, button, dan logika API YouTube di sini

    # --- BAGIAN FOOTER PALING BAWAH ---
    st.markdown("""
        <div class="nightflow-footer-container">
            <div class="nightflow-footer-neon">NIGHTFLOW PRO</div>
        </div>
    """, unsafe_allow_html=True)
