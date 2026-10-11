# Tugas 4 (Pekan 4) — Komunikasi Antar Komponen

**Materi terkait:** Remote Procedure Call (RPC), Message-Oriented Middleware (MOM)/Message Queue.

**Kelompok:** 7 — INTERCORPS

| Nama | NIM |
|---|---|
| Athallah Radja | 103072400034 |
| Calvin Immanuel Lado | 103072400158 |
| Krisna Putra Wicaksana | 103072400079 |

## Hasil Analisis

### Jalur A: RPC (Sinkron)

- **Bukti Client Menunggu**

  Pada pengujian, fungsi `cek_saldo` diberi jeda 10 detik. Waktu tunggu yang tercatat pada terminal client sekitar 12,03–12,04 detik. Selama pengecekan saldo berlangsung, client menunggu respons server sebelum melanjutkan ke proses pembayaran. Hasil tersebut menunjukkan bahwa pemanggilan RPC bersifat sinkron.

  Jeda 10 detik ditambahkan khusus untuk pengujian. Penyebab tambahan waktu di luar jeda tersebut belum dianalisis secara terpisah.

- **Hasil Pengujian Pembayaran**

  Client dijalankan tiga kali tanpa memulai ulang server. Saldo awal `user1` sebesar Rp50.000, sedangkan pembayaran pada setiap percobaan sebesar Rp20.000.

  | Percobaan | Saldo Awal | Hasil | Saldo Akhir |
  |---|---:|---|---:|
  | 1 | Rp50.000 | Sukses | Rp30.000 |
  | 2 | Rp30.000 | Sukses | Rp10.000 |
  | 3 | Rp10.000 | Gagal: saldo tidak cukup | Rp10.000 |

  Pembayaran berhasil ketika saldo mencukupi. Ketika saldo tidak cukup, server menolak pembayaran dan saldo tidak berubah.

- **Keputusan: User Tidak Ditemukan**

  Athallah Radja memilih `return 0.0` pada fungsi `cek_saldo` untuk user yang tidak ditemukan agar client tetap menerima nilai saldo numerik. Namun, nilai tersebut belum membedakan user yang tidak ditemukan dengan user yang saldonya benar-benar nol.

  Karena itu, fungsi `proses_pembayaran` tetap memeriksa keberadaan user dan mengembalikan status gagal dengan pesan `user tidak ditemukan`. Pada implementasi ini, client tetap memanggil fungsi pembayaran setelah pengecekan saldo, sedangkan server menentukan apakah pembayaran berhasil atau gagal.

- **Server Mati di Tengah Proses**

  Server dihentikan ketika permintaan `cek_saldo` sedang diproses. Client kemudian menerima `ConnectionRefusedError: [WinError 10061]` dan tidak memperoleh hasil pengecekan saldo.

  Karena exception belum ditangani, program client berhenti dan tidak melanjutkan pemanggilan pembayaran. Pengujian ini dilakukan saat pengecekan saldo, bukan ketika saldo sedang dipotong.

Bukti pengujian RPC tersedia pada folder [bukti/run-rpc](bukti/run-rpc/). Proses pengujian dan kendala teknis dicatat dalam [JURNAL.md](JURNAL.md).

### Jalur B: Message Queue (Asinkron)

- **Hasil Pengujian**

  Publisher mengirim tiga pesan dalam satu kali eksekusi. Setiap pesan berisi `user_id`, `jumlah`, dan `timestamp`, kemudian dikirim dalam format JSON ke antrean `pembayaran_berhasil`.

  Consumer menerima pesan dan menampilkan notifikasi pembayaran untuk kurir. Setelah setiap pesan diproses, consumer mengirim acknowledgement (ACK) kepada RabbitMQ agar pesan tersebut dapat dihapus dari antrean.

- **Uji “Pesan Tidak Hilang”**

  Berdasarkan pengujian Krisna yang dicatat dalam jurnal, consumer dimatikan terlebih dahulu, kemudian publisher dijalankan sebanyak dua kali. Dashboard RabbitMQ menunjukkan **6 pesan berstatus Ready** ketika consumer tidak aktif.

  Setelah consumer dijalankan kembali, pesan-pesan yang tertunda mulai diterima dan diproses. Hasil ini menunjukkan bahwa publisher tetap dapat mengirim pesan meskipun consumer belum aktif, selama RabbitMQ berjalan dan pesan berhasil masuk ke antrean.

  Pesan menunggu di broker hingga consumer siap menerima. Dengan demikian, publisher tidak perlu menunggu consumer menyelesaikan pemrosesan notifikasi.

  Antrean dideklarasikan dengan `durable=True` dan pesan dikirim menggunakan `delivery_mode=2`. Namun, pengujian yang dicatat hanya mencakup consumer mati dan dinyalakan kembali, bukan pengujian restart broker.

### Analisis Pemilihan Pola Komunikasi

#### Kenapa RPC Cocok untuk Pesanan ke Pembayaran

Modul Pesanan membutuhkan hasil pengecekan saldo dan status pembayaran sebelum menentukan apakah pesanan dapat dilanjutkan. RPC sesuai karena modul Pesanan dapat memanggil fungsi pada modul Pembayaran dan menunggu hasilnya sebelum menjalankan langkah berikutnya.

#### Kenapa MQ Cocok untuk Pembayaran ke Kurir

Notifikasi kepada kurir dapat diproses setelah pembayaran selesai. Modul Pembayaran cukup mengirim event ke broker tanpa menunggu kurir memproses notifikasi.

Ketika consumer belum aktif, pesan dapat menunggu di antrean, seperti pada pengujian yang menghasilkan enam pesan Ready. Hal ini memungkinkan pengiriman dan pemrosesan notifikasi berlangsung pada waktu berbeda.

#### Apa yang Terjadi Jika Dipakai pada Skenario yang Salah

- **MQ untuk Pesanan ke Pembayaran:** jika hanya menggunakan pengiriman satu arah, modul Pesanan tidak langsung mengetahui apakah pembayaran berhasil atau gagal. Sistem membutuhkan mekanisme tambahan untuk menerima dan mencocokkan balasan, serta mengelola status pesanan selama menunggu.
- **RPC untuk Pembayaran ke Kurir:** modul Pembayaran harus menunggu respons layanan kurir. Jika layanan kurir lambat atau tidak tersedia, pemanggilan dapat tertahan atau menghasilkan error sehingga menghambat kelanjutan proses pada modul Pembayaran.

#### Trade-off

- **RPC:** alur permintaan dan respons mudah diikuti, serta hasil diterima melalui pemanggilan yang sama. Keterbatasannya, client harus menunggu respons dan bergantung pada ketersediaan server.
- **Message Queue:** pengiriman dan pemrosesan pesan dapat berlangsung pada waktu berbeda. Keterbatasannya, sistem membutuhkan broker dan pengelolaan acknowledgement, serta pengirim tidak langsung mengetahui kapan pesan selesai diproses.

Kedua jalur pada tugas ini dijalankan sebagai simulasi terpisah. Pembayaran melalui RPC belum secara otomatis memicu publisher MQ.

