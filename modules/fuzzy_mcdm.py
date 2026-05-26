# modules/fuzzy_mcdm.py
# Fuzzy Multi-Criteria Decision Making
# Normalisasi: Linear Max Min

import pandas as pd
import numpy as np


def hitung_fuzzy(df, bobot):
    """
    Fuzzy MCDM dengan normalisasi Linear Max Min.

    Rumus:
    - Benefit : r_ij = (S_ij - min(S_j)) / (max(S_j) - min(S_j))
    - Cost    : r_ij = (max(S_j) - S_ij) / (max(S_j) - min(S_j))

    Setelah dinormalisasi, skor akhir dihitung sama seperti SAW:
    V_i = sum(w_j * r_ij)
    """
    df2 = df.copy()
    skor = pd.Series(0.0, index=df2.index)

    for kolom, info in bobot.items():
        s_max = df2[kolom].max()
        s_min = df2[kolom].min()
        rentang = s_max - s_min

        # Hindari pembagian nol kalau semua nilai sama
        if rentang == 0:
            norm = pd.Series(1.0, index=df2.index)
        else:
            if info['tipe'] == 1:  # Benefit: makin besar makin baik
                norm = (df2[kolom] - s_min) / rentang
            else:                  # Cost: makin kecil makin baik
                norm = (s_max - df2[kolom]) / rentang

        skor += norm * info['bobot']

    hasil = pd.DataFrame({
        'Alternatif':   df2['Alternatif'],
        'Skor_Fuzzy':   skor.round(4)
    })

    return hasil.sort_values('Skor_Fuzzy', ascending=False).reset_index(drop=True)
