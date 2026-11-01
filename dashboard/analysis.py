"""Perhitungan dashboard, sesuai definisi notebook tahap 1–6."""
from pathlib import Path
import numpy as np
import pandas as pd

DAY_TYPES = ['Kerja', 'Nonkerja']
TIME_LABELS = ['Dini hari', 'Pagi', 'Siang', 'Sore', 'Malam']
TIME_EDGES = [0, 6, 10, 16, 20, 24]
TIME_TICKS = ['Dini hari\n00–05', 'Pagi\n06–09', 'Siang\n10–15', 'Sore\n16–19', 'Malam\n20–23']
DEMAND_LABELS = ['Rendah', 'Sedang', 'Tinggi']
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des']


def load_data(data_dir: Path):
    day = pd.read_csv(data_dir / 'day.csv', parse_dates=['dteday'])
    hour = pd.read_csv(data_dir / 'hour.csv', parse_dates=['dteday'])
    for frame in [day, hour]:
        required = {'dteday', 'workingday', 'cnt', 'casual', 'registered', 'hum'}
        if not required.issubset(frame.columns):
            raise ValueError('Kolom CSV tidak sesuai Bike Sharing Dataset yang digunakan notebook.')
        if not frame['cnt'].eq(frame['casual'] + frame['registered']).all():
            raise ValueError('Jumlah total penyewaan tidak sesuai komponennya.')
        frame['year'] = frame['dteday'].dt.year
        frame['month'] = frame['dteday'].dt.month
        frame['day_type'] = frame['workingday'].map({1: 'Kerja', 0: 'Nonkerja'})
        frame['humidity_suspect'] = frame['hum'].eq(0)
        frame['humidity_pct'] = (frame['hum'] * 100).mask(frame['humidity_suspect'])
    if not day['dteday'].is_unique or hour.duplicated(['dteday', 'hr']).any():
        raise ValueError('Tanggal atau catatan jam tidak unik.')
    coverage = hour.groupby('dteday')['hr'].nunique()
    for frame in [day, hour]:
        frame['hours_observed'] = frame['dteday'].map(coverage).fillna(0).astype(int)
        frame['is_complete_day'] = frame['hours_observed'].eq(24)
    reference = day.loc[day['year'].eq(2011), 'cnt']
    if reference.empty:
        raise ValueError('Data acuan tahun 2011 tidak tersedia.')
    q25, q75 = reference.quantile([0.25, 0.75])
    day['demand_level'] = pd.cut(day['cnt'], [-np.inf, q25, q75, np.inf], labels=DEMAND_LABELS)
    hour['time_block'] = pd.cut(hour['hr'], TIME_EDGES, labels=TIME_LABELS, right=False)
    return day.sort_values('dteday'), hour.sort_values(['dteday', 'hr']), float(q25), float(q75)


def filter_data(day, hour, start, end, types, complete_days=True):
    start, end = pd.Timestamp(start), pd.Timestamp(end)
    d = day.loc[day['dteday'].between(start, end) & day['day_type'].isin(types)].copy()
    h = hour.loc[hour['dteday'].between(start, end) & hour['day_type'].isin(types)].copy()
    if complete_days:
        h = h.loc[h['is_complete_day']].copy()
    return d, h


def hourly_profile(hour):
    return hour.groupby(['day_type', 'hr'], observed=True).agg(
        mean_rentals=('cnt', 'mean'), observed_hours=('cnt', 'size')
    ).reset_index()


def time_profile(hour):
    result = hour.groupby(['day_type', 'time_block'], observed=True).agg(
        mean_rentals_per_hour=('cnt', 'mean'), total_rentals=('cnt', 'sum'),
        observed_hours=('cnt', 'size'), registered_rentals=('registered', 'sum')
    ).reset_index()
    result['rental_share_pct'] = (result['total_rentals'] /
        result.groupby('day_type')['total_rentals'].transform('sum') * 100)
    result['registered_share_pct'] = result['registered_rentals'] / result['total_rentals'] * 100
    return result


def monthly_profile(selected_day, full_day, types):
    table = selected_day.groupby(['year', 'month']).agg(
        mean_daily_rentals=('cnt', 'mean'), total_rentals=('cnt', 'sum'),
        observed_days=('cnt', 'size')).reset_index()
    expected = full_day.loc[full_day['day_type'].isin(types)].groupby(['year', 'month']).size()
    table = table.merge(expected.rename('eligible_days').reset_index(), on=['year', 'month'], how='left')
    table['complete_month'] = table['observed_days'].eq(table['eligible_days'])
    means = table.pivot(index='month', columns='year', values='mean_daily_rentals').reindex(columns=[2011, 2012])
    complete = table.pivot(index='month', columns='year', values='complete_month').reindex(columns=[2011, 2012])
    comparison = means.rename(columns={2011: 'mean_2011', 2012: 'mean_2012'}).copy()
    comparison['comparable'] = complete.eq(True).all(axis=1) & means.notna().all(axis=1)
    comparison['yoy_pct'] = np.where(comparison['comparable'] & comparison['mean_2011'].gt(0),
        (comparison['mean_2012'] / comparison['mean_2011'] - 1) * 100, np.nan)
    return table, comparison


def demand_profile(day):
    result = day.groupby(['year', 'demand_level'], observed=True).agg(observed_days=('cnt', 'size')).reset_index()
    result['day_share_pct'] = result['observed_days'] / result.groupby('year')['observed_days'].transform('sum') * 100
    return result


def csv_bytes(frame):
    return frame.to_csv(index=False).encode('utf-8-sig')


def format_number(value, decimals=0):
    return f'{value:,.{decimals}f}'.replace(',', '_').replace('.', ',').replace('_', '.')
