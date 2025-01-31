import requests
import os
import time
from datetime import datetime, date
from threading import Thread

from pytz import timezone
from beetlebox.gmail_api import send_gmail


IP_API_ENDPOINT = 'https://api.ipgeolocation.io/ipgeo'
IP_API_KEY = os.getenv('IP_API_KEY')
ALERT_RECIPIENT = os.getenv('ALERT_RECIPIENT')


def admin_alert(subject, message_body, recipient='admin', datetime_header=True, timestamp_footer=True, repair_token_and_test=False):

    timestamp_now = time.time()

    if recipient == 'admin':
        recipient = ALERT_RECIPIENT

    full_message = ''

    if datetime_header:
        pacific_tz = timezone("US/Pacific")
        time_to_format = datetime.fromtimestamp(timestamp_now, tz=pacific_tz)
        second = round(float(time_to_format.strftime("%S.%f")), 2)
        formatted_datetime = time_to_format.strftime(f"%Y-%m-%d %H:%M:{second}")
        full_message += f'{formatted_datetime}\n'

    full_message += message_body

    if timestamp_footer:
        full_message += f'\n{timestamp_now}'

    print(f"***** ADMIN ALERT START *****\nSubject: {subject}\n{full_message}\n****** ADMIN ALERT END ******")

    send_gmail(recipient, subject, full_message, repair_token_and_test)


def admin_alert_thread(subject, message, recipient='admin', datetime_header=True, timestamp_footer=True):
    alert_args = [subject, message, recipient, datetime_header, timestamp_footer]
    alert_thread = Thread(target=admin_alert, args=alert_args)
    alert_thread.start()


def login_alert(ip_addr, user_id):

    api_params = {
        'apiKey': IP_API_KEY,
        'ip': ip_addr,
        'fields': 'geo',
        'excludes': 'continent_code,continent_name,country_code2,country_code3',
    }

    api_response = requests.get(IP_API_ENDPOINT, params=api_params)
    # if api_response.status_code != 200:
    #     # API call unsuccessful.
    #     pass

    message = f'KID APP\nUser "{user_id}" logged in successfully.\n\n{api_response.text}'
    admin_alert('Web App - Log', message)


def login_alert_thread(ip_addr, user_id):
    alert_args = [ip_addr, user_id]
    alert_thread = Thread(target=login_alert, args=alert_args)
    alert_thread.start()


def year_range_since(first_year):
    current_year = date.today().year
    if current_year > first_year:
        return f'{first_year}-{current_year}'
    else:
        return f'{first_year}'


def copyright_notice(first_year):
    copyright_years = year_range_since(first_year)
    notice_str = f'{copyright_years} Johnathan Pennington | All rights reserved.'
    return notice_str
