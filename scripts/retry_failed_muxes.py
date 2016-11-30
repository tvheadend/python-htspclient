from tvh.htsp import HTSPClient
from tvh.api import HTSPApi
from scripts import CONFIG

htsp = HTSPClient((CONFIG['hostname'], 9982))
msg = htsp.hello()
htsp.authenticate(CONFIG['username'], CONFIG['password'])
htspapi = HTSPApi(htsp=htsp)

# Lookup network name:
LOOKUP_NETWORK_FILTER = 'IPTV'

mux_kwargs = {
    'start': 0,
    'limit': 999999,
    'sort': 'name',
    'dir': 'ASC',
    'filter': [
        {'type': 'string', 'value': LOOKUP_NETWORK_FILTER, 'field': 'network'},
        {'type': 'numeric', 'comparison': 'eq', 'value': htspapi.MUX_SCAN_RESULT_FAILED, 'field': 'scan_result'},
        #{'type': 'string', 'value': 'select', 'field': 'name'}
    ]
}

muxes = htspapi.get_muxes_grid(kwargs=mux_kwargs)
print 'Got %d FAILED muxes' % len(muxes)

found_mux_uuids = [m.get('uuid') for m in muxes]
htspapi.update_channels(found_mux_uuids, data={'scan_state': htspapi.MUX_SCAN_STATUS_PENDING})
