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
import json

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
image = Image.open('oildrop.jpg')
st.sidebar.image(image)

st.sidebar.title("Pengaturan")
left_col, mid_col, right_col = st.columns(3)

## User inputs on the control panel
st.sidebar.subheader("Pengaturan konfigurasi tampilan")
list_negara = df['kode_negara'].unique()
list_tahun = df['tahun'].unique()
negara = st.sidebar.selectbox("Pilih negara", list_negara)
tahun = st.sidebar.selectbox("Pilih tahun", list_tahun)
n_tampil = st.sidebar.number_input("Jumlah data yang ditampilkan", min_value=1, max_value=None, value=10)
############### sidebar ###############

############### upper left column ###############

left_col.subheader("Tabel representasi data")
left_col.dataframe(df.head(n_tampil))

############### upper left column ###############

############### upper middle column ###############
# Bagian a.
mid_col.subheader("Jumlah Produksi Minyak Tiap Tahun")
datanegara = df[df['kode_negara']==negara]
fig, ax = plt.subplots()
ax.plot(datanegara['tahun'], datanegara['produksi'], 'go--', linewidth=2, markersize=12)
ax.set_xlabel("Tahun", fontsize=12)
ax.set_ylabel("Jumlah produksi pada tiap tahun", fontsize=12)

mid_col.pyplot(fig)
############### upper middle column ###############

############### upper right column ###############
# Bagian b. 
df_b = df[df['tahun']==tahun]
df_b_sorted = df_b.sort_values(by=['produksi'], ascending=False).reset_index(drop=True)[:n_tampil]
df_b_sorted.index = df_b_sorted.index + 1

cmap_name = 'tab20c'
cmap = cm.get_cmap(cmap_name)
colors = cmap.colors[:len(df_b_sorted['kode_negara'])]

fig, ax = plt.subplots()
ax.bar(df_b_sorted['kode_negara'],df_b_sorted['produksi'] , color=colors)
ax.set_xticklabels(df_b_sorted['kode_negara'], rotation=90)
ax.set_xlabel("Negara", fontsize=12)
ax.set_ylabel("Jumlah produksi pada tahun %inputjumlahnegara", fontsize=12)

right_col.pyplot(fig)
############### upper right column ###############

############### lower left column ###############
# Bagian c.
df_c = df.groupby(by=['kode_negara'])['produksi'].sum().reset_index(name="total_produksi")
df_c_sorted = df_c.sort_values(by=['total_produksi'],ascending=False).reset_index(drop=True)[:n_tampil]

colors = cmap.colors[:len(df_b_sorted['kode_negara'])]

fig, ax = plt.subplots()
ax.bar(df_c_sorted['kode_negara'],df_c_sorted['total_produksi'] , color=colors)
ax.set_xticklabels(df_c_sorted['kode_negara'], rotation=90)
ax.set_xlabel("Negara", fontsize=12)
ax.set_ylabel("Total Produksi Keseluruhan Tahun", fontsize=12)

right_col.pyplot(fig)
############### lower left column ###############

############### lower middle column ###############
mid_col.subheader("List Negara")
mid_col.markdown(negara)

############### lower middle column ###############

############### lower right column ###############


############### lower right column ###############