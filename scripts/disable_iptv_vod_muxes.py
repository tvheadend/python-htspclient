from tvh.htsp import HTSPClient
from tvh.api import HTSPApi
from scripts import CONFIG

htsp = HTSPClient((CONFIG['hostname'], 9982))
msg = htsp.hello()
htsp.authenticate(CONFIG['username'], CONFIG['password'])
htspapi = HTSPApi(htsp=htsp)

# Lookup network name:
LOOKUP_NETWORK_FILTER = "IPTV"

mux_kwargs = {
    'start': 0,
    'limit': 999999,
    'sort': 'name',
    'dir': 'ASC',
    'filter': [
        {"type": "string", "value": LOOKUP_NETWORK_FILTER, "field": "network"},
        #{"type": "numeric", "comparison": "eq", "value": 2, "field": "scan_result"}
    ]
}

muxes = htspapi.get_muxes_grid(kwargs=mux_kwargs)
print "Processing %d muxes, this can take a while" % len(muxes)

vod_muxes = []
muxes_with_epg_enabled = []
found_muxes = []


def guess_is_file(iptv_url):
    if ".m3u8" in iptv_url:
        return False
    if ".mkv" in iptv_url:
        return True
    if ".mp4" in iptv_url:
        return True
    if ".mkv" in iptv_url:
        return True
    if ".avi" in iptv_url:
        return True

for m in muxes:
    url = m.get('iptv_url')
    epg_enabled = m.get('epg')
    mux_uuid = m.get('uuid')
    if url:
        if guess_is_file(iptv_url=url):
            vod_muxes.append(mux_uuid)
        if epg_enabled:
            muxes_with_epg_enabled.append(mux_uuid)
        found_muxes.append(mux_uuid)
    else:
        print "[DEBUG] no url for IPTV-Mux, mux data:", m

# epg isn't distributed in many (payed) iptv stream or via 3rd party tool (like xmltv), so let's disable epg for all
EPG_FLAG = htspapi.EPG_DISABLE

# you can mark muxes as ignored (MUX_IGNORE) or disable (MUX_DISABLE)
MUX_DEACTIVATE_FLAG = htspapi.MUX_DISABLE

# uncomment the next line if you wish to enable all iptv muxes:
#htspapi.update_channels(found_muxes, data={'enabled': htspapi.MUX_ENABLE, 'epg': EPG_FLAG})
#print len(found_muxes), "enabled muxes, disabled epg"

htspapi.update_channels(vod_muxes, data={'enabled': MUX_DEACTIVATE_FLAG, 'epg': EPG_FLAG})
htspapi.update_channels(muxes_with_epg_enabled, data={'epg': EPG_FLAG})

print len(vod_muxes), "disbled VOD Muxes, disabled EPG"
print len(muxes_with_epg_enabled), "disbled EPG"

