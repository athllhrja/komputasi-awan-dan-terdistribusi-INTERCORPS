# Tugas 3 (Pekan 3) — Efisiensi Proses & Kontainer

**Materi terkait:** Threading, Virtualization, Containers.

## Studi Kasus

Server FoodGo boros sumber daya karena setiap permintaan pesanan masuk diproses sebagai **proses baru yang berat** (mis. `fork()` proses OS penuh per request). Saat 100 pesanan masuk bersamaan, server kehabisan memori karena tiap proses membawa overhead-nya sendiri.

## Tugas Kelompok

1. Implementasikan **simulasi pesanan masuk** di Python (`src/order_simulator.py`) yang memproses banyak pesanan **secara konkuren memakai multithreading** (bukan multiprocessing, bukan sekuensial biasa).
2. Program harus mensimulasikan **race condition yang sengaja dibuat lalu diperbaiki** — buktikan pemahaman kalian tentang `Lock`/sinkronisasi dengan cara:
   - Jalankan dulu versi TANPA lock, tunjukkan hasil counter yang salah (screenshot/log).
   - Perbaiki dengan `threading.Lock()`, tunjukkan hasil counter yang benar.
   - Tulis perbandingan ini di `JURNAL.md`.
3. Paketkan program ke dalam **Docker container** (`Dockerfile` disediakan skeleton-nya, lengkapi bagian yang kosong).
4. Jalankan container di laptop, buktikan program tetap berjalan benar di dalam container (screenshot/video di `bukti/`).

## Skeleton yang Disediakan

- `src/order_simulator.py` — kerangka program dengan `# TODO` di bagian logika inti (worker function, penggunaan lock, agregasi hasil). **Kalian wajib mengisi bagian TODO sendiri** — ini bagian penilaian utama.
- `requirements.txt` — kosong/minimal (program ini sengaja hanya pakai standard library Python, tidak perlu dependency eksternal).
- `Dockerfile` — kerangka dengan beberapa baris `# TODO`, lengkapi agar image bisa di-build dan dijalankan.

## Cara Menjalankan (Setelah Skeleton Dilengkapi)

Tanpa Docker (langsung di laptop, untuk debugging cepat):
```bash
cd tugas-03-multithreading-container
python3 src/order_simulator.py
```

Dengan Docker (wajib untuk submission akhir):
```bash
cd tugas-03-multithreading-container
docker build -t foodgo-order-sim .
docker run --rm foodgo-order-sim
```

## Struktur Submission

```
tugas-03-multithreading-container/
├── README.md          # Analisis: race condition, perbaikan, kenapa threading (bukan multiprocessing/proses OS)
├── JURNAL.md           # Log sebelum/sesudah lock, error yang ditemui saat build Docker
├── Dockerfile
├── requirements.txt
├── src/
│   └── order_simulator.py
└── bukti/              # Screenshot/video: hasil counter salah (tanpa lock), hasil benar (dengan lock), container jalan
```

## Rubrik Penilaian (Tugas 3)

| Komponen | Bobot | Kriteria |
|---|---|---|
| Implementasi multithreading benar | 30% | Worker benar-benar konkuren (bukan `time.sleep` yang menyamarkan sekuensial), pakai `threading` |
| Bukti race condition & perbaikan lock | 25% | Ada bukti nyata (log/screenshot) sebelum & sesudah, bukan cuma klaim di teks |
| Dockerfile & eksekusi container | 20% | Image ter-build, container jalan dan hasilkan output yang sama seperti tanpa Docker |
| Analisis (kenapa threading, bukan proses berat) | 15% | Mengaitkan balik ke masalah "server boros resource" di studi kasus |
| Proses & kontribusi kelompok | 10% | `JURNAL.md`, commit history |

## Batasan Penggunaan AI (Level 2)

Kebijakan **Level 2 (AI Assisted Idea Generation & Structuring)** berlaku — lihat [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Boleh bertanya ke AI soal opsi umum menangani race condition (mis. "apa saja cara sinkronisasi thread di Python"); **tidak boleh** meminta AI menuliskan isi bagian `# TODO` di `order_simulator.py`/`Dockerfile`. Catat pemakaian AI di "Log Penggunaan AI" pada `JURNAL.md`.

- Bagian `# TODO` di `order_simulator.py` dan `Dockerfile` sengaja dikosongkan — solusi yang identik persis antar kelompok (termasuk nama variabel, komentar) akan diperiksa lebih lanjut.
- `JURNAL.md` wajib menunjukkan bukti nyata percobaan **sebelum** (race condition muncul) dan **sesudah** (`Lock()` dipasang) — bukan cuma klaim tanpa data pembanding.

## Analisis Race Condition dan Penggunaan Multithreading

### 1. Implementasi Simulasi Pesanan

Program menyimulasikan pemrosesan 100 pesanan FoodGo menggunakan 10 thread pekerja. Setiap thread menerima 10 pesanan dan menjalankan fungsi `worker()`, yang memanggil `process_order()` untuk setiap pesanan.

Seluruh thread dijalankan menggunakan `start()` sebelum program menunggu penyelesaiannya melalui `join()`. Dengan demikian, pekerjaan antar-thread dapat berlangsung secara konkuren, dan counter baru ditampilkan setelah seluruh thread selesai.

Pengujian menggunakan dua file:

- `src/order_simulator.py`: simulasi tanpa Lock.
- `src/order_simulator_lock.py`: simulasi dengan Lock.

Kedua versi menggunakan jumlah pesanan, jumlah thread, pembagian pekerjaan, dan operasi pembaruan counter yang sama. Perbedaan utamanya adalah perlindungan Lock pada pembaruan counter.

### 2. Race Condition pada Versi Tanpa Lock

Variabel `processed_count` digunakan bersama oleh seluruh thread untuk mencatat jumlah pesanan yang telah diproses. Pembaruan counter melibatkan pembacaan nilai, penambahan satu, dan penulisan nilai baru.

Pada percobaan awal menggunakan increment biasa tanpa Lock, enam pengujian menghasilkan counter 100. Hasil tersebut menunjukkan bahwa race condition belum terlihat pada percobaan awal. Hasil yang benar dalam sejumlah percobaan belum membuktikan bahwa akses terhadap counter sudah aman.

Untuk memperlihatkan race condition, kode kemudian memisahkan pembacaan dan penulisan counter serta menambahkan `time.sleep(0.001)` di antaranya. Jeda ini sengaja digunakan dalam simulasi untuk memberikan kesempatan kepada thread lain membaca nilai counter yang sama sebelum pembaruan selesai.

Sebagai contoh, thread A dan thread B sama-sama membaca counter 9. Keduanya menambahkan satu dan menulis 10. Padahal, setelah dua penambahan, counter seharusnya menjadi 11. Pembaruan yang saling menimpa ini disebut *lost update*.

Berdasarkan pengujian Athallah Radja yang dicatat dalam `JURNAL.md`, versi tanpa Lock setelah perubahan menghasilkan:

| Percobaan | Target Counter | Counter Aktual |
|---|---:|---:|
| 1 | 100 | 41 |
| 2 | 100 | 41 |
| 3 | 100 | 42 |
| 4 | 100 | 38 |
| 5 | 100 | 43 |
| 6 | 100 | 44 |

Seluruh percobaan menghasilkan counter di bawah target, yaitu antara 38–44. Selisih ini menunjukkan hilangnya pembaruan pada counter. Counter yang rendah tidak berarti hanya sejumlah itu pesanan yang dijalankan; masalahnya terletak pada pencatatan jumlah pesanan yang diperbarui secara bersamaan.

### 3. Perbaikan Menggunakan Lock

Perbaikan dilakukan menggunakan satu objek `threading.Lock()` yang dipakai bersama oleh seluruh thread. Rangkaian membaca counter, menjalankan jeda simulasi, dan menulis nilai baru ditempatkan di dalam blok `with lock:`.

Bagian tersebut menjadi *critical section*, yaitu bagian program yang mengakses data bersama dan perlu dilindungi. Ketika satu thread memegang Lock, thread lain harus menunggu sebelum memasuki bagian yang sama. Setelah pembaruan selesai, Lock dilepas dan thread berikutnya dapat membaca nilai counter terbaru.

Jeda pada pembaruan counter dipertahankan pada kedua versi agar perbandingannya setara. Sementara itu, simulasi pekerjaan pesanan tetap berada di luar Lock agar pekerjaan antar-thread tetap dapat berlangsung secara konkuren.

Berdasarkan pengujian Calvin Immanuel Lado dalam jurnal, hasil perbandingannya adalah:

| Percobaan | Tanpa Lock | Dengan Lock | Target |
|---|---:|---:|---:|
| 1 | 41 | 100 | 100 |
| 2 | 41 | 100 | 100 |
| 3 | 42 | 100 | 100 |
| 4 | 38 | 100 | 100 |
| 5 | 43 | 100 | 100 |
| 6 | 44 | 100 | 100 |

Versi dengan Lock menghasilkan counter 100 pada seluruh enam percobaan. Hasil ini menunjukkan bahwa perlindungan terhadap rangkaian pembaruan counter berhasil mencegah kehilangan penambahan pada pengujian tersebut.

Penggunaan Lock berfokus pada ketepatan data. Lock juga menimbulkan waktu tunggu ketika beberapa thread ingin memasuki critical section yang sama, sehingga penggunaannya perlu dibatasi pada bagian yang membutuhkan perlindungan.

### 4. Alasan Memilih Threading Dibanding Multiprocessing

Masalah awal FoodGo adalah penggunaan proses OS baru untuk setiap permintaan pesanan, yang menambah beban sumber daya. Pada simulasi ini, 100 pesanan ditangani oleh 10 thread dalam satu proses.

Thread berbagi ruang memori dalam proses yang sama. Hal ini memudahkan penggunaan data bersama seperti `processed_count`, tetapi juga menimbulkan kebutuhan sinkronisasi agar pembaruannya tidak saling menimpa.

Simulasi pekerjaan menggunakan `time.sleep()` untuk mewakili waktu tunggu, seperti menunggu respons layanan atau operasi I/O. Threading sesuai untuk pola pekerjaan tersebut karena thread lain dapat melanjutkan pekerjaan ketika suatu thread menunggu.

Multiprocessing menggunakan proses terpisah. Penggabungan hasil atau penggunaan data bersama memerlukan mekanisme komunikasi antarproses atau shared memory. Untuk simulasi sederhana yang didominasi waktu tunggu ini, pendekatan tersebut menambah kebutuhan pengelolaan yang belum diperlukan.

Multiprocessing tetap relevan untuk pekerjaan komputasi berat yang membutuhkan pemanfaatan beberapa inti CPU. Pada CPython dengan GIL aktif, eksekusi kode Python oleh thread dibatasi sehingga threading tidak otomatis mempercepat pekerjaan CPU-bound.

Pemilihan threading pada tugas ini didasarkan pada karakter simulasi dan tujuan menghindari pembuatan proses baru untuk setiap pesanan. Pengujian belum mengukur penggunaan memori maupun membandingkan waktu eksekusi dengan multiprocessing, sehingga besarnya penghematan sumber daya belum dapat dinyatakan secara kuantitatif.

### 5. Pengujian di Dalam Docker

Berdasarkan pengujian Krisna Putra Wicaksana yang dicatat dalam jurnal, hasil eksekusi di laptop dan Docker adalah:

| Lingkungan | Metode | Counter Aktual | Target |
|---|---|---:|---:|
| Laptop | Tanpa Lock | 38 | 100 |
| Laptop | Dengan Lock | 100 | 100 |
| Docker | Tanpa Lock | 38 | 100 |
| Docker | Dengan Lock | 100 | 100 |

Pada pengujian tersebut, versi tanpa Lock tetap mengalami kehilangan pembaruan counter ketika dijalankan dalam container. Versi dengan Lock menghasilkan counter yang sesuai target pada kedua lingkungan.

Hasil ini menunjukkan bahwa pengemasan aplikasi dalam Docker tidak menggantikan kebutuhan sinkronisasi di dalam program. Angka 38 merupakan hasil percobaan yang dicatat, bukan nilai yang harus selalu muncul pada setiap eksekusi tanpa Lock.

### 6. Kesimpulan

Simulasi memperlihatkan bahwa penggunaan beberapa thread untuk memperbarui counter bersama memerlukan sinkronisasi. Setelah kesempatan terjadinya race condition diperjelas melalui jeda antara pembacaan dan penulisan, enam pengujian tanpa Lock menghasilkan counter 38–44 dari target 100.

Penggunaan `threading.Lock()` pada seluruh rangkaian pembaruan counter menghasilkan nilai 100 pada seluruh enam pengujian. Pengujian Docker juga mencatat hasil yang sesuai target pada versi dengan Lock.

Threading sesuai dengan simulasi FoodGo yang banyak melibatkan waktu tunggu dan menggunakan sejumlah pekerja dalam satu proses. Lock melengkapi pendekatan tersebut dengan menjaga ketepatan pembaruan data bersama.
