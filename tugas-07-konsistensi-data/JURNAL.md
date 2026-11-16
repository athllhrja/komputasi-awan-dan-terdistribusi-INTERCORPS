# Jurnal Proses — Tugas 7

## Diskusi pemilihan model konsistensi
- Argumen yang dipertimbangkan:
  - Eventual Consistency lebih cepat karena replikasi asinkron, tapi berisiko menyebabkan saldo tidak sinkron sementara (user top-up di Jakarta, order di Bandung ditolak).
  - Sequential Consistency menjamin semua replika melihat urutan yang sama, tapi terlalu ketat dan menambah latency karena harus sinkron dulu ke semua server.
Data saldo e-wallet menyangkut uang, sehingga dampak kesalahan jauh lebih serius dibanding data non-kritis seperti jumlah like.
- Kesimpulan akhir & alasan: Eventual Consistency tidak cukup untuk kasus ini. Sequential Consistency terlalu mahal. Solusi yang paling sesuai adalah Client-Centric Consistency (Read-Your-Writes), agar user yang baru top-up selalu melihat saldo terbarunya sendiri tanpa harus memaksa seluruh sistem selalu sinkron.

## Simulasi (jika dikerjakan)
- **Hasil skenario naif vs Read-Your-Writes:**
  - **Skenario naif:** Pelanggan melakukan top-up Rp50.000 melalui server Jakarta. Saldo Jakarta berhasil diperbarui menjadi Rp50.000 (versi 1), tetapi replikasi ke Bandung tertunda selama 2 detik. Ketika pembacaan dilakukan melalui Bandung setelah 0,5 detik, saldo yang diperoleh masih Rp0. Hal ini menunjukkan terjadinya inconsistent read akibat keterlambatan replikasi.
  - **Skenario Read-Your-Writes:** Pelanggan melakukan top-up tambahan Rp20.000 sehingga saldo Jakarta menjadi Rp70.000 (versi 2). Ketika pelanggan membaca saldo melalui Bandung, sistem mendeteksi bahwa versi Bandung masih 1, sedangkan versi minimal yang dibutuhkan adalah 2. Oleh karena itu, pembacaan dialihkan ke Jakarta dan berhasil memperoleh saldo terbaru sebesar Rp70.000.
  - **Kesimpulan simulasi:** Penerapan Read-Your-Writes berhasil mengatasi masalah inconsistent read pada pengujian. Mekanisme pemeriksaan versi memungkinkan pelanggan membaca saldo terbaru meskipun proses replikasi belum selesai.

- **Evaluasi hasil simulasi:**
  - Pada skenario naif, pembacaan langsung dari Bandung tidak menjamin data yang diperoleh merupakan saldo terbaru.
  - Pada skenario Read-Your-Writes, penggunaan version counter memastikan sistem memeriksa versi data sebelum melakukan pembacaan.
  - Apabila versi replika tujuan masih tertinggal, sistem mengalihkan pembacaan ke Jakarta yang sudah menerima pembaruan.
  - Read-Your-Writes meningkatkan konsistensi pembacaan pelanggan, tetapi belum menjamin keamanan seluruh operasi pembayaran yang membutuhkan transaksi atomik.


## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 11 Nov 2026 | Grok | Membantu menyusun argumen Sequential vs Eventual Consistency untuk kasus e-wallet FoodGo, serta usulan Read-Your-Writes | AI memberikan perbandingan Sequential, Eventual, dan Client-Centric Consistency beserta contoh dampak bisnis | Ide dari AI digunakan sebagai bahan diskusi, lalu ditulis ulang dengan kalimat sendiri dan disesuaikan dengan kasus FoodGo |
