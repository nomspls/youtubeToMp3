from tkinter import *
from tkinter import filedialog, messagebox, ttk
from moviepy.editor import *
from typing import Optional
import os
import pytube

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
        self.down_button = Button(self.window, text='Download', command=pressed)
        self.down_button.place(x=40, y=150)
        
        self.progress = ttk.Progressbar(self.window, orient = HORIZONTAL, length = 120)
        self.progress.pack()
        self.progress.config(mode='indeterminate')
        
        self.window.mainloop()
        
    def browse_button(self):
        self.folder_path
        self.filename = filedialog.askdirectory()
        self.folder_path.set(self.filename)
        
    def download(self, link, path:Optional[str]=None):
        self.link = link
        self.path = path
        self.video = pytube.YouTube(self.link)

        if self.path != None:
            self.video.streams.get_audio_only().download(output_path=self.path)
        else: self.video.streams.get_audio_only().download()
        
    def convert(self, inname, outname, path:Optional[str]=os.getcwd()):
        self.inname = inname
        self.path = path
        self.outname = outname
        self.video = AudioFileClip(os.path.join(self.path, self.inname))
        self.video.write_audiofile(os.path.join(self.path, self.outname))
        os.remove(os.path.join(self.dir, self.inname))
        
    def pressed(self):
        self.progress.start()
        
        self.url = self.url_entry.get()
        self.dir = str(self.path_entry.get())
        self.title = pytube.YouTube(self.url).title.replace('.', '')
        try:
            
            self.download(self.url, self.dir)
            self.convert(f"{self.title}.mp4",f"{self.title}.mp3", self.dir)
            messagebox.showinfo(title='Success', message=f'Finished downloading\n{self.title}.mp3')
            self.progress.stop()
        except:
            messagebox.showerror(title='Server Error', message='\n    please try again    \n')
            self.progress.stop()
            try:
                os.remove(os.path.join(self.dir, self.inname))
            except:
                pass
        
        
if __name__ == '__main__':
    GUI()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
