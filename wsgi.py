from app import create_app
from werkzeug.serving import run_simple

app = create_app()

if __name__ == "__main__":
    host = '0.0.0.0'
    port = 443
    run_simple(host, port, app)