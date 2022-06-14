#!/bin/bash
sleep 2
echo
echo "### setup oidc-agent"
echo
echo "oidc-agent"
echo "eval 'oidc-agent'"
echo
oidc-agent
eval `oidc-agent`
echo
echo
sleep 5

echo "### Obtain a token for MLaaS4HEP_server and TFaaS"
echo
echo 'TOKEN_MLAAS=$(oidc-token luca_api2 --aud=a15f41c9-a974-48ec-967a-2a36d255d524)'
echo 'TOKEN_TFAAS=$(oidc-token luca_api2 --aud=f343be72-8479-4c95-892b-9dfcda0faac1)'
TOKEN_MLAAS=$(oidc-token luca_api2 --aud=a15f41c9-a974-48ec-967a-2a36d255d524)
TOKEN_TFAAS=$(oidc-token luca_api2 --aud=f343be72-8479-4c95-892b-9dfcda0faac1)
echo
echo

echo "### Check if there are models loaded in the TFaaS server"
echo
echo 'curl -L -k -H "Authorization: Bearer ${TOKEN_TFAAS}" https://90.147.174.27:8081/models'
echo
curl -L -k -H "Authorization: Bearer ${TOKEN_TFAAS}" https://90.147.174.27:8081/models
echo
echo
sleep 5

echo "### Prepare the folder with the necessary files"
echo
echo "ls folder_to_upload"
echo
ls folder_to_upload
echo
echo
sleep 5

echo "### File with the definition of the ML model"
echo
echo "cat ex_keras_model.py"
echo
cat ./folder_to_upload/ex_keras_model.py
echo 
echo
echo
sleep 5

echo "### File with the name of local ROOT files"
echo
echo "cat files_local.txt"
echo
cat ./folder_to_upload/files_local.txt
echo 
echo
echo
sleep 5

echo "### File with the path and name of remote ROOT files"
echo
echo "cat files_remote.txt"
echo
cat ./folder_to_upload/files_remote.txt
echo 
echo
echo
sleep 5

echo "### File with labels of the ROOT files"
echo
echo "cat labels_local.json"
echo
cat ./folder_to_upload/labels_local.txt
echo 
echo
echo
sleep 5

echo "### File with MLaaS4HEP parameters"
echo
echo "cat params_local.json"
echo
cat ./folder_to_upload/params_local.json
echo 
echo
sleep 5

echo "### Load the folder to the MLaaS4HEP server"
echo
echo 'curl -L -k -H "Authorization: Bearer ${TOKEN_MLAAS}" -F "file=@folder_to_upload.tar.gz" https://90.147.174.27:4433/upload?name=luca'
echo
curl -L -k -H "Authorization: Bearer ${TOKEN_MLAAS}" -F "file=@folder_to_upload.tar.gz" https://90.147.174.27:4433/upload?name=luca
echo
echo
sleep 5

echo "### Prepare a submission file"
echo
echo "cat submit.json"
echo
cat submit.json
echo 
echo
echo
sleep 5

echo "### Submit a MLaaS4HEP workflow using the loaded ROOT files"
echo
echo 'curl -L -k -H "Authorization: Bearer ${TOKEN_MLAAS}" -H "Content-Type: application/json" -d @submit.json https://90.147.174.27:4433/submit'
echo
curl -L -k -H "Authorization: Bearer ${TOKEN_MLAAS}" -H "Content-Type: application/json" -d @submit.json https://90.147.174.27:4433/submit
echo
echo
echo
sleep 10

echo "### Verify the status of the process"
echo
echo 'curl -L -k -H "Authorization: Bearer ${TOKEN_MLAAS}" https://90.147.174.27:4433/status_docker?process_name=luca_1'
echo
curl -L -k -H "Authorization: Bearer ${TOKEN_MLAAS}" https://90.147.174.27:4433/status_docker?process_name=luca_1
echo
echo
echo
sleep 10

echo "### Get back and save the logs of the process"
echo
echo 'curl -L -k -H "Authorization: Bearer ${TOKEN_MLAAS}" -o logs.txt https://90.147.174.27:4433/logs?process_name=luca_1'
echo 'cat logs.txt | head -20'
echo
curl -L -k -H "Authorization: Bearer ${TOKEN_MLAAS}" -o logs.txt https://90.147.174.27:4433/logs?process_name=luca_1
echo
cat logs.txt | head -20
echo
echo
sleep 10

echo "### Download the ML trained model"
echo
echo 'curl -L -k -H "Authorization: Bearer ${TOKEN_MLAAS}" -o luca_1.tar.gz https://90.147.174.27:4433/model?process_name=luca_1'
echo 'mkdir -p luca_1 && tar -xvf luca_1.tar.gz -C luca_1'
echo 'ls luca_1'
echo
curl -L -k -H "Authorization: Bearer ${TOKEN_MLAAS}" -o luca_1.tar.gz https://90.147.174.27:4433/model?process_name=luca_1
echo
mkdir -p luca_1 && tar -xvf luca_1.tar.gz -C luca_1
ls luca_1
echo
echo
sleep 5

echo "### Check the models loaded in the TFaaS server"
echo
echo 'curl -L -k -H "Authorization: Bearer ${TOKEN_TFAAS}" https://90.147.174.27:8081/models'
echo
curl -L -k -H "Authorization: Bearer ${TOKEN_TFAAS}" https://90.147.174.27:8081/models
echo
echo
sleep 5

echo "### Choose an event to test inference using the trained ML model"
echo
echo 'cat predict_bkg.json'
echo
cat ./TFaaS_material/predict_bkg.json
echo
echo
echo
sleep 5

echo "### Obtain prediction for the selected event using TFaaS"
echo
echo 'curl -L -k -H "Authorization: Bearer ${TOKEN_TFAAS}" -X POST -H "Content-type: application/json" -d @predict_bkg.json https://90.147.174.27:8081/json'
echo
curl -L -k -H "Authorization: Bearer ${TOKEN_TFAAS}" -X POST -H "Content-type: application/json" -d @./TFaaS_material/predict_bkg.json https://90.147.174.27:8081/json
echo
echo
sleep 5

echo "### Delete specs files to be prepared for reading remote ROOT files"
echo
echo 'curl -L -k -H "Authorization: Bearer ${TOKEN_MLAAS}" https://90.147.174.27:4433/delete_specs?name=luca'
echo
curl -L -k -H "Authorization: Bearer ${TOKEN_MLAAS}" https://90.147.174.27:4433/delete_specs?name=luca
echo
echo
sleep 5

echo "### Submit a MLaaS4HEP workflow using remote ROOT files"
echo
echo 'curl -L -k -H "Authorization: Bearer ${TOKEN_MLAAS}" -H "Content-Type: application/json" -d @submit_remote.json https://90.147.174.27:4433/submit'
echo
curl -L -k -H "Authorization: Bearer ${TOKEN_MLAAS}" -H "Content-Type: application/json" -d @submit_remote.json https://90.147.174.27:4433/submit
echo
echo
echo
sleep 15

echo "### Get back and save the logs of the process"
echo
echo 'curl -L -k -H "Authorization: Bearer ${TOKEN_MLAAS}" -o logs_remote.txt https://90.147.174.27:4433/logs?process_name=luca_2'
echo 'cat logs_remote.txt | head -20'
echo
curl -L -k -H "Authorization: Bearer ${TOKEN_MLAAS}" -o logs_remote.txt https://90.147.174.27:4433/logs?process_name=luca_2
echo
cat logs_remote.txt | head -20
echo
echo
sleep 5

echo "### Delete the loaded folder with all the material and the trained ML models"
echo
echo 'curl -L -k -H "Authorization: Bearer ${TOKEN_MLAAS}" https://90.147.174.27:4433/delete_folder?name=luca'
echo 'curl -L -k -H "Authorization: Bearer ${TOKEN_TFAAS}" -X DELETE https://90.147.174.27:8081/delete -F "model=luca_1"'
echo 'curl -L -k -H "Authorization: Bearer ${TOKEN_TFAAS}" -X DELETE https://90.147.174.27:8081/delete -F "model=luca_2"'
echo 'curl -L -k -H "Authorization: Bearer ${TOKEN_TFAAS}" https://90.147.174.27:8081/models'
echo
curl -L -k -H "Authorization: Bearer ${TOKEN_MLAAS}" https://90.147.174.27:4433/delete_folder?name=luca
curl -L -k -H "Authorization: Bearer ${TOKEN_TFAAS}" -X DELETE https://90.147.174.27:8081/delete -F "model=luca_1"
curl -L -k -H "Authorization: Bearer ${TOKEN_TFAAS}" -X DELETE https://90.147.174.27:8081/delete -F "model=luca_2"
curl -L -k -H "Authorization: Bearer ${TOKEN_TFAAS}" https://90.147.174.27:8081/models
echo
echo
sleep 1