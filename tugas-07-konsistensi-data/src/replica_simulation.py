"""
Tugas 7 (opsional) - Simulasi Replikasi Dua Server (Jakarta & Bandung)

Mensimulasikan delay replikasi dan masalah inconsistent read,
lalu memperbaikinya dengan mekanisme Read-Your-Writes sederhana.
"""

import time
import threading

REPLICATION_DELAY = 2.0  # detik, simulasi lambatnya sinkronisasi antar server


class Replica:
    def __init__(self, name: str):
        self.name = name
        self.saldo: dict[str, float] = {}
        self.last_write_version: dict[str, int] = {}

    def write(self, user_id: str, saldo_baru: float, version: int):
        self.saldo[user_id] = saldo_baru
        self.last_write_version[user_id] = version
        print(f"[{self.name}] WRITE saldo {user_id} = {saldo_baru} (versi {version})")

    def read(self, user_id: str) -> float:
        return self.saldo.get(user_id, 0.0)

    def get_version(self, user_id: str) -> int:
        return self.last_write_version.get(user_id, 0)



class ReplicationSystem:
    def __init__(self):
        self.jakarta = Replica("Jakarta")
        self.bandung = Replica("Bandung")
        self.version_counter = 0

    def top_up(self, user_id: str, jumlah: float):
        """Top-up selalu ditulis dulu ke server Jakarta (mis. server terdekat pelanggan)."""
        self.version_counter += 1
        version = self.version_counter
        saldo_baru = self.jakarta.read(user_id) + jumlah
        self.jakarta.write(user_id, saldo_baru, version)

        # TODO 1: replikasi ke Bandung TERTUNDA (simulasikan dengan
        # threading.Timer(REPLICATION_DELAY, ...) yang memanggil
        # self.bandung.write(user_id, saldo_baru, version) setelah delay.
        timer = threading.Timer(
            REPLICATION_DELAY,
            self.bandung.write,
            args=(user_id, saldo_baru, version)
        )
        timer.start()
        print(f"[TODO] Replikasi ke Bandung akan tertunda {REPLICATION_DELAY} detik")

    def baca_saldo_naif(self, user_id: str, server: str) -> float:
        """Baca saldo TANPA mekanisme Read-Your-Writes - bisa saja stale."""
        replica = self.jakarta if server == "Jakarta" else self.bandung
        return replica.read(user_id)

    def baca_saldo_read_your_writes(self, user_id: str, server: str, versi_minimal: int) -> float:
        """TODO 2: implementasikan Read-Your-Writes -
        jika replika yang dituju versi datanya < versi_minimal (client pernah
        melihat versi lebih baru sebelumnya), tunggu/redirect ke replika yang
        sudah punya versi tersebut (di sini cukup simulasikan dengan polling
        sampai versi replika >= versi_minimal, atau redirect ke Jakarta)."""
        replica = self.jakarta if server == "Jakarta" else self.bandung

        versi_sekarang = replica.get_version(user_id)

        print(
            f"[SISTEM] Membaca dari {server}. "
            f"Versi tersedia: {versi_sekarang}, "
            f"versi minimal: {versi_minimal}"
        )

        # Jika versi replika sudah sesuai, baca langsung
        if versi_sekarang >= versi_minimal:
            print(f"[SISTEM] Data tersedia di {server}")
            return replica.read(user_id)

        # Jika belum sesuai, redirect ke Jakarta
        print(
            f"[SISTEM] Versi {server} masih tertinggal. "
            "Redirect pembacaan ke Jakarta..."
        )

        versi_jakarta = self.jakarta.get_version(user_id)

        if versi_jakarta >= versi_minimal:
            print("[SISTEM] Mengambil data terbaru dari Jakarta")
            return self.jakarta.read(user_id)

        # Jika Jakarta juga belum memiliki versi yang dibutuhkan,
        # tunggu hingga versi tersebut tersedia.
        while versi_jakarta < versi_minimal:
            time.sleep(0.05)
            versi_jakarta = self.jakarta.get_version(user_id)

        return self.jakarta.read(user_id)


def main():
    system = ReplicationSystem()
    user_id = "user1"

    print("=== Skenario NAIF (tanpa Read-Your-Writes) ===")
    system.top_up(user_id, 50000)
    time.sleep(0.5)  # pelanggan langsung pesan makanan < REPLICATION_DELAY detik kemudian
    print("Baca saldo dari Bandung (naif):", system.baca_saldo_naif(user_id, "Bandung"))
    print("-> Harusnya 50000, tapi karena delay replikasi, hasilnya bisa 0 (BUG)")

    time.sleep(REPLICATION_DELAY + 0.5)

    print("\n=== Skenario dengan Read-Your-Writes ===")
    system.top_up(user_id, 20000)
    versi_terakhir = system.version_counter
    # TODO 3: panggil baca_saldo_read_your_writes dan tunjukkan hasilnya SELALU benar
    # walau dipanggil segera setelah top_up (< REPLICATION_DELAY detik).
    saldo = system.baca_saldo_read_your_writes(
        user_id,
        "Bandung",
        versi_terakhir
    )

    print("Baca saldo dengan Read-Your-Writes:", saldo)
    print("Saldo seharusnya:", 70000)

    if saldo == 70000:
        print("HASIL: BERHASIL - Saldo terbaru berhasil dibaca")
    else:
        print("HASIL: GAGAL - Saldo belum sesuai")

    # Menunggu proses replikasi terakhir selesai sebelum program berakhir
    time.sleep(REPLICATION_DELAY + 0.5)

    print("\n=== SIMULASI SELESAI ===")



if __name__ == "__main__":
    main()
