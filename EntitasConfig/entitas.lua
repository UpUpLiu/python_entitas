---@class Event
---@field eventTarget entitas.gen.EventTarget
---@field eventType entitas.gen.EventType
---@field priority number

---@class entitas.gen.EventTarget
EventTarget = {
	Any = 'Any',
	self = 'self'
}

---@class entitas.gen.EventType
EventType = {
	ADDED = 'ADDED',
	REMOVED = 'REMOVED',
	ALL = 'ALL',
}

tag = {
	Component = 'Component',
	Context = 'Context',
	Attr = 'Attr'
}
local entitas = {
	namespace ="Entitas",
	component_path = '.',
	source ="Common.entitas",
	output ="../PythonEntitas/Generated",
	service_path = "../PythonEntitas",
	context_index = "ContextIndex",
	tag = tag
}

return entitas