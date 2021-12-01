# MLaaS4HEP_server
To launch the server run in a terminal
```
FLASK_ENV=development FLASK_APP=server.py flask run
```
To sumbit a "submit" request the client should provide a json file like [input.json](https://github.com/lgiommi/MLaaS4HEP_server/blob/master/input.json)
thant contains the useful information to run the [python_script.py](https://github.com/lgiommi/MLaaS4HEP_server/blob/master/python_script.py) script. The request
is launched in the following way:
```
curl -H "Content-Type: application/json" -d @input.json http://localhost:5000/submit
```
Currently the [python_script.py](https://github.com/lgiommi/MLaaS4HEP_server/blob/master/python_script.py) script prints in the server shell the information 
contained in the [input.json](https://github.com/lgiommi/MLaaS4HEP_server/blob/master/input.json) file. The server run this python script getting the PID and 
returns it in the form of json printed on the client shell.
