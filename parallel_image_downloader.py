#!/usr/bin/env python3
import time
import threading
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

TOTAL_IMAGES = 100
BASE_URL = "https://picsum.photos/300"
OUTPUT_DIR = "req3_parallel_downloader_100urls"
MAX_WORKERS = 5
LOG_FILE = "logger.txt"
TIMEOUT_SECONDS = 3
MAX_RETRIES = 3

progress_lock = threading.Lock()
log_lock = threading.Lock()

completed = 0
success = 0

def log_message(url, filename, status):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{timestamp} | {url} | {filename} | {status}\n"

    # mutex: only one thread writes at a time
    with log_lock:
        with open(LOG_FILE, "a") as f:
            f.write(line)

def download_one(i):
    filepath = f"{OUTPUT_DIR}/image_{i}.jpg"
    short_name = f"image_{i}.jpg"

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(BASE_URL, timeout=TIMEOUT_SECONDS)
            response.raise_for_status()

            with open(filepath, "wb") as f:
                f.write(response.content)

            log_message(BASE_URL, short_name, "SUCCESS")
            return True

        except requests.exceptions.Timeout:
            if attempt < MAX_RETRIES:
                log_message(BASE_URL, short_name, f"TIMEOUT | RETRY {attempt}")
            else:
                log_message(BASE_URL, short_name, "TIMEOUT | FAILED")
                return False

        except Exception:
            if attempt < MAX_RETRIES:
                log_message(BASE_URL, short_name, f"FAILED | RETRY {attempt}")
            else:
                log_message(BASE_URL, short_name, "FAILED")
                return False

    return False

def update_progress(ok):
    global completed, success
    with progress_lock:
        completed += 1
        if ok:
            success += 1
        print(f"Downloaded: {completed}/{TOTAL_IMAGES}", flush=True)

def main():
    # clear old logs each run
    open(LOG_FILE, "w").close()

    start = time.perf_counter()

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(download_one, i) for i in range(1, TOTAL_IMAGES + 1)]

        for fut in as_completed(futures):
            try:
                ok = fut.result()
            except Exception:
                ok = False
            update_progress(ok)

    end = time.perf_counter()

    print("\n--- PARALLEL RESULTS ---")
    print(f"Successful downloads: {success}/{TOTAL_IMAGES}")
    print(f"Parallel execution time: {end - start:.2f} second(s)")

if __name__ == "__main__":
    main()