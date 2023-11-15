import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime


api_key = '' #Used the OpenWeatherMap API
endpoint = 'https://api.openweathermap.org/data/2.5/weather?lat=45.96&lon=66.64&appid=<API KEY>'

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
    else:
        print("Error in API request. Status code:", response.status_code)
        print("Response content:", response.content)
    
    weather_condition = data['weather'][0]['main']
    wind_speed = data['wind']['speed']

    return weather_condition, wind_speed


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


def main():
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    weather_condition, wind_speed = get_weather()

    print("Current Time:", current_time)
    print("Weather Condition:", weather_condition)
    print("Wind Speed:", wind_speed)

    if current_time == "7:30":
        subject = f"WEATHER REMINDER! {weather_condition} ALERT!!"
        body = f"Reminder! The weather forecast for today is {weather_condition}. Wind speed: {wind_speed} m/s."
        print("Email should be sent:")
        print("Subject:", subject)
        print("Body:", body)
        send_email(subject, body)

if __name__ == "__main__":
    main()
