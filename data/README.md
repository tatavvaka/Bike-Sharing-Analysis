# Sumber dan cara menggunakan data

- Berkas asli berasal dari `Bike-sharing-dataset.zip` yang disediakan pada penugasan Dicoding.
- `day.csv`: 731 baris, tingkat agregasi satu hari.
- `hour.csv`: 17.379 baris, tingkat agregasi satu jam yang tercatat.
- `Readme.txt`: dokumentasi asli yang disertakan dalam ZIP, disimpan tanpa perubahan.
- Periode: 1 Januari 2011 sampai 31 Desember 2012, Capital Bikeshare, Washington D.C.
- UCI: https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset
- DOI dataset: https://doi.org/10.24432/C5W894
- Atribusi publikasi: Fanaee-T, H., & Gama, J. (2013). Event labeling combining ensemble detectors and background knowledge. https://doi.org/10.1007/s13748-013-0040-3

`cnt` adalah jumlah kejadian penyewaan, dengan `cnt = casual + registered`.
`workingday=1` berarti hari kerja; `workingday=0` berarti akhir pekan atau hari libur.
`hum` merupakan kelembapan relatif dibagi 100.

Kedua tabel merupakan agregasi berbeda dari aktivitas yang sama. Pilih tabel sesuai pertanyaan; jangan menjumlahkan total kedua tabel.
Kamus asli dan halaman UCI memiliki perbedaan keterangan season serta normalisasi suhu. Dua pertanyaan utama proyek tidak menggunakan label musim atau inversi suhu; kode aslinya dipertahankan.

CSV sumber dipertahankan. Hasil cleaning ditulis terpisah di `data/processed/` mulai tahap 4.
