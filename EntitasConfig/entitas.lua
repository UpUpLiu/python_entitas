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
	output ="../PythonEntitas",
	service_path = "../PythonEntitas",
	extension_path = "../Extension",
	context_index = "ContextIndex",
	tag = tag
}

return entitas