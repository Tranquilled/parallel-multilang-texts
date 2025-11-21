from flask import Flask, flash, get_flashed_messages, render_template, redirect, request
import os
import requests
import tempfile
import textract

import ipdb
from itertools import zip_longest
import lorem

app = Flask(__name__)
app.secret_key = b"@UUi8Q!^n&W82@&"  # TODO: don't deploy this
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
with tempfile.TemporaryDirectory() as tmpdir:
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER = tmpdir

def parse_text(file):
    text = textract.process(file)
    return [x.decode("utf-8") for x in text.split(b"\n") if x not in {b"", b"\n"}]

@app.route("/result", methods=["POST"])
def receive_uploads() -> list[list[str]]:
    source = request.files['source']
    cipher = request.files['cipher']
    if not all([source.filename, cipher.filename]):
        flash("Not enough files")
        return redirect("/")
    texts = []
    for file in [source, cipher]:
        suffix = file.filename.split(".")[-1]
        tmpfile = f"{tempfile.mkstemp()[1]}.{suffix}"
        file.save(os.path.join(UPLOAD_FOLDER, tmpfile))
        try:
            texts.append(parse_text(tmpfile))
        except:
            flash(f"{file.filename} could not be read. Try again!")
            return redirect("/")
    rows = zip_longest(*texts)
    return render_template("output.html", title="test tests test", rows=rows)


@app.route("/")
def input_texts():
    try:
        flash = get_flashed_messages().pop()
    except:
        flash = ""
    return render_template("input.html", flash=flash)


# @app.route("/result")
# def output_texts():
#     rows = [
#         [lorem.get_paragraph(count=1), lorem.get_paragraph(count=1)] for _ in range(50)
#     ]
#     return render_template("output.html", title="test tests test", rows=rows)
