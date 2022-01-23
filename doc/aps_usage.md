# How to make auth-proxy-server work
- Download auth-proxy-server from github
```
git clone https://github.com/dmwm/auth-proxy-server.git
```
and do `make` inside the auth-proxy-server folder
- Create the `.crt` and `.key` files for the server, e.g. follow [this](https://www.rosehosting.com/blog/how-to-generate-a-self-signed-ssl-certificate-on-linux/) recipe
- Store the content of [this](https://cms-cric.cern.ch/api/accounts/user/query/?json&preset=roles) site in a `cric.json` file
- Create a config.json file like this:
```
{
  "base": "",
  "client_id": "CLIENT_ID",
  "client_secret": "CLIENT_SECRET",
  "iam_client_id": "CLIENT_ID",
  "iam_client_secret": "IAM_CLIENT_SECRET",
  "iam_url": " ",
  "oauth_url": "",
  "providers":[],

    "static": "/path/static",
    "server_cert": "/etc/httpd/httpscertificate/localhost.crt",
    "server_key": "/etc/httpd/httpscertificate/localhost.key",
    "hmac": "/path/hmac.txt",
    "rootCAs": "/path/certificates/",

  "redirect_url": "http://localhost/callback",
  "document_root": "/tmp/secrets/www",
  "ingress": [
    {"path":"/token", "service_url":"http://localhost:8443"},
    {"path":"/", "service_url":"http://localhost:8888"}
  ],

  "cric_file": "/path/cric.json",
  "cms_headers": true,
  "update_cric": 36000,
  "verbose": 1,
  "port": 8443
}
```
- Run auth-proxy-server in a terminal, with the `useX509` flag to use the x509 certificate
```
sudo ./auth-proxy-server -config ./config.json -useX509
```
- Run the flask server and submit a process in two different terminals
```
FLASK_ENV=development FLASK_APP=server.py flask run -p 8888
curl -L -k  --key ~/.globus/userkey.pem --cert ~/.globus/usercert.pem https://localhost:8443/hello
```
