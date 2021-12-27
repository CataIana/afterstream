from blacksheep import server
from blacksheep import messages
from blacksheep.server import responses
from aiohttp import ClientSession
from disnake import Webhook, Forbidden, HTTPException, NotFound
from json import loads

# Command syntax for fossabot (Just replace url, streamername and token):
# @$(sender) $(customapi <url>/afterstream/<streamername>?token=<token>&message=$(urlencode $(query))&sendername=$(urlencode $(sendername))&time=$(urlencode $(time Australia/Sydney ddd MMM Do YYYY, h:mma z))&uptime=$(urlencode $(uptime $(channel))))

app = server.Application()

#Load it on startup to avoid wasted IO. Means a restart is required to update
with open("webhooks.json") as f:
    webhooks = loads(f.read())

@app.router.get("/afterstream/{channel}")
async def get_request(request: messages.Request, channel: str) -> str:
    if channel not in webhooks.keys():
        return responses.text("Error: Streamer not defined")
    try:
        message = request.query.get("message")[0]
        sendername = request.query.get("sendername")[0]
        time = request.query.get("time")[0]
        uptime = request.query.get("uptime")[0].strip("[Error: ]")
        token = request.query.get("token", [None])[0]
        if webhooks[channel].get("token", None) is not None:
            if token is None:
                return "Error: Token required for this afterstream!"
            if token != webhooks[channel].get("token"):
                return "Error: Invalid Token!"
        for webhook in webhooks[channel]["webhooks"]:
            async with ClientSession() as client:
                w = Webhook.from_url(webhook, session=client)
                try:
                    await w.send(f"```\n{message}\n\n🤵 Submitted by: {sendername}\n⌚ {time}\n📺 Uptime: {uptime}```")
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
    except IndexError:
        return "Error: Not all arguments provided"
