# Catatan tahap 7 — Dashboard Streamlit

## Tujuan

Menyajikan dua pertanyaan bisnis dan analisis lanjutan dari notebook melalui dashboard interaktif
yang dapat dijalankan secara lokal.

## Perubahan

1. Menambahkan `dashboard/dashboard.py` sebagai halaman aplikasi.
2. Memisahkan perhitungan dalam `dashboard/analysis.py` agar bisa diperiksa terhadap dataset.
3. Menambahkan filter tanggal, jenis hari, cakupan catatan jam, tombol reset, serta unduhan CSV.
4. Menyajikan empat grafik beserta interpretasi yang mengikuti filter.
5. Menambahkan konfigurasi tema, dependensi dengan versi, dan petunjuk penggunaan.
6. Menambahkan 11 tes fungsi dan interaksi menggunakan Streamlit AppTest.

## Konsistensi dengan notebook

- Sumber: `data/day.csv` dan `data/hour.csv` dari Bike Sharing Dataset penugasan.
- Metrik total menggunakan tabel harian agar aktivitas tidak terhitung dua kali.
- Analisis jam utama menggunakan tanggal lengkap (24 catatan jam).
- Interval waktu: 00–05, 06–09, 10–15, 16–19, dan 20–23.
- Batas kategori harian dari kuartil 2011: 2.132 dan 4.586, tetap setelah filter.
- Data historis ditafsirkan sebagai pola penyewaan yang tercatat, dengan batasan cakupan data.
- YoY di dashboard hanya tersedia untuk pasangan bulan lengkap dalam filter aktif.

## Bukti pemeriksaan

Pengujian otomatis: 11 lulus. Detail dan daftar pemeriksaan Windows ada di
[pengujian_dashboard.md](pengujian_dashboard.md).

Pemeriksaan browser Windows dan unggahan GitHub diselesaikan oleh pemilik setelah mengikuti panduan.
Catatan ini tidak menyatakan deployment sudah dilakukan.

## Commit tahap ini

`feat: build interactive dashboard`

Commit dilakukan setelah aplikasi dijalankan dan diperiksa pada komputer pemilik.
Tahap berikutnya: deployment, petunjuk penggunaan akhir, dan audit berkas submission.
