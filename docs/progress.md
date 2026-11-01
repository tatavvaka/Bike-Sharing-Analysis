# Catatan progres

Setiap entri menjelaskan isi checkpoint. Tanggal dan penulis commit ditentukan oleh GitHub saat pemilik menyimpan perubahan setelah memeriksa hasilnya.

## Tahap 1

Struktur proyek, notebook template, README, dependensi, dan .gitignore disiapkan. Identitas notebook harus dilengkapi pemilik.

Pesan commit: `chore: initialize analysis project`

## Tahap 2

Dataset Bike Sharing dipilih, CSV sumber disertakan, dan dua pertanyaan SMART ditulis beserta metrik, periode, dan batas cakupan.

Pesan commit: `docs: define business questions and scope`

## Tahap 3

Gathering menghasilkan 731 baris harian dan 17.379 baris jam. Assessing mencatat tipe tanggal, 165 slot jam tidak tercatat, serta indikasi kelembapan nol. Nilai kosong pada sel dan duplikat baris adalah nol.

Pesan commit: `feat: load data and document quality issues`

## Tahap 4

Tanggal dikonversi; catatan sumber dipertahankan; coverage dan kelembapan diberi penanda. Analisis utama per jam dibatasi pada 655 hari lengkap. Pemeriksaan cleaning lulus dan CSV hasil disimpan.

Pesan commit: `feat: clean data and validate results`

## Tahap 5

EDA, dua grafik, tabel analisis, kesimpulan, dan rekomendasi awal dibuat. Peringkat jam puncak dibandingkan dengan semua jam tersedia. Analisis lanjutan dan dashboard masih dijadwalkan.

Pesan commit: `feat: add exploratory analysis and charts`

## Langkah berikutnya

Lanjutkan checkpoint berikutnya secara berurutan. Setelah tahap 5: analisis lanjutan, dashboard lokal, deployment, serta audit seluruh persyaratan submission.

<!-- TAHAP8:BEGIN -->
## Tahap 8 — deployment dan persiapan submission

- Pencatatan: 2026-11-02 04:51 WIB.
- URL yang dicatat pemilik: https://tatavvaka-bike-sharing.streamlit.app/
- Perubahan: README, url.txt, status penutup notebook, pemeriksaan berkas, dan alat pengemasan ZIP.
- Hasil pemeriksaan otomatis berkas: lihat audit_otomatis.md.
- Hasil pemeriksaan manual browser: lihat checklist_final.md; isi sesuai hasil nyata.
- Kendala dan penyelesaian: dicatat oleh pemilik pada checklist_final.md bila ada.
- Pesan commit tahap ini: `docs: finalize deployment and submission`.
- Tindak lanjut: commit/push berkas, buat ZIP, periksa isi ZIP, lalu unggah ke Dicoding.

Catatan ini mencatat persiapan berkas. Riwayat commit/push dan penerimaan submission
dibuktikan melalui GitHub serta status pengiriman pada Dicoding.
<!-- TAHAP8:END -->
