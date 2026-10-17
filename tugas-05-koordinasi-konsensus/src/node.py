"""
Tugas 5 - Simulasi Node untuk Bully Algorithm

Infrastruktur jaringan (socket server/client) sudah disediakan.
Logika Bully Algorithm (bagian # TODO) harus kalian lengkapi sendiri.

Contoh menjalankan (5 terminal terpisah):
    python3 node.py --id 1 --port 5001 --peers 5002,5003,5004,5005
    python3 node.py --id 2 --port 5002 --peers 5001,5003,5004,5005
    ... dst untuk id 3, 4, 5
"""

import argparse
import socket
import threading
import time

ELECTION_TIMEOUT = 2.0  # detik menunggu balasan OK sebelum menyatakan diri leader


class Node:
    def __init__(self, node_id: int, port: int, peers: dict):
        self.node_id = node_id
        self.port = port
        # peers: dict {peer_id: peer_port} untuk semua node LAIN
        self.peers = peers
        self.leader_id = None
        self.lock = threading.Lock()
        self.got_ok = False

    # ---------- Infrastruktur jaringan (SUDAH LENGKAP, jangan diubah) ----------

    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("localhost", self.port))
        server.listen()
        print(f"[Node {self.node_id}] Listening di port {self.port}")
        while True:
            conn, _ = server.accept()
            threading.Thread(target=self.handle_connection, args=(conn,), daemon=True).start()

    def handle_connection(self, conn: socket.socket):
        with conn:
            data = conn.recv(1024).decode()
            if not data:
                return
            sender_id, msg_type = data.split(":")
            self.on_message(int(sender_id), msg_type)

    def send_message(self, target_port: int, msg_type: str) -> bool:
        """Kirim pesan ke node lain. Return False jika node target tidak merespons (dianggap mati)."""
        try:
            with socket.create_connection(("localhost", target_port), timeout=1.0) as s:
                s.sendall(f"{self.node_id}:{msg_type}".encode())
            return True
        except (ConnectionRefusedError, socket.timeout, OSError):
            return False

    # ---------- Logika Bully Algorithm (LENGKAPI BAGIAN INI) ----------

    def on_message(self, sender_id: int, msg_type: str):
        """Menangani pesan yang diterima dari node lain."""
        print(
            f"[Node {self.node_id}] "
            f"Menerima '{msg_type}' dari node {sender_id}"
        )

        if msg_type == "ELECTION":
            # Balas jika ID kita lebih tinggi daripada pengirim.
            if self.node_id > sender_id:
                target_port = self.peers.get(sender_id)

                if target_port is not None:
                    if self.send_message(target_port, "OK"):
                        print(
                            f"[Node {self.node_id}] "
                            f"Mengirim OK ke node {sender_id}"
                        )

                # Mulai election sendiri karena berpotensi jadi leader.
                self.start_election()

        elif msg_type == "OK":
            # Ada node dengan ID lebih tinggi yang masih aktif.
            if sender_id > self.node_id:
                with self.lock:
                    self.got_ok = True

        elif msg_type == "COORDINATOR":
            # Catat pengirim sebagai leader baru.
            with self.lock:
                self.leader_id = sender_id

            print(
                f"[Node {self.node_id}] "
                f"Leader sekarang: node {sender_id}"
            )
    
    def start_election(self):
        """Dipanggil saat node ini mendeteksi leader tidak ada / tidak merespons."""
        with self.lock:
            self.got_ok = False
        # TODO 2: kirim "ELECTION" ke SEMUA peer dengan id LEBIH BESAR dari node_id kita.
        higher_peers = {pid: port for pid, port in self.peers.items() if pid > self.node_id}
        print(f"[Node {self.node_id}] Mulai election ke peer lebih tinggi: {higher_peers}")
        
        if not higher_peers:
            self.declare_leader()
            return

        for pid, port in higher_peers.items():
            terkirim = self.send_message(port, "ELECTION")
            if terkirim:
                print(f"[Node {self.node_id}] Mengirim ELECTION ke node {pid}")
            else:
                print(f"[Node {self.node_id}] Node {pid} tidak merespons (dianggap mati)")
        # Tunggu ELECTION_TIMEOUT detik untuk balasan "OK" (gunakan flag/event yang
        # diset di on_message saat menerima "OK").
        time.sleep(ELECTION_TIMEOUT)
        
        with self.lock:
            ada_ok = self.got_ok
        # Jika TIDAK ADA balasan "OK" dalam waktu tersebut -> panggil declare_leader().
        if not ada_ok:
            print(f"[Node {self.node_id}] Tidak ada OK, menyatakan diri sebagai leader")
            self.declare_leader()
        else:
            print(f"[Node {self.node_id}] Menerima OK, menunggu COORDINATOR")
        #higher_peers = {pid: p for pid, p in self.peers.items() if pid > self.node_id}
        print(f"[Node {self.node_id}] TODO: mulai election ke peer lebih tinggi: {higher_peers}")

    def declare_leader(self):
        """Node ini menyatakan dirinya leader dan memberi tahu semua node lain."""
        # TODO 3: set self.leader_id = self.node_id, lalu kirim "COORDINATOR"
        # ke SEMUA peer (bukan cuma yang lebih tinggi).
        with self.lock:
            self.leader_id = self.node_id
        print(f"[Node {self.node_id}] TODO: broadcast COORDINATOR, saya jadi leader")

    def monitor_leader(self):
        """Loop periodik: cek apakah leader masih hidup, trigger election jika mati."""
        while True:
            time.sleep(3)
            # TODO 4: jika self.leader_id sudah diketahui, coba ping node tsb
            # (mis. kirim pesan "PING" atau cukup coba connect). Jika gagal
            # (leader mati) dan node ini belum tahu leader baru, panggil
            # start_election().
            pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", type=int, required=True)
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--peers", type=str, required=True,
                         help="daftar port peer dipisah koma, mis. 5002,5003,5004,5005")
    args = parser.parse_args()

    # Asumsi konvensi port: id N selalu di port 5000+N (lihat contoh perintah di README).
    peer_ports = [int(p) for p in args.peers.split(",")]
    peers = {port - 5000: port for port in peer_ports}

    node = Node(args.id, args.port, peers)

    threading.Thread(target=node.start_server, daemon=True).start()
    threading.Thread(target=node.monitor_leader, daemon=True).start()

    time.sleep(1)  # beri waktu semua node lain start dulu sebelum election awal
    node.start_election()

    while True:
        time.sleep(60)


if __name__ == "__main__":
    main()
