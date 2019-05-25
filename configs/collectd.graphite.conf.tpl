Hostname "{{ NODE | default("collectd-docker") }}"

FQDNLookup false
Interval 30
Timeout 2
ReadThreads 5

LoadPlugin statsd
LoadPlugin cpu
LoadPlugin df
LoadPlugin memory
LoadPlugin load
LoadPlugin write_graphite
LoadPlugin users

<Plugin statsd>
  Host "::"
  Port "8125"
  DeleteSets      true
  TimerPercentile 90.0
</Plugin>

<Plugin "write_graphite">
 <Node "endpoint">
   Host "{{ EP_HOST }}"
   Port "{{ EP_PORT }}"
   Protocol "tcp"
   LogSendErrors true
   EscapeCharacter "_"
   Prefix "{{ ENV | default("local.debug.") }}.instance."
 </Node>
</Plugin>
