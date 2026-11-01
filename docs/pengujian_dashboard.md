# Pengujian dashboard tahap 7

## Hasil yang sudah diperiksa

Pengujian otomatis pada 1 November 2026: **11 tes dijalankan, 0 gagal, 0 error, 0 dilewati**.
Lingkungan: Linux, Python 3.12.14, Streamlit 1.66.1, pandas 2.2.3,
NumPy 2.3.5, dan Matplotlib 3.10.8.

Tes memakai `unittest`, Streamlit `AppTest`, serta pembandingan dengan CSV sumber dan hasil notebook.
`AppTest` menjalankan logika aplikasi dan mensimulasikan perubahan widget.
Hasil ini belum merupakan bukti bahwa aplikasi sudah dijalankan di browser pada komputer Windows pemilik.

| Pemeriksaan otomatis | Hasil |
|---|---|
| Metrik awal dan empat tab cocok dengan notebook | Lulus |
| Jam sibuk, kelompok waktu, serta kategori harian cocok dengan tahap 6 | Lulus |
| Filter hari kerja mengubah total dengan benar | Lulus |
| Filter satu tahun tidak menghasilkan YoY palsu | Lulus |
| Tanggal awal setelah tanggal akhir ditangani | Lulus |
| Jenis hari kosong ditangani | Lulus |
| Kombinasi filter tanpa data ditangani | Lulus |
| Tanggal dengan catatan jam tidak lengkap ditangani | Lulus |
| Reset mengembalikan filter dan metrik awal | Lulus |
| Bulan parsial dikecualikan dari YoY | Lulus |
| Isi CSV hasil fungsi ekspor cocok dengan data terfilter | Lulus |

Log: [hasil_uji_otomatis.txt](hasil_uji_otomatis.txt).
Empat grafik yang dihasilkan aplikasi juga diperiksa sebagai gambar: label dan legenda terbaca
pada ukuran render yang diperiksa. Tata letak keseluruhan browser dan klik unduh masih perlu
diverifikasi secara manual di Windows.

## Cara mengulang pengujian

Dari folder utama proyek setelah memasang dependensi:

```bat
.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Hasil akhir yang diharapkan: `Ran 11 tests ... OK`.
Peringatan `missing ScriptRunContext` dapat muncul dari lingkungan pengujian; periksa hasil akhir
tes dan pastikan tidak ada `FAILED` atau exception aplikasi.

## Checklist manual pada Windows — isi setelah benar-benar dicoba

- Tanggal pengujian: 01 November 2026
- Nama penguji: Tata Ivanka
- Versi Python (`.venv\Scripts\python.exe --version`): Python 3.12.10
- Browser dan versi: Microsoft Edge Version 156.0.4314.58 (Official build) (64-bit)

Ubah `[ ]` menjadi `[x]` hanya sesudah pemeriksaan berhasil.

- [x] Dashboard terbuka dari perintah Streamlit tanpa traceback.
- [x] Empat tab dan semua grafik terbaca; tidak ada label yang bertumpuk pada ukuran layar yang dipakai.
- [x] Filter awal menunjukkan total 3.292.679, rata-rata 4.504,35, 731 hari, dan 655 hari untuk grafik jam.
- [x] Tab Jam sibuk menampilkan urutan kerja 17:00, 18:00, 08:00 dan nonkerja 13:00, 12:00, 14:00.
- [x] Tanggal 01/01/2012–31/12/2012 menghasilkan total 2.049.576 dan 366 hari.
- [x] Mengubah jenis hari menjadi Kerja mengubah angka dan grafik.
- [x] Pilihan Semua jam tercatat menampilkan 731 hari pada periode penuh dengan kedua jenis hari dipilih.
- [x] Tombol Reset filter mengembalikan seluruh nilai awal.
- [x] Mengosongkan jenis hari menampilkan pesan yang dapat dipahami, tanpa error.
- [x] Tanggal awal setelah tanggal akhir menampilkan peringatan, tanpa error.
- [x] Tombol unduh pada tab Data & metode menghasilkan CSV yang dapat dibuka dan sesuai filter.
- [x] Pengujian otomatis di komputer ini selesai dengan 11 tes OK.

## Status berikutnya

Setelah checklist manual selesai, simpan hasilnya pada dokumen ini dan sertakan dalam commit
`feat: build interactive dashboard`. Deployment dan audit submission merupakan tahap 8.