import tkinter
from tkinter import font

class Application(tkinter.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
        return

    def create_widgets(self):
        self.hi_there = tkinter.Button(self)
        self.hi_there["text"] = "Hello World(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.quit = tkinter.Button(self, text="QUIT", command=self.master.destroy)
            #master.destroyでウィンドウ破棄
        self.quit.pack(side="bottom")
        return

    def say_hi(self):
        print("hi there, everyone!")
        return




def constractor(): 
    root = tkinter.Tk()
    root.title("Window title")
    root.geometry("400x300+1000+10")
    root.mainloop()
    return

def fonts():
    root = tkinter.Tk()
    root.title("Label")
    root.geometry("300x300+1500+10")
    label1 = tkinter.Label(root, text="Hallo")
    label1.pack(side="top")
    font1 = font.Font(family='Helvetica', size=20, weight='bold')
    label2 = tkinter.Label(root, text="Bye", bg="blue", font=font1)
    label2.pack(side="top")
    font2 = font.Font(family='Times', size=40)
    label2 = tkinter.Label(root, text="See you", fg="red", font=font2)
    label2.pack(side="top")
    print("a")

    root.mainloop()
    
    return

def status():
    root = tkinter.Tk()
    root.title("Status bar")
    root.geometry("300x300")
    status = tkinter.Label(root, text="Now processing..",
                            borderwidth=2, relief="groove")
    status.pack(side=tkinter.BOTTOM, fill=tkinter.X)
    root.mainloop()

    return

def buttons():
    root = tkinter.Tk()
    root.geometry("400x300")
    app = Application(master=root)
    app.mainloop()
    return

def pict():
    root = tkinter.Tk()
    img = tkinter.PhotoImage(file='./icon.gif')
    label1 = tkinter.Label(root, image=img)
    label1.grid(row=1, column=1)
    label2 = tkinter.Label(root, image=img)
    label2.grid(row=1, column=2)
    label3 = tkinter.Label(root, image=img)
    label3.grid(row=2, column=1)
    label4 = tkinter.Label(root, image=img)
    label4.grid(row=2, column=2)
    root.mainloop()
    return

def camvas():
    root = tkinter.Tk()
    root.title("Canvas")
    C = tkinter.Canvas(root, bg="white", height=300, width=300)
                #キャンバス作るやつ
    C.create_polygon(10, 10, 50, 170, 130, 140, 180, 40, fill="red")
    C.create_line(10, 10, 200, 200, fill='black')
    C.pack()
    root.mainloop()

    return
def donothing(root):
    filewin = tkinter.Toplevel(root)
    button = tkinter.Button(filewin, text="Do nothing button")
    button.pack()
    return

def menu():
    root = tkinter.Tk()
    menubar = tkinter.Menu(root)

    filemenu = tkinter.Menu(menubar, tearoff=0)
    filemenu.add_command(label="New", command=donothing(root))
    filemenu.add_command(label="Open", command=donothing(root))
    filemenu.add_command(label="Save", command=donothing(root))
    filemenu.add_command(label="Save as...", command=donothing(root))
    filemenu.add_command(label="Close", command=donothing(root))
    filemenu.add_separator()    #メニューのセパレータを追加
    filemenu.add_command(label="Exit", command=root.quit)
    #menubar.add_cascade(label="File", menu=filemenu)        #メニュー名
                                #filemenuを追加

    editmenu = tkinter.Menu(menubar, tearoff=0)
    editmenu.add_command(label="Undo", command=donothing)
    editmenu.add_separator()
    editmenu.add_command(label="Cut", command=donothing(root))
    editmenu.add_command(label="Copy", command=donothing(root))
    editmenu.add_command(label="Paste", command=donothing(root))
    editmenu.add_command(label="Delete", command=donothing(root))
    editmenu.add_command(label="Select All", command=donothing(root))
    menubar.add_cascade(label="Edit", menu=editmenu)     #メニュー名


    helpmenu = tkinter.Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Help Index", command=donothing(root))
    helpmenu.add_command(label="About...", command=donothing(root))
    menubar.add_cascade(label="Help", menu=helpmenu)     #メニュー名

    root.config(menu=menubar)
    root.mainloop()
    return

def check():
    root = tkinter.Tk()
    CheckVar1 = tkinter.IntVar()
    CheckVar2 = tkinter.IntVar()
    C1 = tkinter.Checkbutton(root, text="Music", variable=CheckVar1,
                            onvalue=1, offvalue=0, height=5,
                            width=20, )
    C2 = tkinter.Checkbutton(root, text="Video", variable=CheckVar2,
                            onvalue=1, offvalue=0, height=5,
                            width=20)
    C1.pack()
    C2.pack()
    root.mainloop()
    return

def input_form():
    root = tkinter.Tk()
    L1 = tkinter.Label(root, text="Email")
    L1.pack(side=tkinter.LEFT)
    E1 = tkinter.Entry(root, bd=1)
    E1.pack(side=tkinter.RIGHT)
    root.mainloop()

    return
def grouping():
    root = tkinter.Tk()
    root.title("Frame")
    frame = tkinter.Frame(root)
    frame.pack()

    bottomframe = tkinter.Frame(root)
    bottomframe.pack(side=tkinter.BOTTOM)

    redbutton = tkinter.Button(frame, text="1")
    redbutton.pack(side=tkinter.LEFT)

    greenbutton = tkinter.Button(frame, text="2")
    greenbutton.pack(side=tkinter.LEFT)

    bluebutton = tkinter.Button(frame, text="3")
    bluebutton.pack(side=tkinter.LEFT)

    blackbutton = tkinter.Button(bottomframe, text="Go")
    blackbutton.pack(side=tkinter.BOTTOM)

    root.mainloop()
    return
def list_box():
    root = tkinter.Tk()
    root.title("Listbox")

    Lb1 = tkinter.Listbox(root, selectmode=tkinter.MULTIPLE)
    Lb1.insert(1, "TOKYO")
    Lb1.insert(2, "KYOTO")
    Lb1.insert(3, "OSAKA")
    Lb1.insert(4, "GUNMA")
    Lb1.insert(5, "GIFU")
    Lb1.insert(6, "EHIME")
    Lb1.pack()
    root.mainloop()
    return
def menu2():
    root = tkinter.Tk()
    root.title("check button")
    root.geometry("300x300")
    mb = tkinter.Menubutton(root, text="Subjects", relief=tkinter.RAISED)
    mb.grid()
    mb.menu = tkinter.Menu(mb, tearoff=0)
    mb["menu"] = mb.menu

    Var1 = tkinter.IntVar()
    Var2 = tkinter.IntVar()
    Var3 = tkinter.IntVar()

    mb.menu.add_checkbutton(label="Math", variable=Var1)
    mb.menu.add_checkbutton(label="English", variable=Var2)
    mb.menu.add_checkbutton(label="Physics", variable=Var3)

    mb.pack()
    root.mainloop()
    return

def main():
    #constractor()
    #fonts()
    #status()
    #buttons()
    #pict()
    #camvas()
    menu()
    #check()
    #input_form()
    #grouping()
    #list_box()
    #menu2()
    return

main()