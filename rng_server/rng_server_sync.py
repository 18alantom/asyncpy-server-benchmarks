from .response import get_body


def app(environ, start_response):
    data = get_body()
    status = "200 OK"

    response_headers = [
        ("Content-Type", "application/json"),
        ("Content-Length", str(len(data))),
    ]

    start_response(status, response_headers)

    return [data]

# SERVER COMMAND:
#   gunicorn -w 21 rng_server.rng_server_sync:app
#
# AUTOCANNON OUTPUT:
#   Running 10s test @ http://127.0.0.1:8000
#   10 connections
#
#
#   ┌─────────┬────────┬─────────┬─────────┬─────────┬────────────┬────────────┬─────────┐
#   │ Stat    │ 2.5%   │ 50%     │ 97.5%   │ 99%     │ Avg        │ Stdev      │ Max     │
#   ├─────────┼────────┼─────────┼─────────┼─────────┼────────────┼────────────┼─────────┤
#   │ Latency │ 126 ms │ 2543 ms │ 4823 ms │ 4892 ms │ 2498.26 ms │ 1428.61 ms │ 4980 ms │
#   └─────────┴────────┴─────────┴─────────┴─────────┴────────────┴────────────┴─────────┘
#   ┌───────────┬────────┬────────┬────────┬────────┬────────┬─────────┬────────┐
#   │ Stat      │ 1%     │ 2.5%   │ 50%    │ 97.5%  │ Avg    │ Stdev   │ Min    │
#   ├───────────┼────────┼────────┼────────┼────────┼────────┼─────────┼────────┤
#   │ Req/Sec   │ 4519   │ 4519   │ 4747   │ 4783   │ 4714.8 │ 84.99   │ 4517   │
#   ├───────────┼────────┼────────┼────────┼────────┼────────┼─────────┼────────┤
#   │ Bytes/Sec │ 927 kB │ 927 kB │ 974 kB │ 982 kB │ 967 kB │ 17.4 kB │ 927 kB │
#   └───────────┴────────┴────────┴────────┴────────┴────────┴─────────┴────────┘
#
#   Req/Bytes counts sampled once per second.
#   # of samples: 10
#
#   94k requests in 10.01s, 9.67 MB read
#   46k errors (0 timeouts)


# SERVER COMMAND:
#   gunicorn -w 1 rng_server.rng_server_sync:app
#
# AUTOCANNON OUTPUT:
#   Running 10s test @ http://127.0.0.1:8000
#   10 connections
#   
#   
#   ┌─────────┬────────┬─────────┬─────────┬─────────┬────────────┬───────────┬─────────┐
#   │ Stat    │ 2.5%   │ 50%     │ 97.5%   │ 99%     │ Avg        │ Stdev     │ Max     │
#   ├─────────┼────────┼─────────┼─────────┼─────────┼────────────┼───────────┼─────────┤
#   │ Latency │ 136 ms │ 2747 ms │ 5322 ms │ 5400 ms │ 2740.82 ms │ 1557.6 ms │ 5457 ms │
#   └─────────┴────────┴─────────┴─────────┴─────────┴────────────┴───────────┴─────────┘
#   ┌───────────┬────────┬────────┬────────┬────────┬─────────┬─────────┬────────┐
#   │ Stat      │ 1%     │ 2.5%   │ 50%    │ 97.5%  │ Avg     │ Stdev   │ Min    │
#   ├───────────┼────────┼────────┼────────┼────────┼─────────┼─────────┼────────┤
#   │ Req/Sec   │ 2061   │ 2061   │ 2143   │ 2187   │ 2128.46 │ 42.6    │ 2060   │
#   ├───────────┼────────┼────────┼────────┼────────┼─────────┼─────────┼────────┤
#   │ Bytes/Sec │ 423 kB │ 423 kB │ 440 kB │ 449 kB │ 437 kB  │ 8.76 kB │ 423 kB │
#   └───────────┴────────┴────────┴────────┴────────┴─────────┴─────────┴────────┘
#   
#   Req/Bytes counts sampled once per second.
#   # of samples: 11
#   
#   47k requests in 11.01s, 4.8 MB read
#   23k errors (0 timeouts)