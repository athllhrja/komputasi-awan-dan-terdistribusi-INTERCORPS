# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** [INTERCOROPS]

| Nama | NIM | Kontribusi |
|---|---|---|
| [ANDI ATHALLAH RADJA | [103072400034] | [single point of failure karena arsitektur monolitik ] |
| [KRISNA PUTRA WICAKSANA] | [103072400079] | [network is always reliable] |
| [CALVIN IMMANUEL LADO] | [103072400158] | [bandwith is infinite] |

## Pitfall 1: [single point of failure karena arsitektur monolitik] — ditulis oleh [[ANDI ATHALLAH RADJA]

**Bukti di skenario:** [ "Saat trafik naik, satu server yang menangani semua modul (pesanan, pembayaran, notifikasi kurir) kewalahan karena semuanya berjalan di satu proses monolitik yang sama"]

**Kenapa ini keliru:** [karena sistem monolitik ini menggabungkan semua resource untuk komputasi. jika ada satu modul yang menggunakan terlalu banyak resource maka dampaknya tidak akan terisolisasi yang bisa mengakibatkan seluruh proses server mati, dan juga sistemnya tidak bisa di scale per modul sesuai dari kebutuhan modul masing masing]

**Dampak ke FoodGo:** [dampak pada foodgo nya sendiri adalah jika saat jam makan siang atau adanya sebuah promo maka modul pesanan akan menghabiskan semua resource nya dampak nya adalah karena modul pembayaran dan notifikasi kurir nya itu dalam satu proses yang sama maka semuanya akan kewalahan akibatnya server akan crash out dan harus direstart manualt]

**Solusi desain awal:** [solusi yang saya sarankan adalah dengan menggunakan Microservices jadi semua modul akan dijalankan secara terpisah dengan pemisahan service ini semua modul bisa discale secara indpenden]

**Trade-off:** [maintenance akan jauh lebih sulit karena setiap sistem punya enviroment nya masing masing]

---

## Pitfall 2: [nama pitfall] — ditulis oleh [nama]

(ulangi struktur di atas)

---

## Pitfall 3: [nama pitfall] — ditulis oleh [nama]

(ulangi struktur di atas)

---

## Kesimpulan Kelompok

[Ringkasan: jika FoodGo memperbaiki ketiga pitfall ini, apa arsitektur yang disarankan secara garis besar? Kaitkan dengan Tugas 2.]
