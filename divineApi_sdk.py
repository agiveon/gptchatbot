from datetime import datetime, timezone, timedelta
from typing import Dict, Optional, Any
import requests
import json

DIVINE_API_KEY = "31b3b31a1c2f8a370206f111127c0dbd"

class DivineAPIClient:
    baseURL = "https://json.astrologyapi.com/v1/"

    def __init__(self, key):
        self.apiKey = key
        
  def get_daily_horoscope(
      self, sign: str, day: str, time_zone: int
  ) -> Optional[Dict[str, str]]:
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


  def get_weekly_horoscope(self, sign: str, week: str) -> Optional[Dict[str, str]]:
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


  def get_monthly_horoscope(self, sign: str, month: str) -> Optional[Dict[str, str]]:
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


  def flatten_horoscope(self, horoscope: Dict[str, Any]) -> Optional[str]:
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
