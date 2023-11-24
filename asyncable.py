import time
from concurrent import futures


def get_job(is_asyncable):
    if is_asyncable:

        def job():
            time.sleep(0.1)

        return job

    def job():
        for i in range(50_000_000):
            pass

    return job


def run(is_asyncable=True, n=10):
    job = get_job(is_asyncable)

    print(f"is_asyncable={is_asyncable}")
    start = time.time_ns()
    job()
    one_job = time.time_ns() - start

    print(f"- time taken ( 1 job): {one_job / 1000}µs")

    pool = futures.ThreadPoolExecutor(max_workers=10)
    for _ in range(n):
        pool.submit(job)

    start = time.time_ns()
    pool.shutdown(wait=True)
    n_jobs = time.time_ns() - start

    print(f"- time taken ({n} jobs): {n_jobs / 1000}µs")
    print(f"- ratio: {n_jobs / one_job}")
    print()


run(True)
run(False)

"""
is_asyncable=True
- time taken ( 1 job): 105093.0µs
- time taken (10 jobs): 104917.0µs
- ratio: 0.9983252928358692

is_asyncable=False
- time taken ( 1 job): 405328.0µs
- time taken (10 jobs): 3611792.0µs
- ratio: 8.91078829984605
"""
