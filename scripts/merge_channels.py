from tvh.htsp import HTSPClient
from tvh.api import HTSPApi
from scripts import CONFIG

htsp = HTSPClient((CONFIG['hostname'], 9982))
msg = htsp.hello()
htsp.authenticate(CONFIG['username'], CONFIG['password'])
cap = []
if 'servercapability' in msg:
    cap = msg['servercapability']


htspapi = HTSPApi(htsp=htsp)

search_channelname = raw_input("Search channel name: ")
# found_channels = search_channelnames(search_channelname)
found_channels_grid = htspapi.search_channelsnames_bygrid(lookup=search_channelname)
used_channels = []
# for c in found_channels:
#    channeluuid = c['key']
#    channelname = c['val']
#    use = raw_input('- Verwende Kanal "%s"? [yN]: ' % channelname)
#    if use == "y":
#        used_channels.append(channeluuid)

found_services = []

for chan in used_channels:
    services = htspapi.get_serviceuuids_from_channeluuid(chan)
    found_services.extend(services)

print "Found", len(found_channels_grid), "channels with this name:"

for chan in found_channels_grid:
    service_names = []
    service_uuids = chan['services']
    for suuid in service_uuids:
        service_names.append(htspapi.get_idnode_value(uuid=suuid))
    service_name = "; ".join(service_names)
    chan['service_name'] = service_name
    use = raw_input('- Use channel "%(name)s" @ %(service_name)s (%(number)d)? [yN]: ' % chan)
    if use:
        used_channels.append(chan['uuid'])
        found_services.extend(chan['services'])

# remove duplicates
found_services = list(set(found_services))
used_channels = list(set(used_channels))

merged_channel_name = raw_input("Name of new channel (%d merged services): " % len(found_services))
merged_channel_nr = raw_input("Number of new channel: ")
number = int(merged_channel_nr)

htspapi.create_channel(merged_channel_name, services=found_services, number=number)

disable_existing_channels = raw_input("Disable existing %d channels [yN]: " % len(found_services))
if disable_existing_channels == "y":
    htspapi.enable_channels(uuids=used_channels, enabled=False)
    # for c in used_channels:
    #    update_channel(uuid=c, enabled='false')

print "Done"
