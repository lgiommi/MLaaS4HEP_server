## How to use OAuth2-Proxy server
Here we show how to use [OAuth2-Proxy](https://oauth2-proxy.github.io/oauth2-proxy/) to create a proxy server in front of the [MLaaS4HEP server](https://github.com/lgiommi/MLaaS4HEP_server/blob/master/server.py).
You have different ways to install [OAuth2-Proxy](https://oauth2-proxy.github.io/oauth2-proxy/docs/). We successfully used the prebuilt binary and the prebuilt docker image.

We registered our client using the [https://cms-auth.web.cern.ch/](https://cms-auth.web.cern.ch/) provider and we did the following steps to get access tokens for a new account using [oidc-agent](https://indigo-dc.gitbook.io/oidc-agent/)
```
oidc-agent
eval `oidc-agent`
oidc-gen -w device mlaas
TOKEN = $(oidc-token mlaas --aud=CLIENT_ID)
```
Then we created an example_config.cfg file like this 
```
provider = "oidc"
redirect_url = "http://localhost:4180/oauth2/callback"
oidc_issuer_url = "https://cms-auth.web.cern.ch/"
upstreams = [
    "http://0.0.0.0:8080"
]
email_domains = [
    "*"
]
client_id = "CLIENT_ID"
client_secret = "CLIENT_SECRET"
cookie_secret = "COOKIE_SECRET"
cookie_secure = false
skip_provider_button = true
ssl_insecure_skip_verify = true
```
and we run the proxy server with
```
oauth2-proxy --config ./example_config.cfg --skip-jwt-bearer-tokens=true
```
or using the docker image
```
docker run -v /home/giommi/luca:/etc --net=host quay.io/oauth2-proxy/oauth2-proxy:latest  --config=/etc/example_config.cfg  --skip-jwt-bearer-tokens=true
```
To run the proxy in secure mode we used `https://localhost:4433/oauth2/callback` as `redirect_url` and this example_config.json file
```
provider="oidc"
https_address = ":4433"
redirect_url = "https://localhost:4433/oauth2/callback"
oidc_issuer_url = "https://cms-auth.web.cern.ch/"
 upstreams = [
     "http://127.0.0.1:8080/"
 ]
 email_domains = [
     "*"
 ]
client_id = "CLIENT_ID"
client_secret = "CLIENT_SECRET"
cookie_secret = "COOKIE_SECRET"
cookie_name = "_oauth2_proxy"

tls_cert_file = "./localhost.crt"
tls_key_file = "./localhost.key"

standard_logging = true
request_logging = true
auth_logging = true
pass_basic_auth = true
pass_user_headers = true
```
We followed [this](https://www.rosehosting.com/blog/how-to-generate-a-self-signed-ssl-certificate-on-linux/) recipe to obtain self signed ssl certificate used for the proxy server.
In the docker case we used the `--ssl-insecure-skip-verify=true` flag to run the proxy server.
