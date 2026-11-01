# Audit persiapan tahap 8

## Lingkup pemeriksaan

Pemeriksaan dilakukan terhadap README, requirements, dan gitignore yang diunggah pada tahap 8;
notebook terakhir yang sebelumnya diunggah; serta kode/data dari paket tahap 7 yang telah dibuat.
Isi repository GitHub saat ini belum dapat diperiksa langsung melalui akses yang tersedia.
URL deployment belum diberikan. Karena itu akses publik, commit terbaru, dan penerimaan submission
belum dinyatakan terverifikasi dalam dokumen ini.

## Hasil pemeriksaan

| Bagian | Bukti yang diperiksa | Hasil |
|---|---|---|
| README, requirements, gitignore | Dibandingkan dengan berkas tahap 7 | Isinya sama |
| Notebook terakhir | 44 sel, 12 sel kode terisi | Sel kode memiliki execution_count |
| Output notebook | Tabel, empat gambar PNG, output error | Empat grafik tersimpan; tidak ada output error |
| Eksekusi ulang kode | 12 sel kode dijalankan berurutan dalam namespace Python baru | Berhasil |
| Validasi cleaning | Tabel validation dan assertion | Seluruh pemeriksaan lulus |
| Validasi analisis lanjutan | Tabel advanced_validation dan assertion | Seluruh pemeriksaan lulus |
| CSV sumber | 731 baris harian dan 17.379 baris per jam | Total tiap tabel 3.292.679 penyewaan |
| Visualisasi notebook | Empat gambar output diperiksa | Sumbu, label, dan legenda terbaca pada render yang diperiksa |
| Analisis lanjutan | Markdown tujuan, aturan, interpretasi, dan sensitivitas | Manual grouping waktu dan binning harian tersedia |
| Dashboard tahap 7 | Kode pemuatan data dan dependensi | Entry point dashboard/dashboard.py; juga memerlukan analysis.py serta kedua CSV |

Eksekusi ulang kode memakai backend Matplotlib Agg dan mengabaikan tampilan `display()`.
Ini memeriksa jalannya kode serta assertion; tidak menggantikan pemeriksaan antarmuka Jupyter/Colab.
Paket tahap 7 memiliki laporan 11 tes otomatis yang lulus. Pengujian tersebut dilakukan pada tahap 7.

## Ketentuan yang dicocokkan

Dokumen ketentuan berkas meminta folder proyek dalam ZIP, dataset, notebook yang sudah dijalankan,
kode Python dashboard, requirements, dan README cara menjalankan dashboard. Ketika deployment
diterapkan, URL dashboard dicatat dalam url.txt.

Empat saran yang terbaca pada halaman pertama PDF penilaian: dokumentasi Markdown setiap tahap,
visualisasi dengan desain dan integritas, deployment Streamlit Cloud, serta analisis lanjutan relevan
tanpa algoritma machine learning. Manual grouping dan binning disebut sebagai contoh teknik.

Rincian tabel skala bintang pada halaman 2–6 PDF yang dikirim terpotong/tidak terbaca utuh.
Audit ini menggunakan kriteria utama yang disampaikan dalam percakapan dan empat saran yang terbaca;
tidak mengarang ambang penilaian bintang.

## Penyesuaian berkas akhir

- Aplikasi membaca data/day.csv dan data/hour.csv, sehingga tidak bergantung pada dashboard/main_data.csv.
  Nama main_data.csv pada struktur PDF adalah contoh. Sertakan berkas yang benar-benar dipakai aplikasi.
- dashboard/analysis.py harus ikut dalam repository dan ZIP karena diimpor oleh dashboard.py.
- requirements dari tahap 7 dipertahankan: Streamlit 1.66.1, pandas 2.2.3, NumPy 2.3.5, Matplotlib 3.10.8.
- Pilih Python 3.12 saat deployment agar sesuai versi utama lingkungan pengujian tahap 7.
- Skrip finalize_submission.py mencatat URL, memperbarui dokumentasi, dan memeriksa berkas sebelum pengemasan.
- Skrip tidak memverifikasi halaman online dan tidak menjalankan ulang notebook/dashboard.

## Pemeriksaan tersisa oleh pemilik

Gunakan checklist_final.md untuk uji publik tanpa login, uji filter, unduhan CSV, pencocokan GitHub,
dan pemeriksaan ZIP. Status setiap pemeriksaan harus mengikuti hasil nyata.

## Pengujian alat pengemasan

Lima tes alat finalize_submission.py lulus: audit sumber, penolakan URL yang salah tanpa perubahan berkas,
preservasi kode/output serta progres sebelumnya, kelengkapan ZIP dan pengecualian lingkungan,
serta penolakan notebook yang belum dijalankan atau modul yang hilang. Log: hasil_uji_finalizer.txt.

Pengujian memakai proyek sementara dan alamat contoh khusus pengujian; tidak melakukan deployment
atau menambahkan URL contoh ke berkas proyek pemilik.
