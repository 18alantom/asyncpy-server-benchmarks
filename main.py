from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape



env = Environment(
    loader=FileSystemLoader("./templates"),
    autoescape=select_autoescape(),
)
template = env.get_template("home.html")

print(template.render(server_type="Test", date=datetime.now().isoformat()))
