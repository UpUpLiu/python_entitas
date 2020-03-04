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
