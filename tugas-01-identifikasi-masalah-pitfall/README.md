# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** [INTERCOROPS]

| Nama | NIM | Kontribusi |
|---|---|---|
| [ANDI ATHALLAH RADJA] | [103072400034] | [Single point of failure karena arsitektur monolitik] |
| [KRISNA PUTRA WICAKSANA] | [103072400079] | [Network is Always Reliable] |
| [CALVIN IMMANUEL LADO] | [103072400158] | [Latency Is Zero] |

## Pitfall 1: Single point of failure karena arsitektur monolitik — ditulis oleh ANDI ATHALLAH RADJA

**Bukti di skenario:** "Saat trafik naik, satu server yang menangani semua modul (pesanan, pembayaran, notifikasi kurir) kewalahan karena semuanya berjalan di satu proses monolitik yang sama"

**Kenapa ini keliru:** karena sistem monolitik ini menggabungkan semua resource untuk komputasi. jika ada satu modul yang menggunakan terlalu banyak resource maka dampaknya tidak akan terisolisasi yang bisa mengakibatkan seluruh proses server mati, dan juga sistemnya tidak bisa di scale per modul sesuai dari kebutuhan modul masing masing

**Dampak ke FoodGo:** dampak pada foodgo nya sendiri adalah jika saat jam makan siang atau adanya sebuah promo maka modul pesanan akan menghabiskan semua resource nya dampak nya adalah karena modul pembayaran dan notifikasi kurir nya itu dalam satu proses yang sama maka semuanya akan kewalahan akibatnya server akan crash out dan harus direstart manualt

**Solusi desain awal:** solusi yang saya sarankan adalah dengan menggunakan Microservices jadi semua modul akan dijalankan secara terpisah dengan pemisahan service ini semua modul bisa discale secara indpenden

**Trade-off:** maintenance akan jauh lebih sulit karena setiap sistem punya enviroment nya masing masing

---

## Pitfall 2: Network is Always Reliable — ditulis oleh KRISNA PUTRA WICAKSANA

Bukti di skenario: "Pada code skenario mereka menulis asumsi seperti # network is always reliable, no need for retry dan tidak ada timeout sama sekali pada pemanggilan antar service (modul pesanan memanggil modul pembayaran dan menunggu tanpa batas waktu)"

Kenapa ini keliru: Jaringan fisik (LAN maupun internet) tidak pernah 100% selalu berjalan dengan baik. Selalu ada risiko packet loss, network congestion, fluktuasi sinyal, hingga gangguan pada gateway/API payment provider pihak ketiga. Kalau kita berpikir jaringan selalu lancar, aplikasi jadi seakan-akan yakin setiap request pasti sampai dan responsnya langsung diterima.

Dampak ke FoodGo: Modul pesanan mencoba terhubung ke modul pembayaran tapi jaringan bermasalah, misalnya payment gateway lagi down atau nggak bisa diakses. modul pesanan bisa terus menunggu karena tidak ada batas waktu (timeout). Akibatnya, thread di aplikasi ikut tertahan karena menunggu respons yang sebenarnya tidak kunjung datang. Saat pesanan lagi ramai, misalnya waktu jam makan siang, thread pool server bisa cepat penuh. Lama-lama resource server seperti memory dan CPU ikut terkuras sampai akhirnya server crash dan harus di-restart secara manual.

Solusi desain awal:

1. Timeout & Retry Strategy dengan Exponential Backoff + Jitter: Tentukan batas waktu maksimal, misal timeout 3 detik. Jika tidak ada respons, lakukan retry secara berkala dengan jeda waktu yang meningkat secara acak (jitter) agar tidak membombardir jaringan.

2. Circuit Breaker Pattern: Jika modul pembayaran gagal berturut-turut hingga batas ambang tertentu, circuit breaker akan langsung membuka dan mempercepat kegagalan tanpa mencoba memanggil modul pembayaran lagi secara terus-menerus.
   
Trade-off: Kalau mekanisme retry tidak dibatasi dengan baik, justru bisa bikin kondisi cascading failure makin parah karena payment gateway yang sebenarnya lagi berusaha pulih malah mendapat beban request tambahan. Selain itu, penggunaan fail-fast bikin sistem harus punya solusi cadangan (fallback mechanism) untuk menangani kondisi seperti ini. Misalnya, status pesanan bisa diubah jadi "Menunggu Pembayaran / Pending" daripada langsung dianggap gagal.

---

## Pitfall 3: Latency Is Zero — ditulis oleh CALVIN IMMANUEL LADO

Bukti di skenario: Pada skenario dijelaskan bahwa modul pesanan memanggil modul pembayaran dan menunggu tanpa batas waktu. Selain itu, saat trafik meningkat, aplikasi menjadi sangat lambat dan beberapa permintaan mengalami timeout. Hal ini menunjukkan bahwa FoodGo belum memperhitungkan waktu yang dibutuhkan saat modul saling berkomunikasi.

Kenapa ini keliru: Hal ini keliru karena beranggapan bahwa komunikasi antar komputer atau antar-service terjadi secara instan. Padahal, saat suatu service mengirim request ke service lain, dibutuhkan waktu untuk mengirim data melalui jaringan untuk memproses request dan mengirimkan response kembali. Pada FoodGo, modul pesanan mengirim permintaan ke modul pembayaran dan menunggu hasilnya. Jika modul pembayaran sedang sibuk dan membutuhkan waktu lebih lama, modul pesanan juga akan ikut menunggu. Jika banyak permintaan terjadi bersamaan, waktu tunggu akan semakin lama dan membuat aplikasi menjadi lambat

Dampak ke FoodGo: Saat trafik meningkat, modul pembayaran menerima lebih banyak permintaan sehingga prosesnya bisa menjadi lebih lambat karena modul pesanan menunggu respons dari modul pembayaran sehingga banyak request yang tertahan.

Solusi desain awal: Solusi yang dapat digunakan adalah asynchronous communication. Dengan cara ini, modul pesanan tidak harus terus menunggu respons dari modul pembayaran. Jadi setelah mengirim request, proses dapat melanjutkan pekerjaan lain dan respons pembayaran dapat diproses ketika sudah diterima.

Trade-off: Penggunaan asynchronous communication membuat sistem menjadi lebih kompleks. FoodGo harus mengatur respons yang datang belakangan dan menentukan bagaimana status pesanan jika pembayaran belum selesai atau responsnya terlambat.

---

## Kesimpulan Kelompok

FoodGo memiliki beberapa masalah utama, yaitu asumsi bahwa jaringan selalu andal (Pitfall 1), komunikasi antarmodul yang masih bersifat blocking/synchronous (Pitfall 2), serta kurangnya isolasi kegagalan pada arsitektur monolitik (Pitfall 3). Ketika trafik meningkat, kombinasi komunikasi antarmodul tanpa timeout dan beban proses yang menumpuk pada satu server dapat membuat penggunaan CPU dan RAM meningkat dengan cepat (resource exhaustion). Kondisi ini kemudian dapat memicu cascading failure hingga akhirnya server mengalami crash dan harus di-restart secara manual.

Untuk mengatasi masalah tersebut, secara garis besar arsitektur yang disarankan untuk FoodGo adalah:

1. Pemisahan Layanan (Decoupling & Service Isolation) Aplikasi monolitik dapat dipecah menjadi beberapa layanan terpisah (microservices/decoupled services), seperti layanan Pesanan, Pembayaran, dan Notifikasi Kurir. Dengan pemisahan ini, setiap layanan dapat memiliki resource sendiri dan melakukan scaling secara lebih fleksibel sesuai dengan beban masing-masing.
2. Penerapan Ketahanan Jaringan (Resilience Patterns) Pada setiap komunikasi antar-service dan payment gateway eksternal, perlu diterapkan mekanisme seperti Timeout, Exponential Backoff Retry dengan Jitter, dan Circuit Breaker. Mekanisme ini membantu mencegah proses terus menunggu respons yang tidak kunjung datang dan mengurangi risiko thread starvation.
3. Komunikasi Asinkron (Event-Driven Architecture) Untuk proses yang tidak harus langsung selesai saat pengguna melakukan pemesanan, FoodGo dapat menggunakan Message Broker seperti RabbitMQ atau Apache Kafka. Proses seperti Notifikasi Kurir dan pembaruan status pembayaran dapat dijalankan secara asynchronous di background, sehingga proses pemesanan utama tetap responsif meskipun terjadi lonjakan trafik.
