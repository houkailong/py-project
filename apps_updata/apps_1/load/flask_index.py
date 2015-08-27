# encoding=UTF-8
__author__ = 'xuebaoku'

from flask import Flask , request
app = Flask(__name__)
@app.route('/')
def hello_world():
    name = request.args.get('id',1)
    return 'Hello World! %s'%(name)

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=8888)