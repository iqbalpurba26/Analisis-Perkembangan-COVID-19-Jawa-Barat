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

total_kasus = daily_case_cov_df['kasus'].sum()
meninggal = daily_die_cov_df['meninggal'].sum()
sembuh = daily_heald_cov_df['sembuh'].sum()


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
    st.metric("Sembuh ", value="{:,}".format(sembuh))
with col3:
    st.metric("Meninggal", value="{:,}".format(meninggal))
st.divider()

st.markdown("<br>", unsafe_allow_html=True)

st.subheader('PERKEMBANGAN KASUS BARU, SEMBUH, DAN MENINGGAL')

plt.figure(figsize=(14, 5))
plt.plot(daily_case_cov_df['tanggal'],
         daily_case_cov_df['kasus'], color='red')
plt.xlabel('Tanggal')
plt.ylabel('kasus')
plt.title('Penambahan Kasus Baru Setiap Hari')
plt.grid()
st.pyplot(plt)

st.markdown("<br>", unsafe_allow_html=True)

plt.figure(figsize=(14, 5))
plt.plot(daily_heald_cov_df['tanggal'],
         daily_heald_cov_df['sembuh'], color='blue')
plt.xlabel('Tanggal')
plt.ylabel('kasus')
plt.title('Penambahan Kasus Sembuh Setiap Hari')
plt.grid()
st.pyplot(plt)

st.markdown("<br>", unsafe_allow_html=True)

plt.figure(figsize=(14, 5))
plt.plot(daily_die_cov_df['tanggal'],
         daily_die_cov_df['meninggal'], color='black')
plt.xlabel('Tanggal')
plt.ylabel('kasus')
plt.title('Penambahan Kasus Kematian Setiap Hari')
plt.grid()
st.pyplot(plt)

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
