<h1 align="center">
  PyGWin
</h1>
<p align="center">
  A library for creating Python applications.
</p>

<p align="center">
  <a href="https://github.com/themixray/pygwin/wiki">
    Documentation
  </a>
</p>

<h2 align="center">
  Template
</h2>

```py
import pygwin

win = pygwin.create('Title',(500,500))

run = True
while run:
    for event in pygwin.getEvents():
        if event.type == pygwin.QUIT:
            run = False

    win.update()
pygwin.close()
```
