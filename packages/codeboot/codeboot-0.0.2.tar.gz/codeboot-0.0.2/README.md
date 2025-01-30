# codeboot-tools
Some tools to control codeBoot from Python and the shell

## Usage

```
usage: codeBoot linker [-h] [-x | -s N | -t | -p [path]] [-a] [-f] [-n] [-v V] [-d D] [-l] [-w] path [path ...]

Generate links to executable Python scripts in the browser with codeBoot. Learn more about codeBoot here: https://codeboot.org

positional arguments:
  path                 path to a script or directory

options:
  -h, --help           show this help message and exit
  -x, --exec           execute first given .py file in browser. This is the default if given a single .py file.
  -s, --step N         single-step first given .py file in browser up to step N.
  -t, --stop           open first given .py file in browser without executing.
  -p, --page [path]    open an html page with execution links for each .py file. The html file is written at the given path (index.html by default). This is the
                       default when a directory is given.
  -a, --webapp         execute as a webapp.
  -f, --large-font     use large font.
  -n, --line-numbers   show line numbers.
  -v, --version V      force the use of codeBoot version V.
  -d, --domain D       use domain D for links (default to codeboot.org).
  -l, --link           print a hyperlink instead of opening in browser.
  -w, --show-warnings  show warnings, including files that were skipped.
```