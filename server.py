from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from stackoverflow import fetch_data

app = Flask(__name__, static_url_path='', root_path='./')
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    data = fetch_data.fetch_10_top_questions()
    answer_html = "<h2>this is an answer</h2>"
    return render_template('home.html',
                           newest_questions=data['newest_questions'],
                           most_voted_questions = data['most_voted_questions'],
                           answer_html = answer_html)

if __name__ =='__main__':
    app.run(host='127.0.0.1',port=5000,debug=True)
