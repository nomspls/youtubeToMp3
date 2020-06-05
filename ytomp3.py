from tkinter import *
from tkinter import filedialog, messagebox, ttk
from typing import Optional
import threading
from subprocess import run

class GUI():
    def __init__(self):
        
        ''' Main window '''
        self.window = Tk()
        self.window.title('youtube mp3 downloader')
        self.window.geometry('700x200')
        
        ''' Link input line '''
        self.url_label = Label(self.window, text='Video link(ctrl+v): ',font=(None, 12))
        self.url_label.place(x=40, y=60)
        self.url_entry = Entry(self.window, width=50)
        self.url_entry.place(x=210, y=61)
        
        ''' Path line '''
        self.folder_path = StringVar()
        self.path_label = Label(self.window, text='Save mp3 to: ',font=(None, 12))
        self.path_label.place(x=40, y = 90)
        self.path_entry = Entry(self.window, width=50, textvariable=self.folder_path)
        self.path_entry.place(x=210, y=91)
        
        '''Browse button'''
        self.brws_button = Button(self.window, text='Browse', command=self.browse_button)
        self.brws_button.place(x=580, y=85)
        
        '''Download button'''
        self.down_button = Button(self.window, text='Download', command=self.pressed)
        self.down_button.place(x=40, y=150)
        
        self.progress = ttk.Progressbar(self.window, orient = HORIZONTAL)
        self.progress.pack(side=BOTTOM, fill=X)
        
        self.window.mainloop()
        
    def browse_button(self):
        self.folder_path
        self.filename = filedialog.askdirectory()
        self.folder_path.set(self.filename)
        
    def download(self, link, path:Optional[str]=None):
        self.link = link
        self.path = path
        
        if self.path != None:
            run(f'youtube-dl --prefer-ffmpeg -o "{self.path}/%(title)s.%(ext)s" --extract-audio --audio-format mp3 {self.link}',
                 shell=True, capture_output=True, text=True).stdout
        else: run(f'youtube-dl --prefer-ffmpeg --extract-audio --audio-format mp3 {self.link}',
                 shell=True, capture_output=True, text=True).stdout
              
    def pressed(self):
        self.progress.start()
        def callback():
            self.url = self.url_entry.get()
            self.dir = str(self.path_entry.get())

            if self.url != None and (self.url.startswith('http') or self.url.startswith('www')):
                
                try:
                    self.down_button['state'] = 'disabled'
                    self.download(self.url, self.dir)
                    self.progress.stop()
                    messagebox.showinfo(title='Success', message='Download complete!')
                    self.down_button['state'] = 'normal'
                except:
                    self.progress.stop()
                    messagebox.showerror(title='Server Error', message='\n    please try again    \n')
            else: 
                self.progress.stop()
                messagebox.showerror(title='Error', message='Bad url')

        self.t = threading.Thread(target=callback)
        self.t.start()

        
if __name__ == '__main__':
    GUI()