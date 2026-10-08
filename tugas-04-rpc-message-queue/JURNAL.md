# Jurnal Proses — Tugas 4

## Jalur yang dipilih
- Athallah Radja Memilih untuk menggunakan RPC Alasan: dikarenakan kecepatan respon RPC itu sangat cepat dibandingkan dengan MQ maka untuk Case FoodGo ini saya memilih untuk Menggunakan metode RPC

## Kendala teknis
- Error saat setup (mis. koneksi RabbitMQ ditolak, port bentrok): ...

## Uji "pesan tidak hilang" (khusus Jalur B)
- Langkah uji: matikan consumer → jalankan publisher → nyalakan consumer
- Hasil yang diamati: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 08 Oktober 2026 | Antigravity (Gemini) | "berikan saya penjelasan tentang apa itu RPC dan MQ" | AI menjelaskan konsep RPC (komunikasi sinkron, butuh respon instan, seperti menelepon) dan MQ (komunikasi asinkron, pesan ditampung di broker, seperti kotak surat). AI juga memberikan tabel perbandingan kapan harus menggunakan masing-masing teknologi. | Saya mempelajari perbedaan mendasar antara komunikasi sinkron dan asinkron untuk menjadi dasar argumen pemilihan arsitektur di laporan tugas. |
| 08 Oktober 2026 | Antigravity (Gemini) | "apa plus jika saya menggunakan RPC dan MQ" | AI menjelaskan keuntungan menggabungkan keduanya (arsitektur hibrida): respons cepat (RPC) untuk proses kritis, dan keandalan/penahan beban (MQ) untuk proses background. Keuntungan lainnya termasuk ketahanan terhadap lonjakan trafik (*load leveling*), isolasi kegagalan, dan skalabilitas independen. | Saya menggunakan poin "keseimbangan kecepatan dan keandalan" serta "isolasi kegagalan" sebagai landasan analisis untuk mendesain sistem yang tangguh saat jam sibuk/trafik tinggi di studi kasus aplikasi pemesanan (FoodGo). |
