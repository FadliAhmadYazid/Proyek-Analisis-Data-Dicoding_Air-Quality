import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
from scipy.stats import pearsonr
from scipy.stats.mstats import winsorize

# Judul Dashboard
st.title("Proyek Analisis Data: Air Quality Dataset")
st.markdown("""
- **Nama:** Fadli Ahmad Yazid
- **Email:** fadliahmadyazid2@gmail.com
- **ID Dicoding:** fadli_ahmad_yazid
""")

# Sidebar untuk navigasi
st.sidebar.title("Navigasi")
section = st.sidebar.radio("Pilih Bagian", [
    "Menentukan Pertanyaan Bisnis",
    "Data Wrangling",
    "Exploratory Data Analysis (EDA)",
    "Visualization & Explanatory Analysis",
    "Analisis Lanjutan",
    "Conclusion"
])

# Load Data
def load_data():
    return pd.read_csv('dashboard/PRSA_Data_Combined.csv')

def load_cleaned_data():
    return pd.read_csv('dashboard/PRSA_Data_Cleaned.csv')

data = load_data()
data_cleaned = load_cleaned_data()

if section == "Menentukan Pertanyaan Bisnis":
    st.header("Menentukan Pertanyaan Bisnis")
    st.markdown("""
    1. Bagaimana tren konsentrasi PM2.5 dan PM10 di stasiun Aotizhongxin dari tahun 2013 hingga 2017?
    2. Apakah ada korelasi antara suhu (TEMP) dan konsentrasi O3 (Ozon) di semua stasiun?
    3. Bagaimana distribusi konsentrasi SO2 dan NO2 di setiap stasiun pada tahun 2016?
    4. Apakah Ada Perbedaan Pola Suhu (TEMP) antara Stasiun Gucheng dan Huairou?
    """)

elif section == "Data Wrangling":
    st.header("Data Wrangling")
    
    st.subheader("Gathering Data")
    st.write("Data yang digunakan adalah dataset kualitas udara dari 12 stasiun pemantauan di Beijing.")
    st.write("Berikut adalah 5 baris pertama dari dataset:")
    st.write(data.head())

    st.subheader("Assessing Data")
    
    st.write("Cek Missing Values:")
    st.write(data.isnull().sum())

    st.write("Cek Duplikat:")
    st.write(data.duplicated().sum())

    st.write("Cek Tipe Data:")
    st.write(data.info())

    st.write("Cek Outlier:")
    numerical_columns = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']
    outliers = {}
    for col in numerical_columns:
        Q1 = data[col].quantile(0.25)
        Q3 = data[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers[col] = data[(data[col] < lower_bound) | (data[col] > upper_bound)]
        st.write(f"Jumlah outlier pada {col}: {len(outliers[col])}")

    st.subheader("Cleaning Data")
    
    st.write("Handle Missing Values:")
    st.write("Missing values pada kolom numerik diatasi dengan interpolasi linear.")
    st.write("Missing values pada kolom 'wd' diisi dengan modus.")
    st.write("Cek missing values setelah cleaning:")
    st.write(data_cleaned.isnull().sum())

    st.write("Handle Outlier:")
    st.write("Outlier diatasi menggunakan winsorization.")
    st.image("Images/Boxplot_Sebelum_Winsorization.png", caption="Boxplot Sebelum Winsorization")
    st.image("Images/Boxplot_Setelah_Winsorization.png", caption="Boxplot Setelah Winsorization")

elif section == "Exploratory Data Analysis (EDA)":
    st.header("Exploratory Data Analysis (EDA)")
    
    st.subheader("Analisis Statistik Deskriptif")
    st.write("Statistik deskriptif untuk kolom numerik:")
    numerical_columns = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']
    st.write(data_cleaned[numerical_columns].describe())

    st.subheader("Distribusi Data Numerik")
    st.image("Images/Distribusi_Data_Numerik.png", caption="Distribusi Data Numerik")

    st.subheader("Korelasi Antar Variabel")
    st.image("Images/Heatmap_Korelasi_Antar_Variabel.png", caption="Heatmap Korelasi Antar Variabel")

elif section == "Visualization & Explanatory Analysis":
    st.header("Visualization & Explanatory Analysis")
    
    st.subheader("Pertanyaan 1: Tren Konsentrasi PM2.5 dan PM10 di Stasiun Aotizhongxin")
    st.image("Images/Pertanyaan1.png", caption="Tren Rata-Rata PM2.5 dan PM10 di Stasiun Aotizhongxin (2013-2017)")

    st.subheader("Pertanyaan 2: Korelasi antara Suhu (TEMP) dan Konsentrasi O3 (Ozon)")
    st.image("Images/Pertanyaan2.png", caption="Korelasi antara Suhu dan Konsentrasi O3")

    st.subheader("Pertanyaan 3: Distribusi Konsentrasi SO2 dan NO2 di Setiap Stasiun pada Tahun 2016")
    st.image("Images/Pertanyaan3_SO2.png", caption="Distribusi SO2 di Setiap Stasiun (2016)")
    st.image("Images/Pertanyaan3_NO2.png", caption="Distribusi NO2 di Setiap Stasiun (2016)")

    st.subheader("Pertanyaan 4: Perbedaan Pola Suhu (TEMP) antara Stasiun Gucheng dan Huairou")
    st.image("Images/Pertanyaan4.png", caption="Rata-Rata Suhu Bulanan di Gucheng vs Huairou")

elif section == "Analisis Lanjutan":
    st.header("Analisis Lanjutan")
    st.image("Images/Analisis_Lanjutan.png", caption="Distribusi Rata-Rata PM2.5 di Beijing")

elif section == "Conclusion":
    st.header("Conclusion")
    st.markdown("""
    1. **Tren PM2.5 dan PM10 di Aotizhongxin (2013-2017):** Konsentrasi PM2.5 dan PM10 mengalami tren penurunan dari 2014 hingga 2016, terutama pada 2015-2016 yang mungkin dipengaruhi oleh kebijakan pengendalian polusi udara. Namun, peningkatan kembali pada 2017 menunjukkan bahwa faktor lain, seperti perubahan pola cuaca atau peningkatan aktivitas industri dan transportasi, dapat memengaruhi kualitas udara secara signifikan.

    2. **Korelasi antara Suhu (TEMP) dan O3:** Ditemukan korelasi positif yang cukup kuat antara suhu dan konsentrasi O3, di mana peningkatan suhu cenderung diikuti oleh kenaikan kadar ozon. Hal ini kemungkinan besar disebabkan oleh reaksi fotokimia yang lebih intens pada suhu tinggi. Oleh karena itu, lonjakan suhu selama musim panas dapat memperburuk tingkat ozon dan berdampak pada kualitas udara serta kesehatan masyarakat.

    3. **Distribusi SO2 dan NO2 pada 2016:** Konsentrasi SO2 relatif rendah di semua stasiun, menunjukkan bahwa kebijakan pengurangan emisi sulfur berhasil mengendalikan polusi ini. Sebaliknya, konsentrasi NO2 lebih bervariasi, dengan nilai tinggi di daerah perkotaan seperti Guanyuan, Nongzhanguan, dan Wanliu, yang mungkin disebabkan oleh lalu lintas padat dan aktivitas industri. Sementara itu, daerah pinggiran seperti Dingling dan Huairou memiliki tingkat NO2 yang lebih rendah, menandakan bahwa polusi udara lebih terkonsentrasi di daerah padat penduduk.

    4. **Perbedaan Pola Suhu Gucheng vs Huairou:** Stasiun Gucheng memiliki suhu yang lebih tinggi dibandingkan Huairou hampir sepanjang tahun, yang kemungkinan disebabkan oleh efek urban heat island (UHI). Pola suhu di kedua lokasi tetap serupa, dengan puncak suhu pada bulan Juli-Agustus (~25°C) dan titik terendah pada Desember-Januari (~0°C). Perbedaan ini mencerminkan dampak urbanisasi terhadap suhu lingkungan, di mana daerah dengan lebih banyak area hijau seperti Huairou cenderung lebih sejuk dibandingkan daerah urban seperti Gucheng.

    5. **Analisis Geospasial PM2.5:** Stasiun-stasiun yang berada di pusat kota (latitude 39.8 - 40.1 dan longitude 116.2 - 116.5) menunjukkan tingkat PM2.5 yang lebih tinggi, mencerminkan polusi udara yang lebih parah akibat aktivitas perkotaan seperti transportasi dan industri. Sebaliknya, daerah pinggiran seperti Huairou dan Dingling memiliki tingkat PM2.5 yang lebih rendah, menandakan kualitas udara yang lebih baik. Namun, Shunyi—meskipun berada di pinggiran kota—masih memiliki tingkat polusi yang cukup tinggi, kemungkinan akibat aktivitas industri atau pergerakan massa udara yang membawa polusi dari pusat kota.
    """)