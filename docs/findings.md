# Hasil analisis tahap 5

**Insight:**
- Pada hari kerja lengkap, tiga rata-rata tertinggi berada pada pukul **17:00 (559,66)**, **18:00 (524,11)**, dan **08:00 (504,05)** penyewaan per jam.
- Pada hari nonkerja lengkap, tiga rata-rata tertinggi berada pada pukul **13:00 (390,83)**, **12:00 (385,07)**, dan **14:00 (381,65)**.
- Peringkat tiga jam tertinggi tetap sama ketika dihitung dari seluruh jam yang tercatat, walaupun besaran rata-ratanya lebih rendah. Temuan ini mendukung kestabilan peringkat waktu puncak terhadap pilihan cakupan data.
- Rata-rata harian 2012 lebih tinggi daripada 2011 pada seluruh bulan. **Maret** mempunyai kenaikan absolut dan relatif terbesar: **3.252,58 penyewaan per hari atau 157,44%**.
- Tingkat permintaan rata-rata tertinggi pada 2012 terjadi pada **September: 7.285,77 penyewaan per hari**. Bulan dengan pertumbuhan tertinggi tidak otomatis sama dengan bulan dengan tingkat permintaan tertinggi.

- **Conclusion pertanyaan 1:** Pada hari lengkap selama 2011–2012, prioritas jam sibuk hari kerja adalah 17:00, 18:00, dan 08:00, dengan rata-rata 559,66; 524,11; dan 504,05 penyewaan per jam. Pada hari nonkerja, prioritasnya 13:00, 12:00, dan 14:00, dengan rata-rata 390,83; 385,07; dan 381,65. Peringkat tersebut tetap sama pada pemeriksaan seluruh jam yang tersedia.
- **Conclusion pertanyaan 2:** Seluruh bulan tahun 2012 memiliki rata-rata penyewaan harian yang lebih tinggi daripada bulan yang sama pada 2011. Maret mencatat pertumbuhan tertinggi (+157,44%, atau +3.252,58 penyewaan per hari), sedangkan September 2012 memiliki tingkat permintaan rata-rata tertinggi (7.285,77 penyewaan per hari).

**Batas interpretasi:** Hasil mewakili data historis Capital Bikeshare 2011–2012. Seleksi hari lengkap mengecualikan 76 tanggal dari analisis utama per jam; penyebab gap tidak diketahui. Analisis deskriptif ini tidak mengisolasi sebab pertumbuhan, belum menunjukkan ketersediaan armada, dan tidak dapat menentukan kebutuhan stok tiap stasiun.

**Rekomendasi Action Item:**
- Untuk simulasi perencanaan berdasarkan periode dataset, uji penyesuaian jadwal kesiapan layanan menjelang pukul 08:00 dan 17:00–18:00 pada hari kerja, serta 12:00–14:00 pada hari nonkerja. Penetapan jumlah armada membutuhkan data ketersediaan, durasi sewa, dan lokasi yang belum tersedia di tabel ini.
- Gunakan tingkat permintaan September dan lonjakan pertumbuhan Maret sebagai dua masukan terpisah untuk perencanaan kapasitas musiman; evaluasi kembali dengan data periode terbaru sebelum penerapan operasional saat ini.
- Perbaiki pemeriksaan kelengkapan pencatatan per jam dan verifikasi sumber kelembapan pada 2011-03-10 sebelum melakukan analisis lingkungan lanjutan.

**Status:** Tahap 1–5 selesai dalam checkpoint ini. Analisis lanjutan, aplikasi Streamlit, deployment, dan audit submission final masih dikerjakan pada tahap berikutnya.
