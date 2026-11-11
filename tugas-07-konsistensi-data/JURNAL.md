# Jurnal Proses — Tugas 7

## Diskusi pemilihan model konsistensi
- Argumen yang dipertimbangkan:
  - Eventual Consistency lebih cepat karena replikasi asinkron, tapi berisiko menyebabkan saldo tidak sinkron sementara (user top-up di Jakarta, order di Bandung ditolak).
  - Sequential Consistency menjamin semua replika melihat urutan yang sama, tapi terlalu ketat dan menambah latency karena harus sinkron dulu ke semua server.
Data saldo e-wallet menyangkut uang, sehingga dampak kesalahan jauh lebih serius dibanding data non-kritis seperti jumlah like.
- Kesimpulan akhir & alasan: Eventual Consistency tidak cukup untuk kasus ini. Sequential Consistency terlalu mahal. Solusi yang paling sesuai adalah Client-Centric Consistency (Read-Your-Writes), agar user yang baru top-up selalu melihat saldo terbarunya sendiri tanpa harus memaksa seluruh sistem selalu sinkron.

## Simulasi (jika dikerjakan)
- Hasil skenario naif vs Read-Your-Writes: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 11 Nov 2026 | Grok | Membantu menyusun argumen Sequential vs Eventual Consistency untuk kasus e-wallet FoodGo, serta usulan Read-Your-Writes | AI memberikan perbandingan Sequential, Eventual, dan Client-Centric Consistency beserta contoh dampak bisnis | Ide dari AI digunakan sebagai bahan diskusi, lalu ditulis ulang dengan kalimat sendiri dan disesuaikan dengan kasus FoodGo |
