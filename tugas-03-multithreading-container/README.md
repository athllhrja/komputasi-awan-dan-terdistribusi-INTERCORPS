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

### 4. Mengapa Menggunakan Threading Daripada Multiprocessing

Masalah pertama FoodGo disebabkan oleh penggunaan proses OS baru untuk setiap pesanan yang diterima, yang pada gilirannya meningkatkan beban sumber daya. Ini adalah simulasi single-process, dengan 100 pesanan ditangani oleh 10 thread.

Thread termasuk dalam proses yang sama dan berbagi ruang memori. Meskipun ini membuat data bersama seperti processed_count lebih mudah digunakan, hal ini juga menambah kebutuhan sinkronisasi agar pembaruan tidak saling menimpa.

Simulasi pekerjaan menggunakan time. sleep() untuk menunjukkan bahwa diperlukan waktu tertentu, misalnya menunggu respons layanan atau eksekusi I/O. Threading sangat cocok untuk pola beban kerja seperti ini, karena thread lain dapat terus memproses sementara satu thread sedang memantau dan menunggu.

Multiprocessing menggunakan proses yang terpisah. Menggabungkan hasil atau bekerja dengan data yang sama memerlukan mekanisme komunikasi antarproses atau shared memory. Pendekatan ini menimbulkan overhead manajemen yang sebelumnya tidak ada, padahal hal yang akan disimulasikan dengan sederhana dan didominasi waktu tunggu.

Multiprocessing berguna untuk masalah yang berat secara komputasi, di mana beberapa inti CPU perlu digunakan. Pada CPython dengan GIL yang diberlakukan, eksekusi thread akan diserialkan saat menjalankan kode Python, sehingga threading tidak otomatis membantu pekerjaan yang terikat CPU agar berjalan lebih cepat.

Threading dipilih karena sifat simulasi ini (tujuan di sini adalah menghindari pembuatan proses baru untuk setiap pesanan). Pengujian belum melacak penggunaan memori, juga belum menjalankan perbandingan pada waktu eksekusi terhadap multiprocessing, sehingga besarnya penghematan sumber daya tidak dapat dinyatakan dalam angka.

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

Terlihat bahwa, beberapa thread yang memperbarui counter bersama harus disinkronkan dalam simulasi. Ketika kejadian race condition diselidiki lebih lanjut dengan menambahkan penundaan yang lebih kecil antara proses membaca dan menulis, kemudian enam pengujian tanpa Lock menghasilkan nilai penghitung dari 38–44 alih-alih yang benar yaitu 100.

Menggunakan threading. Pada semua enam pengujian, nilai akhir adalah 100 ketika menggunakan Lock ()` pada seluruh rangkaian pembaruan penghitung. Hasil pengujian Docker yang juga sesuai dengan target dicatat pada versi yang mengaktifkan Lock.

Dalam hal ini, threading sangat cocok dengan simulasi FoodGo, di mana kami menggunakan sejumlah pekerja dalam satu proses, semuanya harus menunggu. Lock membangun pendekatan ini dengan jaminannya untuk pembaruan yang benar terhadap data bersama.
