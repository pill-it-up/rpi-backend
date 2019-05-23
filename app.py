from flask import Flask

app = Flask("pill_it_up_rpi_backend")


@app.route("/start")
def start():
    # Start camera
    pass


@app.route("/newpill", methods=["GET", "POST"])
def newpill():
    # Gets screenshot from camera and send to cloud
    pass


@app.route("/stop")
def stop():
    # Stop camera
    pass


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
