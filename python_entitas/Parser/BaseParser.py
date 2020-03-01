import os
from mako.template import Template
from pathlib import Path
from . import utils
import collections
from lupa import *

class KV:
    def __init__(self):
        self.k = None
        self.v = None


class AttrClass():
    def __init__(self):
        self.class_name = str.lower(self.__class__.__name__)
        self.on_init()

    def on_init(self):
        return


class PrimaryIndex(AttrClass):
    def on_init(self):
        return


class Index(AttrClass):
    def on_init(self):
        return


class MuIndex(AttrClass):
    def on_init(self):
        self.index_data = []
        self.funcName = ""
        return

    def addData(self, comp_name, comp_value):
        temp_t = KV()
        temp_t.k = comp_name
        temp_t.v = comp_value
        self.index_data.append(temp_t)
        return

    def setFuncName(self, name):
        self.funcName = name


class Event(AttrClass):
    def __init__(self):
        super().__init__()
        self.event = None
        self.target = None
        self.type = None
        self.priority = 0
        self.action = None

    def on_init(self):
        self.event = None
        return

    def init_event(self, event):
        self.event = event
        self.target = event.target
        self.type = event.type or 'ADDED'
        self.priority = event.priority or 0
        self.action = event.action

    def get_group_event(self):
        if self.type != "ALL":
            return "GroupEvent." + self.type
        else:
            return "GroupEvent.ADDED | GroupEvent.REMOVED"


class Component():
    def __init__(self, name):
        self.data = []
        self.single = False
        self.attr = []
        self.simple = True
        self.name = name[0].lower() + name[1:]
        self.tag = None
        self.has_attr = False
        self.Name = name[0].upper() + name[1:]
        self.event_target = None
        self.event_action = None
        self.event = []
        return

    def __cmp__(self, other):
        if self.name > other.name:
            return 1
        else:
            return -1

    def is_empty(self):
        return len(self.data) == 0

    def set_data(self, data):
        self.data = []
        self.simple = False
        for i in range(len(data)):
            p = data[i]
            sp_ret = p.split('@')
            self.parse_property_data(i, sp_ret[0])
            if len(sp_ret) > 1:
                sp_ret = sp_ret[1].split('|')
                for prop in sp_ret:
                    prop = prop.replace(' ', '')
                    self.parse_property_data_attr(prop, self.data[i][0])

    def parse_property_data(self, i, property):
        sp_ret = property.split(':')
        self.data.append([0, 0])
        self.data[i][0] = sp_ret[0].replace(' ', '')
        self.data[i][1] = sp_ret[1]
        return

    def parse_property_data_attr(self, attr, p_name):
        if attr == 'primaryIndex':
            temp = PrimaryIndex()
            temp.p_name = p_name
            self.attr.append(temp)
        elif attr == 'index':
            temp = Index()
            temp.p_name = p_name
            self.attr.append(temp)
        return

    def get_property(self, i, context):
        ret_str = self.data[i][1]
        if context.pre_tag:
            ret_str = ret_str.replace('${pre_tag}', context.pre_tag).replace(' ', '')
        return ret_str

    def set_single(self, single):
        self.single = single

    def set_event(self, events):
        for index in events:
            event = events[index]
            if not event.target:
                raise ("event must has target")
            e = Event()
            e.init_event(event)
            self.event.append(e)

    def add_attr(self, key, val):
        self.attr[key] = self['parser_attr' + key](val)

    def parser_attr_primaryIndex(self, attr):
        for at in attr:
            name = at.split(':')
            name.replace(' ', '')
            is_have = False
            for data in self.data:
                if data[0] == name:
                    is_have = True
                    break
            if not is_have:
                raise (' attr value not in comp')

    def parser_attr_Index(self, attr):
        for at in attr:
            name = at.split(':')
            name.replace(' ', '')
            is_have = False
            for data in self.data:
                if data[0] == name:
                    is_have = True
                    break
            if not is_have:
                raise (' attr value not in comp')

    def parser_attr_Event(self, attr):
        for at in attr:
            name = at.split(':')
            name.replace(' ', '')
            is_have = False
            for data in self.data:
                if data[0] == name:
                    is_have = True
                    break
            if not is_have:
                raise (' attr value not in comp')

        return attr

    def get_func_params(self, pre='', sep=', '):
        b = []

        for item in self.data:
            b.append(pre + item[0])
        if len(self.data) > 0:
            return ', ' + sep.join(b)
        return ''

    def set_tag(self, tags):
        self.tag = tags

    def add_event(self, event):
        if event.eventTarget is None:
            raise ("error")
        self.event.append(event)


class ContextData():
    def __init__(self, tag):
        self.components = []
        self.event_comps = []
        self.source = ""
        self.name = tag
        self.Name = tag[0].upper() + tag[1:]
        self.muIndex = []
        self.tag = tag
        self.pre_tag = ""
        self.simple_name = tag
        if '_' in self.tag:
            self.pre_tag = self.tag[0:2]
            self.simple_name = self.simple_name.replace(self.pre_tag, '')

    def setSource(self, source):
        self.source = source

    def setOutPut(self, output):
        self.output = output

    def setComponents(self, comps):
        self.components = comps

    def addComponent(self, comp):
        self.components.append(comp)

    def addEventComponent(self, comp):
        self.event_comps.append(comp)

    def check(self):
        for comp in self.components:
            if comp.tag is None:
                raise (comp.name + "tag is None")

    def addContextMuIndex(self, index):
        self.muIndex.append(index)
        return


class BaseParser:
    def __init__(self, config_file_path):
        self.lua = LuaRuntime()
        self.source = ""
        self.namespace = ""
        self.out_path = ""
        self.parser_tag = None
        self.tag = None
        self.component_path = ''
        self.contexts = collections.OrderedDict()
        self.service_path = Path("")
        self.mako_path = Path(utils.get_python_fiel_Path(__file__)) / '../mako'
        self.python_entitas_soure_path = Path(utils.get_python_fiel_Path(__file__)) / '../entitas'

        self.base_config_file = config_file_path
        self.base_config_path = Path(os.path.dirname(config_file_path))
        self.script_path = Path()

        self.on_init()
        self.load_base_config()
        self.load_context_config()

    def load_base_config(self):
        with open(self.base_config_file , 'r') as load_f:
            text = load_f.read()
            config = self.lua.compile(text)()
        self.source = config.source
        self.component_path = self.base_config_path / config.component_path

        self.out_path = self.base_config_path / config.output
        self.namespace = config.namespace
        self.tag = list(config.tag.values())
        self.service_path = self.base_config_path / config.service_path
        self.tag.sort()

        for tag in self.tag:
            context = ContextData(tag)
            context.setSource(self.source)
            context.setOutPut(self.out_path)
            self.contexts[tag] = context

    def load_context_config(self):
        return

    def on_init(self):
        return

    def get_files_by_path(self):
        return

    def render_mako(self, fime_name, mako_name, context):
        file_path = os.path.join(self.out_path, context.name + fime_name)
        file = utils.open_file(file_path + '.py', 'w')
        template = Template(filename=str(self.mako_path / mako_name),
                            module_directory=os.path.join(self.script_path, 'makoCache'))
        content = self.template_render(template, context)
        content = content.replace('\n', '')
        content = content.replace('\r\n', '')
        file.write(content)
        file.close()

    def template_render(self, template, context):
        return template.render(
            context_name=context.name,
            contexts=context,
            source_path=self.source)

    def generate_context(self):
        for key, context in self.contexts.items():
            self.render_mako("Context" , 'ecs_context.mako', context)
            file_name = os.path.join(self.out_path / "../Extension/Context", context.name + "Context.py" )
            if not os.path.exists(file_name):
                file = utils.open_file(file_name, 'w')
                file.write('''
from ...Generated.{0}Context import {0}Context as Context
class {0}Context(Context):
    def __init__(self):
        super().__init__()'''.format(context.name))
                file.close()

    def generate_entity(self):
        for key, context in self.contexts.items():
            self.render_mako("Entity" , 'ecs_entity.mako', context)
            file_name = os.path.join(self.out_path / "../Extension/Entity", context.name + "Entity.py" )
            if not os.path.exists(file_name):
                file = utils.open_file(file_name, 'w')
                file.write('''
from ...Generated.{0}Entity import {0}Entity as Entity
class {0}Entity(Entity):
    def __init__(self):
        super().__init__()'''.format(context.name))
                file.close()

    def generate_component(self):
        for key, context in self.contexts.items():
            self.render_mako("Components" , 'ecs_make_component.mako', context)

    def generate_matcher(self):
        for key, context in self.contexts.items():
            self.render_mako("Matchers" , 'ecs_matcher.mako', context)

    def generate_autoinc(self):
        template = Template(filename=str(self.mako_path / "ecs_autoinc.mako"),
                            module_directory=os.path.join(self.script_path, 'makoCache'))
        file_name = os.path.join(self.out_path, "Contexts.py" )
        file = utils.open_file(file_name, 'w')
        content = template.render(
            contexts=self.contexts,
            source_path=self.source
        )
        content = content.replace('\n', '')
        content = content.replace('\r\n', '')
        file.write(content)
        file.close()

    def copy_python_entitas_source(self):
        utils.copytree(self.python_entitas_soure_path, self.out_path / 'Source')
        return

    def generate_all_init(self):
        file_name = os.path.join(self.out_path / "../__init__.py")
        file = utils.open_file(file_name, 'w')
        file.write('from .Generated import *')
        entity_inc_list = []
        for key, context in self.contexts.items():
            entity_inc_list.append(context.name + 'Entity')
        file.write('''
from .Extension.Entity import {0}'''.format(','.join(entity_inc_list)))
        entity_inc_list = []
        for key, context in self.contexts.items():
            entity_inc_list.append(context.name + 'Context')
        file.write('''
from .Extension.Context import {0}'''.format(','.join(entity_inc_list)))
    def generate(self):
        self.generate_context()
        self.generate_component()
        self.generate_entity()
        self.generate_autoinc()
        self.copy_python_entitas_source()
        self.generate_all_init()
