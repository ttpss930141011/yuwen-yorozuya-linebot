import sys
from flask import Flask, request, abort
from config import CHANNEL_SECRET, CHANNEL_ACCESS_TOKEN, PORT
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from utils.error_logger import errlogger
from line_bot import handler

app = Flask(__name__)

if CHANNEL_SECRET is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if CHANNEL_ACCESS_TOKEN is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)


@app.route("/")
def hello_world():
    return f'Hello, World! This server is running on port {PORT}'


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info(
            "Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@app.errorhandler(404)
def page_not_found(e):
    app.logger.error('Page not found.')
    errlogger.error('Page not found.')
    return 'This page does not exist', 404

@app.errorhandler(500)
def server_error(e):
    app.logger.error('An error occurred during a request.')
    errlogger.error('An error occurred during a request.')
    return 'An internal error occurred.', 500


if __name__ == "__main__":
    app.run(debug=True, port=PORT, host='0.0.0.0')
