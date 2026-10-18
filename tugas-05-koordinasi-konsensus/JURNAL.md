# Jurnal Proses — Tugas 5

## Implementasi Bully
- Kendala saat mengisi TODO 1-4: Proses pengisian TODO 1–4 berjalan relatif lancar. Bagian yang membutuhkan perhatian lebih adalah pengelolaan kondisi race saat beberapa node memulai election secara bersamaan, serta penggunaan lock agar tidak terjadi election ganda pada node yang sama. 
Pemahaman alur Bully Algorithm (pengiriman ELECTION ke ID lebih tinggi, balasan OK, dan broadcast COORDINATOR) membantu memastikan logika pada `on_message`, `start_election`, `declare_leader`, dan `monitor_leader` berjalan sesuai spesifikasi.

## Skenario 1: Start normal
- Leader yang terpilih: Node 5.
- Log/observasi: Kelima node dijalankan pada proses terpisah. Karena waktu start hampir bersamaan, terjadi beberapa kali pesan “tidak dapat dihubungi” di awal. Node dengan ID lebih rendah sempat menyatakan diri sebagai leader sementara, namun setelah menerima pesan `COORDINATOR` dari node yang lebih tinggi, semua node akhirnya menyepakati Node 5 sebagai leader (ID tertinggi). Node 5 kemudian terus menerima PING dari node lain sebagai tanda monitoring aktif.

## Skenario 2: Leader dimatikan
- Leader baru yang terpilih: Node 4.
- Waktu deteksi: Sekitar 3–5 detik setelah Node 5 dimatikan (sesuai interval monitoring 3 detik + timeout election 2 detik).
- Log/observasi: Setelah Node 5 tidak merespons PING, node-node lain mendeteksi kegagalan leader dan memulai election ulang. Node 4 (ID tertinggi yang masih hidup) berhasil menjadi leader baru dan menyebarkan pesan `COORDINATOR`. Node 1, 2, dan 3 menerima OK dari node yang lebih tinggi, kemudian memperbarui leader menjadi Node 4.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 18 Oktober 2026 | ChatGPT | Jelaskan alur kerja Bully Algorithm pada simulasi lima node dan bagaimana leader dipilih berdasarkan ID node | Node dengan ID lebih tinggi dapat mengambil alih proses election. Jika node dengan ID tertinggi aktif, node tersebut berpotensi menjadi leader | Menggunakan penjelasan sebagai referensi untuk memahami alur election dan mencatat hasil pengujian dengan bahasa sendiri |
| 18 Oktober 2026 | ChatGPT | Berikan outline pengujian untuk skenario start normal dan ketika leader tidak tersedia | Pengujian dibagi menjadi dua skenario, yaitu pemilihan leader awal dan pemilihan ulang setelah leader mati | Menyesuaikan urutan pengujian dengan instruksi tugas, menjalankan node secara lokal, dan mengamati hasil melalui log terminal |
