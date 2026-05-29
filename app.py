import streamlit as st
import pandas as pd
import numpy as np
from modules.saw import hitung_saw
from modules.fuzzy_mcdm import hitung_fuzzy

st.set_page_config(
    page_title="SPK Pemilihan Laptop",
    page_icon="",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background-color: #f8f9fb;
    }

    /* ---- SIDEBAR ---- */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e5e7eb;
    }
    [data-testid="stSidebar"] * {
        color: #374151 !important;
    }
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"],
    [data-testid="stSidebar"] .stTextInput input,
    [data-testid="stSidebar"] .stNumberInput input {
        background-color: #f9fafb !important;
        border: 1px solid #e5e7eb !important;
        color: #111827 !important;
    }
    [data-baseweb="popover"] li,
    [data-baseweb="menu"] div {
        color: #111827 !important;
        background-color: #ffffff !important;
    }

    /* ---- HEADER ---- */
    .page-header {
        margin-bottom: 28px;
        padding-bottom: 20px;
        border-bottom: 1px solid #e5e7eb;
    }
    .page-title {
        font-size: 3rem !important;
        font-weight: 800 !important;
        color: #111827 !important;
        margin: 0 0 8px 0 !important;
        line-height: 1.15 !important;
        letter-spacing: -0.5px !important;
    }
    .page-desc {
        font-size: 1rem !important;
        color: #6b7280 !important;
        margin: 0 !important;
    }

    /* ---- STAT CARDS ---- */
    .stat-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 20px 24px;
    }
    .stat-label {
        font-size: 0.78rem;
        font-weight: 600;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }
    .stat-value {
        font-size: 1.7rem;
        font-weight: 700;
        color: #111827;
    }
    .stat-sub {
        font-size: 0.8rem;
        color: #9ca3af;
        margin-top: 4px;
    }

    /* ---- KRITERIA CARDS ---- */
    .kriteria-row {
        display: flex;
        gap: 12px;
        margin-bottom: 28px;
        flex-wrap: wrap;
    }
    .kriteria-card {
        flex: 1;
        min-width: 120px;
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 16px;
    }
    .kriteria-nama {
        font-size: 0.78rem;
        font-weight: 600;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .kriteria-bobot {
        font-size: 1.5rem;
        font-weight: 700;
        color: #111827;
        margin: 4px 0;
    }
    .badge {
        display: inline-block;
        font-size: 0.7rem;
        font-weight: 600;
        padding: 2px 10px;
        border-radius: 20px;
    }
    .badge-benefit {
        background: #dcfce7;
        color: #166534;
    }
    .badge-cost {
        background: #fee2e2;
        color: #991b1b;
    }

    /* ---- REKOMENDASI CARD ---- */
    .rekomendasi-card {
        background: #111827;
        border-radius: 12px;
        padding: 24px;
        color: white;
        text-align: center;
    }
    .rekomendasi-label {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #9ca3af;
        margin-bottom: 10px;
    }
    .rekomendasi-nama {
        font-size: 1.2rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 6px;
    }
    .rekomendasi-skor {
        font-size: 2rem;
        font-weight: 700;
        color: #ffffff;
    }
    .rekomendasi-skor-label {
        font-size: 0.75rem;
        color: #6b7280;
        margin-top: 2px;
    }

    /* ---- TABS ---- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: #f3f4f6;
        border-radius: 8px;
        padding: 4px;
        border-bottom: none;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        padding: 8px 20px;
        font-size: 0.85rem;
        font-weight: 500;
        color: #6b7280 !important;
        background: transparent;
        border: none;
    }
    .stTabs [aria-selected="true"] {
        background: #ffffff !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    .stTabs [aria-selected="true"] p,
    .stTabs [aria-selected="true"] span,
    .stTabs [aria-selected="true"] div {
        color: #111827 !important;
        font-weight: 600;
    }

    /* ---- BUTTON ---- */
    .stButton > button {
        background-color: #111827;
        color: #ffffff !important;
        border: none;
        border-radius: 8px;
        padding: 10px 18px;
        font-size: 0.85rem;
        font-weight: 500;
        transition: background 0.2s;
    }
    .stButton > button:hover {
        background-color: #1f2937;
        color: #ffffff !important;
    }
    .stButton > button * {
        color: #ffffff !important;
    }

    /* ---- TYPOGRAPHY OVERRIDE ---- */
    h1, h2, h3, h4 {
        color: #111827 !important;
    }
    p, li, label {
        color: #374151 !important;
    }

    /* ---- DIVIDER ---- */
    hr {
        border: none;
        border-top: 1px solid #e5e7eb;
        margin: 24px 0;
    }

    .footer-text {
        font-size: 0.78rem;
        color: #9ca3af;
        text-align: center;
        padding: 16px 0;
    }
</style>
""", unsafe_allow_html=True)


#  DATA AWAL 
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame({
        'Alternatif': ['ASUS ROG Zephyrus', 'Lenovo Legion 5', 'MacBook Pro M2', 'Acer Swift 3', 'MSI Modern 14'],
        'RAM (GB)': [32, 16, 16, 8, 16],
        'SSD (GB)': [1024, 512, 512, 256, 512],
        'Skor Prosesor': [9, 7, 8, 5, 8],
        'Harga (Juta Rp)': [25, 18, 24, 10, 15],
        'Berat (kg)': [1.9, 2.3, 1.6, 1.4, 1.3]
    })

if 'bobot' not in st.session_state:
    st.session_state.bobot = {
        'RAM (GB)':          {'bobot': 0.30, 'tipe': 1},
        'SSD (GB)':          {'bobot': 0.25, 'tipe': 1},
        'Skor Prosesor':     {'bobot': 0.20, 'tipe': 1},
        'Harga (Juta Rp)':   {'bobot': 0.15, 'tipe': 0},
        'Berat (kg)':        {'bobot': 0.10, 'tipe': 0}
    }



#  SIDEBAR 
with st.sidebar:
    st.markdown("""
    <div style="padding: 8px 4px 20px;">
        <div style="font-size: 1.3rem; font-weight: 700; color: #111827;">SPK Laptop</div>
        <div style="font-size: 0.9rem; color: #9ca3af; margin-top: 3px;">Sistem Pendukung Keputusan</div>
    </div>
    <hr style="margin: 0 0 20px 0; border-top: 1px solid #e5e7eb;">
    """, unsafe_allow_html=True)

    with st.expander("Tambah Laptop Baru"):
        nama = st.text_input("Nama Laptop", placeholder="Contoh: Dell XPS 15")
        col_a, col_b = st.columns(2)
        with col_a:
            ram      = st.selectbox("RAM (GB)", [8, 16, 32, 64], index=1)
            prosesor = st.selectbox("Skor Prosesor", [3, 5, 6, 7, 8, 9], index=4)
        with col_b:
            ssd   = st.selectbox("SSD (GB)", [256, 512, 1024, 2048], index=1)
            harga = st.number_input("Harga (Juta Rp)", 5, 50, 15)
            berat = st.number_input("Berat (kg)", 1.0, 3.5, 1.5, step=0.1)

        st.caption("Panduan skor prosesor: i3=3, i5=5, Ryzen5=6, i7=7, Ryzen7/M2=8, i9/M3=9")

        if st.button("Simpan Laptop", use_container_width=True):
            if nama.strip():
                baru = pd.DataFrame({
                    'Alternatif':     [nama.strip()],
                    'RAM (GB)':        [ram],
                    'SSD (GB)':        [ssd],
                    'Skor Prosesor':   [prosesor],
                    'Harga (Juta Rp)': [harga],
                    'Berat (kg)':      [berat]
                })
                st.session_state.data = pd.concat([st.session_state.data, baru], ignore_index=True)
                st.success(f"{nama} berhasil ditambahkan.")
                st.rerun()
            else:
                st.error("Nama laptop tidak boleh kosong.")

    with st.expander("Kelola Kriteria"):

        aksi_kriteria = st.radio(
            "Aksi",
            ["Edit Bobot", "Tambah", "Hapus"],
            horizontal=True,
            label_visibility="collapsed"
        )

        st.markdown("<div style='margin-top:8px;'></div>", unsafe_allow_html=True)

        # ── EDIT BOBOT ──
        if aksi_kriteria == "Edit Bobot":
            bobot_baru = {}
            inputs = {}
            for k, v in st.session_state.bobot.items():
                st.markdown(f"<div style='font-size:0.8rem;font-weight:600;color:#374151;margin-top:10px;margin-bottom:4px;'>{k}</div>", unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                with c1:
                    val = st.number_input("Bobot (%)", 0, 100, int(v['bobot']*100), step=1,
                                          key=f"be_{k}", label_visibility="visible")
                with c2:
                    tipe = st.selectbox("Tipe", ["Benefit", "Cost"],
                                        index=0 if v['tipe']==1 else 1,
                                        key=f"te_{k}", label_visibility="visible")
                inputs[k] = val
                bobot_baru[k] = {'bobot': val/100, 'tipe': 1 if tipe=="Benefit" else 0}

            total = sum(inputs.values())
            st.markdown("<div style='margin-top:6px'></div>", unsafe_allow_html=True)
            if total == 100:
                st.success(f"Total: {total}% ✓")
                if st.button("Simpan", use_container_width=True, key="btn_simpan_bobot"):
                    st.session_state.bobot = bobot_baru
                    st.rerun()
            elif total < 100:
                st.info(f"Total: {total}% — kurang {100-total}%")
            else:
                st.error(f"Total: {total}% — kelebihan {total-100}%")

        # ── TAMBAH ──
        elif aksi_kriteria == "Tambah":
            nama_k  = st.text_input("Nama kriteria", placeholder="Contoh: Layar (inci)")
            bobot_k = st.number_input("Bobot (%)", 1, 100, 10, step=1)
            tipe_k  = st.selectbox("Tipe", [
                "Benefit",
                "Cost"
            ])

            if st.button("Tambah Kriteria", use_container_width=True):
                nama_k = nama_k.strip()
                if not nama_k:
                    st.error("Nama tidak boleh kosong.")
                elif nama_k in st.session_state.bobot:
                    st.error("Kriteria sudah ada.")
                else:
                    st.session_state.bobot[nama_k] = {
                        'bobot': bobot_k/100,
                        'tipe': 1 if tipe_k.startswith("Benefit") else 0
                    }
                    st.session_state.data[nama_k] = 0.0
                    st.success(f"'{nama_k}' ditambahkan! Isi nilainya di tabel Data Laptop.")
                    st.rerun()

        # ── HAPUS ──
        else:
            if len(st.session_state.bobot) <= 1:
                st.warning("Minimal harus ada 1 kriteria.")
            else:
                hapus_k = st.selectbox("Pilih kriteria", list(st.session_state.bobot.keys()))
                if st.button("Hapus Kriteria", use_container_width=True, key="btn_hapus_kriteria"):
                    del st.session_state.bobot[hapus_k]
                    if hapus_k in st.session_state.data.columns:
                        st.session_state.data = st.session_state.data.drop(columns=[hapus_k])
                    st.success(f"'{hapus_k}' dihapus.")
                    st.rerun()

    with st.expander("Hapus Laptop"):
        if not st.session_state.data.empty:
            hapus = st.selectbox("Pilih laptop yang ingin dihapus", st.session_state.data['Alternatif'])
            if st.button("Hapus Laptop", use_container_width=True, key="btn_hapus_laptop"):
                st.session_state.data = st.session_state.data[
                    st.session_state.data['Alternatif'] != hapus
                ].reset_index(drop=True)
                st.success(f"{hapus} berhasil dihapus.")
                st.rerun()
        else:
            st.info("Belum ada data laptop.")

    with st.expander("Reset ke Data Awal"):
        st.warning("Semua perubahan akan hilang dan data dikembalikan ke kondisi awal.")
        if st.button("Reset Sekarang", use_container_width=True):
            st.session_state.data = pd.DataFrame({
                'Alternatif': ['ASUS ROG Zephyrus', 'Lenovo Legion 5', 'MacBook Pro M2', 'Acer Swift 3', 'MSI Modern 14'],
                'RAM (GB)': [32, 16, 16, 8, 16],
                'SSD (GB)': [1024, 512, 512, 256, 512],
                'Skor Prosesor': [9, 7, 8, 5, 8],
                'Harga (Juta Rp)': [25, 18, 24, 10, 15],
                'Berat (kg)': [1.9, 2.3, 1.6, 1.4, 1.3]
            })
            st.session_state.bobot = {
                'RAM (GB)':          {'bobot': 0.30, 'tipe': 1},
                'SSD (GB)':          {'bobot': 0.25, 'tipe': 1},
                'Skor Prosesor':     {'bobot': 0.20, 'tipe': 1},
                'Harga (Juta Rp)':   {'bobot': 0.15, 'tipe': 0},
                'Berat (kg)':        {'bobot': 0.10, 'tipe': 0}
            }
            st.rerun()

#  HEADER 
st.markdown("""
<div class="page-header">
    <div class="page-title">Dashboard Pemilihan Laptop</div>
    <div class="page-desc">Bandingkan dan temukan laptop terbaik berdasarkan kebutuhan Anda menggunakan metode SAW dan TOPSIS.</div>
</div>
""", unsafe_allow_html=True)


# HITUNG HASIL 
if not st.session_state.data.empty:
    hasil_saw   = hitung_saw(st.session_state.data, st.session_state.bobot)
    hasil_fuzzy = hitung_fuzzy(st.session_state.data, st.session_state.bobot)
else:
    hasil_saw   = pd.DataFrame(columns=['Alternatif', 'Skor_SAW'])
    hasil_fuzzy = pd.DataFrame(columns=['Alternatif', 'Skor_Fuzzy'])


#  STAT CARDS 
c1, c2, c3, c4 = st.columns(4)

rekomendasi_utama = hasil_saw.iloc[0]['Alternatif'] if not hasil_saw.empty else "-"
jumlah_laptop     = len(st.session_state.data)
skor_tertinggi    = f"{hasil_saw.iloc[0]['Skor_SAW']:.3f}" if not hasil_saw.empty else "-"
metode_sepakat    = "Ya" if (not hasil_saw.empty and not hasil_fuzzy.empty and
                              hasil_saw.iloc[0]['Alternatif'] == hasil_fuzzy.iloc[0]['Alternatif']) else "Tidak"

with c1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">Rekomendasi Utama</div>
        <div class="stat-value" style="font-size:1.1rem;">{rekomendasi_utama}</div>
        <div class="stat-sub">Berdasarkan metode SAW</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">Total Laptop</div>
        <div class="stat-value">{jumlah_laptop}</div>
        <div class="stat-sub">Laptop yang dibandingkan</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">Skor Tertinggi</div>
        <div class="stat-value">{skor_tertinggi}</div>
        <div class="stat-sub">Skor SAW terbaik (maks. 1.000)</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    warna_sepakat = "#166534" if metode_sepakat == "Ya" else "#991b1b"
    bg_sepakat    = "#dcfce7" if metode_sepakat == "Ya" else "#fee2e2"
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">Kedua Metode Sepakat</div>
        <div class="stat-value" style="font-size:1.1rem; color:{warna_sepakat}; background:{bg_sepakat}; display:inline-block; padding: 2px 14px; border-radius: 20px;">{metode_sepakat}</div>
        <div class="stat-sub">SAW vs Fuzzy MCDM</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)


#  KRITERIA CARDS 
st.markdown("**Bobot Kriteria yang Digunakan**")
st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

nama_display = {
    'RAM (GB)':          'RAM',
    'SSD (GB)':          'SSD',
    'Skor Prosesor':     'Prosesor',
    'Harga (Juta Rp)':   'Harga',
    'Berat (kg)':        'Berat'
}
kol_krit = st.columns(len(st.session_state.bobot))
for i, (k, v) in enumerate(st.session_state.bobot.items()):
    tipe_label = "Semakin tinggi lebih baik" if v['tipe'] == 1 else "Semakin rendah lebih baik"
    badge_class = "badge-benefit" if v['tipe'] == 1 else "badge-cost"
    badge_text  = "Makin besar makin baik" if v['tipe'] == 1 else "Makin kecil makin baik"
    with kol_krit[i]:
        st.markdown(f"""
        <div class="kriteria-card">
            <div class="kriteria-nama">{nama_display.get(k, k)}</div>
            <div class="kriteria-bobot">{int(v['bobot']*100)}%</div>
            <span class="badge {badge_class}">{badge_text}</span>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)


#  TABS 
tab1, tab2, tab3, tab4 = st.tabs(["Data Laptop", "Metode SAW", "Metode Fuzzy MCDM", "Perbandingan"])

# ----- TAB 1: DATA -----
with tab1:
    st.subheader("Daftar Laptop")
    st.caption("Data ini digunakan sebagai bahan perhitungan. Anda bisa menambah atau menghapus laptop lewat menu di sebelah kiri.")
    st.dataframe(st.session_state.data, use_container_width=True, hide_index=True)

    st.markdown("**Panduan Skor Prosesor**")
    panduan = pd.DataFrame({
        'Tipe Prosesor': ['Intel Core i3', 'Intel Core i5', 'AMD Ryzen 5', 'Intel Core i7', 'AMD Ryzen 7', 'Apple M2', 'Intel Core i9', 'Apple M3'],
        'Skor':          [3, 5, 6, 7, 8, 8, 9, 9],
        'Keterangan':    ['Dasar', 'Menengah', 'Menengah', 'Tinggi', 'Tinggi', 'Tinggi', 'Sangat Tinggi', 'Sangat Tinggi']
    })
    st.dataframe(panduan, use_container_width=True, hide_index=True)

# ----- TAB 2: SAW -----
with tab2:
    st.subheader("Hasil Metode SAW")
    st.caption("SAW (Simple Additive Weighting) menghitung skor dengan menjumlahkan nilai setiap kriteria yang sudah dinormalisasi dan dikalikan bobotnya. Skor mendekati 1.000 berarti lebih baik.")
    if not hasil_saw.empty:
        col_tabel, col_rekom = st.columns([2, 1])
        with col_tabel:
            st.dataframe(hasil_saw, use_container_width=True, hide_index=True)
        with col_rekom:
            best = hasil_saw.iloc[0]
            st.markdown(f"""
            <div class="rekomendasi-card">
                <div class="rekomendasi-label">Rekomendasi SAW</div>
                <div class="rekomendasi-nama">{best['Alternatif']}</div>
                <div class="rekomendasi-skor">{best['Skor_SAW']:.3f}</div>
                <div class="rekomendasi-skor-label">Skor (0 – 1)</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Belum ada data. Tambahkan laptop melalui menu di sebelah kiri.")

# ----- TAB 3: FUZZY MCDM -----
with tab3:
    st.subheader("Hasil Metode Fuzzy MCDM")
    st.caption("Fuzzy MCDM menggunakan normalisasi Linear Max Min. Setiap nilai kriteria dikonversi ke skala 0–1 relatif terhadap nilai terbaik dan terburuk di antara semua alternatif, lalu dikalikan bobotnya. Skor mendekati 1.000 berarti lebih baik.")
    if not hasil_fuzzy.empty:
        col_tabel, col_rekom = st.columns([2, 1])
        with col_tabel:
            st.dataframe(hasil_fuzzy, use_container_width=True, hide_index=True)
        with col_rekom:
            best = hasil_fuzzy.iloc[0]
            st.markdown(f"""
            <div class="rekomendasi-card">
                <div class="rekomendasi-label">Rekomendasi Fuzzy MCDM</div>
                <div class="rekomendasi-nama">{best['Alternatif']}</div>
                <div class="rekomendasi-skor">{best['Skor_Fuzzy']:.3f}</div>
                <div class="rekomendasi-skor-label">Skor (0 – 1)</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Belum ada data. Tambahkan laptop melalui menu di sebelah kiri.")

# ----- TAB 4: PERBANDINGAN -----
with tab4:
    st.subheader("Perbandingan SAW vs Fuzzy MCDM")
    st.caption("Tabel di bawah menunjukkan peringkat masing-masing laptop menurut SAW dan Fuzzy MCDM. Semakin kecil angka peringkat, semakin baik.")
    if not hasil_saw.empty and not hasil_fuzzy.empty:
        gabung = pd.merge(hasil_saw, hasil_fuzzy, on='Alternatif')
        gabung['Peringkat SAW']   = gabung['Skor_SAW'].rank(ascending=False).astype(int)
        gabung['Peringkat Fuzzy'] = gabung['Skor_Fuzzy'].rank(ascending=False).astype(int)
        gabung['Rata-rata Peringkat'] = ((gabung['Peringkat SAW'] + gabung['Peringkat Fuzzy']) / 2).round(1)
        gabung = gabung.sort_values('Rata-rata Peringkat')[
            ['Alternatif', 'Peringkat SAW', 'Peringkat Fuzzy', 'Rata-rata Peringkat', 'Skor_SAW', 'Skor_Fuzzy']
        ]
        st.dataframe(gabung, use_container_width=True, hide_index=True)

        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
        st.markdown("**Grafik Perbandingan Skor**")
        chart_data = gabung.set_index('Alternatif')[['Skor_SAW', 'Skor_Fuzzy']]
        st.bar_chart(chart_data, height=400)

        st.markdown("<hr>", unsafe_allow_html=True)
        saw_winner   = hasil_saw.iloc[0]['Alternatif']
        fuzzy_winner = hasil_fuzzy.iloc[0]['Alternatif']
        if saw_winner == fuzzy_winner:
            st.success(f"Kedua metode sepakat: laptop terbaik adalah **{saw_winner}**.")
        else:
            st.warning(f"Kedua metode berbeda pendapat. SAW merekomendasikan **{saw_winner}**, sementara Fuzzy MCDM merekomendasikan **{fuzzy_winner}**. Pertimbangkan keduanya sesuai prioritas Anda.")
    else:
        st.info("Belum ada data untuk dibandingkan.")
