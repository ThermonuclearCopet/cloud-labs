import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

TARGET_URL = os.getenv(
    "TARGET_URL",
    "https://clouda-container-app--0000011.bluehill-65664009.norwayeast.azurecontainerapps.io/api/drivers",
)

TOTAL_REQUESTS = 4000
CONCURRENCY = 80


def send_request(i: int):
    try:
        r = requests.get(TARGET_URL, timeout=5)
        return i, r.status_code, None
    except Exception as e:
        return i, None, e


def main():
    print(f"Target URL: {TARGET_URL}")
    print(f"Total requests: {TOTAL_REQUESTS}, concurrency: {CONCURRENCY}")

    start = time.time()
    ok = 0
    errors = 0

    with ThreadPoolExecutor(max_workers=CONCURRENCY) as executor:
        futures = [executor.submit(send_request, i) for i in range(TOTAL_REQUESTS)]

        for f in as_completed(futures):
            _, status, err = f.result()
            if err is not None:
                errors += 1
            elif status == 200:
                ok += 1
            else:
                errors += 1

    elapsed = time.time() - start
    print(f"\nDone in {elapsed:.2f} s")
    print(f"OK: {ok}, errors/other: {errors}")


if __name__ == "__main__":
    main()
