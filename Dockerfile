FROM ubuntu:latest
LABEL maintainer="Luca Giommi luca.giommi3@unibo.it"
RUN apt-get update && apt-get install -y python3
ENV WDIR=/data
WORKDIR ${WDIR}
ENTRYPOINT ["python3", "./python_script.py"]