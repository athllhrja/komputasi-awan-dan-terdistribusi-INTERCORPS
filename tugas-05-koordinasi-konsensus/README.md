# Tugas 5 (Pekan 5) — Koordinasi & Konsensus

**Materi terkait:** Physical/Logical Clock, Election Algorithm (Bully/Raft).

## Studi Kasus

Terjadi konflik urutan waktu pada pesanan FoodGo (dua server mencatat urutan pesanan berbeda karena jam tidak sinkron), dan sistem membutuhkan satu **"Node Leader"** untuk mengelola antrean pesanan pusat agar tidak terjadi konflik pemrosesan ganda.

## Solusi yang Diimplementasikan

Kelompok mengimplementasikan simulasi **Bully Algorithm** dengan **5 node virtual**. Setiap node berjalan sebagai proses Python terpisah pada port berbeda dan berkomunikasi melalui TCP socket di `localhost`.

Pesan yang digunakan:

- `ELECTION` — memulai pemilihan leader (dikirim ke node ber-ID lebih tinggi)
- `OK` — balasan dari node ber-ID lebih tinggi yang masih hidup
- `COORDINATOR` — pengumuman leader baru ke semua node
- `PING` — monitoring periodik untuk mengecek apakah leader masih aktif

Logika utama ada di `src/node.py` pada fungsi:

- `on_message` — menangani ELECTION, OK, dan COORDINATOR
- `start_election` — mengirim ELECTION dan memutuskan apakah perlu `declare_leader`
- `declare_leader` — menetapkan diri sebagai leader dan broadcast COORDINATOR
- `monitor_leader` — mendeteksi leader mati lalu memicu election ulang

## Hasil Pengujian

### Skenario 1: Start normal

- **Leader yang terpilih:** Node 5
- **Observasi:** Kelima node dijalankan pada proses terpisah. Karena waktu start tidak sepenuhnya bersamaan, sempat muncul leader sementara pada node ber-ID lebih rendah. Setelah node 5 aktif dan mengbroadcast `COORDINATOR`, semua node menyepakati Node 5 sebagai leader (ID tertinggi). Node 5 kemudian menerima `PING` berkala dari node lain sebagai tanda monitoring aktif.
- **Bukti:** folder `bukti/` (log skenario 1 per node)

### Skenario 2: Leader dimatikan

- **Leader baru yang terpilih:** Node 4
- **Waktu deteksi:** sekitar 3–5 detik setelah Node 5 dimatikan (interval monitoring ±3 detik + timeout election ±2 detik)
- **Observasi:** Setelah Node 5 tidak merespons `PING`, node lain mendeteksi kegagalan leader dan memulai election ulang. Tidak ada pesan `OK` dari ID lebih tinggi karena Node 5 sudah tidak aktif. Node 4, sebagai ID tertinggi yang masih hidup, menetapkan diri sebagai leader dan mengbroadcast `COORDINATOR`. Node 1–3 memperbarui `leader_id` menjadi 4.
- **Bukti:** folder `bukti/` (log skenario 2 per node)

## Analisis

### Kenapa sistem membutuhkan leader

Tanpa leader tunggal, beberapa node bisa memproses antrean pesanan secara independen dan menghasilkan urutan atau status yang berbeda. Satu leader memastikan ada otoritas pusat untuk mengelola antrean, sehingga konflik pemrosesan ganda dapat ditekan. Ini relevan dengan masalah FoodGo terkait urutan pesanan dan konsistensi antar server.

### Kenapa Bully Algorithm selalu memilih node ber-ID tertinggi yang masih hidup

Pada Bully Algorithm, node hanya mengirim `ELECTION` ke peer dengan ID lebih besar. Jika ada balasan `OK`, berarti masih ada kandidat yang “lebih kuat”, sehingga node tersebut tidak boleh menyatakan diri sebagai leader. Jika tidak ada `OK` dalam batas waktu, berarti tidak ada node ber-ID lebih tinggi yang hidup, sehingga node itu berhak menjadi leader dan mengirim `COORDINATOR`.

Akibatnya:

- saat semua node hidup → leader = Node 5
- saat Node 5 mati → leader = Node 4
- pola yang sama berlanjut ke ID lebih rendah jika node tinggi lain ikut mati

### Trade-off Bully vs Raft

| Aspek | Bully | Raft |
|---|---|---|
| Cara pilih leader | Berdasarkan ID tertinggi yang hidup | Berdasarkan term & voting mayoritas |
| Kompleksitas | Relatif sederhana | Lebih kompleks |
| Jumlah pesan saat election | Bisa banyak (terutama dari banyak node sekaligus) | Lebih terstruktur lewat request vote |
| Kelemahan | Bergantung penomoran ID; ada jeda tanpa leader selama election | Implementasi dan debugging lebih berat |
| Cocok untuk | Simulasi/koordinasi skala kecil seperti tugas ini | Sistem produksi yang butuh toleransi partisi lebih kuat |

Selama proses election berlangsung, sistem sempat tidak memiliki leader aktif (jeda koordinasi), sehingga ada risiko keputusan tertunda sampai `COORDINATOR` baru diumumkan.

Untuk simulasi 5 node di satu mesin, Bully sudah cukup untuk menunjukkan pemilihan dan penggantian leader secara otomatis. Untuk sistem FoodGo skala besar di banyak server, Raft biasanya lebih dipertimbangkan karena pemilihan leader tidak semata-mata bergantung pada ID statis.
