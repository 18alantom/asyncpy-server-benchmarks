Simple POC to compare async and sync Python.

Servers:

1. WSGI web server: `sync_app.py`
2. ASGI web server: `async_app.py`

Both web servers do a couple of things:

1. `/`: Return a templated HTML page.
2. `/api`: Pings the `fake_db_server.py` to get a random piece of data.

---

# Tests and Results

Tests run using K6 script `load.js`

## Tests with DB Latency of 25ms

Fake DB Server Command

```bash
./fake_db_server.py --sleep 25
```

### One Worker

#### `gunicorn -w 1 sync_app:app`

```bash
data_received..................: 1.6 MB 26 kB/s
data_sent......................: 340 kB 5.7 kB/s
http_req_blocked...............: avg=6.21ms   min=123µs    med=321µs    max=6.71s  p(90)=690µs    p(95)=828.39µs
http_req_connecting............: avg=6.17ms   min=106µs    med=288µs    max=6.71s  p(90)=619.4µs  p(95)=761.2µs
http_req_duration..............: avg=103.57ms min=878µs    med=69.05ms  max=4.55s  p(90)=239.16ms p(95)=258.5ms
  { expected_response:true }...: avg=103.57ms min=878µs    med=69.05ms  max=4.55s  p(90)=239.16ms p(95)=258.5ms
http_req_failed................: 0.00%  ✓ 0         ✗ 4197
http_req_receiving.............: avg=50.72µs  min=13µs     med=39µs     max=5.5ms  p(90)=89µs     p(95)=108µs
http_req_sending...............: avg=22.64µs  min=6µs      med=18µs     max=1.75ms p(90)=38µs     p(95)=47µs
http_req_tls_handshaking.......: avg=0s       min=0s       med=0s       max=0s     p(90)=0s       p(95)=0s
http_req_waiting...............: avg=103.5ms  min=826µs    med=69ms     max=4.55s  p(90)=239.08ms p(95)=258.44ms
http_reqs......................: 4197   69.804625/s
iteration_duration.............: avg=429.72ms min=302.74ms med=396.06ms max=6.91s  p(90)=403.99ms p(95)=405.56ms
iterations.....................: 1399   23.268208/s
vus............................: 10     min=10      max=10
vus_max........................: 10     min=10      max=10
```

#### `uvicorn --workers 1 --log-level error async_app:app`

```bash
data_received..................: 4.8 MB 79 kB/s
data_sent......................: 1.1 MB 18 kB/s
http_req_blocked...............: avg=2.39µs   min=0s       med=1µs      max=810µs    p(90)=3µs      p(95)=5µs
http_req_connecting............: avg=522ns    min=0s       med=0s       max=787µs    p(90)=0s       p(95)=0s
http_req_duration..............: avg=10.72ms  min=126µs    med=951.5µs  max=44.4ms   p(90)=31.52ms  p(95)=32.77ms
  { expected_response:true }...: avg=10.72ms  min=126µs    med=951.5µs  max=44.4ms   p(90)=31.52ms  p(95)=32.77ms
http_req_failed................: 0.00%  ✓ 0          ✗ 13590
http_req_receiving.............: avg=17.87µs  min=4µs      med=15µs     max=373µs    p(90)=25µs     p(95)=37µs
http_req_sending...............: avg=7.71µs   min=1µs      med=5µs      max=1.64ms   p(90)=14µs     p(95)=20µs
http_req_tls_handshaking.......: avg=0s       min=0s       med=0s       max=0s       p(90)=0s       p(95)=0s
http_req_waiting...............: avg=10.69ms  min=117µs    med=930µs    max=44.38ms  p(90)=31.49ms  p(95)=32.73ms
http_reqs......................: 13590  226.251252/s
iteration_duration.............: avg=132.58ms min=127.02ms med=132.24ms max=146.92ms p(90)=135.49ms p(95)=137.16ms
iterations.....................: 4530   75.417084/s
vus............................: 10     min=10       max=10
vus_max........................: 10     min=10       max=10
```

#### `gunicorn -k uvicorn.workers.UvicornWorker -w 1 async_app:app`

```bash
data_received..................: 4.7 MB 79 kB/s
data_sent......................: 1.1 MB 18 kB/s
http_req_blocked...............: avg=2.59µs   min=0s       med=1µs      max=1.42ms   p(90)=3µs      p(95)=4µs
http_req_connecting............: avg=486ns    min=0s       med=0s       max=690µs    p(90)=0s       p(95)=0s
http_req_duration..............: avg=10.89ms  min=236µs    med=1.55ms   max=46.38ms  p(90)=31.06ms  p(95)=32.28ms
  { expected_response:true }...: avg=10.89ms  min=236µs    med=1.55ms   max=46.38ms  p(90)=31.06ms  p(95)=32.28ms
http_req_failed................: 0.00%  ✓ 0          ✗ 13533
http_req_receiving.............: avg=17.72µs  min=4µs      med=15µs     max=982µs    p(90)=25µs     p(95)=37µs
http_req_sending...............: avg=7.14µs   min=1µs      med=5µs      max=303µs    p(90)=13µs     p(95)=18µs
http_req_tls_handshaking.......: avg=0s       min=0s       med=0s       max=0s       p(90)=0s       p(95)=0s
http_req_waiting...............: avg=10.87ms  min=228µs    med=1.53ms   max=46.36ms  p(90)=31.02ms  p(95)=32.25ms
http_reqs......................: 13533  225.465003/s
iteration_duration.............: avg=133.04ms min=127.65ms med=132.77ms max=150.07ms p(90)=135.84ms p(95)=137.19ms
iterations.....................: 4511   75.155001/s
vus............................: 10     min=10       max=10
vus_max........................: 10     min=10       max=10
```

#### `uvicorn --workers 1 --log-level error stupid_async_app:app`

```bash
data_received..................: 1.6 MB 26 kB/s
data_sent......................: 360 kB 6.0 kB/s
http_req_blocked...............: avg=5.27µs   min=0s       med=2µs      max=1.15ms   p(90)=5µs      p(95)=7µs
http_req_connecting............: avg=504ns    min=0s       med=0s       max=250µs    p(90)=0s       p(95)=0s
http_req_duration..............: avg=101.49ms min=194µs    med=1.27ms   max=323.38ms p(90)=303.63ms p(95)=306.25ms
 { expected_response:true }...: avg=101.49ms min=194µs    med=1.27ms   max=323.38ms p(90)=303.63ms p(95)=306.25ms
http_req_failed................: 0.00%  ✓ 0         ✗ 4440
http_req_receiving.............: avg=33.11µs  min=5µs      med=23µs     max=2.91ms   p(90)=56µs     p(95)=77µs
http_req_sending...............: avg=13.14µs  min=1µs      med=8µs      max=1.04ms   p(90)=20µs     p(95)=27µs
http_req_tls_handshaking.......: avg=0s       min=0s       med=0s       max=0s       p(90)=0s       p(95)=0s
http_req_waiting...............: avg=101.45ms min=176µs    med=1.24ms   max=323.34ms p(90)=303.54ms p(95)=306.21ms
http_reqs......................: 4440   73.9748/s
iteration_duration.............: avg=405.72ms min=394.93ms med=405.48ms max=425.64ms p(90)=412.97ms p(95)=415.08ms
iterations.....................: 1480   24.658267/s
vus............................: 10     min=10      max=10
vus_max........................: 10     min=10      max=10
```

### Two Workers

#### `gunicorn -w 2 sync_app:app`

```bash
data_received..................: 1.7 MB 27 kB/s
data_sent......................: 365 kB 6.0 kB/s
http_req_blocked...............: avg=9.03ms   min=113µs   med=446µs    max=13.11s p(90)=858.5µs  p(95)=1.04ms
http_req_connecting............: avg=8.99ms   min=97µs    med=412µs    max=13.11s p(90)=803µs    p(95)=972.74µs
http_req_duration..............: avg=91.65ms  min=856µs   med=32.54ms  max=13.26s p(90)=118.89ms p(95)=141.59ms
  { expected_response:true }...: avg=91.65ms  min=856µs   med=32.54ms  max=13.26s p(90)=118.89ms p(95)=141.59ms
http_req_failed................: 0.00%  ✓ 0         ✗ 4506
http_req_receiving.............: avg=51.53µs  min=10µs    med=38µs     max=3.1ms  p(90)=87µs     p(95)=102µs
http_req_sending...............: avg=22.44µs  min=6µs     med=19µs     max=353µs  p(90)=36µs     p(95)=43µs
http_req_tls_handshaking.......: avg=0s       min=0s      med=0s       max=0s     p(90)=0s       p(95)=0s
http_req_waiting...............: avg=91.58ms  min=797µs   med=32.46ms  max=13.26s p(90)=118.8ms  p(95)=141.49ms
http_reqs......................: 4506   73.679303/s
iteration_duration.............: avg=402.55ms min=244.4ms med=252.94ms max=13.37s p(90)=260.63ms p(95)=308.06ms
iterations.....................: 1502   24.559768/s
vus............................: 3      min=3       max=10
vus_max........................: 10     min=10      max=10
```

#### `uvicorn --workers 2 --log-level error async_app:app`

```bash
data_received..................: 4.7 MB 79 kB/s
data_sent......................: 1.1 MB 18 kB/s
http_req_blocked...............: avg=2.73µs   min=0s       med=1µs      max=1.62ms   p(90)=4µs      p(95)=5.84µs
http_req_connecting............: avg=476ns    min=0s       med=0s       max=735µs    p(90)=0s       p(95)=0s
http_req_duration..............: avg=10.82ms  min=137µs    med=936µs    max=45.7ms   p(90)=31.83ms  p(95)=32.96ms
  { expected_response:true }...: avg=10.82ms  min=137µs    med=936µs    max=45.7ms   p(90)=31.83ms  p(95)=32.96ms
http_req_failed................: 0.00%  ✓ 0          ✗ 13524
http_req_receiving.............: avg=21.79µs  min=5µs      med=19µs     max=770µs    p(90)=31µs     p(95)=42µs
http_req_sending...............: avg=9.26µs   min=1µs      med=6µs      max=691µs    p(90)=17µs     p(95)=22µs
http_req_tls_handshaking.......: avg=0s       min=0s       med=0s       max=0s       p(90)=0s       p(95)=0s
http_req_waiting...............: avg=10.79ms  min=120µs    med=909µs    max=45.68ms  p(90)=31.8ms   p(95)=32.92ms
http_reqs......................: 13524  225.046201/s
iteration_duration.............: avg=133.29ms min=126.85ms med=132.84ms max=148.11ms p(90)=137.08ms p(95)=138.94ms
iterations.....................: 4508   75.0154/s
vus............................: 10     min=10       max=10
vus_max........................: 10     min=10       max=10
```

#### `gunicorn -k uvicorn.workers.UvicornWorker -w 2 async_app:app`

```bash
data_received..................: 4.7 MB 78 kB/s
data_sent......................: 1.1 MB 18 kB/s
http_req_blocked...............: avg=2.62µs   min=0s      med=1µs      max=771µs   p(90)=4µs      p(95)=5µs
http_req_connecting............: avg=479ns    min=0s      med=0s       max=715µs   p(90)=0s       p(95)=0s
http_req_duration..............: avg=11.23ms  min=231µs   med=1.59ms   max=43.85ms p(90)=32.17ms  p(95)=33.51ms
  { expected_response:true }...: avg=11.23ms  min=231µs   med=1.59ms   max=43.85ms p(90)=32.17ms  p(95)=33.51ms
http_req_failed................: 0.00%  ✓ 0          ✗ 13410
http_req_receiving.............: avg=21.4µs   min=4µs     med=19µs     max=739µs   p(90)=30µs     p(95)=40µs
http_req_sending...............: avg=10.19µs  min=2µs     med=6µs      max=1.56ms  p(90)=16µs     p(95)=22µs
http_req_tls_handshaking.......: avg=0s       min=0s      med=0s       max=0s      p(90)=0s       p(95)=0s
http_req_waiting...............: avg=11.2ms   min=218µs   med=1.57ms   max=43.8ms  p(90)=32.13ms  p(95)=33.47ms
http_reqs......................: 13410  223.369489/s
iteration_duration.............: avg=134.29ms min=127.5ms med=133.82ms max=148.9ms p(90)=138.39ms p(95)=140.19ms
iterations.....................: 4470   74.456496/s
vus............................: 10     min=10       max=10
vus_max........................: 10     min=10       max=10
```

#### `gunicorn -k gevent -w 2 sync_app:app`

```bash
data_received..................: 5.1 MB 84 kB/s
data_sent......................: 1.1 MB 18 kB/s
http_req_blocked...............: avg=2.3µs    min=0s      med=1µs      max=740µs    p(90)=3µs      p(95)=5µs
http_req_connecting............: avg=466ns    min=0s      med=0s       max=700µs    p(90)=0s       p(95)=0s
http_req_duration..............: avg=11.05ms  min=306µs   med=1.15ms   max=59.63ms  p(90)=31.95ms  p(95)=33.84ms
  { expected_response:true }...: avg=11.05ms  min=306µs   med=1.15ms   max=59.63ms  p(90)=31.95ms  p(95)=33.84ms
http_req_failed................: 0.00%  ✓ 0          ✗ 13470
http_req_receiving.............: avg=20.48µs  min=4µs     med=16µs     max=1.04ms   p(90)=34µs     p(95)=48µs
http_req_sending...............: avg=8.31µs   min=1µs     med=5µs      max=1.6ms    p(90)=15µs     p(95)=19µs
http_req_tls_handshaking.......: avg=0s       min=0s      med=0s       max=0s       p(90)=0s       p(95)=0s
http_req_waiting...............: avg=11.02ms  min=278µs   med=1.12ms   max=59.62ms  p(90)=31.91ms  p(95)=33.8ms
http_reqs......................: 13470  224.322255/s
iteration_duration.............: avg=133.72ms min=126.8ms med=132.95ms max=163.45ms p(90)=138.19ms p(95)=140.66ms
iterations.....................: 4490   74.774085/s
vus............................: 10     min=10       max=10
vus_max........................: 10     min=10       max=10
```

#### `gunicorn -k gthread -w 2 sync_app:app`

```bash
data_received..................: 2.6 MB 44 kB/s
data_sent......................: 549 kB 9.1 kB/s
http_req_blocked...............: avg=4.17µs   min=0s       med=2µs      max=1.69ms   p(90)=5µs      p(95)=6µs
http_req_connecting............: avg=563ns    min=0s       med=0s       max=423µs    p(90)=0s       p(95)=0s
http_req_duration..............: avg=55.03ms  min=2.17ms   med=36.5ms   max=171.45ms p(90)=128.29ms p(95)=151.38ms
  { expected_response:true }...: avg=55.03ms  min=2.17ms   med=36.5ms   max=171.45ms p(90)=128.29ms p(95)=151.38ms
http_req_failed................: 0.00%  ✓ 0          ✗ 6780
http_req_receiving.............: avg=27.81µs  min=6µs      med=20µs     max=1.29ms   p(90)=55µs     p(95)=72µs
http_req_sending...............: avg=14.9µs   min=1µs      med=7µs      max=2.28ms   p(90)=19µs     p(95)=25µs
http_req_tls_handshaking.......: avg=0s       min=0s       med=0s       max=0s       p(90)=0s       p(95)=0s
http_req_waiting...............: avg=54.98ms  min=1.87ms   med=36.45ms  max=171.41ms p(90)=128.24ms p(95)=151.33ms
http_reqs......................: 6780   112.778197/s
iteration_duration.............: avg=265.98ms min=250.47ms med=265.93ms max=284.53ms p(90)=272.44ms p(95)=274.45ms
iterations.....................: 2260   37.592732/s
vus............................: 10     min=10       max=10
vus_max........................: 10     min=10       max=10
```

#### `gunicorn -w 2 donkey_patched_async_app:app`

```bash
data_received..................: 1.8 MB 28 kB/s
data_sent......................: 386 kB 6.0 kB/s
http_req_blocked...............: avg=25.09ms  min=140µs    med=430µs    max=6.71s  p(90)=778µs    p(95)=895µs
http_req_connecting............: avg=25.05ms  min=127µs    med=394µs    max=6.71s  p(90)=717µs    p(95)=818µs
http_req_duration..............: avg=76.42ms  min=769µs    med=35.82ms  max=8s     p(90)=126.92ms p(95)=150.27ms
 { expected_response:true }...: avg=76.42ms  min=769µs    med=35.82ms  max=8s     p(90)=126.92ms p(95)=150.27ms
http_req_failed................: 0.00%  ✓ 0         ✗ 4764
http_req_receiving.............: avg=47.52µs  min=12µs     med=39µs     max=1.14ms p(90)=86µs     p(95)=99µs
http_req_sending...............: avg=24.89µs  min=6µs      med=21µs     max=2.01ms p(90)=38µs     p(95)=46µs
http_req_tls_handshaking.......: avg=0s       min=0s       med=0s       max=0s     p(90)=0s       p(95)=0s
http_req_waiting...............: avg=76.35ms  min=732µs    med=35.74ms  max=8s     p(90)=126.85ms p(95)=150.2ms
http_reqs......................: 4764   73.958065/s
iteration_duration.............: avg=405.09ms min=241.69ms med=265.17ms max=8.11s  p(90)=274.85ms p(95)=279.56ms
iterations.....................: 1588   24.652688/s
vus............................: 10     min=10      max=10
vus_max........................: 10     min=10      max=10
```

## Tests without DB Latency using two workers

Fake DB Server Command

```bash
./fake_db_server.py
```

### `gunicorn -w 2 sync_app:app`

```bash
data_received..................: 2.0 MB 33 kB/s
data_sent......................: 432 kB 7.2 kB/s
http_req_blocked...............: avg=71.4ms   min=96µs     med=273µs    max=13.11s p(90)=659µs    p(95)=904µs
http_req_connecting............: avg=71.38ms  min=78µs     med=251µs    max=13.11s p(90)=609µs    p(95)=837µs
http_req_duration..............: avg=7.69ms   min=445µs    med=2.66ms   max=3.51s  p(90)=5.11ms   p(95)=5.99ms
  { expected_response:true }...: avg=7.69ms   min=445µs    med=2.66ms   max=3.51s  p(90)=5.11ms   p(95)=5.99ms
http_req_failed................: 0.00%  ✓ 0         ✗ 5337
http_req_receiving.............: avg=29.67µs  min=11µs     med=26µs     max=351µs  p(90)=43µs     p(95)=51µs
http_req_sending...............: avg=16.54µs  min=5µs      med=13µs     max=362µs  p(90)=26µs     p(95)=33µs
http_req_tls_handshaking.......: avg=0s       min=0s       med=0s       max=0s     p(90)=0s       p(95)=0s
http_req_waiting...............: avg=7.65ms   min=409µs    med=2.62ms   max=3.51s  p(90)=5.06ms   p(95)=5.95ms
http_reqs......................: 5337   88.787916/s
iteration_duration.............: avg=337.72ms min=102.84ms med=110.39ms max=13.22s p(90)=119.67ms p(95)=312.92ms
iterations.....................: 1779   29.595972/s
vus............................: 10     min=10      max=10
vus_max........................: 10     min=10      max=10
```

### `uvicorn --workers 2 --log-level error async_app:app`

```bash
data_received..................: 6.0 MB 100 kB/s
data_sent......................: 1.4 MB 23 kB/s
http_req_blocked...............: avg=2.47µs   min=0s       med=1µs      max=1.19ms   p(90)=3µs      p(95)=5µs
http_req_connecting............: avg=405ns    min=0s       med=0s       max=749µs    p(90)=0s       p(95)=0s
http_req_duration..............: avg=1.5ms    min=136µs    med=607µs    max=41.55ms  p(90)=3.75ms   p(95)=4.73ms
  { expected_response:true }...: avg=1.5ms    min=136µs    med=607µs    max=41.55ms  p(90)=3.75ms   p(95)=4.73ms
http_req_failed................: 0.00%  ✓ 0          ✗ 17175
http_req_receiving.............: avg=18.17µs  min=5µs      med=16µs     max=940µs    p(90)=26µs     p(95)=34µs
http_req_sending...............: avg=7.39µs   min=1µs      med=5µs      max=3.35ms   p(90)=14µs     p(95)=19µs
http_req_tls_handshaking.......: avg=0s       min=0s       med=0s       max=0s       p(90)=0s       p(95)=0s
http_req_waiting...............: avg=1.47ms   min=122µs    med=585µs    max=38.17ms  p(90)=3.73ms   p(95)=4.7ms
http_reqs......................: 17175  285.801164/s
iteration_duration.............: avg=104.95ms min=101.63ms med=104.56ms max=143.85ms p(90)=106.75ms p(95)=108.28ms
iterations.....................: 5725   95.267055/s
vus............................: 10     min=10       max=10
vus_max........................: 10     min=10       max=10
```

### `gunicorn -k uvicorn.workers.UvicornWorker -w 2 async_app:app`

```bash
data_received..................: 6.0 MB 99 kB/s
data_sent......................: 1.4 MB 23 kB/s
http_req_blocked...............: avg=2.29µs   min=0s       med=1µs      max=1.1ms    p(90)=3µs      p(95)=4µs
http_req_connecting............: avg=404ns    min=0s       med=0s       max=722µs    p(90)=0s       p(95)=0s
http_req_duration..............: avg=1.78ms   min=209µs    med=920.5µs  max=23.64ms  p(90)=4.16ms   p(95)=5.15ms
  { expected_response:true }...: avg=1.78ms   min=209µs    med=920.5µs  max=23.64ms  p(90)=4.16ms   p(95)=5.15ms
http_req_failed................: 0.00%  ✓ 0          ✗ 17040
http_req_receiving.............: avg=17.68µs  min=5µs      med=15µs     max=334µs    p(90)=26µs     p(95)=33µs
http_req_sending...............: avg=7.56µs   min=1µs      med=5µs      max=2.34ms   p(90)=13µs     p(95)=18µs
http_req_tls_handshaking.......: avg=0s       min=0s       med=0s       max=0s       p(90)=0s       p(95)=0s
http_req_waiting...............: avg=1.75ms   min=200µs    med=899µs    max=23.59ms  p(90)=4.14ms   p(95)=5.12ms
http_reqs......................: 17040  283.579513/s
iteration_duration.............: avg=105.77ms min=101.79ms med=105.27ms max=128.54ms p(90)=108.12ms p(95)=110.19ms
iterations.....................: 5680   94.526504/s
vus............................: 10     min=10       max=10
vus_max........................: 10     min=10       max=10
```
