"""
Tugas 3 - Simulasi Pesanan Masuk dengan Multithreading

Skeleton ini sengaja belum lengkap. Isi bagian bertanda TODO.
Jangan mengubah nama fungsi (dipakai untuk pengecekan otomatis oleh asisten).
"""

import threading
import random
import time

NUM_ORDERS = 500       # jumlah pesanan simulasi yang masuk
NUM_WORKERS = 50       # jumlah thread pekerja

# Counter bersama untuk menghitung total pesanan yang berhasil diproses.
# Sengaja rawan race condition jika diakses tanpa proteksi.
processed_count = 0

# TODO 1: Buat objek Lock di sini untuk melindungi `processed_count`.
lock = threading.Lock()


def process_order(order_id: int) -> None:
    """Proses satu pesanan. Dipanggil oleh tiap thread pekerja."""
    global processed_count

    # Simulasi pekerjaan pesanan tetap di luar Lock.
    time.sleep(random.uniform(0.001, 0.01))

    # Lindungi seluruh rangkaian baca–tambah–tulis counter.
    with lock:
        current_value = processed_count
        time.sleep(0.001)
        processed_count = current_value + 1


def worker(order_ids: list) -> None:
    """Satu thread pekerja memproses sekumpulan order_id."""
    for order_id in order_ids:
        process_order(order_id)


def main() -> None:
    order_ids = list(range(1, NUM_ORDERS + 1))

    # TODO 3: bagi order ke beberapa thread
    threads = []
    chunk_size = (NUM_ORDERS + NUM_WORKERS - 1) // NUM_WORKERS

    for i in range(NUM_WORKERS):
        start = i * chunk_size
        end = min(start + chunk_size, NUM_ORDERS)
        if start >= NUM_ORDERS:
            break
        chunk = order_ids[start:end]
        t = threading.Thread(target=worker, args=(chunk,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"Total pesanan diproses: {processed_count} (seharusnya {NUM_ORDERS})")
    if processed_count != NUM_ORDERS:
        print("RACE CONDITION TERDETEKSI - lengkapi TODO 1 & TODO 2 dengan Lock!")
    else:
        print("Semua pesanan berhasil diproses dengan benar (tidak ada race condition).")


if __name__ == "__main__":
    main()
