from flask import Flask, render_template

app = Flask(__name__, template_folder='../../templates', static_folder="../../static")

@app.route('/')
def index():
    return render_template('index.html')  # No need for './templates/'

def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()
