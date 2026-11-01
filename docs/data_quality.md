# Pemeriksaan kualitas data

| Temuan | Bukti | Tindakan pada cleaning |
|---|---|---|
| Representasi tanggal belum siap untuk operasi waktu | dteday terbaca sebagai object/string pada kedua CSV | Ubah menjadi datetime, verifikasi parsing, lalu buat timestamp per jam |
| Rangkaian waktu per jam tidak lengkap | 165 dari 17.544 slot kalender tidak tercatat; terjadi pada 76 tanggal | Simpan daftar gap dan penanda kelengkapan; gunakan 655 hari lengkap untuk perbandingan jam; bandingkan dengan seluruh jam yang ada |
| Indikasi kelembapan meragukan | hum=0 pada 1 baris harian dan 22 baris jam tanggal 2011-03-10, termasuk catatan berkabut/hujan ringan | Beri flag dan buat humidity_pct yang kosong pada nilai meragukan; pertahankan hum sumber dan semua cnt |

Tidak ditemukan nilai kosong pada sel CSV, baris identik ganda, tanggal/timestamp ganda, atau pelanggaran `cnt = casual + registered`.
Nilai di luar pagar IQR pada `cnt` perlu ditinjau sebagai kemungkinan puncak permintaan; tidak ada bukti yang memadai untuk menghapusnya.
Tidak tercatatnya suatu jam belum membuktikan jumlah penyewaan nol. Penanda gap tidak diisi dengan angka penyewaan buatan.
