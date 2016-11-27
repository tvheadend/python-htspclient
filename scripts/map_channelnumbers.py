from tvh.htsp import HTSPClient
from tvh.api import HTSPApi
from scripts import CONFIG

htsp = HTSPClient((CONFIG['hostname'], 9982))
msg = htsp.hello()
htsp.authenticate(CONFIG['username'], CONFIG['password'])
htspapi = HTSPApi(htsp=htsp)

EXACT = '$'

channels = [
    # [<Channel Name>, <Serive lookup, i.e. Mux>]
    ["Das Erste HD", "11493"],
    ["ZDF HD", "11361"],
    ["RTL HD", "10832"],
    ["SAT.1 HD", "11464"],
    ["ProSieben HD", "11464"],
    ["Kabel eins HD", "11464"],
    ["Kabel eins HD", "11464"],
    ["RTLII HD", "10832"],
    ["VOX HD", "10832"],
    ["arte HD", "11493"],
    ["3sat HD", "11347"],
    ["WDR HD Bonn", "12603"],
    "NDR FS HH HD",
    "BR Fernsehen Nord HD",
    "SWR RP HD",
    "rhein main tv",
    "hr-fernsehen HD",
    "MDR Sachsen HD",
    "PHOENIX HD",
    "ServusTV HD Deutschland",
    "zdf_neo HD",
    ["ONE HD", "11052"],
    "ZDFinfo HD",
    ["tagesschau24 HD", "11052"],
    "ard-alpha",
    "n-tv HD",
    "N24 HD" + EXACT,
    "rbb Berlin HD",
    "N24 DOKU",
    "kabel eins Doku",
    "Zee One HD",
    ["TLC HD" + EXACT, "10964"],
    ["ANIXE HD" + EXACT, "10773"],
    "Comedy Central/VIVA",
    "KiKA HD",
    "sat.1 gold hd" + EXACT,
    "sport1 hd" + EXACT,
    ["Sport1", "12382"],  # SPORT1+
    "Sport1 US HD",
    "SUPER RTL" + EXACT,
    ["NICKELODEON HD" + EXACT, "10773"],
    ["TELE 5 HD" + EXACT, "12574"],
    ["DMAX HD" + EXACT, "12574"],
    "RTLNITRO HD",
    "RTLplus",
    "SIXX HD" + EXACT,
    "Pro7 MAXX HD" + EXACT,

    ["SRF 1 HD", "10971"],
    ["SRF zwei HD", "10971"],
    "ORF1 HD",
    "ORF2W HD",

    "Sky Cinema HD" + EXACT,
    "Sky Cinema +1 HD" + EXACT,
    "Sky Cinema +24 HD" + EXACT,
    "Sky Cinema Hits HD" + EXACT,
    "Sky Cinema Nostalgie" + EXACT,
    "Sky Cinema Action HD" + EXACT,
    ["Sky Cinema Comedy" + EXACT, "11719"],
    "Sky Cinema Emotion" + EXACT,
    "Sky Cinema Family HD" + EXACT,
    "Sky 1 HD" + EXACT,
    ["Sky Atlantic HD" + EXACT, "11992"],
    ["Sky Atlantic +1 HD" + EXACT, "11797"],
    ["Universal HD", "11875"],
    "MGM HD",
    ["Sky Krimi", "12031"],
    ["Fox HD", "11332"],
    ["Fox Serie", "11758"],
    "RTL Crime HD",
    ["13th Street HD", "11992"],
    ["Syfy HD", "12304"],
    ["TNT Serie HD", "12382"],
    # Disney
    ["Disney Junior HD", "12070"],
    ["Disney Cinemagic HD", "11992"],
    ["Disney XD", "11719"],
    "Motorvision TV",
    ["A&E", "10920"],
    ["Romance TV", "10920"],
    "RTL Passion",
    "Heimatkanal",

    ["TNT Comedy HD", "11875"],
    ["E!", "11875"],
    ["Jukebox", "11170"],
    ["Goldstar TV", "11758"],
    ["Classica", "11719"],

    ["Sky 3D", "11332"],
    ["Sky Select HD", "11875"],
    ["NatGeo HD", "11992"],
    ["Nat Geo Wild HD", "11914"],
    ["Discovery HD", "11914"],



    ["Sky Sport News HD", "12304"],
    "Sky Sport Bundesliga 1 HD" + EXACT,
    "Sky Sport Bundesliga 2 HD" + EXACT,
    "Sky Sport Bundesliga 3 HD" + EXACT,
    "Sky Sport Bundesliga 4 HD" + EXACT,
    "Sky Sport Bundesliga 5 HD" + EXACT,
    "Sky Sport Bundesliga 6 HD" + EXACT,
    "Sky Sport Bundesliga 7 HD" + EXACT,
    "Sky Sport Bundesliga 8 HD" + EXACT,
    "Sky Sport Bundesliga 9 HD" + EXACT,
    "Sky Sport Bundesliga 10 HD" + EXACT,
    "Sky Sport Bundesliga 11 HD" + EXACT,
    "Sky Sport Bundesliga UHD" + EXACT,
    ["Eurosport 1 HD", "12382"],
    ["Eurosport 2 HD", "11170"],
    ["Sky Sport 1 HD" + EXACT, "11914"],
    ["Sky Sport 2 HD" + EXACT, "11992"],
    ["Sky Sport 3 HD" + EXACT, "11914"],
    ["Sky Sport 4 HD" + EXACT, "11992"],
    ["Sky Sport 5 HD" + EXACT, "12304"],
    ["Sky Sport 6 HD" + EXACT, "12382"],
    "Sky Sport 7 HD" + EXACT,
    "Sky Sport 8 HD" + EXACT,
    "Sky Sport 9 HD" + EXACT,
    "Sky Sport 10 HD" + EXACT,
    "Sky Sport 11 HD" + EXACT,
    "Sky Sport UHD" + EXACT,
    ["sportdigital HD", "12721"],

    ["Beate-Uhse.TV", "11719"],

    # Spanisch
    ["COMEDYCENTRALHD", "11258"]

]

#tag_name = 'Deutsche Programme'
#tag_uuid = ''

for channelnr, channel in enumerate(channels, start=1):
    if isinstance(channel, list) and len(channel) == 2:
        channel_lookup, service_lookup = channel
        found = htspapi.search_channelsnames_bygrid(lookup=channel_lookup, services=service_lookup)
    else:
        found = htspapi.search_channelsnames_bygrid(lookup=channel)

    if len(found) == 1:
        found = found[0]
    elif len(found) > 1:
        print "Found multiple channels", found
        found = None
    else:
        print "None found for", channel
        found = None

    if found:
        uuid = found.get('uuid')
        print "Found uuid for channel:", uuid, channel
        resp = htspapi.update_channels(uuids=[uuid], data={'number': channelnr})
        if 'error' in resp.keys():
            # Why i'm getting errors here?
            print "  - Error:", resp.get('error')
