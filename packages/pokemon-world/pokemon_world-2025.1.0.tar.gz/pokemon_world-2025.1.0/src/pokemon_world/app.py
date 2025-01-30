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

def main():
    app = create_app()
    app.run(debug=True)

if __name__ == '__main__':
    main()