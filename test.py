# from PythonEntitas.Extension.Context.AttrContext import AttrContext
# from PythonEntitas.Extension.Entity.AttrEntity import AttrEntity
from src.Parser import PythonParser, utils

if __name__ == "__main__":
    # at = AttrContext()
    # e : AttrEntity = at.create_entity()
    # e.replaceTest(1)
    # set = at.GetEntitiesByTestvalue(1)
    # e.replaceTest2(1)
    # print(at.GetEntityByTest2value(1))
    PythonParser(utils.get_python_fiel_Path(__file__) +"/EntitasConfig/entitas.lua").generate()

