# Python-chat-client

Python-chat-client is a basic chat client made using python and socket. 

## Installation

clone the repository. go to the project folder.

### for clients

```bash
python3 client.py
```
### for server

```bash
python3 server.py
```

## Usage
give a username. It isn't stored, therefore you have to provide it every time you run it

```bash
username:bhasju
```
type a message and press enter to send it to the rest of the users

###  commands
to request a list of connected users, send @list
```bash
@list
server>> the user list is 
harry
ron
hermione
```
to send a direct message type @DM <username of receiver> <your message>
```bash
@DM bhaskar Hello there!
```
to quit type @quit then press ctrl+c. The last part should not be neccessary but it somehow is. 

```bash
@quit
```
###further plans

a Text based user interface using curses 

file transfer between clients

chat groups


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
