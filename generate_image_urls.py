import requests

TOTAL_IMAGES = 100
BASE_URL = "https://picsum.photos/300"

def main():
    for i in range(1, TOTAL_IMAGES + 1):
        filename = f"req1_generate_100_imageurls/image_{i}.jpg"

        try:
            response = requests.get(BASE_URL, timeout=3)
            response.raise_for_status()

            with open(filename, "wb") as f:
                f.write(response.content)

            print(f"Saved {filename}")

        except Exception as e:
            print(f"Failed image_{i}.jpg: {e}")

if __name__ == "__main__":
    main()