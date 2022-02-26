import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
#----------twilio details--------#
account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")
#---------------------------------#

MY_LAT = -6.300497
MY_LONG = 22.553838
api_key = os.environ.get("OWM_API_KEY")


parameters = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "appid": api_key,
    "exclude": "current,minutely,daily"
}

response = requests.get(url="https://api.openweathermap.org/data/2.5/onecall", params=parameters)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data["hourly"][:12]

will_rain = False

for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

# send sms to number if rains
if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}

    client = Client(account_sid, auth_token, http_client= proxy_client)
    message = client.messages \
                    .create(
                        body="Bring an Umbrella'☂'. It might be rain.",
                        from_='+18596817355',
                        to='+918178302542'
                    )
    print(message.status)
