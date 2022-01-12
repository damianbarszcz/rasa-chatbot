from typing import Any, Text, Dict, List

from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import datetime as dt
import json

# Ask for restaurant open hours
class ActionOpenHours(Action):

    def name(self) -> Text:
        return "action_open_hours"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        day= ''
        hour = ''

        for blob in tracker.latest_message['entities']:
            if blob['entity'] == 'days_of_the_week':
                day = blob['value']

            if blob['entity'] == 'hour':
                hour = blob['value']

        with open('restaurant_data/opening_hours.json') as opening_file:
            opening_time = json.load(opening_file)

        opening_time_items = opening_time.get('items')
        hours = opening_time_items.get(day.capitalize())

        if hours is None:
            dispatcher.utter_message(text=f"Sorry, I don't understand {day}")
            return []

        if hour is '':
            dispatcher.utter_message(
                text=f"The restaurant is open from {hours.get('open')} to {hours.get('close')} on {day}"
            )
            return []
        if (int(hour) < 0) or (int(hour) > 24):
            dispatcher.utter_message(text=f"Given hour is incorrect")
            return []

        opening_hour = hours.get('open')
        close_hour = hours.get('close')

        if (int(hour) > int(opening_hour)) and (int(hour) < int(close_hour)):
            dispatcher.utter_message(text=f"Yes, our restaurant work at {hour} on {day}")

        else:
            dispatcher.utter_message(text=f"No, the restaurant work at {hour} on {day}")

        return []

# Ask for restaurant menu
class ActionRestaurantMenu(Action):

    def name(self) -> Text:
        return "action_restaurant_menu"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        with open('restaurant_data/menu.json') as menu_file:
            restaurant_menu = json.load(menu_file)

        menu_items = restaurant_menu.get('items')
        menu_to_show = 'RESTAURANT MENU:\n'
        menu_line = '--------------------------\n'

        for item in menu_items:
            meal = item.get('name')
            price = item.get('price')
            preparation = item.get('preparation_time')
            menu_to_show = menu_to_show +  menu_line + f'{meal}\n Price: {price}$\n Prepration time:  {preparation}h\n'

        dispatcher.utter_message(text=menu_to_show)
        dispatcher.utter_message("\n")
        return []

# Receive your order
class ActionReceiveOrder(Action):

    def name(self) -> Text:
        return "action_receive_order"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            meal= tracker.latest_message['text']

            order_title = 'YOUR ORDER:\n'
            order_line = '--------------------------\n'

            order = order_title + order_line + f'{meal}\n'

            if not meal:
                dispatcher.utter_message(text="I don't understand your order")
            else:
                dispatcher.utter_message(text=f"{order}")
                dispatcher.utter_message(f"{order_line}\n")
            return []

# Order delivery
class ActionOrderDelivery(Action):

    def name(self) -> Text:
        return "action_order_delivery"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            address = tracker.latest_message['text']
            dispatcher.utter_message(text=f"Your order will be delivered to {address}")

            return []