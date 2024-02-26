# Game Microservice Communication Contract
In both sending and receiving data from a socket, a connection must be established.  In this case, we will be using Zeromq to facilitate a connection.
```
#  Socket to talk to server
print("Connecting to server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")
```
## Requesting Data
Connect will be made through TCP/IP.  Data will be requested via a JSON file which contains the following:
```
data = { 
        "title":,
        "fields":,
        "where": "",
        "sortby": "",
        "sort": ""
        }
```
#### Input Options
```
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
```
**Convert data to a JSON object, and send over the socket.**
```
json_data = json.dumps(data)
socket.send_json(json_data)
```
## Receiving Data
Data will be sent via TCP/IP protocol.  A JSON object will be sent from the microservice.  
```
# Send data
socket.send_json(data.json())
```
```
# Receive data
message = socket.recv()
```
## UML Sequence Diagram
<img width="637" alt="image" src="https://github.com/jlr295/Game-Microservice/assets/81329844/2d1e244d-09f3-474d-ac43-dbe3d5620d67">



        

