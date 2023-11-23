import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')


st.set_page_config(
    page_title="COVID-19",
    page_icon="gambar/icon.png"
)


def create_case_cov_df(df):
    daily_case_cov_df = df.groupby("tanggal").kasus.sum().reset_index()
    return daily_case_cov_df


def create_heald_cov_df(df):
    daily_heald_cov_df = df.groupby("tanggal").sembuh.sum().reset_index()
    return daily_heald_cov_df


def create_die_cov_df(df):
    daily_die_cov_df = df.groupby("tanggal").meninggal.sum().reset_index()
    return daily_die_cov_df


def create_sum_positive_df(df):
    sum_positive_df = df.groupby("tanggal").akumulasi_kasus.sum().reset_index()
    return sum_positive_df


def create_sum_heald_df(df):
    sum_heald_df = df.groupby("tanggal").akumulasi_sembuh.sum().reset_index()
    return sum_heald_df


def create_sum_die_df(df):
    sum_die_df = df.groupby("tanggal").akumulasi_meninggal.sum().reset_index()
    return sum_die_df


all_df = pd.read_csv('covid19_jabar_clean.csv')
all_df['tanggal'] = pd.to_datetime(all_df['tanggal'])

min_date = all_df["tanggal"].min()
max_date = all_df["tanggal"].max()

with st.sidebar:
    st.image("gambar/virus.png")
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )


start_date_str = start_date.strftime('%Y-%m-%d')
end_date_str = end_date.strftime('%Y-%m-%d')

main_df = all_df[(all_df["tanggal"] >= start_date_str)
                 & (all_df["tanggal"] <= end_date_str)]

main_df = all_df[(all_df["tanggal"] >= str(start_date)) &
                 (all_df["tanggal"] <= str(end_date))]

daily_case_cov_df = create_case_cov_df(main_df)
daily_heald_cov_df = create_heald_cov_df(main_df)
daily_die_cov_df = create_die_cov_df(main_df)
sum_case_df = create_sum_positive_df(main_df)
sum_heald_df = create_sum_heald_df(main_df)
sum_die_df = create_sum_die_df(main_df)


total_kasus = sum_case_df.at[sum_case_df.index[-1], 'akumulasi_kasus']
total_sembuh = sum_heald_df.at[sum_heald_df.index[-1], 'akumulasi_sembuh']
total_meninggal = sum_die_df.at[sum_die_df.index[-1], 'akumulasi_meninggal']

persentase_meninggal = total_meninggal/total_kasus * 100
persentase_sembuh = total_sembuh/total_kasus * 100


st.header('DATA KASUS COVID-19 DI JAWA BARAT :sparkles:')

# Berapa penambahan poitf, sembuh, dan pasien meninggal dalam rentang waktu tertentu?
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Penambahan Kasus Baru", value="{:,}".format(total_kasus))
with col2:
    st.metric("Sembuh ", value="{:,}".format(total_sembuh))
with col3:
    st.metric("Meninggal", value="{:,}".format(total_meninggal))
st.divider()

st.markdown("<br>", unsafe_allow_html=True)


st.write("Kasus pertama kali warga negara Indonesia terinfeksi Corona Virus Disease (COVID-19) terjadi pada 2 Maret 2020. Sejak saat itu, kasus COVID-19 di Indonesia semakin banyak. Mengutip dari CNBC Indonesia, pertambahan kasus baru harian COVID-19 pada September 2020 lalu di wilayah Jawa Barat terpantau mengalami lonjakan setiap harinya.")

st.write("Berikut ini hasil ekplorasi data dan visualisasi data perkembangan kasus COVID-19 di Jawa Barat pada Maret 2020 - April 2022")


st.subheader('PERKEMBANGAN KASUS BARU DI JAWA BARAT')

plt.figure(figsize=(14, 5))
plt.plot(daily_case_cov_df['tanggal'],
         daily_case_cov_df['kasus'], color='red')
plt.xlabel('Tanggal')
plt.ylabel('kasus')
plt.title('Penambahan Kasus Baru Setiap Hari')
plt.grid()
st.pyplot(plt)

index_kasus_tinggi = daily_case_cov_df['kasus'].idxmax()
penambahan_terbanyak_tanggal = daily_case_cov_df.loc[index_kasus_tinggi, 'tanggal'].date(
)
penambahan_terbanyak_total = daily_case_cov_df['kasus'].max()

index_kasus_rendah = daily_case_cov_df['kasus'].idxmin()
tanggal_terendah = daily_case_cov_df.loc[index_kasus_rendah, 'tanggal'].date()
total_rendah = daily_case_cov_df['kasus'].min()

st.write(
    f"Berdasarkan hasil visualisasi data tersebut dapat dilihat perkembangan bagaimana kasus bertambah setiap hari. Total kasus penambahan tertinggi terjadi pada tanggal **{penambahan_terbanyak_tanggal}**, dengan total kasus pertambahan sebesar **{penambahan_terbanyak_total} kasus**. Sedangkan penambahan kasus terendah terjadi pada tanggal **{tanggal_terendah}**, dengan pertambahan sebesar **{total_rendah} kasus**")


st.markdown("<br>", unsafe_allow_html=True)

st.subheader('PERKEMBANGAN KASUS SEMBUH DI JAWA BARAT')

plt.figure(figsize=(14, 5))
plt.plot(daily_heald_cov_df['tanggal'],
         daily_heald_cov_df['sembuh'], color='blue')
plt.xlabel('Tanggal')
plt.ylabel('kasus')
plt.title('Penambahan Kasus Sembuh Setiap Hari')
plt.grid()
st.pyplot(plt)


sembuh_tertinggi = daily_heald_cov_df['sembuh'].max()
index = daily_heald_cov_df['sembuh'].idxmax()
tanggal_sembuh_tertinggi = daily_heald_cov_df.loc[index, 'tanggal'].date()

sembuh_rendah = daily_heald_cov_df['sembuh'].min()
index_rendah = daily_heald_cov_df['sembuh'].idxmin()
tanggal_sembuh_rendah = daily_heald_cov_df.loc[index_rendah, 'tanggal'].date()

st.write(
    f"Grafik diatas menunjukkan perkembangan kasus sembuh harian. Total kasus sembuh tertinggi terjadi pada tanggal**{tanggal_sembuh_tertinggi}** , dengan total kasus pertambahan sebesar **{sembuh_tertinggi} kasus**. Sedangkan penambahan kasus sembuh terendah terjadi pada tanggal **{tanggal_sembuh_rendah}**, dengan pertambahan sebesar **{sembuh_rendah} kasus**")


st.markdown("<br>", unsafe_allow_html=True)

st.subheader('PERKEMBANGAN KASUS MENINGGAL DI JAWA BARAT')
plt.figure(figsize=(14, 5))
plt.plot(daily_die_cov_df['tanggal'],
         daily_die_cov_df['meninggal'], color='black')
plt.xlabel('Tanggal')
plt.ylabel('kasus')
plt.title('Penambahan Kasus Kematian Setiap Hari')
plt.grid()
st.pyplot(plt)


meninggal_tertinggi = daily_die_cov_df['meninggal'].max()
index_meninggal = daily_die_cov_df['meninggal'].idxmax()
tanggal_meninggal_tertinggi = daily_die_cov_df.loc[index_meninggal, 'tanggal'].date(
)

meninggal_rendah = daily_die_cov_df['meninggal'].min()
index_meninggal_rendah = daily_die_cov_df['meninggal'].idxmin()
tanggal_meninggal_rendah = daily_die_cov_df.loc[index_rendah, 'tanggal'].date()

st.write(
    f"Grafik diatas menunjukkan perkembangan kasus meninggal harian. Total kasus meninggal tertinggi terjadi pada tanggal **{tanggal_meninggal_tertinggi}** , dengan total kasus pertambahan sebesar **{meninggal_tertinggi} kasus**. Sedangkan penambahan kasus meninggal terendah terjadi pada tanggal **{tanggal_meninggal_rendah}**, dengan pertambahan sebesar **{meninggal_rendah} kasus**")


st.markdown("<br>", unsafe_allow_html=True)

st.subheader('PERBANDINGAN AKUMULASI KASUS BARU, SEMBUH, DAN MENINGGAL')

plt.figure(figsize=(14, 5))
plt.plot(sum_case_df['tanggal'],
         sum_case_df['akumulasi_kasus'], color="red")
plt.xlabel('Tanggal')
plt.ylabel('Akumulasi')
plt.title('Akumulasi Kasus Baru')
plt.grid()
st.pyplot(plt)

st.markdown("<br>", unsafe_allow_html=True)

plt.figure(figsize=(14, 5))
plt.plot(sum_heald_df['tanggal'],
         sum_heald_df['akumulasi_sembuh'], color="blue")
plt.xlabel('Tanggal')
plt.ylabel('Akumulasi')
plt.title('Akumulasi Kasus Sembuh')
plt.grid()
st.pyplot(plt)


st.markdown("<br>", unsafe_allow_html=True)

plt.figure(figsize=(14, 5))
plt.plot(sum_die_df['tanggal'],
         sum_die_df['akumulasi_meninggal'], color="black")
plt.xlabel('Tanggal')
plt.ylabel('Akumulasi')
plt.title('Akumulasi Kasus Meninggal')
plt.grid()
st.pyplot(plt)


st.write(
    f"Perbandingan akumulasi dari penambahan kasus, sembuh, dan meninggal di akhir periode adalah masing- masing sebesar **{total_kasus} kasus, {total_sembuh} kasus, {total_meninggal} kasus**. ")


st.markdown("<br>", unsafe_allow_html=True)

st.subheader("PERBANDINGAN KASUS MENINGGAL DAN SEMBUH")
labels = ['Persentase Meninggal', 'Persentase Sembuh']
x = [persentase_meninggal, persentase_sembuh]
colors = ('#FF0060', '#0766AD')
fig, ax = plt.subplots(figsize=(8, 6))
pie = ax.pie(x, labels=labels, colors=colors, autopct='%1.1f%%',
             startangle=140, textprops={'fontsize': 10, "color": "white"})
for label in pie[1]:
    label.set_color('black')
st.pyplot(fig)
