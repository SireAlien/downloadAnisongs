# downloadAnisongs
Interface to download anime songs.

## Dependencies 
* [mutagen](https://pypi.org/project/mutagen/)

---

## Usage
To use the graphical interface, launch ui.py.  

### Fields 
* Query: arguments for search, namely title, song name, artist, composer.
* Language: the name of the anime titles will be displayed in this language. Files will also be saved in this language.
* File path to save songs: self explainatory.

### Download
Press the *Download* button in the rightmost column corresponding to the song you want to download.

---

To use the terminal interface, laungh fetchSongs.py from the terminal.

### Fields (terminal)
* Query: arguments for search, namely title, song name, artist, composer.
* Song type: choose all results or filter by openings, endings, inserts. 
* File path to save songs: self explainatory.
* Language for filename: the name of the anime titles will be displayed in this language.

### Download
The terminal version of the program downloads every song resulting from the query.

--- 

## Notes
  Some of <https://anisongdb.com>'s features are disabled when [AMQ](https://animemusicquiz.com/) ranked takes place.  
  This might cause problems, so if you're having issues check on <https://anisongdb.com> if ranked is taking place.
