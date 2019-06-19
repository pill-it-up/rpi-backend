from flask import Flask, jsonify
from picamera import PiCamera
from pathlib import Path

import requests
import json
import logging

logging.basicConfig(
    filename="{}".format(Path.home() / "logs" / "backend.log"),
    format="%(asctime)s == PILLITUP == ACQUISITION == [%(levelname)-8s] %(message)s",
    level=logging.DEBUG,
)

app = Flask("pill_it_up_rpi_backend")

PROT = "http://"
HOST = "35.189.72.164"
PORT = 5000
ENDPOINT = "/predict"

camera = [None]


@app.route("/start")
def start():
    logging.debug("Received start request.")

    if camera[0] is not None:
        logging.warning("Camera is already activated.")
        return jsonify({"camera": "already_on"})

    logging.debug("Activating camera.")
    camera[0] = PiCamera()

    return jsonify({"camera": "on"})


@app.route("/newpill", methods=["GET", "POST"])
def newpill():
    logging.debug("Received newpill request.")

    if camera[0] is None:
        logging.warning("Camera is not activated.")
        return jsonify({"camera": "not_started"})

    logging.debug("Capturing pill image.")
    camera[0].capture("pill.jpg")
    files = {"media": open("pill.jpg", "rb")}

    try:
        logging.debug("POSTing image to server.")
        post = requests.post(f"{PROT}{HOST}:{PORT}{ENDPOINT}", files=files, timeout=5)
    except requests.exceptions.Timeout:
        logging.error("POST request timed out!")
        return jsonify({"medication": "?"})

    ans = json.loads(post.text)

    return jsonify(ans)


@app.route("/stop")
def stop():
    logging.debug("Received stop request.")

    if camera[0] is None:
        logging.warning("Camera is already deactivated.")
        return jsonify({"camera": "already_off"})

    logging.debug("Dectivating camera.")
    camera[0].close()
    camera[0] = None

    return jsonify({"camera": "off"})


if __name__ == "__main__":
    logging.info("Starting server.")
    app.run(host="0.0.0.0", port=5000)
