"""
Tugas 4 - Jalur A: RPC Server (simulasi modul Pembayaran)
Memakai xmlrpc.server dari Python standard library - tidak perlu install apa pun.
"""

from xmlrpc.server import SimpleXMLRPCServer

# Simulasi "database" saldo user
saldo_user = {
    "user1": 50000,
    "user2": 120000,
}

def cek_saldo(user_id: str) -> float:
    if user_id not in saldo_user:
        return 0.0
    return float(saldo_user[user_id])


def proses_pembayaran(user_id: str, jumlah: float) -> dict:
    if user_id not in saldo_user:
        return {"status": "gagal", "saldo_akhir": 0, "pesan": "user tidak ditemukan"}
    if saldo_user[user_id] < jumlah:
        return {
            "status": "gagal",
            "saldo_akhir": saldo_user[user_id],
            "pesan": "saldo tidak cukup",
        }
    saldo_user[user_id] -= jumlah
    return {"status": "sukses", "saldo_akhir": saldo_user[user_id]}


def main():
    server = SimpleXMLRPCServer(("localhost", 8000), allow_none=True)
    server.register_function(cek_saldo, "cek_saldo")
    server.register_function(proses_pembayaran, "proses_pembayaran")
    print("RPC server modul Pembayaran berjalan di port 8000...")
    server.serve_forever()


if __name__ == "__main__":
    main()
