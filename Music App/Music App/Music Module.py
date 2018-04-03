from tkinter import *
import pygame as pygame
from PIL import Image, ImageTk
import os
from tkinter.filedialog import askdirectory
from mutagen.id3 import ID3
from tkinter import messagebox

global mainwindow
mainwindow = Tk()
mainwindow.title("Music App")
mainwindow.geometry("400x400+500+200")

listofsongs = []
listofsongsh=[]
realnames = []
realnamesh = []
albumnames = []
artistnames = []

directory ="/home/manish/PycharmProjects/Music App/Music App/Music"

#for current playing song
v = StringVar()
songlabel = Label(mainwindow, textvariable=v, width=40)

index = 0

#to update the current playing somg name
def updatelabel():
    global index
    global songname
    v.set(realnames[index])
#    return songname

#to next the song
def nextsong():
    global index
    if index == len(listofsongs):
        index = 0
    index += 1
    pygame.mixer.music.load(listofsongs[index])
    pygame.mixer.music.play()
    updatelabel()

#previous song
def prevsong():
    global index
    if index == 0:
        index = len(listofsongs)
    index -= 1
    pygame.mixer.music.load(listofsongs[index])
    pygame.mixer.music.play()
    updatelabel()

#stop the song
def stopsong():
    pygame.mixer.music.stop()
    v.set("")
    # return songname

#resume song #pause the song
pause=False
a=0
def pausesong():
    global index,a
    global pause
    a=a+1
    #print(pause,a)
    if pause == False:
        pygame.mixer.music.pause()
        pause = True
        print(pause,a)

    else:
        pygame.mixer.music.unpause()
        pause = False
        print(pause,a)

def allsongs():
    global directory
    directory = askdirectory()
    os.chdir(directory)


    for files in os.listdir(directory):
        if files.endswith(".mp3"):
            realdir = os.path.realpath(files)
            audio = ID3(realdir)
            realnames.append(audio['TIT2'].text[0])
            listofsongs.append(files)

    pygame.mixer.init()
    pygame.mixer.music.load(listofsongs[index])
    #pygame.mixer.music.play()
    songicon()
def songicon():
    mainwindow.withdraw()
    global windowsongs
    global index
    print(index)
    windowsongs = Toplevel()
    windowsongs.title("All Songs")
    windowsongs.geometry("400x450+500+100")

    # for searching
    def search(event):
        data = str(e1.get())
        length = len(listofsongs)
        for i in range(0, length, 1):
            if data.lower() == realnames[i].lower():
                listbox.select_set(first=i)
                break
        else:
            messagebox.showinfo("message", "No result found")

    e1 = Entry(windowsongs, bd=1)
    e1.pack()
    e1.bind("<Return>", search)

    searchlabel = Label(windowsongs, text='Search', fg="dark orange",bg='grey1')
    searchlabel.pack()

    songlabel = Label(windowsongs, textvariable=v,fg='dark orange',bg='grey1', width=40)

    # volume update
    def chgvol(self):
        i = vol.get()
        pygame.mixer.music.set_volume(i)

    vol = Scale(windowsongs, from_=0, to=100, orient=HORIZONTAL, resolution=10,bg='grey1',fg='snow', command=chgvol)
    vol.place(x=300, y=270)
    vol.set(50)

    listbox = Listbox(windowsongs, selectbackground="dark orange",bg='grey15',fg= 'snow',width=300, height=15)
    listbox.pack()

    realnames.reverse()

    for items in realnames:
        listbox.insert(0, items)

    realnames.reverse()

    #select and play
    def select(event):
        select = listbox.curselection()
        index = int(select[0])
        pygame.mixer.music.load(listofsongs[index])
        pygame.mixer.music.play()
        v.set(realnames[index])
        #updatelabel()

    listbox.bind('<Button-1>', select)

    imagenext = Image.open("/home/manish/PycharmProjects/Music App/Music App/nexticon.png")
    imagenext = imagenext.resize((50,50), Image.ANTIALIAS)
    photonext = ImageTk.PhotoImage(imagenext)
    btnnextsong = Button(windowsongs, image=photonext, width=50, height=50,bg='grey1', command=nextsong)
    btnnextsong.place(x=210, y=340)
    lnext = Label(windowsongs, text="Next", fg='white', bg='grey1')
    lnext.place(x=220, y=400)

    imageplay=Image.open("/home/manish/PycharmProjects/Music App/Music App/playicon.png")
    imageplay = imageplay.resize((50, 50), Image.ANTIALIAS)
    photoplay = ImageTk.PhotoImage(imageplay)
    btnplaysongs = Button(windowsongs, image=photoplay, width=50, height=50, bg='grey1',command=pausesong)
    btnplaysongs.place(x=130, y=340)
    lplay = Label(windowsongs, text="Play/Pause", fg='white', bg='grey1')
    lplay.place(x=124, y=400)

    imageprev = Image.open("/home/manish/PycharmProjects/Music App/Music App/previcon.png")
    imageprev = imageprev.resize((50, 50), Image.ANTIALIAS)
    photoprev = ImageTk.PhotoImage(imageprev)
    btnprevsong = Button(windowsongs, image=photoprev, width=50, height=50, bg='grey1',command=prevsong)
    btnprevsong.place(x=50, y=340)
    lprev = Label(windowsongs, text="Prev", fg='white', bg='grey1')
    lprev.place(x=60, y=400)

    imagestop= Image.open("/home/manish/PycharmProjects/Music App/Music App/stopicon.png")
    imagestop = imagestop.resize((50, 50), Image.ANTIALIAS)
    photostop = ImageTk.PhotoImage(imagestop)
    btnstopsong = Button(windowsongs, image=photostop, width=50, height=50,bg='grey1', command=stopsong)
    btnstopsong.place(x=290, y=340)
    lstop = Label(windowsongs, text="Stop", fg='white', bg='grey1')
    lstop.place(x=300, y=400)

    menubar = Menu(windowsongs)
    # create a pulldown menu, and add it to the menu bar
    filemenu = Menu(menubar,bg='grey1',fg='orange' ,tearoff=0)
    filemenu.add_command(label="Open", command=allsongs)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=mainwindow.quit)
    menubar.add_cascade(label="File", menu=filemenu)

    albummenu = Menu(menubar, bg='grey1',fg='orange',tearoff=0)
    albummenu.add_command(label="Album" , command=album)
    menubar.add_cascade(label="Album", menu=albummenu)

    artistsmenu = Menu(menubar, bg='grey1',fg='orange', tearoff=0)
    artistsmenu.add_command(label="Artist",command=artist)
    menubar.add_cascade(label="Artist", menu=artistsmenu)

    '''
    langmenu = Menu(menubar, bg='grey1', fg='orange', tearoff=0)
    langmenu.add_command(label="Hindi",command=hindi)
    langmenu.add_command(label="English")#, command=english)
    menubar.add_cascade(label="Language", menu=langmenu)
    '''
    helpmenu = Menu(menubar, bg='grey1',fg='orange', tearoff=0)
    helpmenu.add_command(label="About",command=aboutus)
    menubar.add_cascade(label="Help", menu=helpmenu)

    # display the menu
    menubar.configure(background='black',fg='orange')
    windowsongs.config(menu=menubar)
    #songlabel.place(x=40,y=200)
    songlabel.pack()
    windowsongs.configure(background='grey1')
    windowsongs.resizable(width=False, height=False)
    windowsongs.mainloop()

art=0
def artist():
    mainwindow.withdraw()
    global windowartist
    global art
    art=1

    windowartist = Toplevel()
    windowartist.geometry("400x450+500+100")
    windowartist.title("Artist")

    # for searching
    def search(event):
        data = str(e1.get())
        length = len(listofsongs)
        for i in range(0, length, 1):
            if data.lower() == artistnames[i].lower():
                listbox1.select_set(first=i)
                break

        else:
            messagebox.showinfo("message", "No result found")

    e1 = Entry(windowartist, bd=1)
    e1.pack()
    e1.bind("<Return>", search)

    searchlabel = Label(windowartist, text='Search', fg="dark orange",bg='grey1')
    searchlabel.pack()

    songlabel = Label(windowartist, textvariable=v, fg='dark orange', bg='grey1', width=40)

    # volume update
    def chgvol(self):
        i = vol.get()
        pygame.mixer.music.set_volume(i)

    vol = Scale(windowartist, from_=0, to=100, orient=HORIZONTAL, resolution=10,bg='grey1',fg='snow', command=chgvol)
    vol.place(x=300, y=270)
    vol.set(50)

    listbox1 = Listbox(windowartist, selectbackground="dark orange",bg='grey15',fg='snow', width=300, height=15)
    listbox1.pack()

    os.chdir(directory)
    for files in os.listdir(directory):
        if files.endswith(".mp3"):
            realdir = os.path.realpath(files)
            audio = ID3(realdir)
            listofsongs.append(files)
            artistnames.append(audio['TPE1'].text[0])

    #if direct artist is selected then
    pygame.mixer.init()
    pygame.mixer.music.load(listofsongs[index])

    artistnames.reverse()

    for items in artistnames:
        listbox1.insert(0,items)

    artistnames.reverse()

    # select and play
    def select(event):
        select = listbox1.curselection()
        index = int(select[0])
        pygame.mixer.music.load(listofsongs[index])
        pygame.mixer.music.play()
        v.set(realnames[index])
        #updatelabel()

    listbox1.bind('<Button-1>', select)

    imagenext = Image.open("/home/manish/PycharmProjects/Music App/Music App/nexticon.png")
    imagenext = imagenext.resize((50,50), Image.ANTIALIAS)
    photonext = ImageTk.PhotoImage(imagenext)
    btnnextsong = Button(windowartist, image=photonext, width=50, height=50,bg='grey1', command=nextsong)
    btnnextsong.place(x=210, y=340)
    lnext = Label(windowartist, text="Next", fg='white', bg='grey1')
    lnext.place(x=220, y=400)

    imageplay=Image.open("/home/manish/PycharmProjects/Music App/Music App/playicon.png")
    imageplay = imageplay.resize((50, 50), Image.ANTIALIAS)
    photoplay = ImageTk.PhotoImage(imageplay)
    btnplaysongs = Button(windowartist, image=photoplay, width=50, height=50, bg='grey1',command=pausesong)
    btnplaysongs.place(x=130, y=340)
    lplay = Label(windowartist, text="Play/Pause", fg='white', bg='grey1')
    lplay.place(x=124, y=400)


    imageprev = Image.open("/home/manish/PycharmProjects/Music App/Music App/previcon.png")
    imageprev = imageprev.resize((50, 50), Image.ANTIALIAS)
    photoprev = ImageTk.PhotoImage(imageprev)
    btnprevsong = Button(windowartist, image=photoprev, width=50, height=50, bg='grey1',command=prevsong)
    btnprevsong.place(x=50, y=340)
    lprev = Label(windowartist, text="Prev", fg='white', bg='grey1')
    lprev.place(x=60, y=400)


    imagestop= Image.open("/home/manish/PycharmProjects/Music App/Music App/stopicon.png")
    imagestop = imagestop.resize((50, 50), Image.ANTIALIAS)
    photostop = ImageTk.PhotoImage(imagestop)
    btnstopsong = Button(windowartist, image=photostop, width=50, height=50,bg='grey1', command=stopsong)
    btnstopsong.place(x=290, y=340)
    lstop = Label(windowartist, text="Stop", fg='white', bg='grey1')
    lstop.place(x=300, y=400)

    menubar = Menu(windowartist)
    # create a pulldown menu, and add it to the menu bar
    filemenu = Menu(menubar, bg='grey1',fg='orange', tearoff=0)
    filemenu.add_command(label="Open", command=allsongs)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=mainwindow.quit)
    menubar.add_cascade(label="File", menu=filemenu)

    albummenu = Menu(menubar, bg='grey1',fg='orange', tearoff=0)
    albummenu.add_command(label="Album",command=album)
    menubar.add_cascade(label="Album", menu=albummenu)

    artistsmenu = Menu(menubar, bg='grey1',fg='orange', tearoff=0)
    artistsmenu.add_command(label="Artist", command=artist)
    menubar.add_cascade(label="Artist", menu=artistsmenu)

    helpmenu = Menu(menubar, bg='grey1',fg='orange', tearoff=0)
    helpmenu.add_command(label="About", command=aboutus)
    menubar.add_cascade(label="Help", menu=helpmenu)

    # display the menu
    windowartist.config(menu=menubar)
    windowartist.configure(background='grey1')
    menubar.configure(background='black', fg='orange')
    songlabel.pack()
    windowartist.resizable(width=False, height=False)
    windowartist.mainloop()

alb=0
def album():
    mainwindow.withdraw()
    global windowalbum
    global alb
    alb=1

    windowalbum = Toplevel()
    windowalbum.geometry("400x450+500+100")
    windowalbum.title("Album")

    # for searching
    def search(event):
        data = str(e1.get())
        length = len(listofsongs)
        for i in range(0, length, 1):
            if data.lower() == albumnames[i].lower():
                listbox2.select_set(first=i)
                break

        else:
            messagebox.showinfo("message", "No result found")

    e1 = Entry(windowalbum, bd=1)
    e1.pack()
    e1.bind("<Return>", search)

    searchlabel = Label(windowalbum, text='Search', fg="dark orange",bg='grey1')
    searchlabel.pack()

    songlabel = Label(windowalbum, textvariable=v, fg='dark orange', bg='grey1', width=40)

    # volume update
    def chgvol(self):
        i = vol.get()
        pygame.mixer.music.set_volume(i)

    vol = Scale(windowalbum, from_=0, to=100, orient=HORIZONTAL,bg='grey5',fg='snow', resolution=10, command=chgvol)
    vol.place(x=300, y=270)
    vol.set(50)

    listbox2 = Listbox(windowalbum, selectbackground="dark orange",bg='grey15',fg='snow', width=300, height=15)
    listbox2.pack()

    os.chdir(directory)
    for files in os.listdir(directory):
        if files.endswith(".mp3"):
            realdir = os.path.realpath(files)
            audio = ID3(realdir)
            listofsongs.append(files)
            albumnames.append(audio['TALB'].text[0])
            print(albumnames)

    #if fisrt album is clicked
    pygame.mixer.init()
    pygame.mixer.music.load(listofsongs[index])

    albumnames.reverse()

    for items in albumnames:
        listbox2.insert(0, items)

    albumnames.reverse()

    # select and play
    def select(event):
        select = listbox2.curselection()
        index = int(select[0])
        pygame.mixer.music.load(listofsongs[index])
        pygame.mixer.music.play()
        v.set(realnames[index])
        #updatelabel()

    listbox2.bind('<Button-1>', select)

    imagenext = Image.open("/home/manish/PycharmProjects/Music App/Music App/nexticon.png")
    imagenext = imagenext.resize((50, 50), Image.ANTIALIAS)
    photonext = ImageTk.PhotoImage(imagenext)
    btnnextsong = Button(windowalbum, image=photonext, width=50, height=50, bg='grey1', command=nextsong)
    btnnextsong.place(x=210, y=340)
    lnext = Label(windowalbum, text="Next", fg='white', bg='grey1')
    lnext.place(x=220, y=400)

    imageplay = Image.open("/home/manish/PycharmProjects/Music App/Music App/playicon.png")
    imageplay = imageplay.resize((50, 50), Image.ANTIALIAS)
    photoplay = ImageTk.PhotoImage(imageplay)
    btnplaysongs = Button(windowalbum, image=photoplay, width=50, height=50, bg='grey1', command=pausesong)
    btnplaysongs.place(x=130, y=340)
    lplay = Label(windowalbum, text="Play/Pause", fg='white', bg='grey1')
    lplay.place(x=124, y=400)


    imageprev = Image.open("/home/manish/PycharmProjects/Music App/Music App/previcon.png")
    imageprev = imageprev.resize((50, 50), Image.ANTIALIAS)
    photoprev = ImageTk.PhotoImage(imageprev)
    btnprevsong = Button(windowalbum, image=photoprev, width=50, height=50, bg='grey1', command=prevsong)
    btnprevsong.place(x=50, y=340)
    lprev = Label(windowalbum, text="Prev", fg='white', bg='grey1')
    lprev.place(x=60, y=400)


    imagestop = Image.open("/home/manish/PycharmProjects/Music App/Music App/stopicon.png")
    imagestop = imagestop.resize((50, 50), Image.ANTIALIAS)
    photostop = ImageTk.PhotoImage(imagestop)
    btnstopsong = Button(windowalbum, image=photostop, width=50, height=50, bg='grey1', command=stopsong)
    btnstopsong.place(x=290, y=340)
    lstop = Label(windowalbum, text="Stop", fg='white', bg='grey1')
    lstop.place(x=300, y=400)

    menubar = Menu(windowalbum)
    # create a pulldown menu, and add it to the menu bar
    filemenu = Menu(menubar, bg='grey1',fg='orange', tearoff=0)
    filemenu.add_command(label="Open", command=allsongs)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=mainwindow.quit)
    menubar.add_cascade(label="File", menu=filemenu)

    albummenu = Menu(menubar, bg='grey1',fg='orange', tearoff=0)
    albummenu.add_command(label="Album",command=album)
    menubar.add_cascade(label="Album", menu=albummenu)

    artistsmenu = Menu(menubar, bg='grey1',fg='orange', tearoff=0)
    artistsmenu.add_command(label="Artist",command=artist)
    menubar.add_cascade(label="Artist", menu=artistsmenu)

    helpmenu = Menu(menubar, bg='grey1',fg='orange', tearoff=0)
    helpmenu.add_command(label="About", command=aboutus)
    menubar.add_cascade(label="Help", menu=helpmenu)

    # display the menu
    windowalbum.config(menu=menubar)
    windowalbum.configure(background='grey1')
    menubar.configure(background='black', fg='orange')
    songlabel.pack()
    windowalbum.resizable(width=False, height=False)
    windowalbum.mainloop()

def aboutus():
    mainwindow.withdraw()
    windowabout = Toplevel()
    windowabout.title("About Us")
    windowabout.geometry("300x200+500+100")

    def onclick():
        pass

    text = Text(windowabout)
    text.insert(INSERT, "............Python Project...............................SE/A3/457-463...............Made by MAnish ,Sahil Srushti,samiksha,rahul.......")
    text.insert(END, "...............Thank You")
    text.pack()



    menubar = Menu(windowabout)
    # create a pulldown menu, and add it to the menu bar
    filemenu = Menu(menubar, bg='grey1',fg='orange', tearoff=0)
    filemenu.add_command(label="Open", command=allsongs)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=mainwindow.quit)
    menubar.add_cascade(label="File", menu=filemenu)

    albummenu = Menu(menubar, bg='grey1',fg='orange', tearoff=0)
    albummenu.add_command(label="Album", command=album)
    menubar.add_cascade(label="Album", menu=albummenu)

    artistsmenu = Menu(menubar, bg='grey1',fg='orange', tearoff=0)
    artistsmenu.add_command(label="Artist", command=artist)
    menubar.add_cascade(label="Artist", menu=artistsmenu)

    helpmenu = Menu(menubar, bg='grey1',fg='orange', tearoff=0)
    helpmenu.add_command(label="About", command=aboutus)
    menubar.add_cascade(label="Help", menu=helpmenu)

    # display the menu
    windowabout.config(menu=menubar)
    windowabout.configure(background='grey1')

    menubar.configure(background='black', fg='orange')
    windowabout.configure(background='grey1')
    windowabout.resizable(width=False, height=False)
    windowabout.mainloop()

#foldericon
imagefolder = Image.open("foldericon.png")
imagefolder = imagefolder.resize((50, 50), Image.ANTIALIAS)
photofolder = ImageTk.PhotoImage(imagefolder)
btnfolder = Button(mainwindow, image=photofolder, width=60, height=60,bg='grey1',command=allsongs)
btnfolder.place(x=50, y=30)
lfolder = Label(mainwindow, text='Folder',fg='white',bg='grey1')
lfolder.place(x=60,y=110)


#allsongsicon
imageallsongs = Image.open("songsicon.png")
imageallsongs = imageallsongs.resize((50, 50), Image.ANTIALIAS)
photoallsongs = ImageTk.PhotoImage(imageallsongs)
btnallsongs = Button(mainwindow, image=photoallsongs, width=60, height=60,bg='grey1', command=allsongs)
btnallsongs.place(x=170, y=30)
lsongs = Label(mainwindow, text="All Songs",fg='white',bg='grey1')
lsongs.place(x=175,y=110)

#songalbum
imagealbum = Image.open("songalbum.png")
imagealbum = imagealbum.resize((50, 50), Image.ANTIALIAS)
photoalbum = ImageTk.PhotoImage(imagealbum)
btnalbum = Button(mainwindow, image=photoalbum, width=60, height=60,bg='grey1',command=album)
btnalbum.place(x=50, y=160)
lalbum = Label(mainwindow, text="Album",fg='white',bg='grey1')
lalbum.place(x=60,y=240)

#songsartisticon
imagesongsartist = Image.open("songsartisticon.png")
imagesongsartist = imagesongsartist.resize((50, 50), Image.ANTIALIAS)
photosongsartist = ImageTk.PhotoImage(imagesongsartist)
btnsongsartist = Button(mainwindow, image=photosongsartist, width=60, height=60,bg='grey1',command=artist)
btnsongsartist.place(x=170, y=160)
lartist = Label(mainwindow, text="Artist",fg='white',bg='grey1')
lartist.place(x=190,y=240)

#about
imageaboutus = Image.open("aboutusicon.png")
imageaboutus = imageaboutus.resize((50, 50), Image.ANTIALIAS)
photoaboutus = ImageTk.PhotoImage(imageaboutus)
btndaboutus = Button(mainwindow, image=photoaboutus, width=60, height=60,bg='grey1',command=aboutus)
btndaboutus.place(x=290, y=30)
labout = Label(mainwindow, text="About us",fg='white',bg='grey1')
labout.place(x=290,y=110)

#exit
imageexit = Image.open("exiticon.png")
imageexit = imageexit.resize((50, 50), Image.ANTIALIAS)
photoexit = ImageTk.PhotoImage(imageexit)

btndexit = Button(mainwindow, image=photoexit, width=60, height=60,bg='grey1', command=mainwindow.quit)
btndexit.place(x=290, y=160)
lexit = Label(mainwindow, text="Exit",fg='white',bg='grey1')
lexit.place(x=310,y=240)

mainwindow.configure(background='grey1')
#mainwindow.eval('tk::PlaceWindow %s center' % mainwindow.winfo_pathname(mainwindow.winfo_id()))
mainwindow.resizable(width=False, height=False)
mainwindow.mainloop()
