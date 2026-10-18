# Jurnal Proses — Tugas 5

## Implementasi Bully
- Kendala saat mengisi TODO 1-4: Tidak ada kendala yang berarti selama proses implementasi. Setiap bagian dilengkapi sesuai fungsi masing-masing, mulai dari pengiriman pesan election, penentuan leader, hingga pemantauan kondisi leader.

## Skenario 1: Start normal
- Leader yang terpilih: Node 5.
- Log/observasi: Kelima node dijalankan melalui proses Python yang terpisah dengan port masing-masing. Node melakukan proses election dan node 5 terpilih sebagai leader karena memiliki ID tertinggi. Node lain menerima pesan `COORDINATOR` untuk mengetahui leader yang sedang aktif.

## Skenario 2: Leader dimatikan
- Leader baru yang terpilih: Node 4.
- Berapa lama waktu sampai leader baru terdeteksi:  Sekitar beberapa detik setelah node 5 dimatikan, menyesuaikan interval pemantauan leader dan waktu proses election. Waktu pastinya dicatat berdasarkan hasil pengujian.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 18 Oktober 2026 | ChatGPT | Jelaskan alur kerja Bully Algorithm pada simulasi lima node dan bagaimana leader dipilih berdasarkan ID node | Node dengan ID lebih tinggi dapat mengambil alih proses election. Jika node dengan ID tertinggi aktif, node tersebut berpotensi menjadi leader | Menggunakan penjelasan sebagai referensi untuk memahami alur election dan mencatat hasil pengujian dengan bahasa sendiri |
| 18 Oktober 2026 | ChatGPT | Berikan outline pengujian untuk skenario start normal dan ketika leader tidak tersedia | Pengujian dibagi menjadi dua skenario, yaitu pemilihan leader awal dan pemilihan ulang setelah leader mati | Menyesuaikan urutan pengujian dengan instruksi tugas, menjalankan node secara lokal, dan mengamati hasil melalui log terminal |
