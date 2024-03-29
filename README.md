<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [ee-services - Early-est Services](#ee-services---early-est-services)
  - [Introduction](#introduction)
  - [Quickstart](#quickstart)
    - [Get Docker image](#get-docker-image)
      - [1) Get built image from DockerHub (*preferred*)](#1-get-built-image-from-dockerhub-preferred)
      - [2) Build by yourself](#2-build-by-yourself)
    - [Run as a service](#run-as-a-service)
  - [Test ee-services as a stand alone script](#test-ee-services-as-a-stand-alone-script)
  - [Contribute](#contribute)
  - [Authors](#authors)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

[![License](https://img.shields.io/github/license/INGV/ttime.svg)](https://github.com/INGV/ttime/blob/main/LICENSE) [![GitHub issues](https://img.shields.io/github/issues/INGV/ttime.svg)](https://github.com/INGV/ttime/issues)

[![Docker build](https://img.shields.io/badge/docker%20build-from%20CI-yellow)](https://hub.docker.com/r/ingv/ttime)![Docker Image Size (latest semver)](https://img.shields.io/docker/image-size/ingv/ttime?sort=semver)![Docker Pulls](https://img.shields.io/docker/pulls/ingv/ttime)

[![CI](https://github.com/INGV/ttime/actions/workflows/docker-image.yml/badge.svg)](https://github.com/INGV/ttime/actions)[![GitHub](https://img.shields.io/static/v1?label=GitHub&message=Link%20to%20repository&color=blueviolet)](https://github.com/INGV/ttime)

# ee-services - Early-est Services

## Introduction
This project implement the web services exposed by early-est INGV customization

## Quickstart
### Get Docker image
To obtain *ee-services* docker image, you have two options:

#### 1) Get built image from DockerHub (*preferred*)
Get the last built image from DockerHub repository:
```sh
docker pull ingv/ee-services:latest
```

#### 2) Build by yourself
Clone the git repositry:
```sh
git clone https://github.com/INGV/ee-services.git
cd ee-services
```
build the image:
```sh
docker build --tag ingv/ee-services .
```

in case of errors, try:
```sh
docker build --no-cache --pull --tag ingv/ee-services . 
```

### Run as a service
run the container in daemon (`-d`) mode:
```
docker run -it --rm --name ee-services -p 8383:5000 -d ingv/ee-services
docker exec -i ee-services tail -f /opt/log/ee-services.log
```

Choose your preferred port as an alternative to 8383

Then test access to: http://localhost:8383/ for swagger API documentation

Examples of URL:

- ```
  http://localhost:4300/api/make_ee_ellipsoid?lat=40.6&lon=13.2&delta=1&xx=111&xy=55.5&yy=111
  ```



## Test ee-services as a stand alone script

If you have cloned the project, you can check the evaluator engine from command line.
To do this you need *python3.x* installed on your machine and also some python libraries:

```sh
pip install -r requirements.txt
python main/api/services.py --help
```

Here is an example of launch:

```sh
python main/api/services.py --lat 35 --lon 10 --delta 50 --covxx 36.3027 --covxy -0.0486165 --covyy 5.0177
```



## Contribute

Thanks to your contributions!

Here is a list of users who already contributed to this repository: \
<a href="https://github.com/ingv/ttime/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=ingv/ttime" />
</a>

## Authors
(c) 2023 Sergio Bruni sergio.bruni[at]ingv.it \
(c) 2023 Fabrizio Bernardi fabrizio.bernardi[at]ingv.it \
(c) 2023 Valentino Lauciani valentino.lauciani[at]ingv.it

Istituto Nazionale di Geofisica e Vulcanologia, Italia
