def get_kwargs_from_argv():
    import sys

    argv = []
    argv[:] = sys.argv[1:]

    kwargs = {}
    while len(argv) > 0:
        k = argv.pop(0)
        if not k.startswith("--"):
            continue

        k = k[2:]
        v = argv.pop(0)

        try:
            kwargs[k] = int(v)
        except Exception as _:
            kwargs[k] = v

    return kwargs
