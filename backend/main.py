from src.app import create_app
from src.bootstrap import bootstrap
from src.settings import DEBUG, HOST, PORT

bootstrap()
app = create_app()

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=DEBUG)
