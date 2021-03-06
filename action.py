from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet

class ActionWhether(Action):
    def name(self):
        return 'action_weather'

    def run(self,dispatcher,tracker,domain):
        from apixu.client import ApixuClient
        api_key = 'c3488dbfdd024eda80e65216192603'
        client = ApixuClient(api_key)

        loc = tracker.get_slot('location')
        current = client.current(q=loc)
        print("Current is :",current)
        country = current['location']['country']
        city = current['location']['name']
        condition = current['current']['condition']['text']
        temperature_c = current['current']['temp_c']
        humidity = current['current']['humidity']
        wind_mph = current['current']['wind_mph']


        response = f"""It is currently {condition} in {city} as of now.The temparature is {temperature_c} degree celsius.
                        The humidity is {humidity}% and the wind speed is {wind_mph}."""

        dispatcher.utter_message(response) 
        return [SlotSet('location',loc)]