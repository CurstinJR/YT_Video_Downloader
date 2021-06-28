import tkinter as tk
import urllib.request
from io import BytesIO
from tkinter import messagebox

from PIL import Image, ImageTk
from pytube import YouTube
from pytube.exceptions import RegexMatchError


class YouTubeDownloader(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent.title("YouTube Video Downloader")
        self.parent.geometry(f"750x600")

        # colors
        self.nero = "#171717"
        self.whisper = "#EDEDED"
        self.crimson = "#DA0037"

        # init
        self.initUI()

    def initUI(self):
        # background color of parent
        self.parent.config(background=self.nero)
        self.parent.resizable(False, False)

        # containers
        topFrame = tk.Frame(self.parent)
        topFrame.pack()
        entryFrame = tk.Frame(self.parent,
                              pady=45,
                              bg=self.nero,
                              highlightthickness=0)
        entryFrame.pack()
        viewFrame = tk.Frame(self.parent,
                             bg=self.nero,
                             highlightthickness=2,
                             highlightbackground=self.crimson)
        viewFrame.pack()
        downloadFrame = tk.Frame(self.parent)
        downloadFrame.pack(pady=40)

        # header label
        ytIcon = tk.PhotoImage(
            file="resources/icons8-youtube-play-button-100.png")
        lblHeading = tk.Label(topFrame,
                              text="YouTube Video Downloader",
                              font=("Arial", 24, "bold"),
                              pady=30,
                              bg=self.nero,
                              fg=self.whisper,
                              image=ytIcon,
                              compound=tk.LEFT
                              )
        lblHeading.image = ytIcon
        lblHeading.pack()

        # entry field
        self.entryUrl = tk.Entry(entryFrame,
                                 font=("Arial", 14),
                                 bg=self.nero,
                                 fg=self.whisper,
                                 width=36,
                                 highlightthickness=1,
                                 highlightbackground=self.crimson,
                                 highlightcolor=self.crimson,
                                 selectbackground=self.crimson,
                                 selectforeground=self.whisper,
                                 insertbackground=self.whisper,
                                 bd=0,
                                 exportselection=0
                                 )
        self.entryUrl.insert(0, "Enter youtube url...")
        self.entryUrl.bind("<FocusIn>", lambda args: self.entryUrl.delete('0', 'end'))
        self.entryUrl.pack(side="left", ipady=5, ipadx=90)

        # go button
        rightArrowIcon = tk.PhotoImage(file="resources/icons8-right-arrow-29.png")
        btnGo = tk.Button(entryFrame,
                          bg=self.nero,
                          activebackground=self.nero,
                          fg=self.nero,
                          activeforeground=self.nero,
                          image=rightArrowIcon,
                          highlightthickness=1,
                          highlightbackground=self.crimson,
                          justify=tk.CENTER,
                          relief=tk.FLAT,
                          cursor="hand2")
        btnGo["command"] = self.getVideoInfo
        btnGo.image = rightArrowIcon
        btnGo.pack(side="left")

        # video thumbnail
        self.lblThumbnail = tk.Label(viewFrame,
                                     text="IMG",
                                     bg=self.nero)
        self.lblThumbnail.pack(side="left")

        # name of video label
        self.lblTitle = tk.Label(viewFrame,
                                 text="title",
                                 font=("Arial", 14),
                                 wraplength=300,
                                 justify="left",
                                 bg=self.nero,
                                 fg=self.whisper)
        self.lblTitle.pack()

        # video quality
        self.lblQuality = tk.Label(viewFrame,
                                   text=f"Quality: ",
                                   font=("Arial", 14),
                                   bg=self.nero,
                                   fg=self.whisper)
        self.lblQuality.pack(anchor=tk.W, pady=25)

        # video size
        self.lblSize = tk.Label(viewFrame,
                                text=f"Size: ",
                                font=("Arial", 14),
                                bg=self.nero,
                                fg=self.whisper)
        self.lblSize.pack(side=tk.BOTTOM, anchor=tk.W)

        # download button
        btnDownload = tk.Button(downloadFrame,
                                text="Download",
                                font=("Arial", 16, "bold"),
                                bg=self.crimson,
                                activebackground="#AE002C",
                                fg=self.whisper,
                                activeforeground=self.whisper,
                                highlightthickness=1,
                                highlightbackground=self.nero,
                                relief=tk.RAISED,
                                cursor="hand2")
        btnDownload["command"] = self.downloadVideo
        btnDownload.pack()

    def validLink(self):
        link = self.entryUrl.get()

        try:
            yt = YouTube(link)
            return yt
        except RegexMatchError:
            messagebox.showwarning("Invalid YouTube link", "Paste a valid youtube link.")
            return

    def getVideoInfo(self):
        yt = self.validLink()

        if yt is None:
            return

        self.stream = yt.streams.get_highest_resolution()

        # YouTube Image label
        urlHandle = urllib.request.urlopen(yt.thumbnail_url).read()
        photo = Image.open(BytesIO(urlHandle))
        photo.thumbnail(size=(290, 270))
        img = ImageTk.PhotoImage(photo)

        self.lblThumbnail["image"] = img
        self.lblThumbnail.image = img

        # title
        title = yt.title
        self.lblTitle["text"] = title

        res = self.stream.resolution
        self.lblQuality["text"] = f"Quality: {res}"

        # size
        size = f"{round(self.stream.filesize / 1e+6, 1)} MB"
        self.lblSize["text"] = f"Size: {size}"

        return self.stream

    def downloadVideo(self):
        stream = self.getVideoInfo()

        if stream is None:
            return

        return stream.download()


def main():
    window = tk.Tk()
    app = YouTubeDownloader(window)
    window.mainloop()


if __name__ == "__main__":
    main()
