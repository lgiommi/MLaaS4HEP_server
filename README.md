# MLaaS4HEP_server
The code on this repo allows to build a MLaaS4HEP server: the user uploads the required files and runs a ML workflow using [MLaaS4HEP](https://github.com/vkuznet/MLaaS4HEP).

To launch the server, clone the repo and run in a terminal:
```
FLASK_ENV=development FLASK_APP=server.py flask run -p 8080
```

The server has the following APIs:
- `/upload` to push a tarball file containing all the files necessary to run MLaaS4HEP. The name of the folder must be provided as argument.
```
curl -F "file=@folder_to_upload.tar.gz" http://localhost:8080/upload?name=luca
```
- `/submit` to submit a MLaaSHEP workflow. A json file, like [input_new.json](https://github.com/lgiommi/MLaaS4HEP_server/blob/master/input_new.json), must be provided in the curl call with information about which files uses from which uploaded folder. The user can also specify the memory and CPU usage available for the process and if run on a CPU or GPU (not fully implemented).
```
curl -H "Content-Type: application/json" -d @input_new.json http://localhost:8080/submit
```
- `/status_docker` to get back information about the status of an ongoing process. The process name must be provided as argument. 
```
curl http://localhost:8080/status_docker?process_name=luca_1
```
- `/logs` to get back and save in a given file the logs of a docker process. The process name must be provided as argument. 
```
curl -L -o logs.txt http://localhost:8080/logs?process_name=luca_1
```
- `/model` to get back the tarball of the output model delivered by MLaaS4HEP. The process name must be provided as argument. 
```
curl -L -o luca_1.tar.gz http://localhost:8080/model?process_name=luca_1
```
- `/delete_specs` to delete specs files produced by MLaaS4HEP in a previously uploaded folder. The name of the folder must be provided as argument.
```
curl http://localhost:8080/delete_specs?name=luca
```
- `/delete_folder` to delete a previously uploaded folder. The name of the folder must be provided as argument.
```
curl http://localhost:8080/delete_folder?name=luca
```

In order to manage the user's authentication we decided to integrate a proxy server in front of the [MLaaS4HEP one](https://github.com/lgiommi/MLaaS4HEP_server/blob/master/server.py). We succesfully used [auth-proxy-server](https://github.com/dmwm/auth-proxy-server.git) and [OAuth2-Proxy server](https://oauth2-proxy.github.io/oauth2-proxy/). For the instructions about their usage see [here](https://github.com/lgiommi/MLaaS4HEP_server/tree/master/doc).
