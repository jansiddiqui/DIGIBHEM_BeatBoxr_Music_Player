import pygame
import tkinter.messagebox
from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk
import os
import time
from mutagen.mp3 import MP3

class SongPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title('BeatBoxr')
        self.root.geometry("500x600")
        self.root.configure(background='Magenta')

        # Initialize Pygame mixer
        pygame.mixer.init()

        # Initialize variables
        self.filename = None
        self.paused = False
        self.start_time = None

        # Create menu
        self.menubar = Menu(self.root)
        self.root.configure(menu=self.menubar)

        # File submenu
        self.submenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='File', menu=self.submenu)
        self.submenu.add_command(label='Open', command=self.open_file)
        self.submenu.add_command(label='Exit', command=self.root.destroy)

        # Help submenu
        self.submenu2 = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Help', menu=self.submenu2)
        self.submenu2.add_command(label='About', command=self.about)

        # Label
        self.label = Label(text='BeatBoxr', bg='Magenta', fg='yellow', font=('Helvetica', 24, 'bold underline'))
        self.label.place(x=200, y=10)

        # File label
        self.filelabel = Label(text='Select And Play...', bg='Magenta', fg='white', font=('Times', 12, 'bold'))
        self.filelabel.place(x=5, y=20)

        # Image
        self.pic = Image.open('HP.png')
        self.pic = ImageTk.PhotoImage(self.pic)
        pic = Label(self.root, image=self.pic, bg='Magenta')
        pic.place(x=50, y=50)

        # Length label
        self.lengthlabel = Label(self.root, text='Total Length: 00:00:00', bg='Black', fg='White')
        self.lengthlabel.place(x=180, y=503)

        # Time label
        self.timelabel = Label(self.root, text='00:00', bg='Black', fg='White')
        self.timelabel.place(x=220, y=520)

        # Buttons
        self.photo_B1 = PhotoImage(file='play.png')
        self.photo_B1 = self.photo_B1.subsample(5, 5)
        self.play_button = Button(self.root, image=self.photo_B1, bd=0, bg='Magenta', command=self.play_music)
        self.play_button.place(x=30, y=500)

        self.photo_B2 = PhotoImage(file='pause.png')
        self.photo_B2 = self.photo_B2.subsample(5, 5)
        self.pause_button = Button(self.root, image=self.photo_B2, bd=0, bg='Magenta', command=self.pause_music)
        self.pause_button.place(x=80, y=500)

        self.photo_B3 = PhotoImage(file='stop.png')
        self.photo_B3 = self.photo_B3.subsample(5, 5)
        self.stop_button = Button(self.root, image=self.photo_B3, bd=0, bg='Magenta', command=self.stop_music)
        self.stop_button.place(x=130, y=500)

        #animation


        # Volume button
        self.photo_B4_volume = PhotoImage(file='voice.png')
        self.photo_B4_volume = self.photo_B4_volume.subsample(5, 5)
        self.photo_B4_mute = PhotoImage(file='mute.png')
        self.photo_B4_mute = self.photo_B4_mute.subsample(5, 5)
        self.volume_button = Button(self.root, image=self.photo_B4_volume, bd=0, bg='Magenta', command=self.toggle_mute)
        self.volume_button.place(x=300, y=500)
        self.volume_button.bind("<Enter>", self.on_enter_volume)
        self.volume_button.bind("<Leave>", self.on_leave_volume)

        # Initialize mute state
        self.is_muted = False

        # Volume scale
        self.scale = Scale(self.root, from_=0, to=100, bg='Magenta', troughcolor='Black', orient=HORIZONTAL, length=120, sliderrelief='solid')
        self.scale.set(25)
        self.scale.place(x=350, y=503)

        # Label for status
        self.status_label = Label(self.root, text='Ready', bg='Black', fg='white', font=20)
        self.status_label.pack(side=BOTTOM, fill=X)

        # Stop maximizing
        self.root.resizable(False, False)

        # Bind volume scale
        self.scale.bind("<ButtonRelease-1>", self.set_volume)

        # Update timer
        self.update_timer()

    def open_file(self):
        self.filename = filedialog.askopenfilename()
        self.length_bar()
        self.songinf()

    def length_bar(self):
        if self.filename:
            song_mut = MP3(self.filename)
            song_mut_length = song_mut.info.length
            convert_song_mut_length = time.strftime('%M:%S', time.gmtime(song_mut_length))
            self.lengthlabel.config(text=f'Total Length: 00:{convert_song_mut_length}')

    def set_volume(self, event):
        volume = self.scale.get() / 100
        pygame.mixer.music.set_volume(volume)

    def songinf(self):
        if self.filename:
            self.filelabel['text'] = 'Current Music: ' + os.path.basename(self.filename)

    def play_music(self):
        if self.filename:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(self.filename)
                if not self.is_muted:
                    volume = self.scale.get() / 100
                    pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play()
                self.start_time = time.time()  # Start time for timer
                self.status_label.config(text='Music Playing...')
                self.songinf()
            elif self.paused:
                self.start_time = time.time() - self.get_playback_position()
                pygame.mixer.music.unpause()
                self.paused = False
                self.status_label.config(text='Unpaused...')
            else:
                tkinter.messagebox.showerror('Error', 'Music is already playing.')
        else:
            tkinter.messagebox.showerror('Error', 'Please select a file first.')

    def get_playback_position(self):
        if pygame.mixer.music.get_busy():
            return pygame.mixer.music.get_pos() / 1000  # Convert milliseconds to seconds
        else:
            return 0


    def pause_music(self):
        if pygame.mixer.music.get_busy() and not self.paused:
            pygame.mixer.music.pause()
            self.paused = True
            self.status_label.config(text='Music Paused')

    def stop_music(self):
        pygame.mixer.music.stop()
        self.status_label.config(text='Music Stopped')
        self.paused = False

    def toggle_mute(self):
        if self.is_muted:
            volume = self.scale.get() / 100
            pygame.mixer.music.set_volume(volume)
            self.volume_button.config(image=self.photo_B4_volume)
            self.is_muted = False
        else:
            self.muted_volume = pygame.mixer.music.get_volume()
            pygame.mixer.music.set_volume(0)
            self.volume_button.config(image=self.photo_B4_mute)
            self.is_muted = True

    def on_enter_volume(self, event):
        if not self.is_muted:
            self.volume_button.config(image=self.photo_B4_mute)

    def on_leave_volume(self, event):
        if not self.is_muted:
            self.volume_button.config(image=self.photo_B4_volume)

    def about(self):
        tkinter.messagebox.showinfo('About Us', 'BeatBoxr created by Jan Mohammad')

    def update_timer(self):
        if pygame.mixer.music.get_busy() and not self.paused and self.start_time:
            elapsed_time = time.time() - self.start_time
            convert_elapsed_time = time.strftime('%M:%S', time.gmtime(elapsed_time))
            self.timelabel.config(text=convert_elapsed_time)
        self.root.after(1000, self.update_timer)

root = Tk()
obj = SongPlayer(root)
root.mainloop()
