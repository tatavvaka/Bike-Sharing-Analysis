# Bike Sharing: Analisis Pola Penyewaan 2011–2012

Proyek analisis data Capital Bikeshare menggunakan dataset yang disediakan Dicoding.
**Status: tahap 1–6 telah terisi.** Analisis lanjutan sudah ditambahkan. Dashboard, deployment, dan ZIP submission akhir masih dikerjakan pada tahap berikutnya.

## Tujuan

Mengidentifikasi jam sibuk menurut jenis hari dan membandingkan rata-rata penyewaan harian setiap bulan pada 2011 dan 2012 untuk mendukung simulasi perencanaan layanan.

## Isi proyek

| Lokasi | Isi |
|---|---|
| notebook.ipynb | Notebook berdasarkan template Dicoding |
| data/ | CSV sumber; mulai tahap 2 |
| data/processed/ | Hasil cleaning; mulai tahap 4 |
| outputs/quality/ | Bukti assessing dan validasi; mulai tahap 3 |
| outputs/tables/ | Tabel hasil analisis; mulai tahap 5 |
| outputs/figures/ | Grafik hasil analisis; mulai tahap 5 |
| docs/progress.md | Catatan pekerjaan per tahap |
| requirements.txt | Dependensi notebook |
| dashboard/ | Rencana tempat aplikasi Streamlit tahap berikutnya |

## Menjalankan notebook di Google Colab

1. Buka https://colab.research.google.com/ dan pilih File > Upload notebook.
2. Unggah notebook.ipynb dan lengkapi nama, email, serta ID Dicoding pada sel pertama.
3. Mulai tahap 3, unggah day.csv dan hour.csv dari folder data/ ke panel Files Colab.
4. Pilih Runtime > Run all, kemudian periksa output tiap bagian.
5. Unduh notebook dari File > Download > Download .ipynb. Simpan dengan nama notebook.ipynb.
6. Simpan versi yang telah dijalankan tersebut ke repository bersama berkas tahap yang terkait.

Notebook mencari CSV di data/ jika dijalankan dari folder proyek, atau di direktori kerja jika CSV diunggah langsung ke Colab.

## Lingkungan Python lokal (opsional pada tahap ini)

Gunakan Python 3.10 atau lebih baru. Instal dependensi dengan `python -m pip install -r requirements.txt`.
Buka notebook memakai Jupyter atau VS Code yang telah mendukung notebook. Panduan utama tahap 1–5 menggunakan Colab.

## Dashboard

Aplikasi Streamlit dan petunjuk menjalankannya akan ditambahkan pada tahap berikutnya. Folder dashboard saat ini berisi catatan rencana.

## Sumber

Dataset penugasan Dicoding: Bike Sharing Dataset, Fanaee-T (2013). https://doi.org/10.24432/C5W894.
Dokumentasi asli disimpan di data/Readme.txt mulai tahap 2.

## Status pemeriksaan

- Tahap yang sudah terisi dalam checkpoint ini: 1 sampai 6.
- Riwayat commit GitHub terbentuk setelah pemilik menjalankan, memeriksa, dan mengunggah tiap tahap.
- Analisis lanjutan: manual grouping waktu dan binning harian dengan acuan 2011, termasuk pemeriksaan sensitivitas.
- Dashboard lokal dan Streamlit Cloud: belum dikerjakan.
- Submission final: belum diajukan.

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

Dependensi tahap 6 tetap pandas, NumPy, dan Matplotlib; zipfile adalah bagian pustaka standar Python.
