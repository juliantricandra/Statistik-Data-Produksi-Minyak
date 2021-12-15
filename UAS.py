# Nama : Julian Tri Candra Aminudin Hasan
# NIM  : 12220099
# UAS

"""
Aplikasi Streamlit untuk menggambarkan statistik data produksi minyak tiap negara
"""
########### Requirement ###########
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
import streamlit as st
from PIL import Image
########### Requirement ###########

############### Dataset #############
# Membuka file csv
filepath = 'produksi_minyak_mentah.csv'
df = pd.read_csv(filepath)

# Membuka data json
with open("kode_negara_lengkap.json") as f:
    data = json.load(f)

# Konversi kode negara ke nama negara
konversi = {item['alpha-3'] : item['name'] for item in data}
df.loc[:, 'kode_negara'] = df['kode_negara'].map(konversi)

# Mengexclude data NaN
df.dropna(subset=["kode_negara"], inplace=True)

############### Dataset #############

############### title ###############
st.set_page_config(layout="wide")  # this needs to be the first Streamlit command called
st.title("Statistik Produksi Minyak di Berbagai Negara")
st.markdown("*Sumber data berasal dari [Jakarta Open Data](https://data.jakarta.go.id/dataset/data-jumlah-penumpang-trans-jakarta-tahun-2019-kpi)*")
############### title ###############)

############### sidebar ###############
image = Image.open('oildrop.png')
st.sidebar.image(image)

st.sidebar.title("Pengaturan")
left_col, mid_col, right_col = st.columns(3)

## User inputs on the control panel
st.sidebar.subheader("Pengaturan konfigurasi tampilan")
list_negara = df['kode_negara'].unique()
negara = st.sidebar.selectbox("Pilih negara", list_negara)

n_tampil = st.sidebar.number_input("Jumlah data yang ditampilkan", min_value=1, max_value=None, value=10)
############### sidebar ###############

############### upper left column ###############

left_col.subheader("Tabel representasi data")
left_col.dataframe(df.head(n_tampil))

############### upper left column ###############

############### upper middle column ###############
# Bagian a.
mid_col.subheader("Grafik jumlah produksi minyak mentah terhadap waktu (tahun) dari suatu negara")
datanegara = df[df['kode_negara']==negara]
plt.plot(datanegara['tahun'], datanegara['produksi'], 'go--', linewidth=2, markersize=12)
plt.show()

############### upper middle column ###############

############### upper right column ###############


############### upper right column ###############

############### lower left column ###############


############### lower left column ###############

############### lower middle column ###############


############### lower middle column ###############

############### lower right column ###############


############### lower right column ###############