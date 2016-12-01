import sys
from tvh.htsp import HTSPClient
from tvh.api import HTSPApi
from scripts import CONFIG

try:
    limit = int(sys.argv[1])
except (IndexError, ValueError):
    limit = 500

try:
    filename = sys.argv[2]
except (IndexError):
    filename = 'channels.txt'

htsp = HTSPClient((CONFIG['hostname'], 9982))
msg = htsp.hello()
htsp.authenticate(CONFIG['username'], CONFIG['password'])
htspapi = HTSPApi(htsp=htsp)

chans_kwargs = {
    'start': 0,
    'limit': 999999,
    'sort': 'number',
    'dir': 'ASC',
    'filter': [
        {'type': 'numeric', 'comparison': 'gt', 'value': 1*1000000, 'intsplit': 1000000, 'field': 'number'},
        {'type': 'numeric', 'comparison': 'lt', 'value': limit*1000000, 'intsplit': 1000000, 'field': 'number'}
    ],
    'all': 1
}

channels = htspapi.get_channels_grid(kwargs=chans_kwargs)
rows = []
print "# CHANNEL_NAME; CHANNEL_ICON; CHANNEL_SERVICE"
for channel in channels:
    name_regex = '^%s$' % channel.get('name')
    icon = channel.get('icon')
    services = channel.get('services')
    multiplex_value = ''
    for service in services:
        params = htspapi.get_idnode_value(service, path='response.entries.0.params')
        for pdict in params:
            pid = pdict.get('id')
            if pid == 'multiplex':
                multiplex_value = pdict.get('value')

    print "%s;%s;%s" % (name_regex, icon, multiplex_value)

