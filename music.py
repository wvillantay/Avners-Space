from tkinter import *
from tkinter import Tk
from tkinter import filedialog
import pygame
from pygame import mixer
import os 

root = Tk()
#Title of the Window created
root.title('Music player')
#creates the size of the window
root.geometry("500x300")
#window backgroung color


root.resizable(False, False)
mixer.init()

menubar = Menu(root)
root.config(menu=menubar)

songs = []
current_song = ""
pause = False

def load_music():
    global current_song
    root.directory = filedialog.askdirectory()
    
    for song in os.listdir(root.directory):
        name, ext = os.path.splitext(song)
        if ext == '.mp3':
            songs.append(song)
    
    for song in songs:
        songs.insert("End", song)
    
    songlist.selection_set(0)
    current_song = songs[songlist.curselection()[0]]


def play_music():
    global current_song, paused

    if not paused:
        pygame.mixer.music.load(os.path.join(root.directory, current_song))
        pygame.mixer.play()
    else:
        pygame.mixer.unpause()
        paused = False
    

def pause_music():
    global pause
    pygame.mixer.music.pause()
    pause = True

def next_music():
    global current_song, paused
    try:
        songlist.select_clear(0, END)
        songlist.selection_set(songs.index(current_song)+ 1)
        current_song = songs(songlist.curselection()[0])
        play_music()
    except:
        pass

def previous_music():
    global current_song, paused
    try:
        songlist.select_clear(0, END)
        songlist.selection_set(songs.index(current_song) - 1)
        current_song = songs(songlist.curselection()[0])
        play_music()
    except:
        pass

orginize_menu = Menu(menubar, tearoff=False)
orginize_menu.add_command(label='Music Folder',command=load_music)
menubar.add_cascade(label='Music', menu= orginize_menu)

songlist = Listbox(root, bg="black", fg="white", width=100, height=15)
songlist.pack()

play_btn_image = PhotoImage(file='play.png')
pause_btn_image = PhotoImage(file='pause.png')
next_btn_image = PhotoImage(file='next.png')
prev_btn_image = PhotoImage(file='previous.png')

frame = Frame(root)
frame.pack()

#Adding interactive buttons
play_btn = Button(frame, image=play_btn_image, borderwidth=0, command= play_music)
pause_btn = Button(frame, image=pause_btn_image, borderwidth=0, command= pause_music)
next_btn = Button(frame, image= next_btn_image, borderwidth=0, command= next_music)
prev_btn = Button(frame, image= prev_btn_image, borderwidth=0, command= previous_music)

play_btn.grid(row=0, column=1,padx=7,pady=10)
pause_btn.grid(row=0, column=2,padx=7,pady=10)
next_btn.grid(row=0, column=3,padx=7,pady=10)
prev_btn.grid(row=0, column=0,padx=7,pady=10)

mainloop()
