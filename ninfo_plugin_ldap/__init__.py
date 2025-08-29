from datetime import datetime
from ninfo import PluginBase

import logging

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

from ldap3.utils.log import set_library_log_activation_level

set_library_log_activation_level(logging.CRITICAL)


class ldap_plugin(PluginBase):
    """This plugin looks up a user in ldap and returns their information"""

    name = "ldap"
    title = "LDAP"
    description = "LDAP Lookup"
    cache_timeout = 60 * 60
    types = ["username", "hash"]

    def setup(self):
        config = self.plugin_config
        import ldap3

        self.ldap = ldap3
        ldap_user = config["user"]
        ldap_pw = config["pw"]
        server = config["server"]
        dsn = config["dsn"]
        searchpre = config.get("searchpre", "uid")
        searchpost = config.get("searchpost", "")
        field_substitution_str = config.get("field_substitution", "")
        config["field_substitution"] = (
            {
                k.lower(): v
                for k, v in (x.split("=") for x in field_substitution_str.split(","))
            }
            if field_substitution_str
            else {}
        )

        ciphers = config.get("ciphers", "HIGH:!DH:!aNULL")

        tls_context = ldap3.Tls(ciphers=ciphers)
        self.ldap_server = ldap3.Server(server, get_info=ldap3.ALL, tls=tls_context)
        self.ldap_conn = ldap3.Connection(
            self.ldap_server, ldap_user, ldap_pw, auto_bind=True
        )
        self.dsn = dsn

        self.searchpre = searchpre
        self.searchpost = searchpost

    def get_info(self, arg):
        search = "(%s=%s%s)" % (self.searchpre, arg, self.searchpost)
        search_status = self.ldap_conn.search(
            self.dsn, search, attributes=self.ldap.ALL_ATTRIBUTES
        )

        if not search_status:
            return None

        ret = []
        for entry in self.ldap_conn.entries:
            entry_data = {}
            for attr in entry.entry_attributes:
                v = entry[attr].values
                items = []

                for idx, item in enumerate(v):
                    if isinstance(item, datetime):
                        items.append(
                            "{} ({})".format(
                                str(item),
                                entry.entry_raw_attributes[attr][idx].decode("utf-8"),
                            )
                        )
                    else:
                        items.append(str(item))

                entry_data[attr] = ", ".join(items)

            ret.append(entry_data)

        return {"records": ret}


plugin_class = ldap_plugin
