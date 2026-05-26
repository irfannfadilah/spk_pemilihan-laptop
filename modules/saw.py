# modules/saw.py
import pandas as pd

def hitung_saw(df, bobot):
    df_saw = df.copy()
    hasil = pd.DataFrame()
    hasil['Alternatif'] = df_saw['Alternatif']
    
    skor = 0
    for kolom in bobot:
        if bobot[kolom]['tipe'] == 1:
            norm = df_saw[kolom] / df_saw[kolom].max()
        else:
            norm = df_saw[kolom].min() / df_saw[kolom]
        skor += norm * bobot[kolom]['bobot']
    
    hasil['Skor_SAW'] = skor
    return hasil.sort_values('Skor_SAW', ascending=False)
