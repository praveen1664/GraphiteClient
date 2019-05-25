# Docker image containing the Diamond collector
#
# VERSION        n       0.0.1
FROM          ubuntu:14.04
MAINTAINER    Abhinav Kumar <akumar261089@gmail.com>

ENV           DEBIAN_FRONTEND noninteractive

RUN           echo "deb http://us.archive.ubuntu.com/ubuntu/ precise universe" >> /etc/apt/sources.list
RUN           echo "deb http://ppa.launchpad.net/vbulax/collectd5/ubuntu precise main" >> /etc/apt/sources.list
RUN           apt-key adv --recv-keys --keyserver keyserver.ubuntu.com 232E4010A519D8D831B81C56C1F5057D013B9839
RUN           apt-get -y install python3

RUN           apt-get update &&  apt-get install -y python-setuptools make pbuilder python-mock python-configobj python-support cdbs git python-psutil
RUN           apt-get -y install collectd curl vim python-pip
RUN           git clone https://github.com/docker/docker-py.git
EXPOSE        8125

RUN           pip install envtpl
RUN           pip install docker-py
#install docker-py
#WORKDIR       /docker-py
#RUN           python setup.py install

ADD           configs/ /etc/collectd/configs

ADD           start /usr/bin/start
ADD           main.py /main.py

#cleanup
#RUN           apt-get autoremove -y git python-setuptools make pbuilder python-mock &&  apt-get clean && rm -rf /var/lib/apt/lists/* && rm -rf /docker-py





#configure diamond with env
RUN           chmod +x /main.py
RUN           chmod +x /usr/bin/start


CMD           start
#start
#ENTRYPOINT /start.sh
