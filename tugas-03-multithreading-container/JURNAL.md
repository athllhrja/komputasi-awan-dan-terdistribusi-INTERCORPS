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
| ... | ... | ... | ... | ... |
