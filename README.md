# GraphiteClient
Docker image for graphite client for monitoring of the machine and dockers running on that machine 


This is the combination of collectd and dockermonitoring script

for docker 1.6 use - 
docker run -i  -e EP_HOST=GRAPHITEHOST -e EP_PORT=GRAPHITEPORT -e ENV=PREFIX -e NODE=HOSTNAME -v /proc:/host_proc:ro -v /var/run/docker.sock:/var/run/docker.sock:ro  akumar261089/dockerstat:1.2



for docker 1.9 use - 
docker run -i  -e EP_HOST=GRAPHITEHOST -e EP_PORT=GRAPHITEPORT -e ENV=PREFIX -e NODE=HOSTNAME -v /proc:/host_proc:ro -v /var/run/docker.sock:/var/run/docker.sock:ro  akumar261089/dockerstat:1.3




