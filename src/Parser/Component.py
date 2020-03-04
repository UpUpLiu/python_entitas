from src.Parser.AttrClass import PrimaryIndex, Index, Event


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
