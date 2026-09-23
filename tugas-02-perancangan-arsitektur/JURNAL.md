# Jurnal Proses — Tugas 2

## 23 September 2026
- Opsi arsitektur yang dipertimbangkan:
- Andi Athallah Radja : saya mempertibangkan untuk menggunakan arsitektur Pub-Sub karena dari hasil analisis sebelumnya ditemukan bahwa ada masalah pada modul pembayaran yang menunggu tanpa batas waktu dengan menggunakan Pub-sub masalah ini bisa dieliminasi karena pengguanaan sistem Asynchronous Decoupling yang dimana nantinya akan ada decoupling space dan decoupling time yang membuat modul pemesanan tidak perlu tahu ip port atau api dari modul pembayaran yang dibutuhkan cuma alamat message broker
   
- Kenapa akhirnya pilih [SOA/Pub-Sub]: ...
- Revisi diagram (versi 1 → versi 2, apa yang berubah dan kenapa): ...
- Draft Diagram 1 dari Andi Athallah radja
- ```mermaid
  graph TD
      Client[Aplikasi Pelanggan] -->|HTTP Request| OrderSvc[Modul Pesanan]
      
      Broker{Message Broker / Kafka}
      
      OrderSvc -->|Publish Event Asinkron:<br>OrderCreated| Broker
      
      Broker -->|Subscribe Event:<br>OrderCreated| PaySvc[Modul Pembayaran]
      PaySvc -->|Publish Event Asinkron:<br>PaymentSuccessful| Broker
      
      Broker -->|Subscribe Event:<br>PaymentSuccessful| RestoSvc[Modul Katalog Resto]
      RestoSvc -->|Publish Event Asinkron:<br>FoodBeingPrepared| Broker
      
      Broker -->|Subscribe Event:<br>FoodBeingPrepared| CourierSvc[Modul Kurir / Notifikasi]
  ```

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 23 September 2026 | Antigravity (Gemini) | "jelaskan dulu kita harus ngapain apa yang perlu saya siapkan untuk Tugas 2"  | AI memberikan ringkasan tugas: merancang arsitektur baru (SOA/Pub-Sub) untuk mengatasi *coupling* di FoodGo, beserta 4 *deliverable* utama (diagram, alur, analisis, trade-off). |  Saya menggunakan ringkasan ini sebagai panduan *checklist* pekerjaan yang harus diselesaikan kelompok. |
| 23 September 2026 | Antigravity (Gemini) |  "mari kita eksplor ke opsi dua (Publish Subscribe), jelaskan secara detail dulu |AI menjelaskan konsep *Event-Driven Architecture* menggunakan Message Broker, memberikan contoh alur *end-to-end* (Pesanan → Broker → Pembayaran → Kurir), dan menjelaskan kenapa Pub-Sub mengatasi *coupling* (spatial & temporal). AI juga memberikan contoh *draft* diagram Mermaid. |  Saya memahami konsep isolasinya dan menyimpulkan sendiri bahwa Pub-Sub memungkinkan skalabilitas mandiri dan mencegah *crash* beruntun. |
