%for k,con in contexts.items():
from .. import ${con.Name}Context
from .. import ${con.Name}Entity
%endfor


class Contexts:
    %for k,con in contexts.items():
<%
            name = con.Name[0].lower() + con.Name[1:]
        %>
    ${name} = ${con.Name}Context()
    ${name}.set_entity_class(${con.Name}Entity)
    %endfor