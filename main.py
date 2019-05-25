#!/usr/bin/env python
import traceback
import platform
import socket
import time
import subprocess
import json
import sys
import getopt
import docker
import pprint

DELAY = 15  # secs
previous_cpu = {}
previous_system_cpu = {}
cpu_usage_percent = 0.0


def send_msg(message, CARBON_SERVER, CARBON_PORT):
  #  print 'sending message:\n%s' % message
    sock = socket.socket()
    sock.connect((CARBON_SERVER, CARBON_PORT))
    sock.sendall(message)
    sock.close()



def get_dockerdata(ENV,NODE):
    HOSTNAME = socket.gethostname()
    timestamp = int(time.time())
    stat_data = {}
    lines = []
    dockers_list=[]
    docker_image_creation=[]
    cc = docker.Client(base_url='unix://var/run/docker.sock', version='auto')
    for i in cc.containers():
      dockers_list.append(i['Names'][0])
      
    number_of_docker= len(dockers_list)
#    print dockers_list
    for instance in dockers_list:
#        print instance
        cmd = "echo 'GET /containers" + instance  + "/stats HTTP/1.1\\r\\n'  | nc -U -q 1 /var/run/docker.sock | head -8 | tail -1"
#        print cmd
        try:
          out = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
#        print out
          stat_data[instance] = json.loads(out)
      
  #        print out
 #         print "exception"
     
  #      print "exception handled"
          memory_limit = float(stat_data[instance]["memory_stats"]["limit"])
          memory_usage = float(stat_data[instance]["memory_stats"]["usage"])
          memory_percent = (memory_usage / memory_limit)*100.0
          if not(instance in previous_cpu):
            cpu_usage_percent = 0.0
          else:
            cpu_delta = float( stat_data[instance]["cpu_stats"]["cpu_usage"]["total_usage"] - previous_cpu[instance])
            system_delta = float(stat_data[instance]["cpu_stats"]["system_cpu_usage"] - previous_system_cpu[instance])
            cpu_usage_percent = float(cpu_delta / system_delta) * float(len(stat_data[instance]["cpu_stats"]["cpu_usage"]["percpu_usage"])) * 100.0

          network_rx = float(stat_data[instance]["networks"]["eth0"]["rx_bytes"])
          network_tx = float(stat_data[instance]["networks"]["eth0"]["tx_bytes"])
#        blkio_stats = stat_data[instance]["blkio_stats"]["io_serviced_recursive"][0]["value"]
          previous_cpu[instance] = float(stat_data[instance]["cpu_stats"]["cpu_usage"]["total_usage"])
          previous_system_cpu[instance] = float(stat_data[instance]["cpu_stats"]["system_cpu_usage"])
          lines_temp = [

            '%s.docker.server.%s.number-of-dockers %d %d' % (ENV, NODE, number_of_docker, timestamp),
            '%s.docker.server.%s.%s.memory-usage %d %d' % (ENV, NODE, instance, memory_usage, timestamp),
            '%s.docker.server.%s.%s.memory-limit %d %d' % (ENV, NODE, instance, memory_limit, timestamp),
            '%s.docker.server.%s.%s.memory-usage-percent %f %d' % (ENV, NODE, instance, memory_percent, timestamp),
            '%s.docker.server.%s.%s.cpu-usage-percent %f %d' % (ENV, NODE, instance, cpu_usage_percent, timestamp),
            '%s.docker.server.%s.%s.network-rx-bytes %d %d' % (ENV, NODE, instance, network_rx, timestamp),
            '%s.docker.server.%s.%s.network-tx-bytes %d %d' % (ENV, NODE, instance, network_tx, timestamp),
#            '%s.docker.server.%s.%s.blkio_stats %d %d' % (ENV, NODE, instance, blkio_stats, timestamp)
            ]
          lines.extend(lines_temp)
        except:
          pass
    traceback.print_exc()
    return lines

def main(argv):
   CARBON_SERVER = 'localhost'
   CARBON_PORT = 2003
   ENV = "dummy"
   NODE = "localhost"
   try:
      opts, args = getopt.getopt(argv,"hs:p:e:n:",["c_server=","c_port=","env=","node="])
   except getopt.GetoptError:
      print 'main.py -s <graphite server> -p <carbon port> -e <prefix> -n <nodename>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'main.py -s <graphite server> -p <carbon port> -e <prefix> -n <nodename>'
         sys.exit()
      elif opt in ("-s", "--c_server"):
         CARBON_SERVER = arg
      elif opt in ("-p", "--c_port"):
         CARBON_PORT = int(arg)
      elif opt in ("-e", "--env"):
         ENV = arg
      elif opt in ("-n", "--node"):
         NODE = arg

   while True:
        lines = get_dockerdata(ENV,NODE)
        message = '\n'.join(lines) + '\n'
        send_msg(message, CARBON_SERVER, CARBON_PORT)   
        time.sleep(DELAY)



    


if __name__ == '__main__':
    main(sys.argv[1:])
    
