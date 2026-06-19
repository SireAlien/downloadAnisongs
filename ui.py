import fetchSongs as fs
from tkinter import Tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import IntVar
from threading import Thread

root = Tk()
root.geometry('800x600')
root.title('Download AniSongs')

def onSelectDirectoryChangeButtonText(directoryButton):
    directory = filedialog.askdirectory()
    if directory:
        directoryButton.config(text=directory)
        toggleLoadButtonState()

def downloadMp3FromLink_Thread(link, path = "./"):
    Thread(target=lambda: fs.downloadMp3FromLink(link, path)).start()

def onLoadButtonClick( ):
    Thread(target=onLoadButtonClick_Thread).start()

def toggleLoadButtonState():
    if op.get() == 1 or ed.get() == 1 or ins.get() == 1:
        if filedialogButton.cget("text") != "Browse":
            loadButton.config(state = "normal")
    else:
        loadButton.config(state = "disabled")

def onLoadButtonClick_Thread( ):
    for widget in gridFrame.grid_slaves():
        widget.destroy()
    for widget in pagingFrame.grid_slaves():
        widget.destroy()

    title = titleEntry.get()
    language = f"anime{languageCombo.get()}Name"
    song_types = []
    if op.get() == 1:
        song_types.append("Opening")
    if ed.get() == 1:
        song_types.append("Ending")
    if ins.get() == 1:
        song_types.append("Insert")

    if not title:
        messagebox.showerror("Error", "Please enter an anime title.")
        return

    loadingMessage = ttk.Label(gridFrame, text = "Loading...")
    loadingMessage.grid(column = 0, row = 0)

    songs = fs.getMp3ListFromSongList(fs.getSongsFromTitle_SongTypes(title, song_types), language)
    songRecords = []
    #create a grid row for each song with a download button
    for i, song in enumerate(songs):
        songRecords.append({
            "title": ttk.Label(gridFrame, text = song["title"], wraplength=200),
            "name": ttk.Label(gridFrame, text = song["name"], wraplength=200),
            "type": ttk.Label(gridFrame, text = song["type"]),
            "downloadButton": ttk.Button(gridFrame, text = "Download", command = lambda link=song: downloadMp3FromLink_Thread(link, filedialogButton.cget("text")))
        })

    loadingMessage.destroy()

    #create buttons to cycle between pages of results if there are more than 10 songs
    prevButton = ttk.Button(pagingFrame, text = "<<", state = "disabled")
    nextButton = ttk.Button(pagingFrame, text = ">>", state = "disabled")
    pageIndex = ttk.Label(pagingFrame, text = "Page 1")

    onNextPageButtonClick(songRecords, 0, prevButton, nextButton, pageIndex)
    if len(songRecords) > 10:
        prevButton.config(command = lambda: onPrevPageButtonClick(songRecords, 0, prevButton, nextButton, pageIndex))
        nextButton.config(command = lambda: onNextPageButtonClick(songRecords, 10, prevButton, nextButton, pageIndex))
        prevButton.grid(column = 0, row = 0)
        pageIndex.grid(column = 1, row = 0)
        nextButton.grid(column = 2, row = 0)

def onNextPageButtonClick(songRecords, index, prevButton, nextButton, pageIndex):
    for widget in gridFrame.grid_slaves():
        widget.grid_forget()
    for i, record in enumerate(songRecords[index:index+10]):
        record["title"].grid(column = 0, row = i, sticky = "w")
        record["name"].grid(column = 1, row = i, sticky = "w")
        record["type"].grid(column = 2, row = i)
        record["downloadButton"].grid(column = 3, row = i)
    pageIndex.config(text = f"Page {index//10 + 1}")
    if index >= 10:
        prevButton.config(state = "normal", command = lambda: onPrevPageButtonClick(songRecords, index-10, prevButton, nextButton, pageIndex))
    if index + 10 < len(songRecords):
        nextButton.config(state = "normal", command = lambda: onNextPageButtonClick(songRecords, index+10, prevButton, nextButton, pageIndex))
    else:
        nextButton.config(state = "disabled")

def onPrevPageButtonClick(songRecords, index, prevButton, nextButton, pageIndex):
    for widget in gridFrame.grid_slaves():
        widget.grid_forget()
    for i, record in enumerate(songRecords[index:index+10]):
        record["title"].grid(column = 0, row = i, sticky = "w")
        record["name"].grid(column = 1, row = i, sticky = "w")
        record["type"].grid(column = 2, row = i)
        record["downloadButton"].grid(column = 3, row = i)
    
    pageIndex.config(text = f"Page {index//10 + 1}")
    if index >= 10:
        prevButton.config(state = "normal", command = lambda: onPrevPageButtonClick(songRecords, index-10, prevButton, nextButton, pageIndex))
    else:
        prevButton.config(state = "disabled")

    if index + 10 < len(songRecords):
        nextButton.config(state = "normal", command = lambda: onNextPageButtonClick(songRecords, index+10, prevButton, nextButton, pageIndex))
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
ttk.Label(menuFrame, text = "Language:").grid(column = 0, row = 1)
languageCombo = ttk.Combobox(menuFrame, values=["JP", "EN"], state="readonly")
languageCombo.current(0)
languageCombo.grid(column = 1, row = 1)
ttk.Label(menuFrame, text = "Song Type:").grid(column = 0, row = 2)
songTypeFrame = ttk.Frame(menuFrame)
songTypeFrame.grid(column = 1, row = 2)
op = IntVar(value=0)
ed = IntVar(value=0)
ins = IntVar(value=0)
OPCheckButton = ttk.Checkbutton(songTypeFrame, text = "OP", command=toggleLoadButtonState, variable=op)
EDCheckButton = ttk.Checkbutton(songTypeFrame, text = "ED", command=toggleLoadButtonState, variable=ed)
INCheckButton = ttk.Checkbutton(songTypeFrame, text = "IN", command=toggleLoadButtonState, variable=ins)
OPCheckButton.grid(column = 0, row = 0, sticky="w")
EDCheckButton.grid(column = 1, row = 0)
INCheckButton.grid(column = 2, row = 0, sticky="e")
ttk.Label(menuFrame, text = "File path to save songs:").grid(column = 0, row = 3)
filedialogButton = ttk.Button(menuFrame, text = "Browse", command = lambda: onSelectDirectoryChangeButtonText(filedialogButton))
filedialogButton.grid(column = 1, row = 3)
loadButton = ttk.Button(menuFrame, text = "Load results", command = onLoadButtonClick, state="disabled")
loadButton.grid(column = 0, row = 4)


root.mainloop()   
