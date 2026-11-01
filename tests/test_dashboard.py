"""Pengujian perhitungan, filter, dan penanganan kondisi kosong pada dashboard."""
from datetime import date
from io import BytesIO
from pathlib import Path
import logging
import sys
import unittest

import pandas as pd
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'dashboard'))
from analysis import (load_data, filter_data, hourly_profile, monthly_profile,
                      time_profile, demand_profile, csv_bytes)

logging.getLogger('streamlit.runtime.scriptrunner_utils.script_run_context').setLevel(logging.ERROR)


class DashboardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.day, cls.hour, cls.q25, cls.q75 = load_data(ROOT / 'data')

    def app(self):
        app = AppTest.from_file(str(ROOT / 'dashboard/dashboard.py'), default_timeout=30).run()
        self.assertEqual(len(app.exception), 0)
        return app

    @staticmethod
    def metrics(app):
        return {m.label: m.value for m in app.metric}

    def test_01_default_dashboard_matches_notebook(self):
        app = self.app()
        self.assertEqual(self.metrics(app)['Total penyewaan'], '3.292.679')
        self.assertEqual(self.metrics(app)['Hari pada filter'], '731')
        self.assertEqual(self.metrics(app)['Hari untuk grafik jam'], '655')
        self.assertEqual(self.metrics(app)['Rata-rata per hari'], '4.504,35')
        self.assertEqual(len(app.tabs), 4)

    def test_02_hourly_and_advanced_values_match_stage6(self):
        d, h = filter_data(self.day, self.hour, date(2011, 1, 1), date(2012, 12, 31), ['Kerja', 'Nonkerja'])
        profile = hourly_profile(h)
        work = profile.loc[profile['day_type'].eq('Kerja')].nlargest(3, 'mean_rentals')
        self.assertEqual(work['hr'].tolist(), [17, 18, 8])
        self.assertAlmostEqual(work['mean_rentals'].iloc[0], 559.6591422121896)
        blocks = time_profile(h)
        self.assertAlmostEqual(blocks.loc[blocks['day_type'].eq('Kerja') & blocks['time_block'].eq('Sore'), 'mean_rentals_per_hour'].iloc[0], 441.9813769751693)
        self.assertEqual((self.q25, self.q75), (2132.0, 4586.0))
        tiers = demand_profile(d)
        high = tiers.loc[tiers['year'].eq(2012) & tiers['demand_level'].eq('Tinggi')].iloc[0]
        self.assertEqual(high['observed_days'], 264)
        self.assertAlmostEqual(high['day_share_pct'], 72.1311475409836)

    def test_03_workday_filter_changes_totals(self):
        app = self.app()
        app.multiselect(key='day_types').set_value(['Kerja']).run()
        self.assertEqual(len(app.exception), 0)
        direct = pd.read_csv(ROOT / 'data/day.csv')
        expected = int(direct.loc[direct['workingday'].eq(1), 'cnt'].sum())
        displayed = int(self.metrics(app)['Total penyewaan'].replace('.', ''))
        self.assertEqual(displayed, expected)
        self.assertEqual(self.metrics(app)['Hari untuk grafik jam'], '443')

    def test_04_single_year_has_no_false_yoy(self):
        app = self.app()
        app.date_input(key='date_start').set_value(date(2012, 1, 1)).run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(self.metrics(app)['Total penyewaan'], '2.049.576')
        self.assertEqual(self.metrics(app)['Hari pada filter'], '366')
        self.assertTrue(any('Perbandingan YoY memerlukan' in m.value for m in app.info))

    def test_05_invalid_date_range(self):
        app = self.app()
        app.date_input(key='date_start').set_value(date(2012, 6, 1))
        app.date_input(key='date_end').set_value(date(2012, 1, 1)).run()
        self.assertEqual(len(app.exception), 0)
        self.assertTrue(any('Tanggal awal' in m.value for m in app.warning))
        self.assertEqual(len(app.metric), 0)

    def test_06_no_day_type_selected(self):
        app = self.app()
        app.multiselect(key='day_types').set_value([]).run()
        self.assertEqual(len(app.exception), 0)
        self.assertTrue(any('Pilih setidaknya' in m.value for m in app.info))

    def test_07_empty_filter_combination(self):
        app = self.app()
        app.date_input(key='date_start').set_value(date(2011, 1, 1))
        app.date_input(key='date_end').set_value(date(2011, 1, 1))
        app.multiselect(key='day_types').set_value(['Kerja']).run()
        self.assertEqual(len(app.exception), 0)
        self.assertTrue(any('Tidak ada hari yang sesuai' in m.value for m in app.info))

    def test_08_partial_hour_day_switches_safely(self):
        missing_day = self.day.loc[~self.day['is_complete_day'], 'dteday'].iloc[0].date()
        app = self.app()
        app.date_input(key='date_start').set_value(missing_day)
        app.date_input(key='date_end').set_value(missing_day).run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(self.metrics(app)['Hari untuk grafik jam'], '0')
        app.radio(key='hour_scope').set_value('Semua jam tercatat').run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(self.metrics(app)['Hari untuk grafik jam'], '1')

    def test_09_reset_filters(self):
        app = self.app()
        app.multiselect(key='day_types').set_value(['Kerja']).run()
        app.button(key='reset').click().run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(app.multiselect(key='day_types').value, ['Kerja', 'Nonkerja'])
        self.assertEqual(self.metrics(app)['Total penyewaan'], '3.292.679')

    def test_10_partial_month_not_compared_as_full_month(self):
        d, _ = filter_data(self.day, self.hour, date(2011, 1, 15), date(2012, 12, 31), ['Kerja', 'Nonkerja'])
        _, comp = monthly_profile(d, self.day, ['Kerja', 'Nonkerja'])
        self.assertFalse(comp.loc[1, 'comparable'])
        self.assertTrue(pd.isna(comp.loc[1, 'yoy_pct']))
        self.assertTrue(comp.loc[3, 'comparable'])
        raw = pd.read_csv(ROOT / 'data/day.csv', parse_dates=['dteday'])
        march = raw.loc[raw['dteday'].dt.month.eq(3)]
        direct = march.groupby(march['dteday'].dt.year)['cnt'].mean()
        expected_yoy = (direct.loc[2012] / direct.loc[2011] - 1) * 100
        self.assertAlmostEqual(comp.loc[3, 'yoy_pct'], expected_yoy)

    def test_11_download_csv_matches_filter(self):
        d, h = filter_data(self.day, self.hour, date(2012, 1, 1), date(2012, 1, 31), ['Nonkerja'])
        restored = pd.read_csv(BytesIO(csv_bytes(d)))
        self.assertEqual(len(restored), len(d))
        self.assertEqual(restored['cnt'].sum(), d['cnt'].sum())
        self.assertEqual(set(restored['day_type']), {'Nonkerja'})
        self.assertTrue(h['is_complete_day'].all())


if __name__ == '__main__':
    unittest.main(verbosity=2)
