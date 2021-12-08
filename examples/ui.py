import pygwin

win = pygwin.create('UI example',(270,350))
base = pygwin.ui.base(win) # Creating ui base

lbl = pygwin.ui.label('Label') # Creating label
base.put(lbl,(130-(lbl.surface.size[0]/2),10)) # Putting label to base
base.put(pygwin.ui.button('Button',width=250),(10,50)) # Putting button to base
base.put(pygwin.ui.entry('Entry',width=123),(10,100)) # Putting entry to base
base.put(pygwin.ui.keySelect('Key',width=122),(138,100)) # Putting key selector to base
loadbar = pygwin.ui.loadingBar(250,25) # Creating loading bar
base.put(loadbar,(10,150)) # Putting loading bar to base
slider = pygwin.ui.slider(250) # Creating slider
base.put(slider,(10,170)) # Putting slider to base
cb = pygwin.ui.checkBox(25,borderWidth=2) # Creating checkbox
base.put(cb,(10,220)) # Putting checkbox to base
base.put(pygwin.ui.label('Checkbox',20),(45,225)) # Putting checkbox label to base
ta = pygwin.ui.textarea('Textarea',width=250,maxSymbols=20) # Creating textarea
ta.text += '0123456789\n0123456789' # Set text to textarea
ta.focus = True # Focus textarea
ta._generate() # Generate textarea surface
ta.focus = False # Unfocus textarea
base.put(ta,(10,255)) # Putting textarea to base
tta = pygwin.ui.tip('textarea',
                    *ta.surface.size,
                    waitBeforeShowing=30) # Creating textarea tip
base.put(tta,(10,255)) # Putting textarea tip to base

run = True
while run:
    for event in pygwin.getEvents():
        if event.type == pygwin.QUIT:
            run = False
    base.draw() # Drawing base
    if cb.get(): # If checkbox
        loadbar.set(slider.get()) # If checkbox
    else:
        loadbar.step() # Step loading bar
        if loadbar.get() == loadbar.length: # If loading bar is full
            loadbar.set(0) # Reset loading bar
    tta.responceWidth,tta.responceHeight=ta.surface.size # Set responce width, height to textarea tip
    win.update(30)
pygwin.close()
