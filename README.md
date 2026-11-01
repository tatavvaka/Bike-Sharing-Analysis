# Bike Sharing: Analisis Pola Penyewaan 2011–2012

Proyek analisis data Capital Bikeshare menggunakan dataset yang disediakan Dicoding.

**Status:** analisis dan dashboard tersedia. URL aplikasi dicatat pada bagian Dashboard online.
Bukti pemeriksaan akhir dicatat pada docs/checklist_final.md dan docs/audit_otomatis.md.

## Tujuan dan pertanyaan bisnis

1. Selama 1 Januari 2011–31 Desember 2012, tiga jam mana yang memiliki rata-rata jumlah penyewaan
   tertinggi pada hari kerja dan nonkerja, untuk menentukan prioritas jadwal kesiapan layanan?
   Perbandingan utama menggunakan tanggal dengan 24 catatan jam lengkap.
2. Berapa perubahan rata-rata jumlah penyewaan per hari pada setiap bulan tahun 2012 dibandingkan
   bulan yang sama pada 2011, dan bulan mana yang perlu diprioritaskan dalam perencanaan kapasitas
   berdasarkan besarnya penyewaan tercatat dan pertumbuhannya?

## Isi proyek

| Lokasi | Isi |
|---|---|
| notebook.ipynb | Notebook berdasarkan template Dicoding, analisis tahap 1–6 |
| data/day.csv, data/hour.csv | Dataset sumber |
| data/Readme.txt | Dokumentasi dataset asli |
| data/processed/ | Hasil cleaning dan kategori analisis |
| outputs/ | Bukti kualitas, tabel, validasi, dan grafik notebook |
| dashboard/dashboard.py | Aplikasi Streamlit |
| dashboard/analysis.py | Perhitungan dashboard |
| .streamlit/config.toml | Konfigurasi tampilan |
| tests/test_dashboard.py | Pengujian dashboard |
| docs/ | Catatan proses dan hasil pengujian |
| requirements.txt | Dependensi notebook dan dashboard |

## Menjalankan notebook di Google Colab

1. Buka https://colab.research.google.com/ dan pilih File > Upload notebook.
2. Unggah notebook.ipynb dan periksa identitas pada sel pertama.
3. Unggah day.csv dan hour.csv dari folder data/ ke panel Files Colab.
4. Pilih Runtime > Run all, kemudian periksa output tiap bagian.
5. Unduh melalui File > Download > Download .ipynb dan simpan sebagai notebook.ipynb.

Notebook mencari CSV di data/ dari folder proyek atau di direktori kerja Colab.

## Menjalankan dashboard pada Windows

Gunakan Python 3.12. Buka Command Prompt dari folder utama proyek yang berisi requirements.txt.
Jalankan satu per satu:

```bat
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m unittest discover -s tests -v
.venv\Scripts\python.exe -m streamlit run dashboard/dashboard.py
```

Buka alamat Local URL yang muncul, biasanya http://localhost:8501.
Biarkan terminal menyala saat dashboard digunakan. Tekan Ctrl+C untuk berhenti.
Untuk penggunaan berikutnya cukup jalankan perintah Streamlit terakhir.

Jika Python 3.12 belum tersedia, pasang Python install manager dari https://www.python.org/downloads/windows/,
lalu jalankan `pymanager install 3.12`. Jika launcher lama menghalangi perintah `py`, gunakan
`pymanager exec -V:3.12 -m venv .venv` untuk membuat lingkungan.

Versi yang diuji: Python 3.12.14, Streamlit 1.66.1, pandas 2.2.3, NumPy 2.3.5, Matplotlib 3.10.8.
Pemasangan awal memerlukan internet. Aplikasi kemudian membaca dataset lokal.

## Menggunakan dashboard

- Pilih tanggal awal dan akhir pada sidebar.
- Pilih Kerja, Nonkerja, atau keduanya; Nonkerja mencakup akhir pekan dan hari libur.
- Cakupan grafik per jam dapat menggunakan Hari lengkap (24 jam) atau Semua jam tercatat.
- Gunakan empat tab: Jam sibuk, Tren bulanan, Analisis lanjutan, dan Data & metode.
- Tabel dan interpretasi mengikuti filter. Unduh CSV melalui tombol yang tersedia.
- Tombol Reset filter mengembalikan pengaturan awal.

Pada filter awal: 3.292.679 penyewaan, 4.504,35 penyewaan/hari, 731 tanggal, dan 655 tanggal
untuk analisis jam lengkap. Metrik total memakai day.csv; data harian dan per jam tidak dijumlahkan.

YoY hanya dihitung untuk pasangan bulan lengkap dengan jenis hari yang sama. Batas kategori
penyewaan tetap memakai seluruh tahun 2011, meskipun filter diubah. Analisis bersifat deskriptif;
jumlah penyewaan bukan jumlah pelanggan unik, stok armada, atau permintaan yang tidak terlayani.

## Pemeriksaan dan dokumentasi

- Hasil 11 tes otomatis serta checklist browser Windows: [docs/pengujian_dashboard.md](docs/pengujian_dashboard.md).
- Catatan dashboard: [docs/progress_tahap7.md](docs/progress_tahap7.md).
- Commit tahap 7: `feat: build interactive dashboard`.
- URL aplikasi: lihat bagian Dashboard online dan url.txt.

## Sumber

Dataset penugasan Dicoding: Bike Sharing Dataset, Fanaee-T (2013).
https://doi.org/10.24432/C5W894. Dokumentasi asli: data/Readme.txt.

## Analisis lanjutan tahap 6

1. Lima kelompok waktu memakai batas 00, 06, 10, 16, 20, dan 24. Rata-rata per jam digunakan untuk membandingkan interval berbeda panjang.
2. Tingkat penyewaan harian memakai kuartil 2011: rendah <= 2.132, sedang > 2.132 sampai 4.586, dan tinggi > 4.586.
3. Batas yang sama diterapkan pada 2012. Proporsi hari tinggi berubah dari 24,93% menjadi 72,13%.
4. Dua pasangan kuantil pembanding memeriksa kestabilan arah hasil.

Penjelasan: [docs/advanced_analysis.md](docs/advanced_analysis.md).
Catatan tahap: [docs/progress_tahap6.md](docs/progress_tahap6.md).
Tabel dan validasi: outputs/advanced/. Grafik tambahan: outputs/figures/03_time_block_demand.png dan 04_daily_demand_levels.png.
Data dengan kategori: data/processed/day_segmented.csv dan hour_segmented.csv. Berkas jam hanya berisi subset 655 hari lengkap untuk analisis ini.

Sel terakhir analisis lanjutan membuat hasil_tahap6.zip di runtime untuk memudahkan pengunduhan. Notebook harus diunduh terpisah. ZIP sementara tersebut tidak perlu diunggah ke repository.

Tahap 6 memakai pandas, NumPy, dan Matplotlib; zipfile adalah bagian pustaka standar Python. Tahap 7 menambahkan Streamlit.

<!-- DEPLOYMENT_TAHAP8:BEGIN -->
## Dashboard online

[Buka dashboard Bike Sharing](https://tatavvaka-bike-sharing.streamlit.app/)

Repository: https://github.com/tatavvaka/Bike-Sharing-Analysis.
Entrypoint: `dashboard/dashboard.py`. Gunakan Python 3.12 di Advanced settings saat deployment.
Aplikasi membaca `data/day.csv` dan `data/hour.csv`; modul `dashboard/analysis.py` ikut diperlukan.

URL dicatat pada 2026-11-02 04:51 WIB. Pemeriksaan akses publik, filter, grafik, dan unduhan dilakukan
melalui browser dan dicatat pada [checklist akhir](docs/checklist_final.md).
Hasil pemeriksaan berkas: [audit otomatis](docs/audit_otomatis.md).

Sesudah dokumentasi di-commit, buat ZIP dengan:

```bat
.venv\Scripts\python.exe scripts/finalize_submission.py zip
```

Hasil: `dist/Submission_Bike_Sharing_Tata_Ivanka.zip`.
ZIP memuat dataset, notebook beserta output, kode dashboard, requirements, README,
URL aplikasi, serta dokumentasi proyek. Paket tahap 7/8 adalah bahan kerja dan tidak
digunakan sebagai pengganti ZIP submission ini.
<!-- DEPLOYMENT_TAHAP8:END -->
