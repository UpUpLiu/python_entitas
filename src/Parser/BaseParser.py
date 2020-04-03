import json
import os
from mako.template import Template
from pathlib import Path
from . import utils
import collections
from lupa import *


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
        self.extension_path = ""
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

        self.out_path_root = self.base_config_path  /config.output
        self.out_path = self.base_config_path  /config.output / "Generated"
        self.extension_path = self.base_config_path / config.extension_path
        self.namespace = config.namespace
        self.tag = list(config.tag.values())
        self.service_path = self.base_config_path / config.service_path
        self.tag.sort()

        for tag in self.tag:
            context = ContextData(tag)
            context.setSource(self.source)
            context.setOutPut(self.out_path)
            self.contexts[tag] = context

        relative_paths = os.path.relpath( self.extension_path, self.out_path_root)
        self.root_2_extension = relative_paths.replace('/', '').replace('\\', '')
        if not self.root_2_extension.startswith('.'):
            self.root_2_extension = '.' + self.root_2_extension

        relative_paths = os.path.relpath( self.out_path_root, self.extension_path)
        self.extension_to_generate = relative_paths.replace('/','').replace('\\','')
        if not self.extension_to_generate.startswith('.'):
            self.extension_to_generate = '.' + self.extension_to_generate


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
                            module_directory=os.path.join(self.mako_path, 'makoCache'))
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
            self.render_mako("GenerateContext" , 'ecs_context.mako', context)
            file_name = os.path.join(self.extension_path / "Context", context.name + "Context.py" )
            if not os.path.exists(file_name):
                file = utils.open_file(file_name, 'w')
                file.write('''
from .{1} import {0}GenerateContext as Context
class {0}Context(Context):
    def __init__(self):
        super().__init__()'''.format(context.name, self.extension_to_generate))
                file.close()

    def generate_entity(self):
        for key, context in self.contexts.items():
            self.render_mako("GenerateEntity" , 'ecs_entity.mako', context)
            file_name = os.path.join(self.extension_path / "Entity", context.name + "Entity.py" )
            if not os.path.exists(file_name):
                file = utils.open_file(file_name, 'w')
                file.write('''
from .{1} import {0}GenerateEntity as Entity
class {0}Entity(Entity):
    def __init__(self):
        super().__init__()'''.format(context.name, self.extension_to_generate))
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
            source_path=self.source,
            root_2_extension = self.root_2_extension,
            extension_2_generate = self.extension_to_generate
        )
        # content = content.replace('\n', '')
        # content = content.replace('\r\n', '')
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
            entity_inc_list.append(context.name)
            file.write('''
from .Generated.{0}GenerateEntity import {0}GenerateEntity'''.format(context.name))
            file.write('''
from .Generated.{0}GenerateContext import {0}GenerateContext'''.format(context.name))
            file.write('''
from {1}.Entity.{0}Entity import {0}Entity'''.format(context.name, self.root_2_extension))
            file.write('''
from {1}.Context.{0}Context import {0}Context'''.format(context.name, self.root_2_extension))

    def generate(self):
        self.generate_context()
        self.generate_component()
        self.generate_entity()
        self.generate_autoinc()
        self.copy_python_entitas_source()
        self.generate_all_init()

