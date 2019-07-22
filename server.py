from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    return render_template('add_question.html')


if __name__ == '__main__':
    app.run(debug=True)
