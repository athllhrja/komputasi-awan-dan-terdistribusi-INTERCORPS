# Tugas 6 (Pekan 6) — Penamaan & Resolusi Lokasi

**Materi terkait:** Flat Naming, Structured Naming (DNS), Distributed Hash Table (DHT)/Chord.

## Studi Kasus

Pelanggan FoodGo kesulitan menemukan alamat IP server kurir yang **dinamis** (kurir berpindah lokasi/jaringan, IP-nya sering berubah). FoodGo butuh cara memetakan **ID Kurir** (identitas tetap) ke **alamat IP terkininya** tanpa server pusat tunggal yang jadi bottleneck/single point of failure.

## Tugas Kelompok

Implementasikan **simulasi Chord DHT** sederhana (single-process, tidak perlu jaringan sungguhan — cukup simulasi struktur data & algoritma di satu program Python) yang memetakan ID Kurir ke alamat IP mereka.

Konsep yang harus terlihat jalan dalam simulasi kalian:

1. **Consistent hashing**: ID Kurir dan ID Node di-hash ke ruang angka yang sama (mis. 0–255 untuk kesederhanaan, `m=8` bit).
2. **Ring topology**: node-node diurutkan melingkar berdasarkan hasil hash-nya.
3. **Lookup**: fungsi `lookup(kurir_id)` yang menemukan node mana yang bertanggung jawab menyimpan mapping ID Kurir tersebut → alamat IP-nya (aturan Chord: node dengan ID hash **terkecil yang lebih besar atau sama dengan** hash key, disebut _successor_).
4. **Perubahan topologi**: simulasikan minimal satu node baru bergabung (`join`) atau satu node keluar (`leave`), tunjukkan bagaimana mapping berpindah tanggung jawab ke node lain.

Skeleton disediakan di `src/chord_simulation.py` dengan fungsi hashing dan struktur ring sudah ada — bagian `lookup()`, `join()`, dan `leave()` sengaja dikosongkan.

### Cara Menjalankan

```bash
python3 src/chord_simulation.py
```

## Tugas Analisis (`README.md`)

1. Jelaskan **kenapa DHT/Chord** lebih cocok untuk kasus ini dibanding **flat naming sederhana** (mis. tabel pusat ID→IP) atau **DNS konvensional** — kaitkan dengan sifat "IP kurir sering berubah" dan kebutuhan tanpa titik gagal tunggal.

DHT/Chord lebih cocok digunakan pada kasus FoodGo karena sistem perlu menyimpan dan mencari alamat IP kurir yang dapat berubah sewaktu-waktu. Setiap kurir memiliki ID tetap, sedangkan alamat IP-nya dapat berubah mengikuti lokasi atau jaringan yang digunakan.

Perbandingannya dengan metode lain:

- Flat Naming: Jika menggunakan tabel pusat ID Kurir ke alamat IP, seluruh data bergantung pada satu server. Hal ini dapat menjadi bottleneck dan single point of failure apabila server mengalami gangguan.
- DNS Konvensional: DNS dapat menerjemahkan nama menjadi alamat IP, tetapi perubahan alamat IP tetap membutuhkan pembaruan record dan mekanisme propagasi atau cache. Hal ini kurang fleksibel jika perubahan lokasi kurir terjadi secara dinamis.
- DHT/Chord: Data didistribusikan ke beberapa node berdasarkan hasil hashing. Setiap node bertanggung jawab terhadap rentang hash tertentu sehingga pencarian dapat dilakukan tanpa bergantung pada satu server pusat. Ketika node bergabung atau keluar, hanya sebagian mapping yang perlu dipindahkan.
  Dengan demikian, Chord DHT lebih sesuai untuk FoodGo karena mendukung distribusi data, pencarian berdasarkan ID Kurir, dan perubahan topologi secara dinamis.

2. Gambarkan (boleh pakai Mermaid, lihat Tugas 2) ring topology dari simulasi kalian, tandai node mana yang bertanggung jawab atas ID Kurir mana.

Pada simulasi ini, terdapat empat node awal dengan ID hash 40, 102, 136, dan 177. Setelah node Medan bergabung, ring memiliki lima node. Kemudian node Jakarta keluar sehingga tersisa empat node.

Kondisi setelah node baru bergabung:

```mermaid
flowchart LR
    N40["Node Bandung<br>ID: 40"]
    N102["Node Jakarta-2<br>ID: 102"]
    N123["Node Medan<br>ID: 123<br>Kurir: 012, 088"]
    N136["Node Surabaya<br>ID: 136"]
    N177["Node Jakarta-1<br>ID: 177<br>Kurir: 005, 009"]

    N40 --> N102
    N102 --> N123
    N123 --> N136
    N136 --> N177
    N177 --> N40
```

Kondisi setelah node Jakarta-1 keluar:

```mermaid
flowchart LR
    N40["Node Bandung<br>ID: 40<br>Kurir: 005, 009"]
    N102["Node Jakarta-2<br>ID: 102"]
    N123["Node Medan<br>ID: 123<br>Kurir: 012, 088"]
    N136["Node Surabaya<br>ID: 136"]

    N40 --> N102
    N102 --> N123
    N123 --> N136
    N136 --> N40
```

3. Jelaskan apa yang terjadi pada mapping saat sebuah node **keluar** dari ring (siapa yang mengambil alih tanggung jawabnya) — dukung dengan output program.
   Ketika node node-jakarta-1 dengan ID 177 keluar dari ring, data kurir yang sebelumnya menjadi tanggung jawab node tersebut harus dialihkan ke successor berikutnya.

Berdasarkan hasil simulasi, sebelum node keluar terdapat dua data kurir yang disimpan pada node 177:

- kurir-005 (hash=175)
- kurir-009 (hash=170)
  Setelah node 177 keluar, kedua data tersebut berpindah ke node Bandung dengan ID 40.

Hal ini terjadi karena node 40 menjadi successor berikutnya dalam ring melalui mekanisme wrap-around.

bukti output:
--- Sebuah node keluar ---
[LEAVE] Node 'node-jakarta-1' (id=177) keluar dari ring
-> Data 'kurir-005' (hash=175) pindah dari node 177 ke node 40
-> Data 'kurir-009' (hash=170) pindah dari node 177 ke node 40

Hasil tersebut menunjukkan bahwa sistem tetap dapat menemukan data kurir meskipun salah satu node keluar dari ring. Perubahan ini tidak mengharuskan seluruh data dipindahkan, melainkan hanya data yang sebelumnya menjadi tanggung jawab node yang keluar.

## Kesimpulan Analisis

Berdasarkan analisis dan simulasi, DHT/Chord sesuai dengan kebutuhan FoodGo untuk memetakan ID kurir yang tetap ke alamat IP yang dapat berubah. Pembagian tanggung jawab mapping ke beberapa node mengurangi ketergantungan pada server pusat, sementara pembaruan mapping tetap diperlukan saat IP kurir berubah. Mekanisme consistent hashing dan successor memungkinkan penyesuaian tanggung jawab ketika topologi ring berubah. Saat node Medan bergabung, mapping kurir-012 dan kurir-088 beralih ke node 123. Ketika node Jakarta-1 keluar, mapping kurir-005 dan kurir-009 dialihkan dari node 177 ke node 40 melalui wrap-around. Perubahan tersebut hanya memengaruhi sebagian mapping sehingga seluruh data tidak perlu dipindahkan. Hasil simulasi menunjukkan bahwa mapping tetap dapat ditemukan setelah perubahan topologi yang diuji. Namun, karena simulasi berjalan dalam satu proses, ketahanan terhadap kegagalan node secara mendadak belum diuji dan memerlukan pengembangan lebih lanjut.

## Struktur Submission

```
tugas-06-penamaan-dht/
├── README.md      # Analisis + diagram ring
├── JURNAL.md
├── src/
│   └── chord_simulation.py
└── bukti/          # Output program (screenshot/log) untuk skenario join & leave
```

## Rubrik Penilaian (Tugas 6)

| Komponen                               | Bobot | Kriteria                                                        |
| -------------------------------------- | ----- | --------------------------------------------------------------- |
| Implementasi lookup/join/leave benar   | 35%   | Consistent hashing & successor lookup sesuai aturan Chord       |
| Bukti perubahan topologi (join/leave)  | 25%   | Output menunjukkan mapping berpindah dengan benar               |
| Analisis kenapa DHT vs flat naming/DNS | 25%   | Argumen spesifik ke kasus IP kurir dinamis, bukan definisi umum |
| Proses & kontribusi kelompok           | 15%   | `JURNAL.md`, commit history                                     |

## Batasan Penggunaan AI (Level 2)

Kebijakan **Level 2 (AI Assisted Idea Generation & Structuring)** berlaku — lihat [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Boleh bertanya konsep umum consistent hashing/Chord ke AI; **tidak boleh** meminta AI menuliskan isi `# TODO` di `src/chord_simulation.py` (`find_successor`, `join`, `leave`, dst). Catat pemakaian AI di "Log Penggunaan AI" pada `JURNAL.md`.

- `README.md` wajib menelusuri manual (langkah demi langkah) bagaimana `lookup()` menemukan successor untuk salah satu ID Kurir contoh yang dipakai di `chord_simulation.py` — bukan cuma menempelkan output program.
