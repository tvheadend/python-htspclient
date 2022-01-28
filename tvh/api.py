from tvh import utils


class HTSPApi(object):
    EPG_IGNORE = -1
    EPG_DISABLE = 0
    EPG_ENABLE = 0
    MUX_ENABLE = 1
    MUX_DISABLE = 0
    MUX_SCAN_RESULT_NONE = 0
    MUX_SCAN_RESULT_OK = 1
    MUX_SCAN_RESULT_FAILED = 2
    MUX_SCAN_STATUS_INACTIVE = 0
    MUX_SCAN_STATUS_PENDING = 1
    #MUX_SCAN_STATUS_INACTIVE = 0
    #MUX_SCAN_STATUS_INACTIVE = 0

    def __init__(self, htsp):
        self.htsp = htsp

    def search_channelnames(self, lookup):
        """
        Fetch all channels and search for matching channelnames, downsides:
            - fetchs all channels
            - not case insensitive
        """
        self.htsp.send('api', {'path': 'channel/list'})
        msg = self.htsp.recv()
        found = []
        for re in msg['response']['entries']:
            if lookup in re['val']:
                found.append(re)

        return found

    def get_channels_grid(self, kwargs={}):
        self.htsp.send('api', {'path': 'channel/grid', 'args': kwargs})
        msg = self.htsp.recv()
        return msg['response']['entries']

    def search_channelsnames_bygrid(self, lookup='', services=None):
        """
        Fetch the channel grid with filter parameters
        """
        kwargs = {
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
        }
        if services:
            kwargs['filter'].append({
                "type": "string",
                "value": services,
                "field": "services"
            })

        entries = self.get_channels_grid(kwargs=kwargs)
        return entries

    def get_serviceuuids_from_channeluuid(self, uuid):
        self.htsp.send('api', {'path': 'idnode/load', 'args': {'uuid': uuid, 'meta': 1}})
        msg = self.htsp.recv()
        found_services = []
        for re in msg['response']['entries']:
            params = re['params']
            for paramdict in params:
                if 'services' in paramdict.values():
                    found_services.extend(paramdict['value'])
        return found_services

    def get_muxes_grid(self, kwargs={}):
        self.htsp.send('api', {'path': 'mpegts/mux/grid', 'args': kwargs})
        msg = self.htsp.recv()
        return msg['response']['entries']

    def create_channel(self, name, services=[], tags=[], enabled=True, number=0, epg_parent=None):
        conf_args = {
            'conf': {
                'name': name,
                'enabled': 'true',
                'number': number,
                'services': services,
                'tags': tags,
                # 'bouquet': '',
            }
        }
        if epg_parent:
            conf_args['conf']['epg_parent'] = epg_parent

        self.htsp.send('api', {
            'path': 'channel/create',
            'args': conf_args

        })
        return self.htsp.recv()

    def update_channel(self, uuid, enabled='false', ):
        args = {
            'node': [
                {'uuid': uuid, 'enabled': enabled}
            ]
        }
        self.htsp.send('api', {
            'path': 'idnode/save',
            'args': args
        })
        return self.htsp.recv()

    def get_idnode_value(self, uuid, path='response.entries.0.text'):
        self.htsp.send('api', {'path': 'idnode/load', 'args': {'uuid': uuid, 'meta': 0}})
        msg = self.htsp.recv()
        return utils.getindex(msg, dotted_path=path)

    def enable_channels(self, uuids, enabled=True):
        nodes = []
        for uuid in uuids:
            nodes.append({'uuid': uuid, 'enabled': enabled})
        args = {
            'node': nodes
        }
        self.htsp.send('api', {
            'path': 'idnode/save',
            'args': args
        })
        print("enable_channels returned", self.htsp.recv())

    def update_channels(self, uuids, data):
        nodes = []
        for uuid in uuids:
            node_data = {'uuid': uuid}
            node_data.update(data)
            nodes.append(node_data)

        args = {
            'node': nodes
        }

        self.htsp.send('api', {
            'path': 'idnode/save',
            'args': args
        })
        return self.htsp.recv()

    def get_epg(self, kwargs={}):
        self.htsp.send('api', {
            'path': 'epg/events/grid',
            'args': kwargs
        })
        msg = self.htsp.recv()
        return msg['response']['entries']


