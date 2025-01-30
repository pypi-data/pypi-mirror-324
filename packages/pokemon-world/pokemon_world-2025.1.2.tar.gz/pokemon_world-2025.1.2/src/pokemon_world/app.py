import argparse
from flask import Flask, render_template
import os


def create_app():
    app = Flask(__name__,
                static_folder=os.path.join(os.path.dirname(__file__), 'static'),
                template_folder=os.path.join(os.path.dirname(__file__), 'templates'))
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app


def run_server(host='0.0.0.0', port=5000):
    """Run the Flask server with specified host and port"""
    app = create_app()
    app.run(host=host, port=port)

def main():
    parser = argparse.ArgumentParser(
        description='Pokemon World Web Application',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        '-p', '--port',
        type=int,
        default=5000,
        help='Port to run the server on'
    )
    
    parser.add_argument(
        '-H', '--host',
        default='0.0.0.0',
        help='Host interface to bind the server'
    )
    
    args = parser.parse_args()
    run_server(host=args.host, port=args.port)

if __name__ == '__main__':
    main()