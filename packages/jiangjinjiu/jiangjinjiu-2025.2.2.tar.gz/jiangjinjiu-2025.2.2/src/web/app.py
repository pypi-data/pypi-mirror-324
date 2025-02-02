from flask import Flask, abort

app = Flask(__name__)

@app.route('/<int:number>/')
def dynamic_route(number):
    if 0 <= number <= 9:
        return f"这是路径 /{number}/"
    else:
        abort(404)  # 如果数字不在0到9之间，返回404错误

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)