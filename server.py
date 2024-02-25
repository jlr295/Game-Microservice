#
#   
#   Binds REP socket to tcp://*:5555
#   Expects string from the client, replies with a JSON file with game details
#   See API docs at https://api-docs.igdb.com/#game
#
import requests
import time
import zmq
import json
import os
from dotenv import load_dotenv

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    #  Wait for next request from client
    message = socket.recv_json()
    #message = message.encode("utf-8")
    json_message = json.loads(message)
    print(f"Received request: {json_message}")

    #  Do some 'work'
    time.sleep(1)

    # Authentication
    load_dotenv()
    my_client_id = os.getenv('CLIENT_ID')
    my_client_sec = os.getenv('CLIENT_SECRET')
    auth_url = f'https://id.twitch.tv/oauth2/token?client_id={my_client_id}&client_secret={my_client_sec}&grant_type=client_credentials'
    auth_file = requests.post(auth_url)
    access_token = auth_file.json()["access_token"]

    #  Send reply back to client

    # Deconstruct fields list to not include "'" or brackets.
    deconstructed_fields = str(json_message["fields"])[1:-1].replace("'", '')

    # If title is provided do not sort.
    if json_message["title"] and not json_message["sortby"] and not json_message["sort"]:
        to_send = f'fields {deconstructed_fields}; where name = "{json_message["title"]}";'
    # If title is not provided, you may sort the list of games.
    elif not json_message["title"] and json_message["sortby"] and json_message["sort"]:
        if json_message["where"]:
            to_send = f'fields {deconstructed_fields}; where {json_message["where"]}; sort {json_message["sortby"]} {json_message["sort"]};'
        else:
            to_send = f'fields {deconstructed_fields}; sort {json_message["sortby"]} {json_message["sort"]};'
    

    print(f"sending... {to_send}")

    url = f'https://api.igdb.com/v4/games'

    data = requests.post(url, headers = {"Client-ID":"zvikdinr1owt3kbm400zwlyz9cxwtk", "Authorization":f"Bearer {access_token} "}, data = to_send)


    socket.send_json(data.json())

