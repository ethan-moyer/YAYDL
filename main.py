import youtube_dl
import tkinter
from tkinter import *
from tkinter import ttk
import time

def my_hook(d):
    if d['status'] == 'downloading':
        statusGUI.update()
        status.set('ETA: ' + d['_eta_str'])
    print("       " + status.get())
    statusGUI.update()
ydl_opts = {
    'noplaylist' : False,
    'format' : 'best[height=144]',
    'listformats' : False,
    'progress_hooks' : [my_hook]
}
#def downloadStart():
    #status.set('Status: Downloading')
    #time.sleep(0.5)
    #downloadLink()
def downloadLink():
    urlText = url.get()
    print(urlText)
    audioCheck = isAudioOnly.get()
    print(audioCheck)
    if (audioCheck == 0):
        ydl_opts['format'] = 'bestvideo[height<=' + resolutionVar.get() + ']+bestaudio' 
    else:
        ydl_opts['format'] = 'bestaudio[ext=m4a]/bestaudio' 
    print(ydl_opts['format'])
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([urlText])
    status.set('Status: Done')

top = tkinter.Tk()
status = tkinter.StringVar()
status.set("Status: ")
theme = ttk.Style()
#theme.theme_use('vista')
title = ttk.Label(top, text="Yet Another Youtube Downloader")
download = ttk.Button(top, text="Download", command = downloadLink)
url = ttk.Entry(top)
resolutionVar = tkinter.StringVar()
resolutionVar.set("144")
resolution = ttk.OptionMenu(top, resolutionVar, "144", "144", "240", "360", "480", "720", "1080")
isAudioOnly = tkinter.IntVar()
audioGUI = ttk.Checkbutton(top, text="Audio Only   ", variable=isAudioOnly) 
statusGUI = ttk.Label(top, textvariable=status)
title.pack()
url.pack()
resolution.pack(side=LEFT)
audioGUI.pack(side=LEFT)
download.pack(side=TOP)
statusGUI.pack(side=BOTTOM)
top.mainloop()
#while (1 == 1):
    #statusGUI.update()
