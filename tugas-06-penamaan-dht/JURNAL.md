# Jurnal Proses — Tugas 6

## Implementasi find_successor

- Kesalahan pertama yang ditemui: lupa menangani kasus wrap-around (ketika tidak ada node dengan ID ≥ key_hash, harus kembali ke node dengan ID terkecil).
- Cara memperbaikinya: setelah mengurutkan daftar node, lakukan iterasi mencari ID terkecil yang ≥ key_hash; jika tidak ketemu, kembalikan `sorted_nodes[0]`.
- Pemeriksaan: hash 175 dan 170, yang sebelumnya dipegang node 177, setelah node itu keluar ditemukan di node 40. Hasil ini sesuai dengan aturan wrap-around.
- 
### Penyesuaian main()

`main()` awal hanya mendaftarkan `kurir-001` (hash 50), `kurir-002` (hash 28), dan `kurir-003` (hash 132). Ketiganya tidak masuk rentang yang berubah saat `node-medan-1` bergabung atau `node-jakarta-1` keluar, sehingga log perpindahan tidak muncul walaupun algoritmanya sudah benar.

Kurir tambahan didaftarkan agar perpindahan terlihat:

- `kurir-012` (hash 116) dan `kurir-088` (hash 122) berada pada rentang (102, 123], sehingga terdampak join `node-medan-1`.
- `kurir-005` (hash 175) dan `kurir-009` (hash 170) berada pada rentang (136, 177], sehingga terdampak leave `node-jakarta-1`.

Pemindahan yang dicatat program adalah perubahan tanggung jawab lewat `find_successor()`, bukan penyalinan data fisik antar proses. `self.data` tetap satu kamus pada simulasi satu proses ini.

## Skenario join/leave

- Hasil sebelum & sesudah node baru bergabung:
  - Sebelum join node-medan-1 (id=123):
    - `kurir-012` (hash=116) dipegang node 136
    - `kurir-088` (hash=122) dipegang node 136
  - Sesudah join:
    - hash 116 dan 122 berpindah dari node **136 → 123**
    - Ring menjadi: `[40, 102, 123, 136, 177]`
- Hasil sebelum & sesudah node keluar:
  - Sebelum leave node-jakarta-1 (id=177):
    - `kurir-005` (hash=175) dipegang node 177
    - `kurir-009` (hash=170) dipegang node 177
  - Sesudah leave:
    - hash 170 dan 175 berpindah dari node **177 → 40** (wrap-around ke node terkecil)
    - Ring menjadi: `[40, 102, 123, 136]`


## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 28-10-2026 | ChatGPT | Meminta peninjauan kode Chord, membandingkan dua versi main(), menanyakan arti output perpindahan tanggung jawab, serta apakah perubahan perlu dicatat di README dan JURNAL | main() yang hanya mendaftarkan kurir dengan hash 28, 50, dan 132 tidak memperlihatkan perpindahan saat topologi berubah. Skenario yang menambahkan hash 116, 122, 170, dan 175 memperlihatkan perpindahan tanggung jawab saat node bergabung dan keluar. IP kurir tetap sama; node penanggung jawabnya yang berubah | Saya membandingkan penjelasan dengan kode dan output yang saya jalankan. Saya memakai hasil aktual untuk memahami skenario, lalu menulis catatan README/JURNAL dengan kata-kata sendiri |
| 01-11-2026 | ChatGPT | MMendiskusikan konsep DHT/Chord, perbandingannya dengan metode penamaan lain, serta mekanisme perubahan mapping ketika terjadi perubahan topologi. | Memberikan gambaran mengenai perbedaan Flat Naming, DNS, dan DHT/Chord, serta hubungan antara successor, ring topology, dan perpindahan data saat node bergabung atau keluar. | Saya mempelajari kembali konsep yang dijelaskan dan mencocokkannya dengan hasil simulasi program. Penjelasan kemudian disesuaikan dengan implementasi dan hasil pengujian kelompok. |
