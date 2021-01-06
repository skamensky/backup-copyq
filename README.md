# Why
To preseve the history of [copyq](https://github.com/hluk/CopyQ/) items in a searchable manner
See [this issue](https://github.com/hluk/CopyQ/issues/1144) for why this is necessary instead of providing an upstream fix
# What
A simple script that uses the copyq scripting API to export all text item (**this only exports _text/plain_ mimetypes!**)

# Setup
Assuming `PATH_TO_FOLDER_CONTAINING_SCRIPT` is the directory containing this script
- Create a virtual environment named `venv` in `PATH_TO_FOLDER_CONTAINING_SCRIPT` (you can do that by running this command: `python3 -m venv venv`)
- Add `*/5 * * * * bash PATH_TO_FOLDER_CONTAINING_SCRIPT/copyqclipboard/backup.sh` to your crontab (this will work on macOS or linux, windows users, you'll have to use wsl2 😛)
- Add this function to your `.bashrc` (enabling you to run `search_clip "search query"` from anywhere to search your history)
    ```bash
    function search_clip(){
      python -c "import sys;sys.path.insert(0,'PATH_TO_FOLDER_CONTAINING_SCRIPT');from refresh_backup import search as s;s('$1')"
    }
    ```
- Ensure that CopyQ is installed here `/Applications/CopyQ.app/Contents/MacOS/CopyQ ` (that's where it was installed for me)