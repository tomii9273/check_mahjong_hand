import re

from flask import Flask, render_template, request

from get_result import get_result

app = Flask(__name__)

# getのときの処理
@app.route("/", methods=["GET"])
def get():
    return render_template("index.html", message="",)


# postのときの処理
@app.route("/", methods=["POST"])
def post():
    tehai_zip = request.form["name"]
    tehai_zip = "".join(re.findall("[a-zA-Z0-9_]+", tehai_zip))
    waits, agarikeis = get_result(tehai_zip)

    mes0 = f"待ちは {waits} です。"
    mes1 = f"アガリ形の一覧: {agarikeis}"

    return render_template("index.html", message=mes0, message1=mes1)


if __name__ == "__main__":
    app.run()
