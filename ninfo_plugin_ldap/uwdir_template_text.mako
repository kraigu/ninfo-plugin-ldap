<%
    fields = plugin_config['fields'].split()
    if not fields:
        fields = ("preferredDisplayName", "eduPersonPrimaryAffiliation", "eduPersonAffiliation", "title", "eduPersonPrimaryOrgUnitDN", "mail", "campusAddress", "telephoneNumber", "uid")
%>

%for record in records:
----------------------------------------
    %for f in [x for x in fields if x in record]:
${f}: ${record[f]}
    %endfor
%endfor
