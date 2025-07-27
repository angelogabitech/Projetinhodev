from flask import flask 

app= flask(__name__)

@app.route('/')
def home():
    return "flask funcionando"

if __name__ == '__main__':
    app.run(debug=True)