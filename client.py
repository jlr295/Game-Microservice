#
#   Client program which sends a JSON file which contains game title and requested fields.
#   Connects REQ socket to tcp://localhost:5555
#   See API docs at https://api-docs.igdb.com/#game
#

import zmq
import json

context = zmq.Context()

#  Socket to talk to server
print("Connecting to server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

#  Send JSON object
print(f"Sending request …")

""" 
INPUT OPTIONS
1. To SELECT a title with or without fields:
    Enter the title of the game.  If fields are needed, enter the fields needed.  If all fields are needed, place '*' at index 0.
    If you would like the fields to be expanded ".*" should be appended to the fieldname.
    LEAVE the following fields empty: where, sortby, sort.
    EXAMPLE: 
    data = { 
        "title": "Stardew Valley",
        "fields": ['name', 'rating', 'genres.*'],
        "where": "",
        "sortby": "",
        "sort": ""
        }
2. To SELECT and filter through ALL games:
    LEAVE the title field empty.
    Enter the fields that you would like to request (or * for all).
    Enter what you would like to be filtered.  (For example: 'rating < 30' would be used to generate a list of games with a rating of < 30)
    SORT (if needed).  You may sort by asc or desc.  If sorting isn't necessary, leave blank.
    EXAMPLE:
    data = { 
        "title": "",
        "fields": ['name', 'rating'],
        "where": "rating < 30",
        "sortby": "rating",
        "sort": "desc"
        }
"""
data = { 
        "title": "Stardew Valley",
        "fields": ['name', 'rating'],
        "where": "",
        "sortby": "",
        "sort": ""
        }

# Convert data to a JSON file and send over socket.  
json_data = json.dumps(data)
socket.send_json(json_data)
    

#  Get the reply.
message = socket.recv()
print(f"Received reply[ {message} ]")
