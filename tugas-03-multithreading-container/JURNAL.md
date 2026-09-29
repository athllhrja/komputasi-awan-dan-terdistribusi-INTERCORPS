# Jurnal Proses — Tugas 3

## Percobaan tanpa Lock
- Hasil `processed_count` yang didapat: Athallah Radja menjalankan program dan hasilnya adalah semua enam kali RUN program menghasilkan processed_count = 100
- Kenapa bisa meleset (jelaskan mekanisme race condition dengan kata sendiri:
- Beberapa thread mengubah processed_count bersamaan tanpa Lock.
  Operasi += 1 terdiri dari baca, tambah, tulis. Dua thread bisa
  membaca nilai yang sama lalu saling menimpa, sehingga total
  pesanan yang tercatat bisa kurang dari 100. Pada run kami dengan
  100 order, gejala jarang muncul, tetapi risikonya tetap ada.

## Percobaan dengan Lock
- Hasil `processed_count` setelah perbaikan: ...

## Kendala Docker
- Error yang ditemui saat `docker build`/`docker run` dan cara memperbaikinya: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 29-09-2026 | ChatGPT | Menanyakan apakah threading.Lock() tepat untuk TODO 1, apakah increment counter perlu dilakukan di process_order, cara menjalankan percobaan awal, mengapa hasilnya 0 lalu 100, dan apakah main() menggunakan lock. | Lock dibuat di TODO 1 dan digunakan untuk melindungi pembaruan counter di process_order. main() bertugas membagi pesanan dan mengelola thread. Hasil 0 menunjukkan pekerjaan belum berjalan; setelah thread dibuat, hasil 100 tercatat pada enam percobaan tanpa lock. | Saya memeriksa saran dengan membandingkannya terhadap instruksi tugas dan hasil program yang saya jalankan. Saya mengisi serta menjalankan kode sendiri, lalu mencatat hasil aktual—termasuk bahwa race condition tidak tampak pada percobaan tanpa lock. |
| 29-09-2026 | ChatGPT | “Setelah mengganti TODO 3 dengan pembagian order ke beberapa thread, apakah hasilnya sudah benar?" | TODO 3 bertugas membagi daftar pesanan ke thread, memulai thread, lalu menunggu semuanya selesai. Hasil 100 menunjukkan semua pesanan terhitung, tetapi belum membuktikan race condition tanpa lock. | Saya membandingkan penjelasan dengan kode dan output program saya, lalu mencatat hasil percobaan tanpa lock apa adanya. |
