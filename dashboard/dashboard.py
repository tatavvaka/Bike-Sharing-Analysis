"""Jalankan dari folder proyek: python -m streamlit run dashboard/dashboard.py."""
from pathlib import Path
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent))
from analysis import (DAY_TYPES, TIME_LABELS, TIME_TICKS, DEMAND_LABELS, MONTHS,
                      load_data, filter_data, hourly_profile, time_profile,
                      monthly_profile, demand_profile, csv_bytes, format_number)

ROOT = Path(__file__).resolve().parents[1]
COLORS = {'Kerja': '#0072B2', 'Nonkerja': '#D55E00'}
st.set_page_config(page_title='Bike Sharing | Pola Penyewaan', page_icon='🚲', layout='wide')
plt.rcParams.update({'font.size': 10, 'axes.spines.top': False, 'axes.spines.right': False,
                     'axes.labelcolor': '#334155', 'text.color': '#0F172A',
                     'xtick.color': '#475569', 'ytick.color': '#475569'})
st.markdown('''<style>
 .block-container {max-width:1240px;padding-top:2rem;padding-bottom:2rem;}
 [data-testid="stMetric"] {background:white;border:1px solid #DCE4ED;border-radius:12px;padding:16px;}
 [data-testid="stMetricValue"] {font-size:1.9rem;}
 h1 {letter-spacing:-0.035em;}
 button[data-baseweb="tab"] {font-weight:600;}
</style>''', unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def get_data():
    return load_data(ROOT / 'data')


def show_figure(fig):
    st.pyplot(fig, width='stretch')
    plt.close(fig)


try:
    day, hour, q25, q75 = get_data()
except (FileNotFoundError, ValueError) as exc:
    st.error(f'Dataset belum dapat dimuat: {exc}')
    st.info('Pastikan data/day.csv dan data/hour.csv tersedia dalam folder proyek.')
    st.stop()

min_date, max_date = day['dteday'].min().date(), day['dteday'].max().date()


def reset_filters():
    st.session_state['date_start'] = min_date
    st.session_state['date_end'] = max_date
    st.session_state['day_types'] = DAY_TYPES.copy()
    st.session_state['hour_scope'] = 'Hari lengkap (24 jam)'


for key, default in {
    'date_start': min_date,
    'date_end': max_date,
    'day_types': DAY_TYPES.copy(),
    'hour_scope': 'Hari lengkap (24 jam)',
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


with st.sidebar:
    st.header('Jelajahi data')
    st.caption('Capital Bikeshare · Washington, D.C.\n\nData historis 2011–2012')
    start = st.date_input('Tanggal awal', value=None, min_value=min_date, max_value=max_date,
                          format='DD/MM/YYYY', key='date_start')
    end = st.date_input('Tanggal akhir', value=None, min_value=min_date, max_value=max_date,
                        format='DD/MM/YYYY', key='date_end')
    types = st.multiselect('Jenis hari', DAY_TYPES, key='day_types',
                           help='Nonkerja mencakup akhir pekan dan hari libur.')
    scope = st.radio('Cakupan grafik per jam', ['Hari lengkap (24 jam)', 'Semua jam tercatat'],
                     index=None, key='hour_scope', help='Pilihan utama notebook memakai hari dengan 24 catatan jam lengkap.')
    st.button('Reset filter', on_click=reset_filters, width='stretch', key='reset')
    st.divider()
    st.caption('Filter tanggal dan jenis hari berlaku pada seluruh tab. Pilihan cakupan hanya mengubah analisis per jam.')

st.caption('CAPITAL BIKESHARE  /  ANALISIS 2011–2012')
st.title('Pola Penyewaan Sepeda')
st.write('Jelajahi jam sibuk, perubahan bulanan, dan tingkat penyewaan untuk mendukung perencanaan layanan.')
if start is None or end is None:
    st.info('Lengkapi tanggal awal dan tanggal akhir pada panel kiri.')
    st.stop()
if start > end:
    st.warning('Tanggal awal harus sama dengan atau sebelum tanggal akhir.')
    st.stop()
if not types:
    st.info('Pilih setidaknya satu jenis hari pada panel kiri.')
    st.stop()
selected_day, selected_hour = filter_data(day, hour, start, end, types, scope == 'Hari lengkap (24 jam)')
if selected_day.empty:
    st.info('Tidak ada hari yang sesuai dengan kombinasi filter. Ubah tanggal atau jenis hari.')
    st.stop()
st.caption(f"{start:%d/%m/%Y} – {end:%d/%m/%Y} · {', '.join(types)} · Jumlah penyewaan adalah kejadian sewa, bukan pelanggan unik.")
metrics = st.columns(4)
metrics[0].metric('Total penyewaan', format_number(selected_day['cnt'].sum()))
metrics[1].metric('Rata-rata per hari', format_number(selected_day['cnt'].mean(), 2))
metrics[2].metric('Hari pada filter', format_number(len(selected_day)))
metrics[3].metric('Hari untuk grafik jam', format_number(selected_hour['dteday'].nunique()))
st.caption('Total dan rata-rata dihitung dari tabel harian. Grafik jam memakai cakupan yang dipilih pada panel kiri.')

tab_hour, tab_month, tab_advanced, tab_data = st.tabs(
    ['Jam sibuk', 'Tren bulanan', 'Analisis lanjutan', 'Data & metode'])

with tab_hour:
    st.subheader('Kapan penyewaan paling ramai?')
    st.write('Bandingkan rata-rata jumlah penyewaan pada setiap jam menurut jenis hari.')
    if selected_hour.empty:
        st.info('Tidak ada hari lengkap untuk grafik jam pada filter ini. Pilih rentang lebih luas atau Semua jam tercatat.')
    else:
        profile = hourly_profile(selected_hour)
        fig, ax = plt.subplots(figsize=(11.5, 4.5), layout='constrained')
        for kind in DAY_TYPES:
            part = profile.loc[profile['day_type'].eq(kind)].sort_values('hr')
            if not part.empty:
                ax.plot(part['hr'], part['mean_rentals'], marker='o', markersize=3,
                         linewidth=2.3, color=COLORS[kind], label=kind)
        ax.set(xticks=range(24), xlabel='Jam pada dataset', ylabel='Rata-rata penyewaan per jam', ylim=(0, None))
        ax.grid(axis='y', alpha=0.2)
        ax.legend(frameon=False)
        show_figure(fig)
        st.caption(f"Cakupan grafik: {format_number(len(selected_hour))} catatan jam pada {selected_hour['dteday'].nunique()} hari. {scope}.")
        if scope == 'Semua jam tercatat':
            st.caption('Jumlah hari pengamatan dapat berbeda antarjam; catatan jam yang tidak tersedia tidak diisi nol.')
        for kind in DAY_TYPES:
            top = profile.loc[profile['day_type'].eq(kind)].nlargest(3, 'mean_rentals')
            if not top.empty:
                detail = '; '.join(f"{int(row.hr):02d}:00 ({format_number(row.mean_rentals, 2)} sewa/jam)" for row in top.itertuples())
                st.markdown(f'**Tiga jam tertinggi — {kind}:** {detail}.')
        with st.expander('Lihat tabel dan unduh profil jam'):
            st.dataframe(profile.round(2), hide_index=True, width='stretch')
            st.download_button('Unduh profil jam (CSV)', csv_bytes(profile), 'profil_jam.csv', 'text/csv', key='download_hour_profile')

with tab_month:
    st.subheader('Bagaimana pola bulanan berubah?')
    st.write('Rata-rata per hari memperhitungkan perbedaan jumlah hari dalam setiap bulan.')
    monthly, comparison = monthly_profile(selected_day, day, types)
    means = monthly.pivot(index='month', columns='year', values='mean_daily_rentals').sort_index()
    fig, ax = plt.subplots(figsize=(11.5, 4.5), layout='constrained')
    x = np.arange(len(means))
    years = list(means.columns)
    width = 0.75 / len(years)
    for position, year in enumerate(years):
        ax.bar(x + (position - (len(years)-1)/2) * width, means[year], width,
               color={2011: '#56B4E9', 2012: '#0072B2'}.get(year, '#0072B2'), label=str(year))
    ax.set(xticks=x, xticklabels=[MONTHS[m-1] for m in means.index],
           xlabel='Bulan', ylabel='Rata-rata penyewaan per hari', ylim=(0, None))
    ax.grid(axis='y', alpha=0.2)
    ax.set_axisbelow(True)
    ax.legend(title='Tahun', frameon=False)
    show_figure(fig)
    if not monthly['complete_month'].all():
        st.info('Ada bulan yang hanya tercakup sebagian. Batang menampilkan rata-rata tanggal terpilih; persentase YoY untuk bulan tersebut tidak dihitung.')
    comparable = comparison.dropna(subset=['yoy_pct'])
    if comparable.empty:
        st.info('Perbandingan YoY memerlukan bulan yang lengkap pada 2011 dan 2012 dengan filter jenis hari yang sama.')
    else:
        peak_month = int(comparable['yoy_pct'].idxmax())
        st.markdown(f"**Perubahan YoY paling tinggi pada bulan yang dapat dibandingkan:** {MONTHS[peak_month-1]}, **{format_number(comparable.loc[peak_month, 'yoy_pct'], 2)}%**.")
    peak = monthly.loc[monthly['mean_daily_rentals'].idxmax()]
    st.markdown(f"**Rata-rata tertinggi pada pilihan ini:** {MONTHS[int(peak['month'])-1]} {int(peak['year'])}, **{format_number(peak['mean_daily_rentals'], 2)} penyewaan per hari**.")
    with st.expander('Lihat tabel dan unduh ringkasan bulanan'):
        st.dataframe(monthly.round(2), hide_index=True, width='stretch')
        st.dataframe(comparison.reset_index().round(2), hide_index=True, width='stretch')
        st.download_button('Unduh ringkasan bulanan (CSV)', csv_bytes(monthly), 'ringkasan_bulanan.csv', 'text/csv', key='download_month')

with tab_advanced:
    st.subheader('Kelompok waktu dan tingkat penyewaan')
    st.markdown('#### Kelompok waktu')
    st.caption('Manual grouping dengan interval tetap. Rata-rata per jam membuat interval empat dan enam jam dapat dibandingkan.')
    if selected_hour.empty:
        st.info('Kelompok waktu belum tersedia untuk cakupan grafik jam yang dipilih.')
    else:
        blocks = time_profile(selected_hour)
        block_means = blocks.pivot(index='time_block', columns='day_type', values='mean_rentals_per_hour').reindex(TIME_LABELS)
        kinds = [kind for kind in DAY_TYPES if kind in block_means.columns]
        fig, ax = plt.subplots(figsize=(11.5, 4.5), layout='constrained')
        x = np.arange(len(TIME_LABELS))
        width = 0.75 / len(kinds)
        for position, kind in enumerate(kinds):
            bars = ax.bar(x + (position - (len(kinds)-1)/2)*width, block_means[kind], width,
                          color=COLORS[kind], label=kind)
            ax.bar_label(bars, fmt='%.1f', padding=3, fontsize=9)
        ax.set(xticks=x, xticklabels=TIME_TICKS, ylabel='Rata-rata penyewaan per jam',
               ylim=(0, max(1, block_means.max().max()) * 1.2))
        ax.grid(axis='y', alpha=0.2)
        ax.set_axisbelow(True)
        ax.legend(frameon=False)
        show_figure(fig)
        for kind in kinds:
            peak = blocks.loc[blocks['day_type'].eq(kind)].nlargest(1, 'mean_rentals_per_hour').iloc[0]
            st.markdown(f"**{kind}:** kelompok **{peak['time_block']}** tertinggi, {format_number(peak['mean_rentals_per_hour'], 2)} sewa/jam; pangsa volume {format_number(peak['rental_share_pct'], 2)}% pada jenis hari tersebut.")
        with st.expander('Tabel kelompok waktu'):
            st.dataframe(blocks.round(2), hide_index=True, width='stretch')

    st.markdown('#### Tingkat penyewaan harian')
    st.caption(f'Batas dari seluruh data 2011: rendah ≤ {format_number(q25)}; sedang > {format_number(q25)} sampai {format_number(q75)}; tinggi > {format_number(q75)}. Filter tidak mengubah batas acuan.')
    tiers = demand_profile(selected_day)
    pct = tiers.pivot(index='year', columns='demand_level', values='day_share_pct').reindex(columns=DEMAND_LABELS).fillna(0)
    fig, ax = plt.subplots(figsize=(10, 4.6), layout='constrained')
    bottoms = np.zeros(len(pct))
    for category, color, text_color in [('Rendah', '#C8D2DC', '#172B3A'), ('Sedang', '#0072B2', 'white'), ('Tinggi', '#D55E00', 'white')]:
        values = pct[category].to_numpy()
        ax.bar(np.arange(len(pct)), values, bottom=bottoms, width=0.5, color=color, label=category)
        for position, value in enumerate(values):
            if value >= 4:
                ax.text(position, bottoms[position]+value/2, f'{value:.2f}%', ha='center', va='center', color=text_color, fontsize=10)
        bottoms += values
    ax.set(xticks=np.arange(len(pct)), xticklabels=[str(y) for y in pct.index],
           ylabel='Persentase hari pada filter', xlabel='Tahun', ylim=(0, 100))
    ax.legend(loc='upper left', bbox_to_anchor=(1.01, 1), frameon=False)
    show_figure(fig)
    for year in pct.index:
        st.markdown(f"**{year}:** {format_number(pct.loc[year, 'Tinggi'], 2)}% hari pada filter melampaui batas {format_number(q75)} penyewaan.")
    st.caption('Kategori ini relatif terhadap distribusi 2011. Tingkat tinggi tidak langsung menunjukkan kekurangan armada.')
    with st.expander('Tabel dan penjelasan binning'):
        st.dataframe(tiers.round(2), hide_index=True, width='stretch')
        st.write('Kuartil 25% dan 75% ditetapkan dari tahun acuan yang sama. Notebook juga memeriksa sensitivitas dengan kuantil 20/80 dan 30/70.')

with tab_data:
    st.subheader('Data yang mendasari tampilan')
    st.write('Unduhan mengikuti filter aktif. CSV harian dan per jam memiliki tingkat agregasi berbeda; total keduanya tidak dijumlahkan.')
    day_export = selected_day[['dteday', 'year', 'month', 'day_type', 'casual', 'registered', 'cnt', 'demand_level', 'is_complete_day']]
    hour_export = selected_hour[['dteday', 'hr', 'day_type', 'time_block', 'casual', 'registered', 'cnt', 'is_complete_day']]
    left, right = st.columns(2)
    left.download_button('Unduh data harian (CSV)', csv_bytes(day_export), 'data_harian_terfilter.csv', 'text/csv', key='download_day')
    right.download_button('Unduh data per jam (CSV)', csv_bytes(hour_export), 'data_jam_terfilter.csv', 'text/csv', key='download_hour')
    st.dataframe(day_export, hide_index=True, width='stretch', height=280)
    with st.expander('Cakupan dan kualitas data sumber'):
        missing_slots = int((24 - day['hours_observed']).sum())
        st.write(f"Sumber memuat {len(day)} tanggal dan {format_number(len(hour))} catatan jam. Ada {missing_slots} slot jam tanpa catatan pada {int((~day['is_complete_day']).sum())} tanggal; {int(day['is_complete_day'].sum())} tanggal memiliki 24 catatan jam lengkap.")
        st.write('Tanggal dikonversi untuk analisis. Kelembapan nol ditandai sebagai meragukan; nilai sumber dipertahankan. Jam yang tidak tercatat tidak diisi angka penyewaan nol.')
        st.write('Grafik bulanan menghitung rata-rata tanggal yang dipilih. YoY hanya dihitung bila bulan yang sama tercakup lengkap pada kedua tahun, setelah mempertimbangkan filter jenis hari.')
    st.markdown('#### Cara menggunakan hasil')
    st.write('Gunakan profil jam dan kelompok waktu untuk meninjau jadwal kesiapan layanan. Gunakan pola bulanan dan kategori harian untuk meninjau asumsi kapasitas. Penentuan jumlah armada membutuhkan data ketersediaan, durasi sewa, dan lokasi.')
    st.caption('Analisis bersifat deskriptif pada periode historis. Data ini tidak mengisolasi penyebab pertumbuhan atau kebutuhan stok tiap stasiun.')
    st.markdown('**Sumber:** Bike Sharing Dataset dari penugasan Dicoding. [Fanaee-T (2013), UCI](https://doi.org/10.24432/C5W894). Dokumentasi asli tersedia pada data/Readme.txt.')

st.divider()
st.caption('Proyek Analisis Data · Tata Ivanka · Capital Bikeshare 2011–2012')
