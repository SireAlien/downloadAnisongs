import fetchSongs as fs
from tkinter import Tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

root = Tk()
root.geometry('800x600')
root.title('Download AniSongs')

def onSelectDirectoryChangeButtonText(directoryButton):
    directory = filedialog.askdirectory()
    if directory:
        directoryButton.config(text=directory)

def onLoadButtonClick( ):
    for widget in gridFrame.grid_slaves():
        widget.destroy()
    for widget in pagingFrame.grid_slaves():
        widget.destroy()

    title = titleEntry.get()
    language = f"anime{languageCombo.get()}Name"
    song_type = fs.songTypes[songTypeCombo.get()]
    if not title:
        messagebox.showerror("Error", "Please enter an anime title.")
        return

    songs = fs.getMp3ListFromSongList(fs.getSongsFromTitle_SongType(title, song_type), language)
    songRecords = []
    #create a grid row for each song with a download button
    for i, song in enumerate(songs):
        songRecords.append({
            "title": ttk.Label(gridFrame, text = song["title"], wraplength=200),
            "name": ttk.Label(gridFrame, text = song["name"], wraplength=200),
            "type": ttk.Label(gridFrame, text = song["type"]),
            "downloadButton": ttk.Button(gridFrame, text = "Download", command = lambda link=song: fs.downloadMp3FromLink(link, filedialogButton.cget("text")))
        })

    #create buttons to cycle between pages of results if there are more than 10 songs
    prevButton = ttk.Button(pagingFrame, text = "<<", state = "disabled")
    nextButton = ttk.Button(pagingFrame, text = ">>", state = "disabled")

    onNextPageButtonClick(songRecords, 0, prevButton, nextButton)
    if len(songRecords) > 10:
        prevButton.config(command = lambda: onPrevPageButtonClick(songRecords, 0, prevButton, nextButton))
        nextButton.config(command = lambda: onNextPageButtonClick(songRecords, 10, prevButton, nextButton))
        prevButton.grid(column = 0, row = 0)
        nextButton.grid(column = 1, row = 0)

def onNextPageButtonClick(songRecords, index, prevButton, nextButton):
    for widget in gridFrame.grid_slaves():
        widget.grid_forget()
    for i, record in enumerate(songRecords[index:index+10]):
        record["title"].grid(column = 0, row = i, sticky = "w")
        record["name"].grid(column = 1, row = i, sticky = "w")
        record["type"].grid(column = 2, row = i)
        record["downloadButton"].grid(column = 3, row = i)

    if index >= 10:
        prevButton.config(state = "normal", command = lambda: onPrevPageButtonClick(songRecords, index-10, prevButton, nextButton))
    if index + 10 < len(songRecords):
        nextButton.config(state = "normal", command = lambda: onNextPageButtonClick(songRecords, index+10, prevButton, nextButton))
    else:
        nextButton.config(state = "disabled")

def onPrevPageButtonClick(songRecords, index, prevButton, nextButton):
    for widget in gridFrame.grid_slaves():
        widget.grid_forget()
    for i, record in enumerate(songRecords[index:index+10]):
        record["title"].grid(column = 0, row = i, sticky = "w")
        record["name"].grid(column = 1, row = i, sticky = "w")
        record["type"].grid(column = 2, row = i)
        record["downloadButton"].grid(column = 3, row = i)
    
    if index >= 10:
        prevButton.config(state = "normal", command = lambda: onPrevPageButtonClick(songRecords, index-10, prevButton, nextButton))
    else:
        prevButton.config(state = "disabled")

    if index + 10 < len(songRecords):
        nextButton.config(state = "normal", command = lambda: onNextPageButtonClick(songRecords, index+10, prevButton, nextButton))
    else:
        nextButton.config(state = "disabled")



menuFrame = ttk.Frame(root)
gridFrame = ttk.Frame(root)
gridFrame.grid_columnconfigure(0, pad=10, minsize=200)
gridFrame.grid_columnconfigure(1, pad=10, minsize=200)
gridFrame.grid_columnconfigure(2, pad=5)
pagingFrame = ttk.Frame(root)
menuFrame.grid(column = 0, row = 0, sticky = "nw")
gridFrame.grid(column = 0, row = 1, sticky = "w")
pagingFrame.grid(column = 0, row = 2, sticky = "sw")
ttk.Label(menuFrame, text = "Query:").grid(column = 0, row = 0)
titleEntry = ttk.Entry(menuFrame, width = 30)
titleEntry.grid(column = 1, row = 0)
ttk.Label(menuFrame, text = "Language:").grid(column = 0, row = 3)
languageCombo = ttk.Combobox(menuFrame, values=["JP", "EN"], state="readonly")
languageCombo.current(0)
languageCombo.grid(column = 1, row = 3)
ttk.Label(menuFrame, text = "Song Type:").grid(column = 0, row = 4)
songTypeCombo = ttk.Combobox(menuFrame, values=["ALL", "OP", "ED", "IN"], state="readonly")
songTypeCombo.current(0)
songTypeCombo.grid(column = 1, row = 4)
ttk.Label(menuFrame, text = "File path to save songs:").grid(column = 0, row = 5)
filedialogButton = ttk.Button(menuFrame, text = "Browse", command = lambda: onSelectDirectoryChangeButtonText(filedialogButton))
filedialogButton.grid(column = 1, row = 5)
loadButton = ttk.Button(menuFrame, text = "Load results", command = onLoadButtonClick)
loadButton.grid(column = 0, row = 6)
loadButton = ttk.Label(menuFrame, text = "")


root.mainloop()   
