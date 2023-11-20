Simple POC to compare async and sync Python.

Two webservers are to be made:
1. WSGI web server
2. ASGI web server

Both web servers do a couple of things:
1. `/`: Return a templated HTML page.
2. `/api`: Pings the "db" server to get a random piece of data.
  - another server that takes a fixed amount of time and returns a random number.
3. Background jobs: completes background jobs.
  - executes some function that takes some time to run.

