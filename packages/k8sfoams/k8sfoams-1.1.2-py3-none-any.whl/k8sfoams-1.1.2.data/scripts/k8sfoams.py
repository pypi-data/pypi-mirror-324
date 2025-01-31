#!python
import argparse
from k8sfoam.src.app import create_app


app = create_app()

if __name__ == '__main__' and app:
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='127.0.0.1', required=False, help='Host IP on which server listen')
    parser.add_argument('--port', type=int, default=8080, required=False, help='Port on which server listen')
    parser.add_argument('-d', action='store_true', help='Run server in debug mode')
    args = parser.parse_args()
    app.run(host=args.host, port=args.port, debug=args.d)
