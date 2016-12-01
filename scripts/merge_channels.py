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

used_channel_names = []

for chan in found_channels_grid:
    service_names = []
    service_uuids = chan['services']
    for suuid in service_uuids:
        service_names.append(htspapi.get_idnode_value(uuid=suuid))
    service_name = "; ".join(service_names)
    chan['service_name'] = service_name
    chan_repr = '"%(name)s" @ %(service_name)s' % chan
    use = raw_input('- Use channel "%(name)s" @ %(service_name)s (%(number)d)? [yN]: ' % chan)
    if use:
        used_channels.append(chan['uuid'])
        used_channel_names.append(chan_repr)
        found_services.extend(chan['services'])

# remove duplicates
found_services = list(set(found_services))
used_channels = list(set(used_channels))

merged_channel_name = raw_input("Name of new channel (%d merged services): " % len(found_services))
merged_channel_nr = raw_input("Number of new channel: ")
number = int(merged_channel_nr)

for i, chanuuid in enumerate(used_channels, start=1):
    chan_epg = htspapi.get_epg(uuid=chanuuid)
    chan_repr = used_channel_names[i - 1]
    if len(chan_epg) > 0:
        print "- %d | %d EPG entries, Name=%s" % (i, len(chan_epg), chan_repr)

reuse_epg_index = raw_input("Number of EPG channel to reuse (0=disabled): ")
reuse_epg_index = int(reuse_epg_index)
epg_parent = None
if reuse_epg_index > 0:
    epg_parent = used_channels[reuse_epg_index - 1]

htspapi.create_channel(merged_channel_name, services=found_services, number=number, epg_parent=epg_parent)

disable_existing_channels = raw_input("Disable existing %d channels [yN]: " % len(found_services))
if disable_existing_channels == "y":
    htspapi.enable_channels(uuids=used_channels, enabled=False)
    # for c in used_channels:
    #    update_channel(uuid=c, enabled='false')

print "Done"
