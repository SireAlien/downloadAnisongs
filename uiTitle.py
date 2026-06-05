import fetchSongs as fs
from tkinter import Tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

root = Tk()
root.geometry('500x300')
root.title('Download AniSongs')


def onSelectDirectoryChangeButtonText(directoryButton):
    directory = filedialog.askdirectory()
    if directory:
        directoryButton.config(text=directory)

def onLoadButtonClick( ):
    for widget in gridFrame.grid_slaves():
        if int(widget.grid_info()["row"]):
            widget.destroy()

    title = titleEntry.get()
    language = f"anime{languageCombo.get()}Name"

    if not title:
        messagebox.showerror("Error", "Please enter an anime title.")
        return

    songs = fs.getMp3ListFromSongList(fs.getSongListFromTitle(title), language)
    
    #create a grid row for each song with a download button
    for i, song in enumerate(songs):
        ttk.Label(gridFrame, text = song["title"]).grid(column = 0, row = i)
        ttk.Label(gridFrame, text = song["name"]).grid(column = 1, row = i)
        ttk.Label(gridFrame, text = song["type"]).grid(column = 2, row = i)
        downloadButton = ttk.Button(gridFrame, text = "Download", command = lambda link=song: fs.downloadMp3FromLink(link, filedialogButton.cget("text")))
        downloadButton.grid(column = 3, row = i)

menuFrame = ttk.Frame(root)
gridFrame = ttk.Frame(root)
menuFrame.grid(column = 0, row = 0)
gridFrame.grid(column = 0, row = 1)
ttk.Label(menuFrame, text = "Query:").grid(column = 0, row = 0)
titleEntry = ttk.Entry(menuFrame, width = 30)
titleEntry.grid(column = 1, row = 0)
ttk.Label(menuFrame, text = "Language:").grid(column = 0, row = 3)
languageCombo = ttk.Combobox(menuFrame, values=["JP", "EN"], state="readonly")
languageCombo.current(0)
languageCombo.grid(column = 1, row = 3)
ttk.Label(menuFrame, text = "File path to save songs:").grid(column = 0, row = 4)
filedialogButton = ttk.Button(menuFrame, text = "Browse", command = lambda: onSelectDirectoryChangeButtonText(filedialogButton))
filedialogButton.grid(column = 1, row = 4)
loadButton = ttk.Button(menuFrame, text = "Load results", command = onLoadButtonClick)
loadButton.grid(column = 0, row = 5)
loadButton = ttk.Label(menuFrame, text = "")


root.mainloop()   