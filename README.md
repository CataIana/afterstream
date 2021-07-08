# afterstream
Command that submits messages from a twitch chat to discord webhook. 
A small script that I'm not really going to bother going with a highly detailed readme for.

You'll need a webserver to run this, set that port in the systemd service you run the script with, the one I use has been provided. I run this behind an nginx reverse proxy, I highly recommend you do too.

Make sure you install the dependencies in the requirements.txt

Fill in the settings file (make sure to rename it to `webhooks.json`)

For the token part, set it to null in the settings and it won't be required as a query parameter, otherwise it will be required

Command syntax for fossabot (I think nightbot just replaces customapi with urlfetch):
`@$(sender) $(customapi <url>/<streamername>?token=<tokenforthatstreamerifrequired>&message=$(urlencode $(query))&sendername=$(urlencode $(sendername))&time=$(urlencode $(time <timezone> ddd MMM Do YYYY, h:mma z))&uptime=$(urlencode $(uptime $(channel))))`
Replace anything surrounded by <> with what it should be
