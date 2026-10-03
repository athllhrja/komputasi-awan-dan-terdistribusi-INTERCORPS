"""
Tugas 3 - Simulasi Pesanan Masuk dengan Multithreading
Versi dengan Lock: melindungi pembaruan counter.
"""

import threading
import random
import time

NUM_ORDERS = 100
NUM_WORKERS = 10

processed_count = 0
lock = threading.Lock()


def process_order(order_id: int) -> None:
    """Proses satu pesanan. Dipanggil oleh tiap thread pekerja."""
    global processed_count

    # Simulasi pekerjaan pesanan tetap di luar Lock.
    time.sleep(random.uniform(0.001, 0.01))

    # Lindungi seluruh rangkaian baca–tambah–tulis.
    with lock:
        current_value = processed_count

        # Jeda yang sama dipertahankan untuk perbandingan.
        time.sleep(0.001)

        processed_count = current_value + 1


def worker(order_ids: list) -> None:
    """Satu thread pekerja memproses sekumpulan order_id."""
    for order_id in order_ids:
        process_order(order_id)


def main() -> None:
    global processed_count
    processed_count = 0

    order_ids = list(range(1, NUM_ORDERS + 1))
    threads = []

    chunk_size = (NUM_ORDERS + NUM_WORKERS - 1) // NUM_WORKERS

    for i in range(NUM_WORKERS):
        start = i * chunk_size
        end = min(start + chunk_size, NUM_ORDERS)

        if start >= NUM_ORDERS:
            break

        thread = threading.Thread(
            target=worker,
            args=(order_ids[start:end],),
        )
        threads.append(thread)

    # Jalankan semua thread sebelum menunggu penyelesaiannya.
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print("Mode: DENGAN LOCK")
    print(f"Jumlah pesanan: {NUM_ORDERS}")
    print(f"Jumlah thread: {len(threads)}")
    print(
        f"Total pesanan diproses: {processed_count} "
        f"(seharusnya {NUM_ORDERS})"
    )

    if processed_count != NUM_ORDERS:
        print("PENGUJIAN GAGAL: counter tidak sesuai.")
    else:
        print("PENGUJIAN BERHASIL: counter sesuai dengan jumlah pesanan.")


if __name__ == "__main__":
    main()
