from pygwin._pg import pg as _pg

def getPressed():
    fkeys = {}
    keys = _pg.key.get_pressed()
    for i in range(len(keys)):
        fkeys.update({_pg.key.name(i):keys[i]})
    return fkeys
def isPressed(key):
    return getPressed()[key]

import inspect as _i

_aliases = {'getPressed':['gprs','getkeys'],
            'isPressed':['isprs','keyprs']}

for i in _aliases.items():
    exec(f'args = _i.signature({i[0]})')
    args = [str(i[1]) for i in dict(args.parameters).items()]
    args = ', '.join(args)
    for i0 in i[1]:
        exec(f"def {i0}({args}):return {i[0]}({args})")
