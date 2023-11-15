import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime


api_key = 'bd1b3955b0d2e7af1a7080900322197e'
endpoint = 'https://api.openweathermap.org/data/2.5/weather?lat=45.96&lon=66.64&appid=bd1b3955b0d2e7af1a7080900322197e'

#enter the respective information
sender_email = ''
sender_pass = ''
receiver_email = ''



def get_weather():
    city = "Fredericton"
    parameters = {
        'lat': 45.96,
        'lon': 66.64,
        'exclude': 'minutely,hourly',
        'appid': api_key,
        'units': 'metric'
    }

    response = requests.get(endpoint, params=parameters)
    if response.status_code == 200:
        data = response.json()
        print("API Response:", data)
    else:
        print("Error in API request. Status code:", response.status_code)
        print("Response content:", response.content)
    

    # if 'current' not in data:
    #     print("Error: 'current' key not found in API response")
    #     return None, None

    # Extract the current date, weather condition, and wind speed
    #current_date = datetime.utcfromtimestamp(data['current']['dt']).strftime('%Y-%m-%d')
    weather_condition = data['weather'][0]['main']
    wind_speed = data['wind']['speed']

    print(weather_condition)
    print(wind_speed)

    return weather_condition, wind_speed


# Enable debugging for the SMTP connection
# logging.basicConfig(level=logging.DEBUG)
# logging.getLogger('smtplib').setLevel(logging.DEBUG)

def send_email(subject, body):
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_pass)
        server.sendmail(sender_email, receiver_email, message.as_string())
    print("Email sent successfully!")


def main():
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    weather_condition, wind_speed = get_weather()

    print("Current Time:", current_time)
    print("Weather Condition:", weather_condition)
    print("Wind Speed:", wind_speed)

    if current_time == "14:40":
        subject = f"WEATHER REMINDER! {weather_condition} ALERT!!"
        body = f"Reminder! The weather forecast for today is {weather_condition}. Wind speed: {wind_speed} m/s."
        print("Email should be sent:")
        print("Subject:", subject)
        print("Body:", body)
        send_email(subject, body)
    else:
        print("No need to send an email.")

if __name__ == "__main__":
    main()