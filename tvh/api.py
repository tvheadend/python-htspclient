class HTSPApi(object):
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

    def search_channelsnames_bygrid(self, lookup='', services=''):
        """
        Fetch the channel grid with filter parameters
        """
        self.htsp.send('api', {'path': 'channel/grid', 'args': {
            'start': 0,
            'limit': 999999,
            'sort': 'name',
            'dir': 'ASC',
            'filter': [
                {
                    "type": "string",
                    "value": lookup,
                    "field": "name"
                },
                {
                    "type": "string",
                    "value": services,
                    "field": "services"
                }
            ],
            'all': 1
        }})
        msg = self.htsp.recv()
        return msg['response']['entries']

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

    def create_channel(self, name, services=[], tags=[], epg_parent="", enabled=True, number=0):
        self.htsp.send('api', {
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

    def get_idnode_value(self, uuid):
        self.htsp.send('api', {'path': 'idnode/load', 'args': {'uuid': uuid, 'meta': 0}})
        msg = self.htsp.recv()
        return msg['response']['entries'][0]["text"]

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
        print "enable_channels returned", self.htsp.recv()

    def update_channels(self, uuids, data):
        nodes = []
        for uuid in uuids:
            node_data = {'uuid': uuid}
            node_data.update(data)
            nodes.append(node_data)

        args = {
            'node': nodes
        }

        print " - ", args

        self.htsp.send('api', {
            'path': 'idnode/save',
            'args': args
        })
        return self.htsp.recv()

