# Analisis lanjutan tahap 6

### Tujuan dan metode tahap 6

Analisis ini memperdalam dua pertanyaan bisnis melalui **manual grouping dan binning**, sesuai contoh analisis lanjutan pada ketentuan penilaian. Unit yang dikelompokkan adalah catatan waktu dan hari penyewaan.

**A. Pengelompokan waktu untuk pertanyaan 1.** Kolom `hr` dibagi dengan `pd.cut()` menjadi lima interval yang ditentukan secara eksplisit:

| Kelompok | Jam yang masuk | Lebar interval |
|---|---|---:|
| Dini hari | 00–05 | 6 jam |
| Pagi | 06–09 | 4 jam |
| Siang | 10–15 | 6 jam |
| Sore | 16–19 | 4 jam |
| Malam | 20–23 | 4 jam |

Interval tersebut merupakan pilihan analitis untuk merangkum pola waktu dan membantu perencanaan jadwal layanan. Batas waktu tidak diklaim sebagai jadwal resmi operator. Digunakan 655 hari dengan 24 catatan jam lengkap, konsisten dengan EDA. Rata-rata penyewaan **per jam** menjadi metrik perbandingan intensitas karena lebar interval berbeda. Pangsa volume dihitung terhadap total penyewaan pada jenis hari yang sama. Pangsa `registered` dihitung dari total kejadian sewa kategori tersebut dalam setiap kelompok.

**B. Binning tingkat penyewaan untuk pertanyaan 2.** Batas kategori dihitung dari kuartil 25% dan 75% jumlah penyewaan harian pada **2011**, lalu batas yang sama diterapkan pada 2011 dan 2012. Acuan tetap membuat perubahan komposisi antar-tahun dapat dibandingkan. Ini adalah kategori relatif terhadap distribusi 2011, bukan standar kapasitas operator.

Seluruh 731 tanggal dipakai dalam analisis harian. Jumlah hari per kategori dibagi jumlah hari pada tahun terkait, sehingga perbedaan 365 dan 366 hari diperhitungkan. Pemeriksaan sensitivitas memakai pasangan kuantil 20/80 dan 30/70, dengan acuan tetap 2011.

Implementasi menggunakan operasi pandas dan visualisasi Matplotlib. Referensi fungsi: [pandas.cut](https://pandas.pydata.org/docs/reference/api/pandas.cut.html) dan [Series.quantile](https://pandas.pydata.org/docs/reference/api/pandas.Series.quantile.html).


### Interpretasi kelompok waktu

- **Hari kerja:** sore (16–19) mempunyai rata-rata tertinggi, **441,98 penyewaan per jam**, dan menyumbang **36,08%** volume penyewaan hari kerja dalam sampel hari lengkap. Pagi (06–09) berada pada **294,07 penyewaan per jam**; pangsa penyewaan kategori registered dalam kelompok pagi mencapai **94,25%**.
- **Hari nonkerja:** siang (10–15) mempunyai rata-rata tertinggi, **355,93 penyewaan per jam**, dan menyumbang **46,86%** volume penyewaan hari nonkerja dalam sampel yang sama.
- Hasil ini merangkum puncak jam individual pada EDA menjadi rentang waktu yang dapat digunakan untuk menyusun jadwal kesiapan layanan. Pangsa volume memperhitungkan seluruh jam dalam interval; interval enam jam memiliki paparan waktu lebih panjang daripada interval empat jam.
- `registered` menunjukkan kategori penyewaan. Data agregat ini tidak mengidentifikasi orang unik atau membuktikan tujuan perjalanan. Cakupan analisis tetap terbatas pada 655 hari lengkap.


### Interpretasi tingkat penyewaan harian

Batas kuartil acuan 2011 adalah **Q25 = 2.132** dan **Q75 = 4.586** penyewaan per hari:

| Kategori | Aturan jumlah penyewaan per hari |
|---|---|
| Rendah | `cnt <= 2132` |
| Sedang | `2132 < cnt <= 4586` |
| Tinggi | `cnt > 4586` |

- Pada 2011 terdapat **91 dari 365 hari (24,93%)** berkategori tinggi. Pada 2012 terdapat **264 dari 366 hari (72,13%)**.
- Proporsi hari tinggi meningkat **47,20 poin persentase**. Poin persentase adalah selisih dua persentase, bukan persentase pertumbuhan relatif.
- Rata-rata penyewaan dalam kategori tinggi adalah **4.978,13** pada 2011 dan **6.527,92** pada 2012. Kategori tetap memakai satu batas yang sama; masing-masing kelompok dapat mempunyai rata-rata berbeda.
- Pergeseran kategori mendukung temuan pertumbuhan bulanan pada EDA. Hasil ini menunjukkan lebih seringnya hari dengan penyewaan melampaui ambang 2011; tidak mengukur kekurangan armada atau penyebab pertumbuhan.


### Pemeriksaan sensitivitas, validasi, dan batas interpretasi

- Dengan batas atas kuantil 80% (4.696,8), proporsi hari tinggi berubah dari **20,00%** menjadi **71,04%**.
- Dengan batas atas kuantil 70% (4.447,4), proporsi berubah dari **30,14%** menjadi **74,32%**.
- Pada ketiga skenario, proporsi hari tinggi tetap lebih besar pada 2012. Arah kesimpulan stabil terhadap pergeseran ambang yang diperiksa. Pemeriksaan ini bukan uji signifikansi statistik atau pembuktian bahwa satu ambang merupakan batas terbaik.
- Seluruh pemeriksaan integritas harus bernilai **True**: kategori terisi, baris dan total penyewaan dipertahankan, serta persentase berjumlah 100% untuk kelompok acuannya.
- Batas kuartil tidak dihitung ulang secara terpisah pada 2012. Menghitung kuartil tiap tahun secara terpisah akan mengubah definisi kategori dan menyamarkan pergeseran terhadap acuan yang sama.
- Data tahun 2011–2012 menggambarkan kondisi historis. Penerapan pada operasional sekarang memerlukan data terbaru dan informasi kapasitas layanan.
