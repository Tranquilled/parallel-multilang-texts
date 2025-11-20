from flask import Flask, render_template
import lorem
import requests

app = Flask(__name__)


def get_texts(urls: list[str]) -> list[list[str]]:
    pass


@app.route("/")
def hello_world():
    rows = [
        [lorem.get_paragraph(count=1), lorem.get_paragraph(count=1)] for _ in range(50)
    ]
    return render_template("test.html", title="test tests test", rows=rows)
