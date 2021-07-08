from bottle import request, default_app
from discord import Webhook, RequestsWebhookAdapter
import json

from discord.errors import Forbidden, HTTPException, NotFound

app = default_app()

def get_request(channel, request):
    with open("webhooks.json") as f:
        webhooks = json.load(f)
    if channel not in webhooks.keys():
        return "Error: Streamer not defined"
    try:
        message = request.query["message"]
        sendername = request.query["sendername"]
        time = request.query["time"]
        uptime = request.query["uptime"]
        token = request.query.get("token", None)
        if webhooks[channel].get("token", None) is not None:
            if token is None:
                return "Error: Token required for this afterstream!"
            if token != webhooks[channel].get("token"):
                return "Error: Invalid Token!"
        for webhook in webhooks[channel]["webhooks"]:
            w = Webhook.from_url(webhook, adapter=RequestsWebhookAdapter())
            try:
                w.send(f"```\n{message}\n\n🤵 Submitted by: {sendername}\n⌚ {time}\n📺 Uptime: {uptime}```")
            except HTTPException:
                return "Error while submitting afterstream. Please try again later."
            except NotFound:
                return "Error: Unknown Webhook"
            except Forbidden:
                return "Error while submitting afterstream. Please try again later."
            else:
                return "Afterstream Message Submitted Succesfully."
    except KeyError:
        return "Error: Not all arguments provided"

@app.route("/afterstream/<channel>", method="get")
def index(channel):
    return get_request(channel, request)

if __name__ == '__main__':
    app.run(host='localhost', port=58496, debug=False)
