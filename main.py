import threading
import tkinter as tk
import urllib.error
import urllib.request
from io import BytesIO
from tkinter import messagebox

from PIL import Image, ImageTk
from pytube import YouTube
from pytube.exceptions import RegexMatchError


class YouTubeDownloader(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        # dimensions
        self.WIDTH = 750
        self.HEIGHT = 600

        self.parent = parent
        self.parent.title("YouTube Video Downloader")
        self.parent.geometry(f"{self.WIDTH}x{self.HEIGHT}")

        # colors
        self.nero = "#171717"
        self.whisper = "#EDEDED"
        self.crimson = "#DA0037"

        # init
        self.init_ui()

    def init_ui(self):
        # background color of parent
        self.parent.config(background=self.nero)
        self.parent.resizable(False, False)

        # containers
        self.top_frame = tk.Frame(self.parent)
        self.top_frame.pack()
        self.entry_frame = tk.Frame(self.parent,
                                    pady=45,
                                    bg=self.nero,
                                    highlightthickness=0)
        self.entry_frame.pack()
        self.view_frame = tk.Frame(self.parent,
                                   bg=self.nero,
                                   highlightthickness=2,
                                   highlightbackground=self.crimson)
        self.view_frame.pack()
        download_frame = tk.Frame(self.parent)
        download_frame.pack(pady=40)

        # header label
        yt_icon = tk.PhotoImage(
            file="resources/icons8-youtube-play-button-100.png")
        lbl_heading = tk.Label(self.top_frame,
                               text="YouTube Video Downloader",
                               font=("Arial", 24, "bold"),
                               pady=30,
                               bg=self.nero,
                               fg=self.whisper,
                               image=yt_icon,
                               compound=tk.LEFT
                               )
        lbl_heading.image = yt_icon
        lbl_heading.pack()

        # entry field
        self.text = tk.StringVar()

        self.entry_url = tk.Entry(self.entry_frame,
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
                                  exportselection=0,
                                  textvariable=self.text
                                  )
        self.entry_url.insert(0, "Enter youtube url...")
        self.entry_url.bind("<FocusIn>", lambda args: self.entry_url.delete('0', 'end'))
        self.entry_url.pack(side="left", ipady=5, ipadx=90)

        self.text.trace_add("write", self.start_video_info_thread)

        # go button
        right_arrow_icon = tk.PhotoImage(file="resources/icons8-right-arrow-29.png")
        btn_go = tk.Button(self.entry_frame,
                           bg=self.nero,
                           activebackground=self.nero,
                           fg=self.nero,
                           activeforeground=self.nero,
                           image=right_arrow_icon,
                           highlightthickness=1,
                           highlightbackground=self.crimson,
                           justify=tk.CENTER,
                           relief=tk.FLAT,
                           cursor="hand2")
        btn_go["command"] = self.btn_go
        btn_go.image = right_arrow_icon
        btn_go.pack(side="left")

        # video thumbnail
        self.lbl_thumbnail = tk.Label(self.view_frame,
                                      text="IMG",
                                      bg=self.nero)
        self.lbl_thumbnail.pack(side="left")

        # name of video label
        self.lbl_title = tk.Label(self.view_frame,
                                  text="title",
                                  font=("Arial", 14),
                                  wraplength=300,
                                  justify="left",
                                  bg=self.nero,
                                  fg=self.whisper)
        self.lbl_title.pack()

        # video quality
        self.lbl_quality = tk.Label(self.view_frame,
                                    text=f"Quality: ",
                                    font=("Arial", 14),
                                    bg=self.nero,
                                    fg=self.whisper)
        self.lbl_quality.pack(anchor=tk.W, pady=25)

        # video size
        self.lbl_size = tk.Label(self.view_frame,
                                 text=f"Size: ",
                                 font=("Arial", 14),
                                 bg=self.nero,
                                 fg=self.whisper)
        self.lbl_size.pack(side=tk.BOTTOM, anchor=tk.W)

        # download button
        btn_download = tk.Button(download_frame,
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
        btn_download["command"] = self.download_video
        btn_download.pack()

    def valid_link(self):
        link = self.entry_url.get()

        if not link:
            return None

        try:
            yt = YouTube(link)
            return yt
        except RegexMatchError:
            pass
        except urllib.error.HTTPError:
            messagebox.showinfo("Link Broken", "The link is broken.\nTry again.")
            self.invalid_link_reset_widgets()

    def invalid_link_reset_widgets(self):
        self.entry_url.insert(0, "")
        self.lbl_thumbnail["image"] = ""
        self.lbl_title["text"] = "Title: "
        self.lbl_quality["text"] = "Quality: "
        self.lbl_size["text"] = "Size: "

    @staticmethod
    def video_stream(valid_link):
        stream = valid_link.streams.get_highest_resolution()
        return stream

    def video_thumbnail(self, valid_link):
        # get video thumbnail
        url_handle = urllib.request.urlopen(valid_link.thumbnail_url).read()
        photo = Image.open(BytesIO(url_handle))
        photo.thumbnail(size=(290, 270))
        img = ImageTk.PhotoImage(photo)

        # set video thumbnail
        self.lbl_thumbnail["image"] = img
        self.lbl_thumbnail.image = img

    def video_info(self):
        yt = self.valid_link()

        if yt is None:
            return

        # video thumbnail
        self.video_thumbnail(yt)

        # video title
        title = yt.title
        self.lbl_title["text"] = title

        # video quality
        res = self.video_stream(yt).resolution
        self.lbl_quality["text"] = f"Quality: {res}"

        # video size
        size = f"{round(self.video_stream(yt).filesize / 1e+6, 1)} MB"
        self.lbl_size["text"] = f"Size: {size}"

    def start_video_info_thread(self, *args):
        if self.valid_link() is None:
            return

        thread = threading.Thread(target=self.video_info)
        thread.start()

    def btn_go(self):
        user_input = self.entry_url.get()
        try:
            yt = YouTube(user_input)
        except RegexMatchError:
            tk.messagebox.showwarning("Invalid YouTube link", "Paste a valid YouTube link.")
            self.invalid_link_reset_widgets()
            return

        self.start_video_info_thread()

    def download_video(self):
        yt = self.valid_link()
        stream = self.video_stream(yt)

        if stream is None:
            return

        return stream.download()


def main():
    window = tk.Tk()
    app = YouTubeDownloader(window)
    window.mainloop()


if __name__ == "__main__":
    main()
