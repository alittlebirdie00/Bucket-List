from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/signUp', methods=['POST'])
def signUp():
    _name = request.form['inputName']

@app.route("/")
def main():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()
