# Jurnal Proses — Tugas 4

## Jalur yang dipilih

- Athallah Radja : Saya memilih RPC karena pada kasus FoodGo, modul Pesanan membutuhkan jawaban langsung dari modul Pembayaran (cek saldo dan proses pembayaran). Operasi ini bersifat sinkron: hasil sukses/gagal harus diketahui sebelum alur pesanan dilanjutkan. RPC cocok karena client memanggil fungsi remote dan menunggu respons sebelum melanjutkan
- Calvin Immanuel Lado : Saya memilih RPC karena proses pembayaran pada FoodGo membutuhkan jawaban langsung untuk menentukan apakah pesanan dapat dilanjutkan. Modul Pesanan harus menunggu hasil dari modul Pembayaran agar dapat mengetahui apakah transaksi berhasil atau gagal. RPC sesuai untuk kebutuhan ini karena client menunggu respons server sebelum melanjutkan proses berikutnya.



## Kendala teknis
- Error saat setup (mis. koneksi RabbitMQ ditolak, port bentrok): ...
- Calvin Immanuel Lado : Ketika saya menekan Ctrl+C saat request diproses, client menerima Fault: KeyboardInterrupt, tetapi server tetap berjalan. Saya kemudian menggunakan Stop-Process melalui PowerShell untuk menghentikan server.

## Uji komunikasi sinkron dan server mati (Jalur A)

- Calvin Immanuel Lado : Pembayaran berhasil ketika saldo mencukupi dan ditolak ketika saldo tidak cukup. Setelah fungsi cek_saldo diberi jeda 10 detik, waktu tunggu client menjadi sekitar 12 detik. Client baru melanjutkan pembayaran setelah menerima respons pengecekan saldo, sehingga terlihat bahwa pemanggilan RPC bersifat sinkron.
- Saat server dimatikan ketika permintaan cek_saldo sedang diproses, client menerima ConnectionRefusedError: [WinError 10061]. Permintaan tersebut tidak menghasilkan respons saldo yang berhasil diterima client. Program client berhenti karena error belum ditangani, sehingga pemanggilan pembayaran berikutnya tidak dijalankan.

## Uji "pesan tidak hilang" (khusus Jalur B)

- Langkah uji: matikan consumer → jalankan publisher → nyalakan consumer
  Krisna Putra Wicaksana - Langkah uji: Saya mematikan consumer, menjalankan publisher sebanyak dua kali, kemudian memeriksa antrean melalui dashboard RabbitMQ sebelum menjalankan consumer kembali.
- Hasil yang diamati: ...
  Krisna Putra Wicaksana - Hasil yang diamati: Dashboard RabbitMQ menunjukkan 6 pesan berstatus Ready ketika consumer tidak aktif. Setelah consumer dijalankan kembali, pesan-pesan yang tertunda mulai diterima dan diproses. Hasil ini menunjukkan bahwa publisher tetap dapat mengirim pesan meskipun consumer tidak aktif, selama RabbitMQ berjalan dan pesan berhasil masuk ke antrean.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal         | Tool AI              | Prompt yang diberikan                                | Ringkasan saran/ide AI                                                                                                                                                                                                                                                                                      | Bagaimana diolah jadi tulisan/kode sendiri                                                                                                                                                                                    |
| --------------- | -------------------- | ---------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 08 Oktober 2026 | Antigravity (Gemini) | "berikan saya penjelasan tentang apa itu RPC dan MQ" | AI menjelaskan konsep RPC (komunikasi sinkron, butuh respon instan, seperti menelepon) dan MQ (komunikasi asinkron, pesan ditampung di broker, seperti kotak surat). AI juga memberikan tabel perbandingan kapan harus menggunakan masing-masing teknologi.                                                 | Saya mempelajari perbedaan mendasar antara komunikasi sinkron dan asinkron untuk menjadi dasar argumen pemilihan arsitektur di laporan tugas.                                                                                 |
| 08 Oktober 2026 | Antigravity (Gemini) | "apa plus jika saya menggunakan RPC dan MQ"          | AI menjelaskan keuntungan menggabungkan keduanya (arsitektur hibrida): respons cepat (RPC) untuk proses kritis, dan keandalan/penahan beban (MQ) untuk proses background. Keuntungan lainnya termasuk ketahanan terhadap lonjakan trafik (_load leveling_), isolasi kegagalan, dan skalabilitas independen. | Saya menggunakan poin "keseimbangan kecepatan dan keandalan" serta "isolasi kegagalan" sebagai landasan analisis untuk mendesain sistem yang tangguh saat jam sibuk/trafik tinggi di studi kasus aplikasi pemesanan (FoodGo). |
