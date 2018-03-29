import os
from subprocess import run
from shlex import quote

import youtube_dl
import tkinter
from tkinter import ttk

import logging

logging.basicConfig(level=logging.DEBUG) # For dev purposes

VIDEO_FORMAT = "bestvideo[height<={res}]+bestaudio/worstvideo[height>={res}]+bestaudio/best[height<={res}]/worst[height>={res}]/best"
AUDIO_FORMAT = "bestaudio"

def progress_hook(d):
    if d['status'] == 'downloading':
        status.set('Status: ' + d['_percent_str'] + ' ETA: ' + d['_eta_str'])
    elif d['status'] == 'error':
        status.set('Status: Fatal Error')
    elif d['status'] == 'finished':
         status.set('Status: Done')

    logging.info(status.get())
    statusGUI.update()

ydl_opts = {
    'noplaylist' : False,
    'format' : 'best[height=144]',
    'listformats' : False,
    'progress_hooks' : [progress_hook],
    'outtmpl' : 'downloads/%(title)s.%(ext)s'
}

#def downloadStart():
    #status.set('Status: Downloading')
    #time.sleep(0.5)
    #downloadLink()


def download_link():
    url_text = url.get()
    logging.debug(url_text)
    audio_check = isAudioOnly.get()
    logging.debug(audio_check)

    res = resolutionVar.get()

    if audio_check:
        ydl_opts['format'] = AUDIO_FORMAT
    else:
        ydl_opts['format'] = VIDEO_FORMAT.format(res=res)
    logging.info(ydl_opts['format'])

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url_text])


def stream_command():
    res = resolutionVar.get()

    vformat = VIDEO_FORMAT.format(res=res)
    command = ['mpv', "--ytdl-format=''{}''".format(vformat), quote(url.get())]
    logging.debug(command)
    run(command)

logging.debug(os.getcwd())

top = tkinter.Tk()
top.title("Yet Another Youtube Downloader")

status = tkinter.StringVar()
status.set("Status: ")

theme = ttk.Style()

title = ttk.Label(top, text="Yet Another Youtube Downloader")
download = ttk.Button(top, text="Download", command = download_link)
stream = ttk.Button(top, text="Stream", command=stream_command)
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