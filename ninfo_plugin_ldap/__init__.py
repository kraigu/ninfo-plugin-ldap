from ninfo import PluginBase

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
            ret[k] = ', '.join(v)

        return {'record': ret}

plugin_class = ldap_plugin
