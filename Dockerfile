FROM redhat/ubi8:latest
LABEL maintainer="Luca Giommi luca.giommi3@unibo.it"

RUN yum -y update && yum -y install python3 python3-pip git
RUN pip3 install Flask
RUN yum install -y yum-utils
RUN groupmod -g 1009 render && groupadd -g 998 docker && newgrp docker
RUN yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
RUN yum update -y
RUN yum install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

ENV WDIR=/workarea
WORKDIR ${WDIR}
RUN git clone https://github.com/lgiommi/MLaaS4HEP_server.git
WORKDIR ${WDIR}/MLaaS4HEP_server
RUN git checkout devel
ENV FLASK_ENV=development
ENV FLASK_APP=server.py

CMD flask run -p 8080
