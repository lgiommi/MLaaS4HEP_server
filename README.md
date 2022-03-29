# MLaaS4HEP_server
To launch the server run in a terminal
```
FLASK_ENV=development FLASK_APP=server.py flask run -p 8080
```
To submit a `submit` request the client should provide a json file like [input.json](https://github.com/lgiommi/MLaaS4HEP_server/blob/master/input.json)
thant contains the useful information to run a [docker container](https://hub.docker.com/layers/mlaas/felixfelicislp/mlaas/tf_2.7/images/sha256-81808e10a0b7dcbbe744bdde070fa3c5652a0e8fd7f8bffe679541a156547920?context=explore) able to perform the ML pipeline provided by MLaaS4HEP. The user can specify the memory and CPU usage for the container and if run on a CPU or GPU (non fully implemented). The request is submitted in the following way:
```
curl -H "Content-Type: application/json" -d @input.json http://localhost:8080/submit
```
This sends back to the client info about the process name and job id:
```
{
 "process_name": "luca_1",
 "job_id": 20547
}
```
The user can retrieve the status of the request in the following way:
```
curl http://localhost:8080/status_docker?process_name=luca_1
```
and save in logs.txt the logs of the process with:
```
curl 'http://localhost:8080/logs?process_name=luca_1&log_file=logs.txt'
```
This example works with a set of files you can download from gdrive with:
```
gdown https://drive.google.com/uc?id=1pO_6Uz85JVLVaM5csXDbS6RkYgVTFa63
```
In order to manage the user's authentication we decided to integrate a proxy server in front of the [MLaaS4HEP one](https://github.com/lgiommi/MLaaS4HEP_server/blob/master/server.py). We succesfully used [auth-proxy-server](https://github.com/dmwm/auth-proxy-server.git) and [OAuth2-Proxy server](https://oauth2-proxy.github.io/oauth2-proxy/). For the instructions about their usage see [here](https://github.com/lgiommi/MLaaS4HEP_server/tree/master/doc).
