#!/usr/bin/env python

from flask import Flask

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def index():
    return "api online"

@app.route('/beer/<legi>')
def beer_legi(legi):
    return legi

if __name__ == '__main__':
    app.run(debug=True)

print('imported app!')
