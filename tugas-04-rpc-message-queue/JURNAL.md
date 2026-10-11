# Jurnal Proses — Tugas 4

## Jalur yang dipilih

- Athallah Radja : Saya memilih RPC karena pada kasus FoodGo, modul Pesanan membutuhkan jawaban langsung dari modul Pembayaran (cek saldo dan proses pembayaran). Operasi ini bersifat sinkron: hasil sukses/gagal harus diketahui sebelum alur pesanan dilanjutkan. RPC cocok karena client memanggil fungsi remote dan menunggu respons sebelum melanjutkan

- // masukin komen ini nnti di readme yak : Athallah Radja : Saya memilih return 0.0 pada cek_saldo untuk user yang tidak ditemukan karena dalam konteks simulasi ini, client (modul Pesanan) cukup mengetahui bahwa saldo = 0, lalu client sendiri yang memutuskan apakah akan lanjut proses atau tidak.

Krisna Putra Wicaksana: Saya memilih Message Queue (MQ) untuk komunikasi antara modul Pembayaran dan modul Kurir/Notifikasi karena notifikasi pembayaran tidak harus diproses secara langsung. Dengan RabbitMQ, modul Pembayaran dapat mengirim event tanpa perlu menunggu modul Kurir menyelesaikan tugasnya. Jika consumer sedang tidak aktif, pesan dapat disimpan di antrean dan diproses kembali ketika consumer dijalankan. Hal ini membuat komunikasi antarmodul lebih fleksibel dan membantu menjaga responsivitas sistem FoodGo.

Kesimpulan pemilihan jalur: Kelompok kami mengerjakan RPC dan Message Queue. RPC digunakan untuk operasi yang membutuhkan respons langsung, seperti pengecekan saldo dan proses pembayaran. Sementara itu, Message Queue digunakan untuk mengirim notifikasi pembayaran berhasil ke modul Kurir tanpa harus menunggu modul tersebut selesai memproses pesan.

## Kendala teknis

- Krisna Putra Wicaksana: Saat menjalankan RabbitMQ, saya mengalami kendala karena Docker Engine belum aktif. Selain itu, program Python sempat mengalami error ModuleNotFoundError: No module named 'pika'. Kendala tersebut diatasi dengan menjalankan Docker Desktop dan menginstal library pika pada virtual environment.

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
