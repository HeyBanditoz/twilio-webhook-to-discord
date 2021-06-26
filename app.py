import argparse
import hashlib
import sys
from discord_webhook import DiscordWebhook, DiscordEmbed
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
parsed = None


@app.route("/", methods=['POST'])
def sms_reply():
    # we log original body instead of modified body which could have attachments at the end (prevents double attachments)
    original_body = request.values.get('Body', str)
    body = original_body
    number = phone_format(request.values.get('From', int))
    # don't give robohash exact phone number
    number_hash = hashlib.md5(str(number).encode('utf-8')).hexdigest()
    nummedia = int(request.values.get('NumMedia', int))

    if nummedia > 0:
        if parsed.m:
            for x in range(0, nummedia):
                body += '\n<' + \
                    request.values.get('MediaUrl{}'.format(x)) + '>'
        elif nummedia > 0:
            body += '\n{} attachment(s).'.format(nummedia)

    webhook = DiscordWebhook(
        url=parsed.w,
        username=number,
        content=body,
        # robohash for unique avatar per number
        avatar_url='https://robohash.org/{}'.format(number_hash)
    )

    webhook.execute()

    attachments = ''
    if nummedia > 0:
        for x in range(0, nummedia):
            attachments += '\n' + \
                request.values.get('MediaUrl{}'.format(x))
    print('[{}] {}{}'.format(number, original_body, attachments))

    return str(MessagingResponse())


def phone_format(n):
    """
    Formats a phone number.
    See https://stackoverflow.com/a/7058216
    """
    return format(int(n[:-1]), ",").replace(",", "-") + n[-1]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Handles inbound SMS messages and delivers to Discord.")
    parser.add_argument(
        '-p', help='Specifies the port to run the webserver on.')
    parser.add_argument(
        '-w', help='The Discord webhook to deliver to.', type=str)
    parser.add_argument('-m', action='store_true',
                        help='Send media links to Discord.', default=False)
    parsed = parser.parse_args()

    # args passed via `flask` on commandline
    app.run(host='0.0.0.0', port=parsed.p)
