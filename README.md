# Twilio Webhook -> Discord Bridge

A simple Flask webserver that listens on HTTP for incoming Twilio messages.

It is recommended you run this behind a reverse proxy, such as Apache, Nginx,
træfik, or others, so you can have authentication and HTTPS.

## Example
![Example](example.png)

## Commandline Arguments
```
usage: app.py [-h] [-p P] [-w W] [-m]

Handles inbound SMS messages and delivers to Discord.

optional arguments:
  -h, --help  show this help message and exit
  -p P        Specifies the port to run the webserver on.
  -w W        The Discord webhook to deliver to.
  -m          Send media links to Discord.
```