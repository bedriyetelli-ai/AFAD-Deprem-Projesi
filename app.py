import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.title("AFAD Deprem Verisi Analiz Panosu")


df = pd.read_csv("deprem.csv")

# Tarih sütununu dönüştür
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)




st.sidebar.header("Filtreler")


min_mag = st.sidebar.slider(
    "Minimum Deprem Büyüklüğü",
    float(df["Magnitude"].min()),
    float(df["Magnitude"].max()),
    3.0,
    0.1
)


yerler = ["Tümü"] + sorted(df["Location"].unique().tolist())
secilen_yer = st.sidebar.selectbox("Yer Seçiniz", yerler)


filtreli_df = df[df["Magnitude"] >= min_mag]

if secilen_yer != "Tümü":
    filtreli_df = filtreli_df[filtreli_df["Location"] == secilen_yer]


yillar = filtreli_df.groupby(filtreli_df["Date"].dt.year).size()


fig, ax = plt.subplots(figsize=(8,5))
ax.plot(yillar.index, yillar.values, marker="o")
ax.set_title("Yıllara Göre Deprem Sayısı")
ax.set_xlabel("Yıl")
ax.set_ylabel("Deprem Sayısı")
ax.grid(True)


st.pyplot(fig)



st.subheader("📋 Filtrelenmiş Deprem Verileri")

st.dataframe(filtreli_df)



csv = filtreli_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Filtrelenmiş Veriyi CSV Olarak İndir",
    data=csv,
    file_name="filtrelenmis_depremler.csv",
    mime="text/csv"
)

if secilen_yer != "Tümü":
    filtreli_df = filtreli_df[filtreli_df["Location"] == secilen_yer]
    

st.subheader("📊 Özet Bilgiler")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Toplam Deprem", len(filtreli_df))

with col2:
    st.metric("En Büyük Deprem", filtreli_df["Magnitude"].max())

with col3:
    st.metric("Ortalama Derinlik", round(filtreli_df["Depth"].mean(), 2))
