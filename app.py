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
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #f8f9fb; }

    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e5e7eb; }
    [data-testid="stSidebar"] * { color: #374151 !important; }
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"],
    [data-testid="stSidebar"] .stTextInput input,
    [data-testid="stSidebar"] .stNumberInput input { background-color: #f9fafb !important; border: 1px solid #e5e7eb !important; color: #111827 !important; }
    [data-baseweb="popover"] li, [data-baseweb="menu"] div { color: #111827 !important; background-color: #ffffff !important; }

    .page-header { margin-bottom: 28px; padding-bottom: 20px; border-bottom: 1px solid #e5e7eb; }
    .page-title { font-size: 3rem !important; font-weight: 800 !important; color: #111827 !important; margin: 0 0 8px 0 !important; line-height: 1.15 !important; letter-spacing: -0.5px !important; }
    .page-desc { font-size: 1rem !important; color: #6b7280 !important; margin: 0 !important; }

    .stat-card { background: #ffffff; border: 1px solid #e5e7eb; border-radius: 12px; padding: 20px 24px; }
    .stat-label { font-size: 0.78rem; font-weight: 600; color: #6b7280; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px; }
    .stat-value { font-size: 1.7rem; font-weight: 700; color: #111827; }
    .stat-sub { font-size: 0.8rem; color: #9ca3af; margin-top: 4px; }

    .kriteria-card { background: #ffffff; border: 1px solid #e5e7eb; border-radius: 10px; padding: 16px; }
    .kriteria-nama { font-size: 0.78rem; font-weight: 600; color: #6b7280; text-transform: uppercase; letter-spacing: 0.04em; }
    .kriteria-bobot { font-size: 1.5rem; font-weight: 700; color: #111827; margin: 4px 0; }
    .badge { display: inline-block; font-size: 0.7rem; font-weight: 600; padding: 2px 10px; border-radius: 20px; }
    .badge-benefit { background: #dcfce7; color: #166534; }
    .badge-cost { background: #fee2e2; color: #991b1b; }

    .rekomendasi-card { background: #111827; border-radius: 12px; padding: 24px; color: white; text-align: center; }
    .rekomendasi-label { font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; color: #9ca3af; margin-bottom: 10px; }
    .rekomendasi-nama { font-size: 1.2rem; font-weight: 700; color: #ffffff; margin-bottom: 6px; }
    .rekomendasi-skor { font-size: 2rem; font-weight: 700; color: #ffffff; }
    .rekomendasi-skor-label { font-size: 0.75rem; color: #6b7280; margin-top: 2px; }

    .stTabs [data-baseweb="tab-list"] { gap: 4px; background: #f3f4f6; border-radius: 8px; padding: 4px; border-bottom: none; }
    .stTabs [data-baseweb="tab"] { border-radius: 6px; padding: 8px 20px; font-size: 0.85rem; font-weight: 500; color: #6b7280 !important; background: transparent; border: none; }
    .stTabs [aria-selected="true"] { background: #ffffff !important; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }
    .stTabs [aria-selected="true"] p, .stTabs [aria-selected="true"] span, .stTabs [aria-selected="true"] div { color: #111827 !important; font-weight: 600; }

    .stButton > button { background-color: #111827; color: #ffffff !important; border: none; border-radius: 8px; padding: 10px 18px; font-size: 0.85rem; font-weight: 500; transition: background 0.2s; }
    .stButton > button:hover { background-color: #1f2937; color: #ffffff !important; }
    .stButton > button * { color: #ffffff !important; }

    h1, h2, h3, h4 { color: #111827 !important; }
    p, li, label { color: #374151 !important; }
    hr { border: none; border-top: 1px solid #e5e7eb; margin: 24px 0; }
    .footer-text { font-size: 0.78rem; color: #9ca3af; text-align: center; padding: 16px 0; }

    /* Header sembunyiin bawaan Streamlit */
    header[data-testid="stHeader"] { display: none !important; }
    .stApp { margin-top: -80px; }
</style>
""", unsafe_allow_html=True)


# ===================== DATA AWAL =====================
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame({
        'Alternatif':      ['ASUS ROG Zephyrus', 'Lenovo Legion 5', 'MacBook Pro M2', 'Acer Swift 3', 'MSI Modern 14'],
        'RAM (GB)':        [32, 16, 16, 8, 16],
        'SSD (GB)':        [1024, 512, 512, 256, 512],
        'Skor Prosesor':   [9, 7, 8, 5, 8],
        'Harga (Juta Rp)': [25, 18, 24, 10, 15],
        'Berat (kg)':      [1.9, 2.3, 1.6, 1.4, 1.3]
    })

if 'bobot' not in st.session_state:
    st.session_state.bobot = {
        'RAM (GB)':          {'bobot': 0.30, 'tipe': 1},
        'SSD (GB)':          {'bobot': 0.25, 'tipe': 1},
        'Skor Prosesor':     {'bobot': 0.20, 'tipe': 1},
        'Harga (Juta Rp)':   {'bobot': 0.15, 'tipe': 0},
        'Berat (kg)':        {'bobot': 0.10, 'tipe': 0}
    }

# Kriteria aktif — default semua aktif
if 'kriteria_aktif' not in st.session_state:
    st.session_state.kriteria_aktif = list(st.session_state.bobot.keys())


def get_bobot_aktif():
    """Ambil hanya bobot dari kriteria yang sedang aktif."""
    return {k: v for k, v in st.session_state.bobot.items()
            if k in st.session_state.kriteria_aktif}


# ===================== SIDEBAR =====================
with st.sidebar:
    st.markdown("""
    <div style="padding: 8px 4px 20px;">
        <div style="font-size: 1.3rem; font-weight: 700; color: #111827;">SPK Laptop</div>
        <div style="font-size: 0.9rem; color: #9ca3af; margin-top: 3px;">Sistem Pendukung Keputusan</div>
    </div>
    <hr style="margin: 0 0 20px 0; border-top: 1px solid #e5e7eb;">
    """, unsafe_allow_html=True)

    # ── PILIH KRITERIA AKTIF ──────────────────────────────
    with st.expander("Pilih Kriteria yang Digunakan"):
        st.caption("Centang kriteria yang ingin diikutkan dalam perhitungan.")
        semua_kriteria = list(st.session_state.bobot.keys())
        pilihan = []
        for k in semua_kriteria:
            checked = k in st.session_state.kriteria_aktif
            if st.checkbox(k, value=checked, key=f"chk_{k}"):
                pilihan.append(k)

        if len(pilihan) < 2:
            st.error("Pilih minimal 2 kriteria.")
        else:
            total_bobot = sum(
                st.session_state.bobot[k]['bobot'] for k in pilihan
            )
            if abs(total_bobot - 1.0) > 0.001:
                st.warning(f"Total bobot kriteria terpilih: {total_bobot*100:.0f}% (harus 100%). Sesuaikan bobot dulu.")
            else:
                st.success(f"{len(pilihan)} kriteria aktif — total bobot 100%.")

            if st.button("Terapkan Pilihan", use_container_width=True):
                if len(pilihan) < 2:
                    st.error("Minimal 2 kriteria.")
                else:
                    st.session_state.kriteria_aktif = pilihan
                    st.success("Kriteria aktif diperbarui.")
                    st.rerun()

    # ── TAMBAH LAPTOP BARU ───────────────────────────────
    with st.expander("Tambah Laptop Baru"):
        nama = st.text_input("Nama Laptop", placeholder="Contoh: Dell XPS 15")
        kolom_kriteria = [k for k in st.session_state.bobot.keys()]
        nilai_input = {}
        for k in kolom_kriteria:
            tipe = st.session_state.bobot[k]['tipe']
            label_tipe = "(benefit)" if tipe == 1 else "(cost)"
            nilai_input[k] = st.number_input(
                f"{k} {label_tipe}",
                min_value=0.0,
                value=0.0,
                step=1.0,
                key=f"input_laptop_{k}"
            )

        if st.button("Simpan Laptop", use_container_width=True):
            if nama.strip():
                baru = {'Alternatif': nama.strip()}
                baru.update(nilai_input)
                st.session_state.data = pd.concat(
                    [st.session_state.data, pd.DataFrame([baru])],
                    ignore_index=True
                )
                # Isi kolom yang belum ada dengan 0
                for k in st.session_state.bobot.keys():
                    if k not in st.session_state.data.columns:
                        st.session_state.data[k] = 0.0
                st.success(f"{nama} berhasil ditambahkan.")
                st.rerun()
            else:
                st.error("Nama laptop tidak boleh kosong.")

    # ── ATUR BOBOT KRITERIA ──────────────────────────────
    with st.expander("Atur Bobot Kriteria"):
        st.caption("Ketik bobot untuk masing-masing kriteria. Total harus 100%.")
        bobot_baru = {}
        inputs = {}
        for k, v in st.session_state.bobot.items():
            val = st.number_input(
                f"{k} (%)",
                min_value=0, max_value=100,
                value=int(v['bobot'] * 100),
                step=1,
                key=f"bobot_input_{k}"
            )
            inputs[k] = val
            bobot_baru[k] = {'bobot': val / 100, 'tipe': v['tipe']}

        total = sum(inputs.values())
        sisa  = 100 - total
        if total == 100:
            st.success(f"Total: {total}% — siap disimpan.")
        elif total < 100:
            st.info(f"Total: {total}% — masih kurang {sisa}% lagi.")
        else:
            st.error(f"Total: {total}% — kelebihan {abs(sisa)}%, kurangi salah satu.")

        if total == 100:
            if st.button("Simpan Bobot", use_container_width=True):
                st.session_state.bobot = bobot_baru
                st.success("Bobot berhasil disimpan.")
                st.rerun()

    # ── TAMBAH KRITERIA BARU ─────────────────────────────
    with st.expander("Tambah Kriteria Baru"):
        st.caption("Tambah kriteria selain yang sudah ada.")
        nama_kriteria = st.text_input("Nama kriteria", placeholder="Contoh: Kapasitas Baterai (Wh)", key="nama_kriteria_baru")
        tipe_kriteria = st.radio(
            "Tipe kriteria",
            options=["Benefit (makin besar makin baik)", "Cost (makin kecil makin baik)"],
            key="tipe_kriteria_baru"
        )
        bobot_kriteria = st.number_input("Bobot awal (%)", min_value=0, max_value=100, value=10, step=1, key="bobot_kriteria_baru")
        nilai_default  = st.number_input("Nilai default untuk laptop lama", min_value=0.0, value=0.0, step=1.0, key="nilai_default_baru")

        if st.button("Tambah Kriteria", use_container_width=True):
            if not nama_kriteria.strip():
                st.error("Nama kriteria tidak boleh kosong.")
            elif nama_kriteria.strip() in st.session_state.bobot:
                st.error("Kriteria dengan nama ini sudah ada.")
            else:
                tipe_val = 1 if "Benefit" in tipe_kriteria else 0
                k_baru   = nama_kriteria.strip()
                st.session_state.bobot[k_baru] = {'bobot': bobot_kriteria / 100, 'tipe': tipe_val}
                st.session_state.data[k_baru]  = nilai_default
                st.session_state.kriteria_aktif.append(k_baru)
                st.success(f"Kriteria '{k_baru}' berhasil ditambahkan. Jangan lupa sesuaikan total bobot ke 100%.")
                st.rerun()

    # ── HAPUS KRITERIA ───────────────────────────────────
    with st.expander("Hapus Kriteria"):
        if len(st.session_state.bobot) <= 2:
            st.info("Minimal harus ada 2 kriteria, tidak bisa dihapus lagi.")
        else:
            hapus_kriteria = st.selectbox(
                "Pilih kriteria yang ingin dihapus",
                list(st.session_state.bobot.keys()),
                key="hapus_kriteria_select"
            )
            st.warning(f"Kolom '{hapus_kriteria}' akan dihapus dari semua data laptop.")
            if st.button("Hapus Kriteria", use_container_width=True, key="btn_hapus_kriteria"):
                del st.session_state.bobot[hapus_kriteria]
                if hapus_kriteria in st.session_state.data.columns:
                    st.session_state.data.drop(columns=[hapus_kriteria], inplace=True)
                if hapus_kriteria in st.session_state.kriteria_aktif:
                    st.session_state.kriteria_aktif.remove(hapus_kriteria)
                st.success(f"Kriteria '{hapus_kriteria}' berhasil dihapus.")
                st.rerun()

    # ── HAPUS LAPTOP ─────────────────────────────────────
    with st.expander("Hapus Laptop"):
        if not st.session_state.data.empty:
            hapus = st.selectbox("Pilih laptop yang ingin dihapus", st.session_state.data['Alternatif'])
            if st.button("Hapus", use_container_width=True):
                st.session_state.data = st.session_state.data[
                    st.session_state.data['Alternatif'] != hapus
                ].reset_index(drop=True)
                st.success(f"{hapus} berhasil dihapus.")
                st.rerun()
        else:
            st.info("Belum ada data laptop.")

    # ── RESET ─────────────────────────────────────────────
    with st.expander("Reset ke Data Awal"):
        st.warning("Semua perubahan akan hilang dan data dikembalikan ke kondisi awal.")
        if st.button("Reset Sekarang", use_container_width=True):
            for key in ['data', 'bobot', 'kriteria_aktif']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

# ===================== HEADER =====================
st.markdown("""
<div class="page-header">
    <div class="page-title">Dashboard Pemilihan Laptop</div>
    <div class="page-desc">Bandingkan dan temukan laptop terbaik berdasarkan kebutuhan Anda menggunakan metode SAW dan Fuzzy MCDM.</div>
</div>
""", unsafe_allow_html=True)


# ===================== VALIDASI KRITERIA AKTIF =====================
bobot_aktif = get_bobot_aktif()

if len(bobot_aktif) < 2:
    st.error("Pilih minimal 2 kriteria aktif dari menu 'Pilih Kriteria yang Digunakan' di sebelah kiri.")
    st.stop()

total_bobot_aktif = sum(v['bobot'] for v in bobot_aktif.values())
if abs(total_bobot_aktif - 1.0) > 0.001:
    st.warning(
        f"Total bobot kriteria aktif saat ini **{total_bobot_aktif*100:.0f}%** (harus 100%). "
        "Sesuaikan bobot di menu 'Atur Bobot Kriteria' sebelum melihat hasil."
    )
    st.stop()


# ===================== HITUNG HASIL =====================
if not st.session_state.data.empty:
    hasil_saw   = hitung_saw(st.session_state.data, bobot_aktif)
    hasil_fuzzy = hitung_fuzzy(st.session_state.data, bobot_aktif)
else:
    hasil_saw   = pd.DataFrame(columns=['Alternatif', 'Skor_SAW'])
    hasil_fuzzy = pd.DataFrame(columns=['Alternatif', 'Skor_Fuzzy'])


# ===================== STAT CARDS =====================
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
        <div class="stat-label">Kriteria Aktif</div>
        <div class="stat-value">{len(bobot_aktif)}</div>
        <div class="stat-sub">dari {len(st.session_state.bobot)} kriteria tersedia</div>
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


# ===================== KRITERIA CARDS =====================
st.markdown("**Kriteria yang Digunakan dalam Perhitungan**")
st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

kol_krit = st.columns(len(bobot_aktif))
for i, (k, v) in enumerate(bobot_aktif.items()):
    badge_class = "badge-benefit" if v['tipe'] == 1 else "badge-cost"
    badge_text  = "Makin besar makin baik" if v['tipe'] == 1 else "Makin kecil makin baik"
    with kol_krit[i]:
        st.markdown(f"""
        <div class="kriteria-card">
            <div class="kriteria-nama">{k}</div>
            <div class="kriteria-bobot">{int(v['bobot']*100)}%</div>
            <span class="badge {badge_class}">{badge_text}</span>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)


# ===================== TABS =====================
tab1, tab2, tab3, tab4 = st.tabs(["Data Laptop", "Metode SAW", "Metode Fuzzy MCDM", "Perbandingan"])

# ----- TAB 1: DATA -----
with tab1:
    st.subheader("Daftar Laptop")
    st.caption("Data ini digunakan sebagai bahan perhitungan. Anda bisa menambah atau menghapus laptop lewat menu di sebelah kiri.")
    kolom_tampil = ['Alternatif'] + list(st.session_state.bobot.keys())
    kolom_tampil = [c for c in kolom_tampil if c in st.session_state.data.columns]
    st.dataframe(st.session_state.data[kolom_tampil], use_container_width=True, hide_index=True)

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
        st.info("Belum ada data.")

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
        st.info("Belum ada data.")

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
        import plotly.graph_objects as go

        fig = go.Figure(data=[
            go.Bar(name='SAW', x=gabung['Alternatif'], y=gabung['Skor_SAW'],
                   marker_color='#1A73E8', text=gabung['Skor_SAW'].round(3),
                   textposition='outside', textfont=dict(size=11)),
            go.Bar(name='Fuzzy MCDM', x=gabung['Alternatif'], y=gabung['Skor_Fuzzy'],
                   marker_color='#0F3460', text=gabung['Skor_Fuzzy'].round(3),
                   textposition='outside', textfont=dict(size=11)),
        ])
        fig.update_layout(
            barmode='group', height=480,
            plot_bgcolor='#F8F9FA', paper_bgcolor='#FFFFFF',
            margin=dict(t=40, b=60, l=40, r=40),
            yaxis=dict(range=[0, 1.15], gridcolor='#E5E7EB', tickformat='.2f', title=None),
            xaxis=dict(tickangle=-20, title=None),
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='left', x=0),
            bargap=0.25, bargroupgap=0.08,
            font=dict(family='Inter, Arial', size=12, color='#374151'),
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        saw_winner   = hasil_saw.iloc[0]['Alternatif']
        fuzzy_winner = hasil_fuzzy.iloc[0]['Alternatif']
        if saw_winner == fuzzy_winner:
            st.success(f"Kedua metode sepakat: laptop terbaik adalah **{saw_winner}**.")
        else:
            st.warning(f"Kedua metode berbeda pendapat. SAW merekomendasikan **{saw_winner}**, sementara Fuzzy MCDM merekomendasikan **{fuzzy_winner}**.")
    else:
        st.info("Belum ada data untuk dibandingkan.")
