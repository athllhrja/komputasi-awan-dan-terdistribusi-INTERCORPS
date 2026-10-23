# Jurnal Proses — Tugas 6

## Implementasi find_successor
- Kesalahan pertama yang ditemui: lupa menangani kasus wrap-around (ketika tidak ada node dengan ID ≥ key_hash, harus kembali ke node dengan ID terkecil).
- Cara memperbaikinya: setelah mengurutkan daftar node, lakukan iterasi mencari ID terkecil yang ≥ key_hash; jika tidak ketemu, kembalikan `sorted_nodes[0]`.

### Penyesuaian main()
Skenario `main()` diubah dengan mendaftarkan kurir tambahan yang hash-nya berada pada rentang terdampak, supaya perpindahan tanggung jawab saat join dan leave terlihat di output:
- `kurir-012` (hash=116) dan `kurir-088` (hash=122) → rentang (102, 123] → terdampak join node-medan-1 (id=123)
- `kurir-005` (hash=175) dan `kurir-009` (hash=170) → rentang (136, 177] → terdampak leave node-jakarta-1 (id=177)

Tanpa penyesuaian ini, kurir awal (hash 28, 50, 132) tidak jatuh di rentang yang berubah, sehingga log perpindahan tidak muncul meskipun algoritma sudah benar.

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
| 23-10-2026 | ChatGPT | Meminta peninjauan kode Chord, membandingkan dua versi main(), menanyakan arti output perpindahan tanggung jawab, serta apakah perubahan perlu dicatat di README dan JURNAL | main() yang hanya mendaftarkan kurir dengan hash 28, 50, dan 132 tidak memperlihatkan perpindahan saat topologi berubah. Skenario yang menambahkan hash 116, 122, 170, dan 175 memperlihatkan perpindahan tanggung jawab saat node bergabung dan keluar. IP kurir tetap sama; node penanggung jawabnya yang berubah | Saya membandingkan penjelasan dengan kode dan output yang saya jalankan. Saya memakai hasil aktual untuk memahami skenario, lalu menulis catatan README/JURNAL dengan kata-kata sendiri |
