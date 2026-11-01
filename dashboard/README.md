# Dashboard Streamlit — tahap 7

Aplikasi: `dashboard/dashboard.py`. Perhitungan pendukung: `dashboard/analysis.py`.
Jalankan perintah berikut dari **folder utama proyek**, yang memuat `requirements.txt` dan `data/`.

```bash
python -m pip install -r requirements.txt
python -m streamlit run dashboard/dashboard.py
```

Untuk Windows dengan lingkungan `.venv`:

```bat
.venv\Scripts\python.exe -m streamlit run dashboard/dashboard.py
```

## Isi dashboard

- Filter tanggal awal/akhir, jenis hari, cakupan per jam, serta tombol reset.
- Empat indikator: total penyewaan, rata-rata per hari, jumlah tanggal, dan tanggal untuk analisis jam.
- Tab Jam sibuk: profil 24 jam dan tiga jam tertinggi menurut jenis hari.
- Tab Tren bulanan: rata-rata harian per bulan dan perubahan YoY pada bulan yang dapat dibandingkan.
- Tab Analisis lanjutan: lima kelompok waktu dan kategori penyewaan harian dengan batas tetap dari 2011.
- Tab Data & metode: unduhan CSV sesuai filter, penjelasan kualitas data, dan batasan analisis.

## Definisi penting

Dataset asli berada di `data/day.csv` dan `data/hour.csv`. Aplikasi menyiapkan tipe tanggal,
label kategori, dan pemeriksaan kelengkapan jam secara deterministik ketika memuat data.
Analisis jam utama menggunakan 655 tanggal yang masing-masing mempunyai 24 catatan jam.
Filter cakupan jam tidak mengubah metrik dari tabel harian.

Tabel harian dan per jam merupakan dua tingkat agregasi dari aktivitas yang sama;
total keduanya tidak dijumlahkan. Jumlah penyewaan bukan jumlah pelanggan unik atau stok sepeda.

YoY hanya dihitung apabila bulan yang sama tercakup lengkap pada kedua tahun, dengan jenis hari
yang sama. Batas kategori harian tetap memakai kuartil seluruh 2011: 2.132 dan 4.586.

## Pengujian

```bat
.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Hasil otomatis dan checklist pemeriksaan Windows: [../docs/pengujian_dashboard.md](../docs/pengujian_dashboard.md).
Deployment dan URL publik dilanjutkan pada tahap 8.
