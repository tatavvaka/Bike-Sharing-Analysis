# Bike Sharing: Analisis Pola Penyewaan 2011–2012

Proyek analisis data Capital Bikeshare menggunakan dataset yang disediakan Dicoding.
**Status: checkpoint tahap 3 dari paket tahap 1–5.** Dashboard, analisis lanjutan, deployment, dan ZIP submission akhir belum selesai.

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

- Tahap yang sudah terisi dalam checkpoint ini: 1 sampai 3.
- Riwayat commit GitHub terbentuk setelah pemilik menjalankan, memeriksa, dan mengunggah tiap tahap.
- Analisis lanjutan tanpa machine learning: belum dikerjakan.
- Dashboard lokal dan Streamlit Cloud: belum dikerjakan.
- Submission final: belum diajukan.
