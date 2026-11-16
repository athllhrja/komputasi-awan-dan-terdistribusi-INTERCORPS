# Tugas 7 (Pekan 7) — Konsistensi Data

**Materi terkait:** Data-Centric Consistency (Sequential, Eventual), Client-Centric Consistency.

## Studi Kasus

Data saldo *e-wallet* pelanggan FoodGo berbeda antara server wilayah **Jakarta** dan **Bandung** karena replikasi antar server berjalan lambat. Contoh kasus nyata: pelanggan top-up saldo lewat server Jakarta, lalu dalam hitungan detik memesan makanan lewat aplikasi yang tersambung ke server Bandung — saldo belum ter-update, transaksi ditolak padahal saldo sebenarnya cukup.

## 1. Analisis Sequential vs Eventual + Usulan Solusi
Analisis Model Konsistensi
Pada kasus e-wallet FoodGo, terdapat dua server (Jakarta dan Bandung) yang saling mereplikasi data saldo. Ketika pelanggan melakukan top-up di server Jakarta, data saldo belum tentu langsung tersedia di server Bandung karena adanya delay replikasi. Akibatnya, pelanggan yang segera melakukan pemesanan melalui server Bandung dapat mengalami penolakan transaksi meskipun saldo sebenarnya sudah mencukupi.

Dalam konteks ini, Eventual Consistency tidak cukup. Eventual Consistency memang memungkinkan sistem berjalan lebih cepat karena replikasi dilakukan secara asinkron, namun inkonsistensi sementara yang terjadi sangat berisiko pada data yang menyangkut uang. Berbeda dengan data non-kritis seperti jumlah like di media sosial, kesalahan pada saldo e-wallet dapat menurunkan kepercayaan pengguna dan berdampak langsung pada pengalaman serta reputasi layanan.
Sequential Consistency dapat menjamin bahwa semua replika melihat urutan operasi yang sama. Namun pendekatan ini terlalu ketat dan mahal karena setiap operasi tulis harus menunggu sinkronisasi ke seluruh replika sebelum dianggap selesai. Hal ini dapat meningkatkan latency secara signifikan, terutama pada sistem yang tersebar secara geografis.

Solusi yang lebih tepat adalah menerapkan Client-Centric Consistency, khususnya model Read-Your-Writes. Dengan mekanisme ini, pelanggan yang baru saja melakukan top-up di server Jakarta akan selalu melihat saldo terbarunya sendiri pada operasi baca berikutnya, meskipun proses replikasi ke server Bandung belum selesai. Pendekatan ini memberikan jaminan yang cukup kuat bagi pengguna tanpa harus memaksa seluruh sistem menjadi Sequential Consistency.
## 2. Kerangka Sequence Diagram — untuk dilengkapi anggota kelompok

> **Catatan proses:** Bagian ini merupakan kerangka/daftar pemeriksaan hasil brainstorming AI, **bukan** diagram jawaban akhir. Sesuai Level 2, anggota kelompok harus menyusun sendiri sintaks dan isi diagram Mermaid sebelum pengumpulan.

### Diagram A — Tanpa jaminan Read-Your-Writes

- [ ] Tampilkan empat partisipan: pelanggan, server Jakarta, server Bandung, dan proses replikasi.
- [ ] Perlihatkan top-up berhasil ditulis di Jakarta, sementara data Bandung belum diperbarui.
- [ ] Tunjukkan waktu permintaan saldo/pemesanan di Bandung yang terjadi **sebelum** replikasi selesai.
- [ ] Beri penanda pada pembacaan saldo lama dan akibatnya terhadap pesanan.
- [ ] Lengkapi dengan Mermaid `sequenceDiagram` buatan kelompok.

### Diagram B — Dengan Read-Your-Writes

- [ ] Tampilkan empat partisipan yang sama agar perbedaan kedua skenario mudah dibandingkan.
- [ ] Tentukan cara klien membawa informasi versi penulisan terakhir.
- [ ] Gambarkan pemeriksaan versi di Bandung saat permintaan pembacaan masuk.
- [ ] Jelaskan melalui alur kapan pembacaan dapat dipenuhi di Bandung dan kapan perlu dialihkan/ditunda.
- [ ] Perlihatkan hasil pembacaan saldo terbaru tanpa mengasumsikan semua replika sudah sinkron.
- [ ] Lengkapi dengan Mermaid `sequenceDiagram` buatan kelompok.

## 3. Skenario Tambahan — untuk dipilih dan dianalisis sendiri

**Pilihan ide untuk diskusi:** ketersediaan pengemudi FoodGo yang diperbarui dari beberapa wilayah.

Pertanyaan analisis yang perlu dijawab kelompok:
1. Data apa yang direplikasi dan peristiwa apa yang bisa membuat replika berbeda?
2. Apa konsekuensi bisnis jika dua server membaca data yang belum sama?
3. Model konsistensi apa yang dibutuhkan untuk **tampilan status** dan untuk **keputusan alokasi pesanan**? Apakah keduanya harus identik?
4. Bagaimana mekanisme yang dipilih menangani konflik, keterlambatan, atau transaksi bersamaan?
5. Apa konsekuensinya terhadap latensi dan ketersediaan layanan?

> Jangan gunakan pertanyaan di atas sebagai jawaban akhir. Tulis analisis dan keputusan model konsistensi dengan penalaran kelompok sendiri.

## 4. Rencana Verifikasi Simulasi (opsional)

| Kasus uji | Hal yang diamati | Status / bukti |
|---|---|---|
| Pembacaan Bandung sebelum replikasi selesai | Apakah saldo lama masih terbaca pada skenario naif? | Diisi setelah diuji |
| Pembacaan dengan versi minimum klien | Apakah data diarahkan ke replika dengan versi yang memenuhi syarat? | Diisi setelah diuji |
| Dua top-up berdekatan | Apakah replikasi yang selesai belakangan dapat menimpa versi lebih baru? | Diisi setelah diuji |
| Pembacaan setelah replikasi selesai | Apakah kedua server akhirnya menunjukkan data yang sesuai? | Diisi setelah diuji |

Tuliskan hasil aktual di `JURNAL.md`, serta tautkan bukti tangkapan layar/rekaman di folder `bukti/`.

## 5. Tabel Kontribusi Anggota

> Lengkapi **berdasarkan pekerjaan yang benar-benar dilakukan**; tiap anggota wajib memiliki commit sendiri.

| Nama | NIM | Kontribusi aktual dan tautan commit |
|---|---|---|
| [Anggota 1] | [NIM] | [Pekerjaan yang sudah selesai] |
| [Anggota 2] | [NIM] | [Pekerjaan yang sudah selesai] |
| [Anggota 3] | [NIM] | [Pekerjaan yang sudah selesai] |
| [Anggota 4, jika ada] | [NIM] | [Pekerjaan yang sudah selesai] |

## Tugas Kelompok

### Bagian 1 — Analisis (wajib)

1. Tentukan: apakah kasus ini **membutuhkan Sequential Consistency** (semua replika melihat urutan operasi yang sama) atau **cukup Eventual Consistency** (replika akan konsisten "pada akhirnya", boleh sementara berbeda)? Berikan argumen berbasis dampak bisnis (mis. kasus saldo *e-wallet* jauh lebih sensitif dibanding kasus "jumlah like" di media sosial).
2. Jika kalian menyimpulkan Eventual Consistency saja **tidak cukup** untuk skenario ini, usulkan pendekatan **Client-Centric Consistency** yang relevan (mis. *Read-Your-Writes*: pelanggan yang baru top-up harus selalu melihat saldo terbarunya sendiri, walau replika lain belum sinkron).
3. Gambarkan **diagram alir urutan (sequence diagram)** yang menunjukkan operasi read/write antara pelanggan, server Jakarta, server Bandung, dan proses replikasi — untuk skenario **tanpa** jaminan konsistensi (bug terjadi) DAN skenario **dengan** solusi yang kalian usulkan (bug teratasi). Pakai Mermaid (`sequenceDiagram`) di `README.md` — lihat contoh cara pakai di Tugas 2.

### Bagian 2 — Simulasi (opsional, nilai tambah)

Skeleton `src/replica_simulation.py` mensimulasikan dua replika (Jakarta & Bandung) dengan delay replikasi buatan. Lengkapi TODO untuk:
1. Menunjukkan kondisi **inconsistent read** (replika Bandung masih menunjukkan saldo lama walau Jakarta sudah update).
2. Mengimplementasikan mekanisme **Read-Your-Writes** sederhana (mis. dengan version/timestamp per client) yang memperbaiki masalah tersebut.

```bash
python3 src/replica_simulation.py
```

## Struktur Submission

```
tugas-07-konsistensi-data/
├── README.md      # Analisis konsistensi + sequence diagram Mermaid
├── JURNAL.md
├── src/            # (opsional) simulasi replikasi
└── bukti/          # (jika mengerjakan simulasi) output program
```

## Rubrik Penilaian (Tugas 7)

| Komponen | Bobot | Kriteria |
|---|---|---|
| Ketepatan pemilihan model konsistensi | 30% | Argumen berbasis dampak bisnis nyata, bukan hafalan definisi |
| Kualitas sequence diagram | 30% | Menunjukkan jelas titik kegagalan & titik perbaikan |
| Usulan solusi client-centric | 25% | Solusi konkret dan dapat diimplementasikan (bukan wacana abstrak) |
| Proses & kontribusi kelompok | 15% | `JURNAL.md`, commit history (+ bonus jika simulasi dikerjakan) |

## Batasan Penggunaan AI (Level 2)

Kebijakan **Level 2 (AI Assisted Idea Generation & Structuring)** berlaku — lihat [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Boleh bertanya konsep umum consistency model ke AI untuk brainstorming; **tidak boleh** meminta AI menuliskan analisis akhir/sequence diagram atau isi `# TODO` di `src/replica_simulation.py` yang tinggal ditempel. Catat pemakaian AI di "Log Penggunaan AI" pada `JURNAL.md`.

- Sebagai bukti pemahaman konsep (bukan hafalan jawaban skenario FoodGo saja), `README.md` wajib menyertakan **satu skenario tambahan** yang kalian buat sendiri (mis. kasus lain di aplikasi ojek online) dan menentukan model konsistensi yang tepat untuk skenario tambahan tersebut.
