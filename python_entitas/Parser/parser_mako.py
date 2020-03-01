from mako.template import Template

ecs_autoinc = '''
%for k,con in contexts.items():
from ..Extension.Context.${con.Name}Context import ${con.Name}Context
%endfor


class Contexts:
    %for k,con in contexts.items():
<%
            name = con.Name[0].lower() + con.Name[1:]
        %>
    ${name} = ${con.Name}Context()
    %endfor
'''

ecs_context = '''
<%
    Context_name = context_name[0].upper() + context_name[1:]
    components = contexts.components
    import json
    def params_str(a, sep = ', ' , b = []):
        b = []
        for item in a:
            b.append('"' + item[0] + '"')
        return sep.join(b)
    def params(a, sep = ', ' , b = []):
        b = []
        for item in a:
            b.append(item[0])
        return sep.join(b)
%>\\

from .Source import Context, Entity, PrimaryEntityIndex, EntityIndex, Matcher
from ..Extension.Entity.${Context_name}Entity import ${Context_name}Entity
from .${Context_name}Components import ${Context_name}Components as Attr_comps



class ${Context_name}Context(Context):
    def __init__(self):
%for comp in components:
<%
    Name = comp.Name
    name =  comp.name
    Context_name = context_name[0].upper() + context_name[1:]
    properties = comp.data
%>\\
    %if comp.single:
        %if not comp.simple and comp.single:
        self.${name} = None
        self.${name}Entity = None
        %endif
    %endif
%endfor
        super().__init__()
        return

    %for comp in components:
    <%
        Name = comp.Name
        name =  comp.name
        Context_name = context_name[0].upper() + context_name[1:]
        properties = comp.data
    %>\\
        %if comp.single:
            %if not comp.simple:
    def set${Name}(self,${params(properties)}):
        if self.has_unique_component(${Context_name}_comps.${Name}) then
            error('${Name}Component already have')
        end
        return self.set_unique_component('${name}', ${Context_name}_comps.${Name}, ${params(properties)})

    def replace${Name}(self,${params(properties)}):
        local entity = self.${name}Entity
        if entity == nil then
            self.set${Name}(${params(properties)})
        else
            self.${name} = entity.replace(${Context_name}_comps.${Name}, ${params(properties)})
        end
        return entity


            %else:
    def set${Name}(self, value):
        if (value ~= self.has${Name}()) then
            if (value) then
                self.set_unique_component('${name}',${Context_name}_comps.${Name}, true)
            else
                self.remove_unique_component('${name}')
            end
        end
        return self

            %endif

    def has${Name}(self):
        return self.has_unique_component(${Context_name}_comps.${Name})

    def remove${Name}(self):
        self.remove_unique_component('${name}')
        %endif
    %endfor

    def _create_entity(self):
        return ${context_name}Entity()

    def initGenerateEntityIndexes(self):
    %for comp in components:
    <%
        Name = comp.Name
        name =  comp.name
        Context_name = context_name[0].upper() + context_name[1:]
        properties = comp.data
    %>\\
            %for attr in  comp.attr:
                %if attr.class_name == "primaryindex":
        local group = self:get_group(Matcher({${Context_name}_comps.${Name}}))
        self._${Name}${attr.p_name}PrimaryIndex = PrimaryEntityIndex:new(${Context_name}_comps.${Name}, group, '${attr.p_name}')
        self.add_entity_index(self._${Name}${attr.p_name}PrimaryIndex)
                %elif attr.class_name == "index":
        local group = self:get_group(Matcher({${Context_name}_comps.${Name}}))
        self._${Name}${attr.p_name}Index = EntityIndex:new(${Context_name}_comps.${Name}, group, '${attr.p_name}')
        self.add_entity_index(self._${Name}${attr.p_name}Index)
                %endif
            %endfor
    %endfor

    <%
        i = 0
    %>
    %for index in contexts.muIndex:
    <%
        matcher_parm = []
        call_parm = []
        i += 1
        for index_data in index.index_data:
            Name = index_data.k
            Name = Name[0].upper() + Name[1:]
            matcher_parm.append(Context_name + "_comps." + Name)
            value = index_data.v
            call_parm.append('{' + 'comp_type={0},  key =  "{1}"'.format(Context_name + "_comps." + Name, value) + '}')
        print(','.join(matcher_parm))
    %>\\
        local group = self.get_group(Matcher({${','.join(matcher_parm)}}))
        self._ContextIndex${i} = classMap.EntityMuIndex:new(group, {
            ${','.join(call_parm)}
        })
    %endfor
        return


    %for comp in components:
    <%
        Name = comp.Name
        name =  comp.name
        Context_name = context_name[0].upper() + context_name[1:]
        properties = comp.data
    %>\\
            %for attr in  comp.attr:
                %if attr.class_name == "primaryindex":
    def GetEntityBy${Name}${attr.p_name}(self,${attr.p_name}):
        return self._${Name}${attr.p_name}PrimaryIndex.get_entity(self,${attr.p_name})
                %elif attr.class_name == "index":
    def GetEntitiesBy${Name}${attr.p_name}(self,${attr.p_name}):
        return self._${Name}${attr.p_name}Index.get_entities(${attr.p_name})

                %endif
            %endfor
    %endfor


    <%
        i = 0
    %>
    %for index in contexts.muIndex:
    <%
        call_parm = []
        i += 1
        name_parm = []
        for index_data in index.index_data:
            Name = index_data.k
            Name = Name[0].upper() + Name[1:]
            name_parm.append(Name)
            name_parm.append(index_data.v)
            call_parm.append(Name+'_'+value)
    %>\\

    def ${index.funcName}(self,${','.join(call_parm)}):
        return self._ContextIndex${i}.get_entities(${','.join(call_parm)})

    %endfor
'''

ecs_entity = '''
<%
    Context_name = context_name[0].upper() + context_name[1:]
    components = contexts.components
    event_comps = contexts.event_comps
    import json
    def params(a, sep = ', ' , b = []):
        b = []
        for item in a:
            b.append(item[0])
        return sep.join(b)

    def params_str(a, sep = ', ' , b = []):
        b = []
        for item in a:
            b.append('"' + item[0] + '"')
        return sep.join(b)
%>\

from .Source import Context, Entity, PrimaryEntityIndex, EntityIndex, Matcher
from .${Context_name}Components import ${Context_name}Components as ${Context_name}_comps


class ${Context_name}Entity(Entity):
    def __init__(self):
        super().__init__()
% for comp in components:
<%
    Name = comp.Name
    name =  comp.name
    Context_name = context_name[0].upper() + context_name[1:]
    properties = comp.data
%>\
        self.${name} = None
% endfor
        return


%for comp in components:
<%
    Name = comp.Name
    name =  comp.name
    Context_name = context_name[0].upper() + context_name[1:]
    properties = comp.data
%>
    %if not comp.simple:
    def has${Name}(self):
        return self.has(${Context_name}_comps.${Name})

    def add${Name} (self, ${params(properties)}):
        self.add(${Context_name}_comps.${Name}, ${params(properties)})
        return self

    def replace${Name} (self,${params(properties)}):
        self.replace(${Context_name}_comps.${Name}, ${params(properties)})
        return self

    def remove${Name} (self):
        self.remove(${Context_name}_comps.${Name})
        return self
        %else:
    def has${Name}(self):
        return self.has(${Context_name}_comps.${Name})

    def set${Name}(self, v):
        if (v != self.has${Name}()):
            if (v):
                self.add(${Context_name}_comps.${Name})
            else:
                self.remove(${Context_name}_comps.${Name})
        return self
        %endif
    %endfor
    %if event_comps:
        %for comp in event_comps:
    def Add${comp.Name}CallBack(self, callback, target):
        local list
        if not self.has${comp.Name}() then
            list = set.new(false)
        else
            list = self.${comp.name}.value
        end
        list:insertkv(callback, target)
        self.replace${comp.Name}(list)

    def Remove${comp.Name}CallBack(self, callback, removeComponentWhenEmpty):
        if removeComponentWhenEmpty == nil then
            removeComponentWhenEmpty = true
        end
        local listeners = self.${comp.name}.value
        listeners:remove(callback)
        if removeComponentWhenEmpty and listeners:size() == 0 then
            self.remove${comp.Name}()
        else
            self.replace${comp.Name}(listeners)
        end
        %endfor
    %endif

'''

ecs_make_component = '''
<%
    Context_name = context_name[0].upper() + context_name[1:]
    def params_str(a, sep = ', ' , b = []):
        b = []
        for item in a:
            b.append('' + item[0] + '')
        return sep.join(b)
    components = contexts.components
%>\\
class ${Context_name}Components:
%for comp in components:
<%
    Name = comp.Name
    name =  comp.name
    Context_name = context_name[0].upper() + context_name[1:]
    properties = comp.data
%>\\
    %if not comp.simple:

    class ${Name}:
        _name = '${name}'
        _Name = '${Name}'

        def __init__(self, ${params_str(properties)}):
            %for p in properties:
            self.${p[0]} = ${p[0]}
            %endfor
    %else:

    class ${Name}:
        _name = '${name}'
        _Name = '${Name}'
    %endif
%endfor


'''

ecs_service = '''
<%
    Context_name = context_name[0].upper() + context_name[1:]
    components = contexts.components
%>\\

---@class ${Context_name}Service
local M = {}

function M.init()
end

return M

'''

ecs_service_inc = '''
<%
    Context_name = context_name[0].upper() + context_name[1:]
    components = contexts.components
%>\\
---@type ${contexts.simple_name}Service
Service.${contexts.simple_name} = import(".${contexts.simple_name}Service")
Service.${contexts.simple_name}.init()
'''


if __name__ == "__main__":
    # PythonParser("E:\python_entitas\EntitasConfig\entitas.lua").generate()
    template = Template(text=ecs_context)