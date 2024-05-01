import customtkinter, os, pygame, time, random
from tkinter import *
from tkinter import filedialog as fd
from mutagen.mp3 import MP3

# Set the theme and color options.
customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme('blue')

# -------------- Variables Section -------------- #
# Variable needed to be global.
global songbox_songs, paused, new_song, shuffle, \
    repeat, stopped, click_time, song_playing_index,\
    last_song_played_indx

songbox_songs = []
paused = False 
new_song = False
shuffle = False
repeat = False
stopped = False
click_time = 0
song_playing_index = ''
last_song_played_indx = song_playing_index

# Colors
font_clr = "#E2F1FF"
pannels_bg_clr = "#333333"
song_highlight = "#2F3545"
playlist_bg_clr = "#212930"
main_bg_clr = "#252525"
prog_clr = "#87BEF1"
font_name = "Bahnschrift Light"

# MP3 player main info
main = customtkinter.CTk(fg_color=(main_bg_clr))
main.title("Music media player")
main.geometry("800x550")
main.resizable(False, False)

# Initializing pygame mixer
pygame.mixer.init()

# Images
song_display = PhotoImage(file="images/dvd.png")
now_palying = PhotoImage(file="images/now_playing.png")
volume_img = PhotoImage(file="images/volume.png")
repeat_img = PhotoImage(file="images/repeat.png")
shuffle_img = PhotoImage(file="images/shuffle.png")

prev_img = PhotoImage(file="images/prev_img.png")
pause_img = PhotoImage(file="images/pause_img.png")
play_img = PhotoImage(file="images/play_img.png")
stop_img = PhotoImage(file="images/stop_img.png")
next_img = PhotoImage(file="images/next_img.png")

add_song_img = PhotoImage(file="images/add_song.png")
remove_song_img = PhotoImage(file="images/remove_song.png")
# -------------- Variables Section End -------------- #


# -------------- Functionalities Section -------------- #
def select_to_play(song):
    """Return the path of selected song."""

    # Loop through 'songbox_song' list.
    for evr_song in songbox_songs:
        song_name = os.path.basename(evr_song)
        # Find the complete file path of selected song.
        if song_name == f'{song}.mp3':
            return evr_song


def add_song():
    """To add a song to the playlist."""

    # Open file explorer for user to choose songs, store 
    songs = fd.askopenfilenames(initialdir="musics/",
                                title="Choose Songs",
                                filetypes=(("mp3 Files", "*.mp3"), ))
    # Loop through 'songs'.
    for song in songs:
        # Check if song is already added.
        # Not allowing user to add same song multiple times
        if song not in songbox_songs: 
            # Store each song (file path) in a list 'songbocx_songs'
            songbox_songs.append(song)
            # Get the basename (title) of the file path and remove '.mp3'.
            filename = os.path.basename(song)
            songname = filename.replace(".mp3", "")
            # Insert the extracted song title into the list box (songbox or playlist).
            songbox.insert(END, songname)
    if songs:
        songbox.select_set(0)


def remove_song():
    """Function that can remove song from the playlist when the 'remove' button is clicked."""

    # Get the current selected song in list box (songbox or playlist).
    current_selec = songbox.curselection()
    # Check if the user selected a song to delete.
    if current_selec != ():
        # Get the file path of the selected song.
        selected_song_fp = select_to_play(songbox.get(current_selec))
        # Remove the file path in the 'songbox_songs' (list).
        songbox_songs.remove(selected_song_fp)
        # Remove the selected song from listbox (songbox or playlist).
        songbox.delete(current_selec)
        # Stop the selected song if it is currently playing.
        stop()


def play():
    """Play the selected song when 'play' is clicked."""

    global click_time, new_song, paused, stopped

    # Check if user added a song.
    if songbox_songs != []:
        # If user already added songs, check if 'pause' is clicked.
        if paused:
            # If clicked, click it again.
            # This is for 'play' btn to be use as unpause btn.
            pause()
        else:
            if stopped:
                pass
            # To end the last recursion of 'play_time' function.
            else:
                click_time += 1
            # Get the active song from listbox (songbox or playlist).
            # By default ACTIVE song is index 0 or the first song in the playlist.
            seleted_song = songbox.get(ACTIVE)
            # Get the currently selected song in the listbox (songbox or playlist).
            selected_song = songbox.curselection()
            # If there is NO selected song the first song will automatically get selected (highlighted).
            if selected_song == ():
                songbox.select_set(0)
            # Get the file path of the ACTIVE song.
            song_to_play = select_to_play(seleted_song)
            # Play the song tha is ACTIVE.
            play_song(song_to_play)



def play_song(song):
    """"Playing the song."""

    global song_playing_index, stopped, last_song_played_indx
    
    try:
        # Playing the song using 'Pygame' mixer.
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)

        # Setting the timer back to 00:00 min and sec.
        time_one.configure(text="00:00")
        time_two.configure(text="00:00")
        # Check if the 'last_song_played_indx' is default or not
        if last_song_played_indx != '':
            # If NOT DEFAULT ('') set it to the currently playing.
            last_song_played_indx = song_playing_index
        else:
            # If DEFAULT set it to 0 (index of the first song in the playlist).
            last_song_played_indx = 0
        # Setting the index of the song currently playing.
        song_playing_index = songbox_songs.index(song)
        # Setting the lenght of slider equal to audio's length.
        get_song_lenght()
        slider_pos = current_song_length
        song_prog_slider.configure(to=slider_pos)
        # Setting the slider back to zero value position.
        song_prog_slider.set(0)
        # Setting the now playing song text to what is currently playing.
        currently_playing.delete(0, END)
        to_display_path = os.path.basename(song)
        to_display = to_display_path.replace(".mp3", "")
        currently_playing.insert(END, to_display)
        # Setting 'stopped' to FALSE.
        stopped = False
        # Calling the 'play_time()'.
        play_time()
    except:
        return


def pause():
    """Puase and Unpause the current playing song when 'pause' btn is clicked."""

    global paused, song_playing_index

    # Check if there's a song to pause.
    if song_playing_index != '':
        if paused:
            # If paused, unpaused
            pygame.mixer.music.unpause()
            paused = False
        else:
            pygame.mixer.music.pause()
            paused = True


def stop():
    """Stop the song currently playing when the 'stop' btn is clicked"""
    global stopped, click_time, song_playing_index

    # Setting the 'stopped' to TRUE to indicate that a song is stopped in playing.
    stopped = True
    # Setting back 'song_playing_index' to 0.
    song_playing_index = 0
    # Remove the title of the song from the 'currently_playing' llstbox.
    currently_playing.delete(0, END)
    currently_playing.insert(END, 'Please select a song.')
    # Stop the playing music using Pygame music mixer.
    pygame.mixer.music.stop()
    # Clear the hightlight of the the currently seleted song from the listbox (songbox or playlist).
    songbox.selection_clear(0, END)
    # Activate the first song in the listbox (songbox or playlist).
    songbox.activate(0)
    songbox.select_set(0)
    # Setting back the song slider back to zero. 
    song_prog_slider.set(0)
    # Setting the both timer back to default.
    time_one.configure(text="00:00")
    time_two.configure(text="00:00")

    click_time = 1


def shuffle_song():
    """Turn on/off the shuffle function, when the 'shuffle' btn is clicked."""

    global shuffle

    # Check or uncheck the checkbox for shuffle function
    shu_checkbox_event()
    # Check if the 'shuffle' btn is already cliked or not.
    if shuffle:
        shuffle = False
    else:
        shuffle = True
    

def get_random_num(value):
    """Return random number (index of song) for the shuffle function."""

    last_num = value
    # Loop to make sure the random number that will be generated is not equal to the currently pkaying.
    while True:
        # Get random number using the 'randint' function from 'random' module.
        number = random.randint(0, len(songbox_songs)-1)
        # Check if the 'number' (random number) is not equal to index of the last song playing.
        if number == last_num:
            continue
        else:
            return number


def repeat_song():
    """Turn on/off the repeat function, when the 'shuffle' btn is clicked."""
    global repeat

    # Check or uncheck the checkbox for repeat function
    rep_checkbox_event()
    # Check if the 'repeat' btn is already cliked or not.
    if repeat:
        repeat = False
    else:
        repeat = True


def previous():
    """Function for playing the last song played."""

    global click_time, new_song, song_playing_index

    try:
        # Check if the 'song_playing_index' is same as the 'last_song_played_indx'.
        if last_song_played_indx != song_playing_index: # If NOT set use the 'last_song_played_indx' to play the previous song.
            # Set 'pre_song_index' to equal to 'last_song_played_indx'.
            pre_song_index = last_song_played_indx
            # Remove any highlight from the listbox of songs (PLAYLIST).
            songbox.selection_clear(0, END)
            # Activate and hightlight the previous song.
            songbox.activate(pre_song_index)
            songbox.selection_set(pre_song_index, last=None)
            # Play the previous song.
            play()
        else: # If YES play the index 0 (first song from the playlist).
            # Remove any highlight from the listbox of songs (PLAYLIST).
            songbox.selection_clear(0, END)
            # Activate and hightlight the index 0 (first song from the playlist).
            songbox.activate(0)
            songbox.selection_set(0, last=None)
            play()
    except:
        play()


def next_song():
    """Function for playing the last song played."""

    global next_click_time, new_song, song_playing_index, stopped

    # Catching an error if the user hasn't added any song or not played any song. 
    try:
        # Check if 'song_playing_index' is equal to the last song in the playlist.
        if song_playing_index != songbox.index(END)-1 and stopped == False:
            # If NOT, find and play the next song.
            if shuffle:
                ran_num = get_random_num(song_playing_index)
                
                next_song_index = ran_num
            else:
                next_song_index = song_playing_index+1

            songbox.selection_clear(0, END)
            songbox.activate(next_song_index)
            songbox.selection_set(next_song_index, last=None)
            play()
        elif song_playing_index == songbox.index(END)-1 or stopped:
            songbox.selection_clear(0, END)
            # If YES just play the first song in the playist, if the shuffle is off.
            if shuffle:
                # If shuffle is ON, get random number and play a random song.
                ran_num = get_random_num(0)
                # Activate and highlight the random song.
                songbox.activate(ran_num)
                songbox.selection_set(ran_num, last=None)
            else:
                # If shuffle is OFF, play the last song in the playlist.
                # Activate and highlight the random song.
                songbox.selection_clear(0, END)
                songbox.activate(0)
                songbox.selection_set(0, last=None)
            play()
    except:
        # Catching an error if the user hasn't added any song or not played any song. 
        play()


def play_time():
    """Updating the slider (song_prog_slider) and the timer every second."""

    global stopped, new_song, click_time, next_click_time

    # Check if the song is stop.
    if stopped:
        return
    else:
        # Get song's current time in second.
        current_time = pygame.mixer.music.get_pos() / 1000
        if current_time <= 1:
            current_time += 2
        # Convert song's current time to a formated time.
        min_sec_time_format = time.strftime('%M:%S', time.gmtime(current_time))
        # Check if song's current time is equal to song's length (end of the song).
        if int(song_prog_slider.get()) == int(current_song_length):
            # To display that the song's current time is equal to the song's length.
            min_sec_time_format = time.strftime('%M:%S', time.gmtime(int(song_prog_slider.get())))
            time_one.configure(text=min_sec_time_format)
            # If repeat is ON, call 'play()' to play the song again.
            if repeat:
                play()
            # If OFF, play the next song.
            else:
                next_song()
        # Check if song is pause, if YES do nothing.
        elif paused:
            pass
        # Setting the position of the slider equal to the song's current position.
        else:
            # If slider is update by the user set the slider's position equal to updated position.
            song_prog_slider.set(int(song_prog_slider.get()))
            # Update the time progress to the slider position.
            min_sec_time_format = time.strftime('%M:%S', time.gmtime(int(song_prog_slider.get())))
            time_one.configure(text=min_sec_time_format)
            # To update the next time for slider and the song's progress time by one.
            next_time = int(song_prog_slider.get()) + 1
            song_prog_slider.set(next_time)

        # # Check if new song, to stop the present recursion of 'play_time' function.
        if click_time >= 2:
            click_time = 1
            return
        else:
            # If it isn't a song call the play_time function for recursion, this is done every second.
            time_one.after(1000, play_time)



def forward(value):
    """Start the song according to the position of the slider."""
    # Triggered when the slider's position is updated manually by the user. 

    # The 'value' is the return value of the slider when moved (slider's position).

    # Catching a Pygame error if the slider is moved and no song is playing or load.
    try:
        # Get the slider's new position.
        forwarded_pos = value
        # Start the song where slider's new position is using Pygame's mixer.
        pygame.mixer_music.play(start=forwarded_pos)
    except:
        # Error is triggered, do nothing.
        return

  
def get_song_lenght():
    """Get the song's length and set is to 'current_song_length'."""
    
    global current_song_length

    # Get the title of the song what to get the length
    song_title = songbox.get(ACTIVE)
    # Get the song's file path.
    current_song = select_to_play(song_title)
    # Use the MP3 function from mutagen module to get its info.
    song_mut = MP3(current_song)
    # Get the length of the song.
    current_song_length = song_mut.info.length
    # Display the total length of the song in proper format.
    min_sec_length = time.strftime('%M:%S', time.gmtime(current_song_length))
    time_two.configure(text=min_sec_length)


def adjust_volume(value):
    """Function to adjust the volume using pygame's mixer."""

    # The 'value' is the return value of the slider when moved (slider's position).
    pygame.mixer.music.set_volume(value)


def shu_checkbox_event():
    """Function for checking and uncheking the shuffle's checkbox."""
    if shuf_check_var.get() == 0:
        shuf_checkbox.configure(state="normal")
        shuf_checkbox.select()
        shuf_checkbox.configure(state="disable")
        shuf_check_var.set(1)
    else:
        shuf_checkbox.configure(state="normal")
        shuf_checkbox.deselect()
        shuf_checkbox.configure(state="disable")
        shuf_check_var.set(0)


def rep_checkbox_event():
    """Function for checking and uncheking the repeat's checkbox."""
    if rep_check_var.get() == 0:
        rep_checkbox.configure(state="normal")
        rep_checkbox.select()
        rep_checkbox.configure(state="disable")
        rep_check_var.set(1)
    else:
        rep_checkbox.configure(state="normal")
        rep_checkbox.deselect()
        rep_checkbox.configure(state="disable")
        rep_check_var.set(0)
# -------------- Functionalities Section End -------------- #


# -------------- Widgets Section -------------- #
# Main frame for the left side of the song GUI.
main_frame_1 = customtkinter.CTkFrame(main,
                                      fg_color="transparent")
main_frame_1.pack(side=LEFT, expand=True, fill=BOTH, pady=8, padx=8)

# Frame for the upper part of the left side.
playing_top_frame = customtkinter.CTkFrame(main_frame_1,
                                           fg_color=pannels_bg_clr,
                                           border_width=1,
                                           border_color=prog_clr)
playing_top_frame.pack(expand=True, fill=BOTH, pady=(0, 8))

# Left side frame inside the 'playing_top_frame'.
song_playing_frame = customtkinter.CTkFrame(playing_top_frame,
                                            fg_color="transparent")
song_playing_frame.pack(side=LEFT, pady=2, padx=(2, 0), expand=True, fill=BOTH)

# Frame inside 'song_playing_frame' to easily align the content inside.
song_playing_frame_2 = customtkinter.CTkFrame(song_playing_frame,
                                            fg_color="transparent")
song_playing_frame_2.pack(expand=True)

# Frame for 'Now now_playing_text' label.
now_playing_frame = customtkinter.CTkFrame(song_playing_frame_2,
                                           fg_color="transparent")
now_playing_frame.pack(fill=X, padx=(48, 0), pady=(0, 12))
# Now playing label.
now_playing_text = Label(now_playing_frame,
                         text="",
                         image=now_palying,
                         bg=pannels_bg_clr)
now_playing_text.pack(fill=BOTH)

# Frame for the rectangular dvd.
dvd_frame = customtkinter.CTkFrame(song_playing_frame_2,
                                   fg_color="transparent")
dvd_frame.pack(fill=X, padx=(48, 0), pady=(0, 8))
# The rectangular dvd.
song_display_label = Label(dvd_frame,
                           text="",
                           image=song_display,
                           bg=pannels_bg_clr)
song_display_label.pack(fill=BOTH)

# Frame for the shuffle, repeat, and the listbox for displaying the currently playing song. 
rep_shuf_frame = customtkinter.CTkFrame(song_playing_frame_2,
                                        fg_color="transparent")
rep_shuf_frame.pack(fill=X, padx=(48, 0), pady=(12, 16))
# Suffle btn.
shuffle_btn = Button(rep_shuf_frame,
                      image=shuffle_img,
                      borderwidth=0,
                      bg=pannels_bg_clr,
                      activebackground=pannels_bg_clr,
                      command=shuffle_song)

shuffle_btn.pack(side=LEFT, expand=True, padx=(70, 0))
# Suffle btn checkbox.
shuf_check_var = customtkinter.IntVar()
shuf_checkbox = customtkinter.CTkCheckBox(rep_shuf_frame, text="", command=shu_checkbox_event,
                                     variable=shuf_check_var, onvalue="1", offvalue="0",
                                     checkbox_height=10, checkbox_width=10, bg_color=pannels_bg_clr,
                                     width=0, fg_color="#333333", border_color="#333333")
shuf_checkbox.pack(side=LEFT)
# Listbox for displaying the currently playing song. 
currently_playing = Listbox(rep_shuf_frame,
                            bg=pannels_bg_clr,
                            fg=font_clr,
                            font=(font_name, 12),
                            width=24,
                            height=1,
                            borderwidth=0,
                            highlightthickness=0,
                            activestyle="none",
                            relief=FLAT,
                            selectbackground=pannels_bg_clr,
                            selectforeground=font_clr, 
                            justify=CENTER)
currently_playing.pack(side=LEFT, expand=True, padx=40)
currently_playing.insert(END, 'Please select a song.')
# Repeat btn.
repeat_btn = Button(rep_shuf_frame,
                      image=repeat_img,
                      borderwidth=0,
                      bg=pannels_bg_clr,
                      activebackground=pannels_bg_clr,
                      command=repeat_song)
repeat_btn.pack(side=LEFT, expand=True)
# Repeat btn checkbox.
rep_check_var = customtkinter.IntVar()
rep_checkbox = customtkinter.CTkCheckBox(rep_shuf_frame, text="", command=rep_checkbox_event,
                                     variable=rep_check_var, onvalue="1", offvalue="0",
                                     checkbox_height=10, checkbox_width=10, bg_color=pannels_bg_clr,
                                     width=0, fg_color="#333333", border_color="#333333")
rep_checkbox.pack(side=LEFT, padx=(0, 40))

# Frame for the song_prog_slider_frame, time_frame_one, and time_frame_two.
song_progress_frame = customtkinter.CTkFrame(song_playing_frame_2,
                                             fg_color="transparent",
                                             height=16) 
song_progress_frame.pack(fill=X, padx=(80, 32))

# Frame for the how long the song is been playing. 
time_frame_one = customtkinter.CTkFrame(song_progress_frame,
                                    fg_color="transparent",
                                    height=16) 
time_frame_one.pack(side=LEFT)
# Time for how long the song is been playing. 
time_one = customtkinter.CTkLabel(time_frame_one,
                                  text="00:00",
                                  font=(font_name, 12),
                                  width=40)
time_one.pack(side=LEFT)

# Frame for the song's song_prog_slider.
song_prog_slider_frame = customtkinter.CTkFrame(song_progress_frame,
                                    fg_color="transparent",
                                    height=16) 
song_prog_slider_frame.pack(side=LEFT, expand=True, fill=X)
# Song slider so user can see how much of the song is played.
song_prog_slider = customtkinter.CTkSlider(song_prog_slider_frame, 
                                           from_=0, 
                                           to=100,
                                           height=20,
                                           width=240,
                                           progress_color=prog_clr,
                                           button_color=font_clr,
                                           hover=False,
                                           fg_color="#747474",
                                           command=forward)
song_prog_slider.pack(side=LEFT, expand=True, fill=X)
song_prog_slider.set(0)

# Frame for the how long the song is. 
time_frame_two = customtkinter.CTkFrame(song_progress_frame,
                                    fg_color="transparent",
                                    height=16) 
time_frame_two.pack(side=LEFT)
# Time for how long the song is going play. 
time_two = customtkinter.CTkLabel(time_frame_two, 
                                  text="00:00", 
                                  font=(font_name, 12),
                                  width=40)
time_two.pack(side=RIGHT)

# Right side frame inside the 'playing_top_frame' (frame for volume).
volume_frame = customtkinter.CTkFrame(playing_top_frame,
                                      fg_color="transparent")
                                      
volume_frame.pack(side=RIGHT, pady=2, padx=(0, 2), fill=Y)
# Volume icon.
volume_icon = Label(volume_frame,
                      image=volume_img,
                      bg=pannels_bg_clr,
                      activebackground=pannels_bg_clr)
volume_icon.pack(side=BOTTOM, padx=(0, 24), pady=(0, 28))
# Volume slider.
vol_slider = customtkinter.CTkSlider(volume_frame, 
                                     from_=0, 
                                     to=1,
                                     width=16,
                                     height=100,
                                     progress_color=prog_clr,
                                     button_color=font_clr,
                                     hover=False,
                                     fg_color="#747474",
                                     orientation="vertical",
                                     command=adjust_volume)
vol_slider.pack(side=BOTTOM, padx=(0, 24))
vol_slider.set(1)

# Control pannel first frame.
playing_bot_frame = customtkinter.CTkFrame(main_frame_1,
                                           fg_color=pannels_bg_clr,
                                           border_width=1, 
                                           border_color=prog_clr)
playing_bot_frame.pack(side=BOTTOM, fill=X)
# Frame inside 'playing_bot_frame' for easy alignment of the buttons.
playing_frame_btn = customtkinter.CTkFrame(playing_bot_frame,
                                           fg_color="transparent")
playing_frame_btn.pack(expand=True, pady=20)

# Buttons
previous_btn = Button(playing_frame_btn,
                      image=prev_img,
                      borderwidth=0,
                      bg=pannels_bg_clr,
                      activebackground=pannels_bg_clr,
                      command=previous)
previous_btn.pack(side=LEFT)

pause_btn = Button(playing_frame_btn,
                   image=pause_img,
                   borderwidth=0,
                   bg=pannels_bg_clr,
                   activebackground=pannels_bg_clr,
                   command=pause)
pause_btn.pack(side=LEFT)

play_btn = Button(playing_frame_btn,
                  image=play_img,
                  borderwidth=0,
                  bg=pannels_bg_clr,
                  activebackground=pannels_bg_clr,
                  command=play)
play_btn.pack(side=LEFT)

stop_btn = Button(playing_frame_btn,
                  image=stop_img,
                  borderwidth=0,
                  bg=pannels_bg_clr,
                  activebackground=pannels_bg_clr,
                  command=stop)
stop_btn.pack(side=LEFT)

next_btn = Button(playing_frame_btn,
                  image=next_img,
                  borderwidth=0,
                  bg=pannels_bg_clr,
                  activebackground=pannels_bg_clr,
                  command=next_song)
next_btn.pack(side=LEFT)

# Main frame for the playist in the right side.
main_frame_2 = customtkinter.CTkFrame(main,
                                      fg_color=playlist_bg_clr,
                                      border_width=1,
                                      border_color=prog_clr)
main_frame_2.pack(side=RIGHT, fill=BOTH, pady=8, padx=(0, 8))

# Top frame of the playlist main frame containing the 'PLAYLIST' (word), add song btn, and the remove song btn. 
playlist_top_frame = customtkinter.CTkFrame(main_frame_2,
                                            fg_color='transparent')
playlist_top_frame.pack(pady=(12, 0), padx=12, fill=X)
# 'PLAYLIST' text.
plalist_txt = customtkinter.CTkLabel(playlist_top_frame, 
                                     text="PLAYLIST",
                                     font=('Franklin Gothic Demi Cond', 18))
plalist_txt.pack(side=LEFT, padx=(0, 16), pady=(1,0))
# Add song btn
add_song_btn = Button(playlist_top_frame,
                      image=add_song_img,
                      borderwidth=0,
                      bg=playlist_bg_clr,
                      activebackground=playlist_bg_clr,
                      command=add_song)
add_song_btn.pack(side=LEFT, padx=(0, 8))
# Remove song btn
remove_song_btn = Button(playlist_top_frame,
                      image=remove_song_img,
                      borderwidth=0,
                      bg=playlist_bg_clr,
                      activebackground=playlist_bg_clr,
                      command=remove_song)
remove_song_btn.pack(side=LEFT)
# Buttom frame of the playlist main frame containing the 'playlist' listbox. 
playlist_bot_frame = customtkinter.CTkFrame(main_frame_2,
                                            fg_color='transparent')
playlist_bot_frame.pack(pady=(4, 8), padx=(12,4), fill=BOTH, expand=True)
# Playlist listbox.
songbox = Listbox(playlist_bot_frame,
                  bg=playlist_bg_clr,
                  fg=font_clr,
                  font=(font_name, 12),
                  selectbackground=song_highlight,
                  selectforeground=font_clr,
                  width=36,
                  borderwidth=0, 
                  highlightthickness=0,
                  activestyle="none",
                  relief=FLAT)

songbox.pack(side=LEFT, fill=BOTH, expand=True)
# Playlist scrollbar.
songbox_scrollbar = customtkinter.CTkScrollbar(playlist_bot_frame, 
                                               command=songbox.yview,
                                               hover=False,
                                               button_color="#505F6C",
                                               width=13)
songbox_scrollbar.pack(side=RIGHT, fill=Y)
# Playlist scrollbar command.
songbox.configure(yscrollcommand=songbox_scrollbar.set)
# -------------- Widgets Section End -------------- #

main.mainloop()