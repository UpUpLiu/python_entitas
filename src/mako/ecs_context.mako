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
%>\

from .Source import Context, Entity, PrimaryEntityIndex, EntityIndex, Matcher
from ..Extension.Entity.${Context_name}Entity import ${Context_name}Entity
from .${Context_name}Components import ${Context_name}Components as ${Context_name}_comps

class ${Context_name}GenerateContext(Context):
    def __init__(self):
%for comp in components:
<%
    Name = comp.Name
    name =  comp.name
    Context_name = context_name[0].upper() + context_name[1:]
    properties = comp.data
%>\
    %if comp.single:
        %if not comp.simple and comp.single:
        self.${name} = None
        self.${name}Entity = None
        %endif
    %endif
%endfor
        super().__init__()
        self.initGenerateEntityIndexes()
        return

    def _create_entity(self):
        return  ${Context_name}Entity()

    %for comp in components:
    <%
        Name = comp.Name
        name =  comp.name
        Context_name = context_name[0].upper() + context_name[1:]
        properties = comp.data
    %>\
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

    def initGenerateEntityIndexes(self):
    %for comp in components:
<%
        Name = comp.Name
        name =  comp.name
        Context_name = context_name[0].upper() + context_name[1:]
        properties = comp.data
    %>\
            %for attr in  comp.attr:
                %if attr.class_name == "primaryindex":
\
        group = self.get_group(Matcher(all_of =[${Context_name}_comps.${Name}]))
        self._${Name}${attr.p_name}PrimaryIndex = PrimaryEntityIndex(${Context_name}_comps.${Name}, group, '${attr.p_name}')
        self.add_entity_index(self._${Name}${attr.p_name}PrimaryIndex)
                %elif attr.class_name == "index":
        group = self.get_group(Matcher(all_of =[${Context_name}_comps.${Name}]))
        self._${Name}${attr.p_name}Index = EntityIndex(${Context_name}_comps.${Name}, group, '${attr.p_name}')
        self.add_entity_index(self._${Name}${attr.p_name}Index)
                %endif
            %endfor
    %endfor
        return
    %for comp in components:
    <%
        Name = comp.Name
        name =  comp.name
        Context_name = context_name[0].upper() + context_name[1:]
        properties = comp.data
    %>
            %for attr in  comp.attr:
                %if attr.class_name == "primaryindex":

    def GetEntityBy${Name}${attr.p_name}(self,${attr.p_name}):
        return self._${Name}${attr.p_name}PrimaryIndex.get_entity(${attr.p_name})

                %elif attr.class_name == "index":

    def GetEntitiesBy${Name}${attr.p_name}(self,${attr.p_name}):
        return self._${Name}${attr.p_name}Index.get_entities(${attr.p_name})

                %endif
            %endfor
    %endfor