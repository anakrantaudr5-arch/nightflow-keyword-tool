# ... (bagian kode atas tetap sama) ...

# ==========================================
# 3. UI CLEANER & STYLING (DIUPDATE)
# ==========================================
with streamlit_analytics.track():
    st.markdown("""
        <style>
        /* [Hapus Header & Sidebar tetap sama seperti sebelumnya] */
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

        /* --- FOOTER DENGAN JARAK LEBIH JAUH --- */
        .nightflow-footer-container {
            margin-top: 250px; /* Menambah jarak jauh dari konten di atasnya */
            padding-bottom: 100px; /* Jarak dari batas paling bawah layar */
            text-align: center;
        }

        .nightflow-footer-neon {
            font-size: 40px; 
            font-weight: 900;
            color: white;
            text-shadow: 
                0 0 7px #fff,
                0 0 10px #fff,
                0 0 21px #d200ff,
                0 0 42px #d200ff,
                0 0 82px #d200ff;
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

    # ... (bagian pencarian dan logika tabel tetap sama) ...

    # --- BAGIAN FOOTER YANG DIUBAH (Sesuai Permintaan) ---
    st.markdown("""
        <div class="nightflow-footer-container">
            <div class="nightflow-footer-neon">NIGHTFLOW PRO</div>
        </div>
    """, unsafe_allow_html=True)
