from flask import Flask, jsonify
from picamera import PiCamera

import requests
import json

app = Flask("pill_it_up_rpi_backend")

camera = [None]


@app.route("/start")
def start():
    if camera[0] is not None:
        return jsonify({ 'camera': 'already_on' })

    camera[0] = PiCamera()
    camera[0].resolution = (800, 600)

    return jsonify({ 'camera': 'on' })


@app.route("/newpill", methods=["GET", "POST"])
def newpill():
    if camera[0] is None:
        return jsonify({ 'camera': 'not_started' })

    camera[0].capture("image.jpg")
    files = {"media": open("image.jpg", "rb")}

    post = requests.post("http://104.197.248.132:5000/predict", files=files)
    ans = json.loads(post.text)

    return jsonify(ans)


@app.route("/stop")
def stop():
    if camera[0] is None:
        return jsonify({ 'camera': 'already_off' })

    camera[0].stop()
    camera[0] = None

    return jsonify({ 'camera': 'off' })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
