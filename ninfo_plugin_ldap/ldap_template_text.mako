<%
    fields = plugin_config['fields'].split()
    if not fields:
        fields = ("preferredDisplayName", "eduPersonPrimaryAffiliation", "eduPersonAffiliation", "title", "eduPersonPrimaryOrgUnitDN", "mail", "campusAddress", "telephoneNumber", "uid")
    field_substitution = plugin_config['field_substitution']
%>

%for record in records:
    %if loop.index != 0:

    %endif
    %for f in [x for x in fields if x in record]:
${field_substitution.get(f.lower(), f)}  ${record[f]}
    %endfor
%endfor
