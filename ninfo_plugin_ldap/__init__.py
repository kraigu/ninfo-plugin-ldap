from ninfo import PluginBase

import struct

# from https://stackoverflow.com/a/52825313
def convert_sid(binary):
    version = struct.unpack('B', binary[0:1])[0]
    # I do not know how to treat version != 1 (it does not exist yet)
    assert version == 1, version
    length = struct.unpack('B', binary[1:2])[0]
    authority = struct.unpack(b'>Q', b'\x00\x00' + binary[2:8])[0]
    string = 'S-%d-%d' % (version, authority)
    binary = binary[8:]
    assert len(binary) == 4 * length
    for i in range(length):
        value = struct.unpack('<L', binary[4*i:4*(i+1)])[0]
        string += '-%d' % value
    return string

class ldap_plugin(PluginBase):
    """This plugin looks up a user in ldap and returns their information"""

    name = "ldap"
    title = "LDAP"
    description = "LDAP Lookup"
    cache_timeout = 60*60
    types = ['username']

    def setup(self):
        c = self.plugin_config
        import ldap
        self.ldap = ldap
        ldap_user   = c['user']
        ldap_pw     = c['pw']
        server      = c['server']
        dsn         = c['dsn']
        searchpre   = c.get('searchpre', 'uid')
        searchpost  = c.get('searchpost', '')
        ignore_cert = 'ignore_cert' in c
        if ignore_cert:
            ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, 0)

        self.l = ldap.initialize(server)
        self.l.simple_bind_s(ldap_user, ldap_pw)
        self.dsn = dsn
        self.searchpre = searchpre
        self.searchpost = searchpost

    def get_info(self, arg):
        search = '%s=%s%s' % (self.searchpre, arg, self.searchpost)
        res = self.l.search_s(self.dsn, self.ldap.SCOPE_SUBTREE, search)
        if not res:
            return None
        res = res[0]
        key, values = res

        ret = {}
        for k,v in values.items():
            if k == "objectSid":
                v = [convert_sid(i) for i in v]

            ret[k] = ', '.join(v)

        return {'record': ret}

plugin_class = ldap_plugin
