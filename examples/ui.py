import pygwin

win = pygwin.create('UI Example',(270,350))
base = pygwin.ui.base(win)

lbl = pygwin.ui.label('Label')
base.put(lbl,(130-(lbl.surface.size[0]/2),10))
base.put(pygwin.ui.button('Button',width=250),(10,50))
base.put(pygwin.ui.entry('Entry',width=123),(10,100))
base.put(pygwin.ui.keySelect('Key',width=122),(138,100))
loadbar = pygwin.ui.loadingBar(250,25)
base.put(loadbar,(10,150))
slider = pygwin.ui.slider(250)
base.put(slider,(10,170))
cb = pygwin.ui.checkBox(25,borderWidth=2)
base.put(cb,(10,220))
base.put(pygwin.ui.label('Checkbox',20),(45,225))
ta = pygwin.ui.textarea('Textarea',width=250,maxSymbols=20)
ta.text += '0123456789\n0123456789'
ta.focus = True
ta._generate()
ta.focus = False
base.put(ta,(10,255))

run = True
while run:
    for event in pygwin.getEvents():
        if event.type == pygwin.QUIT:
            run = False
    base.draw()
    if cb.get():
        loadbar.set(slider.get())
    else:
        loadbar.step()
        if loadbar.get() == loadbar.length:
            loadbar.set(0)
    win.update(30)
pygwin.close()
