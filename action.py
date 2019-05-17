from __future__ import absolute_import, division, unicode_literals

from typing import Any, Dict, List, Text, Union
from rasa_core_sdk import Action, ActionExecutionRejection, Tracker
from rasa_core_sdk.events import (AllSlotsReset, FollowupAction,SlotSet,Form)
from rasa_core_sdk.executor import CollectingDispatcher
from rasa_core_sdk.forms import REQUESTED_SLOT, FormAction
import requests

class WeatherForm(FormAction):

    def name(self):
        return "weather_form"

    @staticmethod
    def required_slots(tracker:Tracker) :
              
        return ["location"]

    def slot_mappings(self):
        return {"location": [self.from_entity(entity="location",intent=["entered_location"]),self.from_text()]}

    def validate(self,
                 dispatcher: CollectingDispatcher,
                 tracker: Tracker,
                 domain: Dict[Text, Any]) -> List[Dict]:
        
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)

        slot_to_fill = tracker.get_slot(REQUESTED_SLOT)
        if slot_to_fill:
            slot_values.update(self.extract_requested_slot(dispatcher,
                                                           tracker, domain))

        # validation succeed, set the slots values to the extracted values
        return [SlotSet(slot, value) for slot, value in slot_values.items()]

    def submit(self,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]) -> List[Dict]:
        location = tracker.get_slot("location")
        r = requests.get(f"http://api.apixu.com/v1/current.json?key=c3488dbfdd024eda80e65216192603&q={location}")
        json_data = r.json()
        print(json_data)
        if json_data.get("error"):
            dispatcher.utter_message(json_data['error']['message'])
            return [SlotSet('location',None),FollowupAction("weather_form")]
        else:
            city = json_data['location']['name']
            condition = json_data['current']['condition']['text']
            temperature_c = json_data['current']['temp_c']
            humidity = json_data['current']['humidity']
            wind_mph = json_data['current']['wind_mph']
            response = f"It is currently {condition} in {city} at the moment. The temperature is {temperature_c} degrees, the humidity is {humidity}% and the wind speed is {wind_mph} mph."

            dispatcher.utter_message(response)
            return [SlotSet('location',None)]