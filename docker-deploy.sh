#!/bin/bash

version=`python -c "import avengers; print(avengers.__version__)"`

echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin registry.entrydsm.hs.kr

if [[ "$1" == "develop" ]];then
    echo "Docker build on develop started"

    docker build -t registry.entrydsm.hs.kr/avengers:dev .

    docker push registry.entrydsm.hs.kr/avengers:dev
elif [[ "$1" == "master" ]];then
    echo "Docker build on master started"

    docker build -t registry.entrydsm.hs.kr/avengers:${version} .

    docker tag registry.entrydsm.hs.kr/avengers:${version} registry.entrydsm.hs.kr/avengers:latest

    docker push registry.entrydsm.hs.kr/avengers:${version}
    docker push registry.entrydsm.hs.kr/avengers:latest

fi

exit
