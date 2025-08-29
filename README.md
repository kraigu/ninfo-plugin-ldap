ninfo-plugin-ldap
=================

LDAP plugin for ninfo: https://github.com/ninfo-py/ninfo


Configuration:

```
[plugin:ldap]
user   = foo
pw     = bar
server = ldaps://ldap.example.com:636
dsn    = ou=People,dc=example,dc=com
```

and optionally:
```
ignore_cert = true
fields = list,of,ldap,fields
field_substitution = list=testing,of=another_rename
```
