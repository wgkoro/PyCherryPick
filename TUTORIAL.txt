Requirement:
・Python 2.x
・BeautifulSoup.py (bundled)

Basic usage:
You can use this script via command-line.
$ python pycherrypick.py [target page's URL]

Example:
$ cd PyCherryPick/python
$ python pycherrypick.py http://foo.bar.com/
This command collects links on the page http://foo.bar.com/, and download jpg files to PyCherryPick/python/downloads.

Advanced Option:
There are some options.
  --version             Show program's version number and exit
  -h, --help            Show this help message and exit
  -f FILE, --file=FILE  Local HTML file path. example:"/Users/foo/html/bar.html"'
                        If both of 'target URL' and -f option are defined, Local file will be loaded and scraped.
  -t TYPE, --type=TYPE  Download file type. example:"jpg" "jpg,png,gif"
                        If both of -r and -t options are defined, -t will be ignored.
  -i INTERVAL, --interval=INTERVAL      Interval seconds of downloading files (default - 2 seconds)
  -d DOWNLOAD, --download=DOWNLOAD      Download directory path. example:"/User/foo/downloads"
  -e ENCODE, --encode=ENCODE            Character encoding of target page. example:"utf-8"
  -u UA, --ua=UA        custom user-agent (default user-agent - IE8)
  -r REGEX, --regex=REGEX               Regular expression for dowload file's url. example:"http.+\.jpg"
                                        If both of -r and -t options are defined, -t will be ignored.

Example:
$ cd PyCherryPick/python
$ python pycherrypick.py http://foo.bar.com/bar.html -t png -d /User/foo/downloads
PNG files will be downloaded to /User/foo/downloads
If you want to download jpg, png, gif, pdf files, set -t option like "jpg,png,gif,pdf"

Want another files?:
If you want another files(img tags srcfile,etc), make new class extends PyCherryPick, and overwride scrape().
(See PyCherryPick/python/custom_example.py)
