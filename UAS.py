# Nama : Julian Tri Candra Aminudin Hasan
# NIM  : 12220099
# UAS

"""
Aplikasi Streamlit untuk menggambarkan statistik data produksi minyak tiap negara
"""
########### Requirement ###########

import pandas as pd
import streamlit as st
from PIL import Image
import json
import plotly.express as px
import altair as alt

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

# sub region, region data, dan kode alpha-3 data
subregion = {item['name'] : item['sub-region'] for item in data}
region = {item['name'] : item['region'] for item in data}
alphanegara = {item['name'] : item['alpha-3'] for item in data}

# variabel list untuk menyimpan subregion,region,dan kode negara(alpha-3)
listsubregion = []
listregion = []
listalphanegara = []

for country in df['kode_negara'] :
    for k,v in subregion.items():
        if country == k :
            listsubregion.append(v)
        else :
            continue

for country in df['kode_negara'] :
    for k,v in region.items():
        if country == k :
            listregion.append(v)
        else :
            continue

for country in df['kode_negara'] :
    for k,v in alphanegara.items():
        if country == k :
            listalphanegara.append(v)
        else :
            continue

# memasukkan region,sub-region,dan kode negara ke dataframe
df['region'] = listregion
df['sub_region'] = listsubregion
df['alpha3_negara'] = listalphanegara
############### Dataset #############

############### title ###############
st.set_page_config(layout="wide")  # this needs to be the first Streamlit command called
st.title("Statistik Produksi Minyak Mentah di Berbagai Negara")
st.markdown("Nama : Julian Tri Candra Aminudin Hasan  \nNIM : 12220099")
############### title ###############)

############### sidebar ###############
image = Image.open('perminyakan.png')
st.sidebar.image(image)
st.sidebar.title("Pengaturan")

## User inputs on the control panel
st.sidebar.subheader("Pengaturan konfigurasi tampilan")
list_negara = list(df['kode_negara'].unique())
list_tahun = df['tahun'].unique()
negara = st.sidebar.selectbox("Pilih negara", list_negara)
tahun = st.sidebar.slider('Pilih tahun', min_value=1971, max_value=2015)
n_tampil = st.sidebar.number_input("Jumlah data yang ditampilkan", min_value=1, max_value=None, value=10)
############### sidebar ############### 

############ tampilan data ############

# data produksi minyak mentah original
df_old = pd.read_csv(filepath)
st.subheader("Tabel representasi data")
st.dataframe(df_old.head(n_tampil))

############ tampilan data ############

############ container data visualization ############
# Bagian a.
with st.container() :
    st.subheader("**_Data Visualization_**")
    df_new = pd.read_csv(filepath)
    df_new.loc[:, 'kode_negara'] = df_new['kode_negara'].map(konversi)
    df_new = df.rename(columns={'kode_negara': 'nama_negara'})
    df_old = df_old.join(df_new['nama_negara'])

    fig = px.choropleth(
        df_old, 
        locations='kode_negara', 
        color='produksi', 
        range_color = [0,523000],
        hover_name='nama_negara',
        animation_frame='tahun')
    fig.show()
    with st.expander("Gambaran jumlah produksi minyak mentah dunia per tahun",expanded=False) :
        st.plotly_chart(fig,use_container_width=True)

    datanegara = df[df['kode_negara']==negara]
    df_linechart = alt.Chart(datanegara).mark_line().encode(tooltip=['produksi','tahun'],
    x=alt.X('tahun', axis=alt.Axis(title='Tahun')),
    y=alt.Y('produksi', axis=alt.Axis(title='Jumlah Produksi')))
    with st.expander("Grafik jumlah produksi minyak mentah {} per tahun".format(negara),expanded=False) :
        st.altair_chart(df_linechart,use_container_width=True)
        st.dataframe(datanegara)
    
    # Bagian b. 
    df_b = df[df['tahun']==tahun]
    df_b_sorted = df_b.sort_values(by=['produksi'], ascending=False).reset_index(drop=True)[:n_tampil]
    df_b_sorted.index = df_b_sorted.index + 1

    df_barchart = alt.Chart(df_b_sorted).mark_bar().encode(tooltip=['produksi','tahun','region','sub_region','alpha3_negara'],
    x=alt.X('produksi', axis=alt.Axis(title='Jumlah Produksi')),
    y=alt.Y('kode_negara', axis=alt.Axis(title='Negara'),sort=alt.EncodingSortField(field='produksi', order='descending',op='sum')))
    with st.expander('Grafik {}-besar negara dengan jumlah produksi minyak mentah terbesar pada tahun {}'.format(n_tampil,tahun),expanded=False) :
        st.altair_chart(df_barchart,use_container_width=True)
        st.dataframe(df_b_sorted)

    #Bagian c.
    df_c = df.groupby(['kode_negara','region','sub_region','alpha3_negara'])['produksi'].sum().reset_index(name="total_produksi")
    df_c_sorted = df_c.sort_values(by=['total_produksi'],ascending=False).reset_index(drop=True)[:n_tampil]
    df_barvchart = alt.Chart(df_c_sorted).mark_bar().encode(tooltip=['total_produksi','region','sub_region','alpha3_negara'],
    x=alt.X('kode_negara', axis=alt.Axis(title='Negara'),sort=alt.EncodingSortField(field='total_produksi', order='descending',op='sum')),
    y=alt.Y('total_produksi', axis=alt.Axis(title='Total Produksi')))
    with st.expander("Grafik {}-besar negara dengan jumlah produksi minyak mentah terbesar pada keseluruhan tahun".format(n_tampil),expanded=False) :
        st.altair_chart(df_barvchart,use_container_width=True)
        st.dataframe(df_c_sorted)
    
    # Tambahan : Rata - rata produksi per tahun
    df_e = df.groupby(['kode_negara','region','sub_region','alpha3_negara'])['produksi'].mean().reset_index(name="mean")
    df_e_sorted = df_e.sort_values(by=['mean'],ascending=False).reset_index(drop=True)[:n_tampil]

    df_areachart = alt.Chart(df_e_sorted).mark_area().encode(tooltip=['mean','region','sub_region','alpha3_negara'],
    x=alt.X('kode_negara', axis=alt.Axis(title='Negara'),sort=alt.EncodingSortField(field='mean', order='descending',op='sum')),
    y=alt.Y('mean', axis=alt.Axis(title='Rata - Rata Produksi')))
    with st.expander("Grafik {}-besar negara dengan rata - rata produksi minyak mentah terbesar per tahun ".format(n_tampil),expanded=False) :
        st.altair_chart(df_areachart,use_container_width=True)
        st.dataframe(df_e_sorted)

############ container data visualization ############


# Bagian d.
df_d = df[df['tahun']==tahun]
df_d_nozero = df_d.drop(df_d.index[df_d['produksi'] == 0])
df_c_nozero = df_c.drop(df_c.index[df_c['total_produksi'] == 0])

# Dataframe - dataframe yang dibutuhkan
df_d_maxall = df_c_sorted[:1]  # jumlah produksi keseluruhan tahun terbesar
df_d_max = df_d[df_d['produksi']==df_d['produksi'].max()] # produksi terbesar pada tahun T
df_d_min = df_d_nozero[df_d_nozero['produksi']==df_d_nozero['produksi'].min()] # produksi terkecil pada tahun T
df_d_minall = df_c_nozero[df_c_nozero['total_produksi']==df_c_nozero['total_produksi'].min()] # produksi terkecil pada keseluruhan tahun tidak termasuk nol
df_d_minzeroall = df_c.drop(df_c.index[df_c['total_produksi'] != 0]).reset_index(drop=True) # produksi nol pada keseluruhan tahun
df_d_min_zero = df_d[df_d['produksi']==df_d['produksi'].min()].reset_index(drop=True) # produksi nol pada tahun T

# Rename column
df_d_minzeroall_new = df_d_minzeroall.rename(columns={"kode_negara" : "nama_negara"})
df_d_minzeroall_new.index = df_d_minzeroall_new.index + 1
df_d_min_zero_new =  df_d_min_zero.rename(columns={"kode_negara" : "nama_negara"})
df_d_min_zero_new.index = df_d_min_zero_new.index + 1

############ container summary ############
with st.container() :
    st.subheader("**_Summary_**")
    st.markdown("**Summary Jumlah Produksi Mentah pada Tahun** {}".format(tahun))
    st.write('Jumlah produksi terbesar pada tahun', tahun,':', df_d_max['produksi'].iloc[0],
    '  \n Nama lengkap negara :', df_d_max['kode_negara'].iloc[0],
    '  \n Kode negara :', df_d_max['alpha3_negara'].iloc[0],
    '  \n Region :', df_d_max['region'].iloc[0],
    '  \n Sub-region :',df_d_max['sub_region'].iloc[0],
    '  \n  \n Jumlah produksi terkecil pada tahun',  tahun ,':', df_d_min['produksi'].iloc[0],
    '  \n Nama lengkap negara :', df_d_min['kode_negara'].iloc[0],
    '  \n Kode negara :', df_d_min['alpha3_negara'].iloc[0],
    '  \n Region :', df_d_min['region'].iloc[0],
    '  \n Sub-region :',df_d_min['sub_region'].iloc[0])
    with st.expander("Data jumlah produksi sama dengan nol pada tahun {}".format(tahun), expanded=False) :
        st.dataframe(df_d_min_zero_new)
    st.markdown('  \n **Summary Jumlah Produksi Minyak Mentah pada Keseluruhan Tahun**')
    st.write('Jumlah produksi pada keseluruhan tahun terbesar :', df_d_maxall['total_produksi'].iloc[0],
    '  \n Nama lengkap negara :', df_d_maxall['kode_negara'].iloc[0],
    '  \n Kode negara :', df_d_maxall['alpha3_negara'].iloc[0],
    '  \n Region :', df_d_maxall['region'].iloc[0],
    '  \n Sub-region :',df_d_maxall['sub_region'].iloc[0],'  \n  \n Jumlah produksi pada keseluruhan tahun terkecil :', df_d_minall['total_produksi'].iloc[0],
    '  \n Nama lengkap negara :', df_d_minall['kode_negara'].iloc[0],
    '  \n Kode negara :', df_d_minall['alpha3_negara'].iloc[0],
    '  \n Region :', df_d_minall['region'].iloc[0],
    '  \n Sub-region :',df_d_minall['sub_region'].iloc[0])
    with st.expander("Data jumlah produksi sama dengan nol pada keseluruhan tahun", expanded=False) :
        st.dataframe(df_d_minzeroall_new)
############ container summary ############