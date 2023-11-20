def get_template():
    from jinja2 import Environment, FileSystemLoader, select_autoescape

    env = Environment(
        loader=FileSystemLoader("./templates"),
        autoescape=select_autoescape(),
    )
    return env.get_template("home.html")


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
