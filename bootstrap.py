import os
import sys
from twilio.rest import TwilioRestClient

if __name__ == "__main__":
    # TODO Better arg input & validation (maybe using argparse)
    # Validate arguments
    argc = len(sys.argv)
    if argc < 3 or argc > 4:
        print("Usage: python bootstrap.py <account_sid> <auth_token> <phone_number> [<app_route>]")
        sys.exit(-1)
    account_sid = sys.argv[1]
    auth_token = sys.argv[2]
    phone_number_sid = sys.argv[3]
    app_route = sys.argv[4]
    if app_route is None:
        app_route = ''
    print "Account SID: " + account_sid
    print "Auth Token: " + auth_token
    print "Phone Number SID: " + phone_number_sid

    # Scrape app url from env and update PN SMS URL
    app_url = 'http://' + os.environ['C9_HOSTNAME'] + '/' + app_route
    print "App URL: " + app_url
    print "Updating SMS URL for phone number..."
    client = TwilioRestClient(account_sid, auth_token)
    number = client.phone_numbers.update(phone_number_sid, sms_url=app_url)
