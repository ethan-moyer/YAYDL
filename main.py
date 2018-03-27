import youtube_dl
import tkinter
from tkinter import *
from tkinter import ttk
import os
from threading import Thread

def my_hook(d):
    if d['status'] == 'downloading':
        statusGUI.update()
        status.set('Status: ' + d['_percent_str'] + ' ETA: ' + d['_eta_str'])
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

def streamCommand():
    command = 'mpv --ytdl-format="bestvideo[height<=' + resolutionVar.get() + ']+bestaudio" ' + url.get()
    t = Thread(target = lambda: os.system(command))
    t.start()

top = tkinter.Tk()
status = tkinter.StringVar()
status.set("Status: ")
theme = ttk.Style()
#theme.theme_use('vista')
title = ttk.Label(top, text="Yet Another Youtube Downloader")
download = ttk.Button(top, text="Download", command = downloadLink)
stream = ttk.Button(top, text="Stream", command=streamCommand)
url = ttk.Entry(top)
resolutionVar = tkinter.StringVar()
resolutionVar.set("144")
resolution = ttk.OptionMenu(top, resolutionVar, "144", "144", "240", "360", "480", "720", "1080")
isAudioOnly = tkinter.IntVar()
audioGUI = ttk.Checkbutton(top, text="Audio Only", variable=isAudioOnly) 
statusGUI = ttk.Label(top, textvariable=status)
title.grid(row=0, column=1)
url.grid(row=1, column=1)
resolution.grid(row=2, column=0)
audioGUI.grid(row=2, column=1)
stream.grid(row=2, column=3)
download.grid(row=2, column=2)
statusGUI.grid(row=3, column=1)
top.mainloop()