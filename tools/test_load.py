import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

TARGET_URL = os.getenv(
    "TARGET_URL",
    "https://clouda-container-app.bluehill-65664009.norwayeast.azurecontainerapps.io/api/drivers",
)

CONCURRENCY = 300
DURATION_SECONDS = 120
def send_request(i: int):
    try:
        r = requests.get(TARGET_URL, timeout=5)
        return r.status_code, None
    except Exception as e:
        return None, e

def worker(stop_at: float, idx: int):
    ok = 0
    err = 0
    while time.time() < stop_at:
        status, error = send_request(idx)
        if error is not None:
            err += 1
        elif status == 200:
            ok += 1
        else:
            err += 1
    return ok, err

def main():
    print(f"Target URL: {TARGET_URL}")
    print(f"Concurrency: {CONCURRENCY}, duration: {DURATION_SECONDS}s")

    stop_at = time.time() + DURATION_SECONDS
    start = time.time()

    totals_ok = 0
    totals_err = 0

    with ThreadPoolExecutor(max_workers=CONCURRENCY) as executor:
        futures = [executor.submit(worker, stop_at, i) for i in range(CONCURRENCY)]
        for f in as_completed(futures):
            ok, err = f.result()
            totals_ok += ok
            totals_err += err

    elapsed = time.time() - start
    print(f"\nDone in {elapsed:.2f} s")
    print(f"OK: {totals_ok}, errors: {totals_err}")

if __name__ == "__main__":
    main()
