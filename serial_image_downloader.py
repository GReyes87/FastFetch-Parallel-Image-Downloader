#!/usr/bin/env python3
import time
import requests

TOTAL_IMAGES = 100
BASE_URL = "https://picsum.photos/300"
OUTPUT_DIR = "req2_serial_downloader_100urls"

def main():
    start = time.perf_counter()
    success = 0

    for i in range(1, TOTAL_IMAGES + 1):
        filename = f"{OUTPUT_DIR}/image_{i}.jpg"

        try:
            response = requests.get(BASE_URL, timeout=3)
            response.raise_for_status()

            with open(filename, "wb") as f:
                f.write(response.content)

            success += 1
            print(f"Saved {filename} ({i}/{TOTAL_IMAGES})")

        except Exception as e:
            print(f"Failed {filename}: {e} ({i}/{TOTAL_IMAGES})")

    elapsed = time.perf_counter() - start

    print("\n--- SERIAL BASELINE RESULTS ---")
    print(f"Successful downloads: {success}/{TOTAL_IMAGES}")
    print(f"Total execution time: {elapsed:.2f} seconds")

if __name__ == "__main__":
    main()