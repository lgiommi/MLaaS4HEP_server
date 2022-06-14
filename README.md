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
- `/submit` to submit a MLaaSHEP workflow. A json file, like [input_new.json](https://github.com/lgiommi/MLaaS4HEP_server/blob/master/input_new.json), must be provided in the curl call with information about which files from which uploaded folder must be used. The user can also specify the memory and CPU usage available for the process and if run on a CPU or GPU (not fully implemented).
```
curl -H "Content-Type: application/json" -d @input_new.json http://localhost:8080/submit
```
- `/status_docker` to get back information about the status of an ongoing process. The process name must be provided as argument. 
```
curl http://localhost:8080/status_docker?process_name=luca_1
```
- `/logs` to get back and save in a given file the logs of a process. The process name must be provided as argument. 
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

### Enable the reading of remote ROOT files
Since the reading of remote files from grid data centers can be done only using an x509 proxy, an xrootd proxy server and renewer can be used and integrated with MLaaS4HEP_server following [this](https://github.com/comp-dev-cms-ita/compose-xrootd) recipe.

### Add an authentication layer
In order to manage the user's authentication we decided to integrate a proxy server in front of the [MLaaS4HEP one](https://github.com/lgiommi/MLaaS4HEP_server/blob/master/server.py). We succesfully used [auth-proxy-server](https://github.com/dmwm/auth-proxy-server.git) and [OAuth2-Proxy server](https://oauth2-proxy.github.io/oauth2-proxy/). For the instructions about their usage see [here](https://github.com/lgiommi/MLaaS4HEP_server/tree/master/doc).

# The entire service
We implemented a working prototype connecting OAuth2-Proxy server, MLaaS4HEP_server, xrootd proxy-cache server, X509 proxy renewer and [TFaaS](https://github.com/vkuznet/TFaaS), hosted by a VM of the INFN Cloud. The MLaaS4HEP_server APIs can be reached at the following address https://90.147.174.27:4433 while TFaaS at https://90.147.174.27:8081.

In the following we provide a practical example about how to perform the entire pipeline, from preparing the data to get predictions. You can find a demo version [here](https://youtu.be/_JHg4oTeVbc). The commands used for the demo are [here](https://github.com/lgiommi/MLaaS4HEP_server/blob/master/demo.sh).

```
### setup oidc-agent

oidc-agent
eval 'oidc-agent'

OIDC_SOCK=/tmp/oidc-VfwO5P/oidc-agent.55537; export OIDC_SOCK;
OIDCD_PID=55542; export OIDCD_PID;
echo Agent pid $OIDCD_PID
Agent pid 55546


### Obtain a token for MLaaS4HEP_server and TFaaS

TOKEN_MLAAS=$(oidc-token luca_api2 --aud=a15f41c9-a974-48ec-967a-2a36d255d524)
TOKEN_TFAAS=$(oidc-token luca_api2 --aud=f343be72-8479-4c95-892b-9dfcda0faac1)


### Check if there are models loaded in the TFaaS server

curl -L -k -H "Authorization: Bearer ${TOKEN_TFAAS}" https://90.147.174.27:8081/models

null


### Prepare the folder with the necessary files

ls folder_to_upload

QCD_HT1000to1500.root	QCD_HT2000toInf.root	QCD_HT500to700.root	TTBar.root		files_local.txt		labels_local.txt	params_local.json	ttH_noDRmatch.root
QCD_HT1500to2000.root	QCD_HT300to500.root	QCD_HT700to1000.root	ex_keras_model.py	files_remote.txt	labels_remote.txt	params_remote.json	ttH_signal.root


### File with the definition of the ML model

cat ex_keras_model.py

"""
Basic example of ML model implemented via Keras framework
"""
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense

def model(idim):
    "Simple Keras model for testing purposes"
    ml_model = keras.Sequential([keras.layers.Dense(128, activation='relu',input_shape=(idim,),name='inputs'),
                              keras.layers.Dropout(0.5),
                              keras.layers.Dense(64, activation='relu'),
                              keras.layers.Dropout(0.5),
                              keras.layers.Dense(1, activation='sigmoid')])
    ml_model.compile(optimizer=keras.optimizers.Adam(lr=1e-3), loss=keras.losses.BinaryCrossentropy(),
                  metrics=[keras.metrics.BinaryAccuracy(name='accuracy'), keras.metrics.AUC(name='auc')])
    return ml_model


### File with the name of local ROOT files

cat files_local.txt

ttH_signal.root
ttH_noDRmatch.root
TTBar.root
QCD_HT700to1000.root
QCD_HT1500to2000.root
QCD_HT1000to1500.root
QCD_HT2000toInf.root
QCD_HT300to500.root
QCD_HT500to700.root


### File with the path and name of remote ROOT files

cat files_remote.txt

/store/user/lgiommi/flatTree_ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8.root
/store/user/lgiommi/flatTree_TT_TuneCUETP8M2T4_13TeV-powheg-pythia8.root
/store/user/lgiommi/flatTree_QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root
/store/user/lgiommi/flatTree_QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root
/store/user/lgiommi/flatTree_QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root
/store/user/lgiommi/flatTree_QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root
/store/user/lgiommi/flatTree_QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root
/store/user/lgiommi/flatTree_QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root


### File with labels of the ROOT files

cat labels_local.json

1
0
0
0
0
0
0
0
0


### File with MLaaS4HEP parameters

cat params_local.json

{
    "nevts": 30000,
    "shuffle": true,
    "chunk_size": 10000,
    "epochs": 5,
    "batch_size": 100,
    "identifier":["runNo", "evtNo", "lumi"],
    "branch": "events",
    "selected_branches":"",
    "exclude_branches": "",
    "hist": "pdfs",
    "redirector": "root://stormgf1.pi.infn.it",
    "verbose": 1
  }


### Load the folder to the MLaaS4HEP server

curl -L -k -H "Authorization: Bearer ${TOKEN_MLAAS}" -F "file=@folder_to_upload.tar.gz" https://90.147.174.27:4433/upload?name=luca

Successfully uploaded!


### Prepare a submission file

cat submit.json

{
    "name": "luca",
    "device": "cpu",
    "memory": "3gb",
    "cpus": "2",
    "files": "files_local.txt",
    "labels": "labels_local.txt",
    "model": "ex_keras_model.py",
    "params": "params_local.json"
  }


### Submit a MLaaS4HEP workflow using the loaded ROOT files

curl -L -k -H "Authorization: Bearer ${TOKEN_MLAAS}" -H "Content-Type: application/json" -d @submit.json https://90.147.174.27:4433/submit

{
 "process_name": "luca_1",
 "job_id": 5557
}


### Verify the status of the process

curl -L -k -H "Authorization: Bearer ${TOKEN_MLAAS}" https://90.147.174.27:4433/status_docker?process_name=luca_1

{
 "process_name": "luca_1",
 "status": "Up 8 seconds"
}


### Get back and save the logs of the process

curl -L -k -H "Authorization: Bearer ${TOKEN_MLAAS}" -o logs.txt https://90.147.174.27:4433/logs?process_name=luca_1
cat logs.txt | head -20

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 27881  100 27881    0     0   124k      0 --:--:-- --:--:-- --:--:--  126k

2022-06-14 15:28:44.016611: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'libcudart.so.11.0'; dlerror: libcudart.so.11.0: cannot open shared object file: No such file or directory
2022-06-14 15:28:44.016674: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
load ex_keras_model.py <function model at 0x7fd34d81df28> Simple Keras model for testing purposes
DataGenerator: <MLaaS4HEP.generator.RootDataGenerator object at 0x7fd34d7d76a0> [14/Jun/2022:15:28:46] 1655220526.0
model parameters: {"nevts": 30000, "shuffle": true, "chunk_size": 10000, "epochs": 5, "batch_size": 100, "identifier": ["runNo", "evtNo", "lumi"], "branch": "events", "selected_branches": "", "exclude_branches": "", "hist": "pdfs", "redirector": "root://stormgf1.pi.infn.it", "verbose": 1}
Reading ttH_signal.root
# 10000 entries, 29 branches, 1.10626220703125 MB, 0.05584907531738281 sec, 19.808066664389877 MB/sec, 179.05399405758 kHz
# 10000 entries, 29 branches, 1.10626220703125 MB, 0.019169092178344727 sec, 57.7107249909827 MB/sec, 521.6731135184885 kHz
# 10000 entries, 29 branches, 1.10626220703125 MB, 0.016225099563598633 sec, 68.18215214612141 MB/sec, 616.3290376618224 kHz
###total time elapsed for reading + specs computing: 0.09430861473083496; number of chunks 3
###total time elapsed for reading: 0.09124016761779785; number of chunks 3

--- first pass: 38036 events, (29-flat, 0-jagged) branches, 29 attrs
<MLaaS4HEP.reader.RootDataReader object at 0x7fd34d7d79e8> init is complete in 0.1035768985748291 sec
writing specs specs-ttH_signal.json
write specs-ttH_signal.json
Reading ttH_noDRmatch.root
# 10000 entries, 29 branches, 1.10626220703125 MB, 0.046973228454589844 sec, 23.550908537204343 MB/sec, 212.8872195716171 kHz
# 10000 entries, 29 branches, 1.10626220703125 MB, 0.017837047576904297 sec, 62.020477450744515 MB/sec, 560.6308979602749 kHz
# 10000 entries, 29 branches, 1.10626220703125 MB, 0.01699066162109375 sec, 65.11001347103726 MB/sec, 588.5585990121239 kHz


### Download the trained ML model

curl -L -k -H "Authorization: Bearer ${TOKEN_MLAAS}" -o luca_1.tar.gz https://90.147.174.27:4433/model?process_name=luca_1
mkdir -p luca_1 && tar -xvf luca_1.tar.gz -C luca_1
ls luca_1

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  147k  100  147k    0     0   680k      0 --:--:-- --:--:-- --:--:--  717k

x ./
x ./assets/
x ./saved_model.pb
x ./keras_metadata.pb
x ./params.json
x ./variables/
x ./variables/variables.index
x ./variables/variables.data-00000-of-00001
assets			keras_metadata.pb	params.json		saved_model.pb		variables


### Check the models loaded in the TFaaS server

curl -L -k -H "Authorization: Bearer ${TOKEN_TFAAS}" https://90.147.174.27:8081/models

[{"name":"luca_1","model":"saved_model.pb","labels":"","options":null,"inputNode":"","outputNode":"","description":"","timestamp":"2022-06-14 15:29:17.456513917 +0000 UTC m=+261933.688268477"}]


### Choose an event to test inference using the trained ML model

cat predict_bkg.json

{
    "values": [0.19563319290790765, 0.8628343629750731, 0.20469675544301077, 0.5979233885840486, 0.5624403641089002, 0.4966360687831127, 0.9971232134875923, 0.9641571184466814, 0.016140890033353065, 0.012642983007060364, 0.044779417127065256, 0.04623121102305415, 0.027365998536597175, 0.004034759345313149, 0.07267125173331217, 0.4668842294559054, 0.10894376909915392, 0.044679238817932156, 1.0, 0.9496461903794253, 0.9982200258458422, 0.5, 0.0, 0.0, 0.35235498377667923, 0.6612158851740676, 0.6065199265679636, 0.3931907707503391, 0.37482121042755157],
    "model": "luca_1"
}


### Obtain prediction for the selected event using TFaaS

curl -L -k -H "Authorization: Bearer ${TOKEN_TFAAS}" -X POST -H "Content-type: application/json" -d @predict_bkg.json https://90.147.174.27:8081/json

[0.08601278]


### Delete specs files to be prepared for reading remote ROOT files

curl -L -k -H "Authorization: Bearer ${TOKEN_MLAAS}" https://90.147.174.27:4433/delete_specs?name=luca

Specs deletion completed!


### Submit a MLaaS4HEP workflow using remote ROOT files

curl -L -k -H "Authorization: Bearer ${TOKEN_MLAAS}" -H "Content-Type: application/json" -d @submit_remote.json https://90.147.174.27:4433/submit

{
 "process_name": "luca_2",
 "job_id": 6138
}


### Get back and save the logs of the process

curl -L -k -H "Authorization: Bearer ${TOKEN_MLAAS}" -o logs_remote.txt https://90.147.174.27:4433/logs?process_name=luca_2
cat logs_remote.txt | head -20

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  2021  100  2021    0     0  12608      0 --:--:-- --:--:-- --:--:-- 13123

2022-06-14 15:29:40.371538: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'libcudart.so.11.0'; dlerror: libcudart.so.11.0: cannot open shared object file: No such file or directory
2022-06-14 15:29:40.371628: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
load ex_keras_model.py <function model at 0x7fc254249f28> Simple Keras model for testing purposes
DataGenerator: <MLaaS4HEP.generator.RootDataGenerator object at 0x7fc2541fe630> [14/Jun/2022:15:29:42] 1655220582.0
model parameters: {"nevts": 30000, "shuffle": true, "chunk_size": 10000, "epochs": 5, "batch_size": 100, "identifier": ["runNo", "evtNo", "lumi"], "branch": "boostedAk8/events", "selected_branches": "", "exclude_branches": "", "hist": "pdfs", "redirector": "root://stormgf1.pi.infn.it", "verbose": 1}
Reading root://stormgf1.pi.infn.it//store/user/lgiommi/flatTree_ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8.root
# 10000 entries, 77 branches, 4.863739013671875 MB, 3.1020548343658447 sec, 1.5679087809117251 MB/sec, 3.223669642849594 kHz
# 10000 entries, 77 branches, 4.863739013671875 MB, 2.2151570320129395 sec, 2.1956633066560243 MB/sec, 4.514352642039505 kHz
# 10000 entries, 77 branches, 4.863739013671875 MB, 2.0409839153289795 sec, 2.3830364252958383 MB/sec, 4.899597652335311 kHz
###total time elapsed for reading + specs computing: 8.13843321800232; number of chunks 3
###total time elapsed for reading: 7.35819149017334; number of chunks 3

--- first pass: 948348 events, (22-flat, 52-jagged) branches, 328 attrs
<MLaaS4HEP.reader.RootDataReader object at 0x7fc2541fe978> init is complete in 8.150626182556152 sec
writing specs specs-flatTree_ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8.json
write specs-flatTree_ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8.json
Reading root://stormgf1.pi.infn.it//store/user/lgiommi/flatTree_TT_TuneCUETP8M2T4_13TeV-powheg-pythia8.root


### Delete the loaded folder with all the material and the trained ML models

curl -L -k -H "Authorization: Bearer ${TOKEN_MLAAS}" https://90.147.174.27:4433/delete_folder?name=luca
curl -L -k -H "Authorization: Bearer ${TOKEN_TFAAS}" -X DELETE https://90.147.174.27:8081/delete -F "model=luca_1"
curl -L -k -H "Authorization: Bearer ${TOKEN_TFAAS}" -X DELETE https://90.147.174.27:8081/delete -F "model=luca_2"
curl -L -k -H "Authorization: Bearer ${TOKEN_TFAAS}" https://90.147.174.27:8081/models

Folder deletion completed!
null
```


The MLaaS4HEP APIs can be used in the following way:
```
curl -L -k -H "Authorization: Bearer ${TOKEN_MLAAS}" -F "file=@folder_to_upload.tar.gz" https://90.147.174.27:4433/upload?name=luca
curl -L -k -H "Authorization: Bearer ${TOKEN_MLAAS}" -H "Content-Type: application/json" -d @input_new.json https://90.147.174.27:4433/submit
curl -L -k -H "Authorization: Bearer ${TOKEN_MLAAS}" https://90.147.174.27:4433/status_docker?process_name=luca_1
curl -L -k -H "Authorization: Bearer ${TOKEN_MLAAS}" -o logs.txt https://90.147.174.27:4433/logs?process_name=luca_1
curl -L -k -H "Authorization: Bearer ${TOKEN_MLAAS}" -o luca_1.tar.gz https://90.147.174.27:4433/model?process_name=luca_1
curl -L -k -H "Authorization: Bearer ${TOKEN_MLAAS}" https://90.147.174.27:4433/delete_specs?name=luca
curl -L -k -H "Authorization: Bearer ${TOKEN_MLAAS}" https://90.147.174.27:4433/delete_folder?name=luca
```

The TFaaS APIs can be used in the following way:
```
curl -L -k -H "Authorization: Bearer ${TOKEN_TFAAS}" https://90.147.174.27:8081/models
curl -L -k -H "Authorization: Bearer ${TOKEN_TFAAS}" -X POST -H "Content-Encoding: gzip" -H "content-type: application/octet-stream" --data-binary @model.tar.gz https://90.147.174.27:8081/upload
curl -L -k -H "Authorization: Bearer ${TOKEN_TFAAS}" -X POST -H "Content-type: application/json" -d @predict_bkg.json https://90.147.174.27:8081/json
curl -L -k -H "Authorization: Bearer ${TOKEN_TFAAS}" -X DELETE https://90.147.174.27:8081/delete -F "model=luca_1"
```

