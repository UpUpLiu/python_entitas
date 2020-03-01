# -*- coding: utf-8 -*-
from .BaseParser import BaseParser, Component
from . import utils


class PythonParser(BaseParser):
    def load_context_config(self):
        json_files = utils.get_file_list_with_suffix(self.component_path, '.lua')
        for file_path in json_files:
            if not file_path.endswith('entitas.lua'):
                with open(file_path, 'r', encoding='utf8') as load_f:
                    text = load_f.read()
                    ttt = self.lua.compile(text)()
                    components = self.get_components(ttt)
                    for comp in components:
                        for tag in comp.tag:
                            self.contexts[tag].addComponent(comp)

    def get_components(self, table):
        ret = []
        for key in table:
            ret.append(self.get_component(key, table[key]))
        return ret

    def get_component(self, key, table):
        comp = Component(key)
        if table.data:
            comp.set_data(list(table.data.values()))
        if table.single is not None:
            comp.set_single(True)
        comp.set_tag(list(table.tag.values()))
        if table.event is not None:
            comp.set_event(table.event)

        # if table.attr is not None:
        #     for at in table.attr:
        #         comp.add_attr(at, at)
        return comp

    def parse_context(self, key, table):
        context_files = utils.get_file_list_with_suffix(self.config_path, '.' + self.parser_tag)
        comp = Component(key)
        if table.data:
            comp.set_data(list(table.data.values()))
        if table.single is not None:
            comp.set_single(True)

        comp.set_tag(list(table.tag.values()))
        if table.event is not None:
            comp.set_event(table.event)

        # if table.attr is not None:
        #     for at in table.attr:
        #         comp.add_attr(at, at)
        return comp