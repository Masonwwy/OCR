import tkinter
from pyocr import pyocr
import os
from PIL import ImageGrab
from time import sleep
from tkinter import StringVar, IntVar
import pyperclip
root = tkinter.Tk()
root.geometry('200x80+400+300')
root.resizable(False, False)
class MyCapture:
    def __init__(self, png):
        self.X = tkinter.IntVar(value=0)
        self.Y = tkinter.IntVar(value=0)
        self.selectPosition=None
        screenWidth = root.winfo_screenwidth()
        screenHeight = root.winfo_screenheight()
        self.top = tkinter.Toplevel(root, width=screenWidth, height=screenHeight)
        self.top.overrideredirect(True)
        self.canvas = tkinter.Canvas(self.top,bg='white', width=screenWidth, height=screenHeight)
        self.image = tkinter.PhotoImage(file=png)
        self.canvas.create_image(screenWidth//2, screenHeight//2, image=self.image)
        def onLeftButtonDown(event):
            self.X.set(event.x)
            self.Y.set(event.y)
            self.sel = True
        self.canvas.bind('<Button-1>', onLeftButtonDown)
        def onLeftButtonMove(event):
            if not self.sel:
                return
            global lastDraw
            try:
                self.canvas.delete(lastDraw)
            except Exception as e:
                pass
            lastDraw = self.canvas.create_rectangle(self.X.get(), self.Y.get(), event.x, event.y, outline='black')
        self.canvas.bind('<B1-Motion>', onLeftButtonMove)

        def onLeftButtonUp(event):
            self.sel = False
            try:
                self.canvas.delete(lastDraw)
            except Exception as e:
                pass
            sleep(0.1)
            myleft, myright = sorted([self.X.get(), event.x])
            mytop, mybottom = sorted([self.Y.get(), event.y])
            self.selectPosition=(myleft,myright,mytop,mybottom)
            pic = ImageGrab.grab((myleft+1, mytop+1, myright, mybottom))
            tools = pyocr.get_available_tools()[:]
            code = tools[0].image_to_string(pic)
            self.result=code       
            self.top.destroy()
        self.canvas.bind('<ButtonRelease-1>', onLeftButtonUp)
        self.canvas.pack(fill=tkinter.BOTH, expand=tkinter.YES)


text = StringVar()
text.set('Click Capture to start!')
def buttonCaptureClick():
    filename = 'temp.png'
    im = ImageGrab.grab()
    im.save(filename)
    im.close()
    w = MyCapture(filename)
    buttonCapture.wait_window(w.top)
    text.set(str(w.result))
    pyperclip.copy(str(w.result))
    root.state('normal')
    os.remove(filename)
label=tkinter.Label(root,textvariable=text)
label.place(x=10, y=30, width=160, height=20)
label.config(text='Capture by Mason')
buttonCapture = tkinter.Button(root, text='Capture!', command=buttonCaptureClick)
buttonCapture.place(x=10, y=10, width=160, height=20)

root.mainloop()
