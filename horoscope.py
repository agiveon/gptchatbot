from datetime import datetime, timezone, timedelta
from typing import Dict, Optional, Any
import requests
import json


DIVINE_API_KEY = "31b3b31a1c2f8a370206f111127c0dbd"
ASTROAPI_API_KEY = 'ByVOIaODH57QRVi6CqswHXGlcpDvj7tZBRoorY'
ASTROAPI_USER_ID = '4545'


def get_daily_horoscope(
    sign: str, day: str, time_zone: int) -> Optional[Dict[str, str]]:
    """Returns the persons daily horoscope in this format:
    Personal, Health, Profession, Emotions, Travel, Luck"""

    url = "https://divineapi.com/api/1.0/get_daily_horoscope.php"

    data = {
        "api_key": DIVINE_API_KEY,
        "date": day,
        "sign": sign.upper(),
        "timezone": time_zone,
    }
    try:
        response = requests.post(url, data=data)
    except Exception as e:
        print("Bad request", e)
        return None

    if response.status_code != 200:
        print("Bad request")
        return None

    try:
        res_json = json.loads(response.text)
    except Exception as e:
        print("Bad request", e)
        return None

    return res_json["data"]["prediction"]


def get_weekly_horoscope(sign: str, week: str) -> Optional[Dict[str, str]]:
    """Returns the persons weekly horoscope in this format:
    Personal, Health, Profession, Emotions, Travel, Luck
    week has to be one of these three values: current, prev or next"""

    url = "https://divineapi.com/api/1.0/get_weekly_horoscope.php"

    data = {
        "api_key": DIVINE_API_KEY,
        "week": week,
        "sign": sign.upper(),
    }
    try:
        response = requests.post(url, data=data)
    except Exception as e:
        print("Bad request", e)
        return None

    if response.status_code != 200:
        print("Bad request")
        return None

    try:
        res_json = json.loads(response.text)
    except Exception as e:
        print("Bad request", e)
        return None

    return res_json["data"]["weekly_horoscope"]


def get_monthly_horoscope(sign: str, month: str) -> Optional[Dict[str, str]]:
    """Returns the persons monthly horoscope in this format:
    Personal, Health, Profession, Emotions, Travel, Luck
    month has to be one of these three values: current, prev or next"""

    url = "https://divineapi.com/api/1.0/get_monthly_horoscope.php"

    data = {
        "api_key": DIVINE_API_KEY,
        "month": month,
        "sign": sign.upper(),
    }
    try:
        response = requests.post(url, data=data)
    except Exception as e:
        print("Bad request", e)
        return None

    if response.status_code != 200:
        print("Bad request")
        return None

    try:
        res_json = json.loads(response.text)
    except Exception as e:
        print("Bad request", e)
        return None

    return res_json["data"]["monthly_horoscope"]


def flatten_horoscope(horoscope: Dict[str, Any]) -> Optional[str]:
    personal_horoscope = ""
    try:
        for k, v in horoscope.items():
            if k == "luck":
                for i in v:
                    personal_horoscope = personal_horoscope + "\n" + i
            else:
                personal_horoscope = personal_horoscope + "\n" + v
    except Exception as e:
        print("Unable to flatten dictionary", e)
        return None

    return personal_horoscope


def get_horoscope_content(
    sign: str,
    day: str = None,
    month: str = None,
    week: str = None,
    time_zone: int = -8,
) -> Optional[str]:
    """Get the clean content of the user's horoscope
    to get the daily include a day and timezone values, to include the weekly provide a week value, to get monthly provide a month value.
    sign is required for all calls
    """
    personal_horoscope = ""

    if day:
        if day not in ["today", "tomorrow", "yesterday"]:
            print(
                "Day has to be one of these three values: today, tomorrow or yesterday"
            )
            return None
        try:
            date_str = datetime.now().strftime("%Y-%m-%d")
        except Exception as e:
            print("Need a datetime in the right format", e)
            return None
        daily_horoscope = get_daily_horoscope(sign, date_str, time_zone)
        personal_horoscope = personal_horoscope + flatten_horoscope_by_topic(daily_horoscope)

    if week:
        if week not in ["prev", "current", "next"]:
            print("Week has to be one of these three values: current, prev or next")
            return None
        weekly_horoscope = get_weekly_horoscope(sign, week)
        personal_horoscope = personal_horoscope + flatten_horoscope_by_topic(weekly_horoscope)

    if month:
        if month not in ["prev", "current", "next"]:
            print("Month has to be one of these three values: current, prev or next")
            return None
        monthly_horoscope = get_monthly_horoscope(sign, month)
        personal_horoscope = personal_horoscope + flatten_horoscope_by_topic(monthly_horoscope)

    return personal_horoscope

def flatten_horoscope_by_topic(horoscope: Dict[str, Any]) -> Optional[str]:
    personal_horoscope = ""
    try:
        for k, v in horoscope.items():
            personal_horoscope += f'\nQuestions regarding {k}:'
            if k == "luck":
                for i in v:
                    personal_horoscope += f"\n{i}"
            else:
                personal_horoscope += f"\n{v}"
    except Exception as e:
        print("Unable to flatten dictionary", e)
        return None

    return personal_horoscope

if __name__ == '__main__':

    date_str = datetime.now().strftime("%Y-%m-%d")
    daily = get_daily_horoscope(sign = 'Gemini', day = date_str, time_zone = -8)
    weekly = get_weekly_horoscope(sign = 'Gemini', week = 'current')
    monthly = get_monthly_horoscope(sign = 'Gemini', month = 'current')
    print(flatten_horoscope_by_topic(monthly))