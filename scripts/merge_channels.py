from tvh.htsp import HTSPClient
from scripts import CONFIG

htsp = HTSPClient((CONFIG['hostname'], 9982))
msg = htsp.hello()
htsp.authenticate(CONFIG['username'], CONFIG['password'])
cap = []
if 'servercapability' in msg:
    cap = msg['servercapability']


def search_channelnames(lookup):
    """
    Fetch all channels and search for matching channelnames, downsides:
        - fetchs all channels
        - not case insensitive
    """
    htsp.send('api', {'path': 'channel/list'})
    msg = htsp.recv()
    found = []
    for re in msg['response']['entries']:
        if lookup in re['val']:
            found.append(re)

    return found


def search_channelsnames_bygrid(lookup=''):
    """
    Fetch the channel grid with filter parameters
    """
    htsp.send('api', {'path': 'channel/grid', 'args': {
        'start': 0,
        'limit': 999999,
        'sort': 'name',
        'dir': 'ASC',
        'filter': [
            {
                "type": "string",
                "value": lookup,
                "field": "name"
            }
        ],
        'all': 1
    }})
    msg = htsp.recv()
    return msg['response']['entries']


def get_serviceuuids_from_channeluuid(uuid):
    htsp.send('api', {'path': 'idnode/load', 'args': {'uuid': uuid, 'meta': 1}})
    msg = htsp.recv()
    found_services = []
    for re in msg['response']['entries']:
        params = re['params']
        for paramdict in params:
            if 'services' in paramdict.values():
                found_services.extend(paramdict['value'])
    return found_services


def create_channel(name, services=[], tags=[], epg_parent="", enabled=True, number=0):
    htsp.send('api', {
        'path': 'channel/create',
        'args': {
            'conf': {
                'name': name,
                'enabled': 'true',
                'number': number,
                'services': services,
                'tags': tags,
                # 'bouquet': '',
            }
        }

    })
    return htsp.recv()


def update_channel(uuid, enabled='false', ):
    args = {
        'node': [
            {'uuid': uuid, 'enabled': enabled}
        ]
    }
    htsp.send('api', {
        'path': 'idnode/save',
        'args': args
    })
    return htsp.recv()


def get_idnode_value(uuid):
    htsp.send('api', {'path': 'idnode/load', 'args': {'uuid': uuid, 'meta': 0}})
    msg = htsp.recv()
    return msg['response']['entries'][0]["text"]


def update_channels(uuids, enabled=True):
    nodes = []
    for uuid in uuids:
        nodes.append({'uuid': uuid, 'enabled': enabled})
    args = {
        'node': nodes
    }
    htsp.send('api', {
        'path': 'idnode/save',
        'args': args
    })
    print "update_channels returned", htsp.recv()


search_channelname = raw_input("Search channel name: ")
# found_channels = search_channelnames(search_channelname)
found_channels_grid = search_channelsnames_bygrid(search_channelname)
used_channels = []
# for c in found_channels:
#    channeluuid = c['key']
#    channelname = c['val']
#    use = raw_input('- Verwende Kanal "%s"? [yN]: ' % channelname)
#    if use == "y":
#        used_channels.append(channeluuid)

found_services = []

for chan in used_channels:
    services = get_serviceuuids_from_channeluuid(chan)
    found_services.extend(services)

for chan in found_channels_grid:
    service_names = []
    service_uuids = chan['services']
    for suuid in service_uuids:
        service_names.append(get_idnode_value(uuid=suuid))
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

create_channel(merged_channel_name, services=found_services, number=number)

disable_existing_channels = raw_input("Disable existing %d channels [yN]: " % len(found_services))
if disable_existing_channels == "y":
    update_channels(uuids=used_channels, enabled=False)
    # for c in used_channels:
    #    update_channel(uuid=c, enabled='false')

print "Done"
