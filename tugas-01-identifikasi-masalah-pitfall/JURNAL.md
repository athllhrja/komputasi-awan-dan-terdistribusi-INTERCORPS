# Jurnal Proses — Tugas 1

> Isi jurnal ini selama proses diskusi berlangsung, bukan ditulis ulang rapi di akhir. Tulis dengan gaya bebas — poin diskusi, kebuntuan, perubahan pikiran.

## [17 September 2026]
- Peserta: [ANDI ATHALLAH RADJA MALIQ MUHAMMAD, KRISNA PUTRA WICAKSANA, CALVIN IMMANUEL LADO]

- Poin diskusi: Membaca skenario FoodGo bersama-sama. Kita mengidentifikasi kenapa pas promo jam makan siang servernya selalu modar.
- Poin utama yang langsung kelihatan: kodenya ada komentar `# network is always reliable, no need for retry` dan tidak ada timeout. Ini jelas-    jelas pitfall 1 Deutsch (*The network is reliable*).
- server crash total: ternyata karena arsitekturnya masih monolitik run di 1 proses yang sama. Waktu modul notifikasi kurir sibuk, modul pesanan ikut mati.
  
- Perbedaan pendapat (jika ada): ...

## Review Silang
- ANDI ATHALLAH RADJA MALIQ MUHAMMAD Komentar ke CALVIN IMMANUEL LADO: Catatan soal user nge-klik tombol berulang kali saat aplikasi lambat sangat pas untuk memperkuat bagian dampak Latency is Zero.

- CALVIN IMMANUEL LADO Komentar ke KRISNA PUTRA WICAKSANA: Di draf Krisna, istilah cascading failure dan jitter/backoff memang sudah tertulis jelas di bagian Trade-off & Solusi, jadi poin review ini terbukti valid dan sudah direvisi.

- KRISNA PUTRA WICAKSANA Komentar ke ANDI ATHALLAH RADJA MALIQ MUHAMMAD: Di draf Radja, bagian Trade-off baru menyebut "maintenance jauh lebih sulit". Menyebutkan poin operasional (tracing/Saga pattern) di jurnal akan membuat alasan perubahan drafnya terlihat makin logis.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
 17 Sep 2026 | Gemini | Pattern arsitektur apa yang digunakan untuk mengatasi service hanging akibat tidak adanya timeout dan retry pada jaringan terdistribusi? | AI menyarankan penerapan Timeout, Exponential Backoff dengan Jitter, dan Circuit Breaker Pattern. | Mempelajari konsep dasar pattern tersebut, lalu tulis analisisnya menggunakan contoh kasus FoodGo (modul pesanan ke modul pembayaran) serta dampaknya pada thread pool server. |
| 17 Sep 2026 | Gemini | Jelaskan pitfall: "the network is reliable", "latency is zero", "bandwidth is infinite", "the network is secure", "topology doesn't change", "there is one administrator", "transport cost is zero", "the network is homogeneous" dan single point of failure karena arsitektur monolitik. | AI menjelaskan konsep "The 8 Fallacies of Distributed Computing" beserta realita dan solusinya, serta memaparkan kelemahan struktural dari Single Point of Failure (SPOF) pada aplikasi monolitik.| Menganalisis contoh dampak nyata pada ekosistem terdistribusi yang masih menggunakan arsitektur monolitik sebagai pusat layanannya.|
|17 Sep 2026 | Gemini | Berikan contoh dampak yang akan terjadi jika sebuah sistem terdistribusi menggunakan Arsitektur Monolitik sebagai Single Point of Failure. | AI menjabarkan 4 dampak kritis (Total Downtime, Cascading Failure, Scalability Bottleneck, Risiko Deployment) dan mengilustrasikannya melalui studi kasus e-commerce yang lumpuh saat Flash Sale. | Mempelajari strategi migrasi dari arsitektur monolitik ke microservices untuk memitigasi risiko SPOF dan bottleneck pada sistem. |
|17 Sep 2026|ChatGPT|Jelaskan trade-off dari masing-masing solusi untuk mengatasi masalah Latency is Zero pada sistem terdistribusi.|AI menjelaskan bahwa setiap solusi memiliki kelebihan dan kekurangan, seperti komunikasi asynchronous yang dapat mengurangi waktu tunggu tetapi membuat sistem lebih kompleks, caching yang dapat mempercepat akses tetapi berisiko menghasilkan data yang tidak terbaru, serta optimasi komunikasi yang dapat mengurangi latency tetapi membutuhkan sumber daya dan konfigurasi tambahan.|Mempelajari kelebihan dan kekurangan dari setiap solusi, lalu membandingkan trade-off-nya berdasarkan kebutuhan sistem dan menerapkannya pada analisis kasus sistem terdistribusi.|
|17 Sep 2026|ChatGPT|Apa solusi untuk masalah yang diakibatkan pitfall Latency is Zero pada sistem terdistribusi?|AI menyarankan penggunaan asynchronous communication agar client tidak harus menunggu response, penggunaan handler terpisah untuk menangani response, serta mengurangi komunikasi antar-node melalui partitioning, caching, dan replication.|Mempelajari konsep setiap solusi, kemudian menyesuaikannya dengan kasus sistem terdistribusi yang dianalisis dan menjelaskan bagaimana solusi tersebut dapat mengurangi dampak latency terhadap performa sistem.|
|17 Sep 2026|ChatGPT|Masalah apa saja yang dapat disebabkan oleh pitfall Latency is Zero pada sistem terdistribusi?|AI menjelaskan bahwa mengabaikan latency jaringan dapat menyebabkan response aplikasi menjadi lambat, sistem tidak responsif, performa menurun akibat waktu tunggu komunikasi antar-node, masalah semakin terlihat pada jaringan WAN, serta pengalaman pengguna menjadi buruk.|Memahami hubungan antara latency dengan komunikasi synchronous dan waktu tunggu antar-node, kemudian merangkum dampaknya dan menghubungkannya dengan contoh komunikasi Client–Server pada sistem terdistribusi.|
|17 Sep 2026|ChatGPT|Dari slide materi ini, tolong jelaskan secara ringkas jenis pitfall yang sering terjadi pada sistem terdistribusi beserta contohnya.|AI menjelaskan 8 pitfall utama, yaitu The network is reliable, The network is secure, The network is homogeneous, The topology does not change, Latency is zero, Bandwidth is infinite, Transport cost is zero, dan There is one administrator, beserta contoh sederhana dari masing-masing pitfall.|Mempelajari makna setiap pitfall, kemudian merangkum definisi dan contohnya dalam bentuk tabel agar lebih mudah dipahami dan digunakan dalam analisis kasus sistem terdistribusi.|
