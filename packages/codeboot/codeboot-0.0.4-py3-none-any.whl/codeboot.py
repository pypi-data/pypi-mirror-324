#!/usr/bin/env python3

# Logger config
import logging

__version__ = '0.0.4'

logger = logging.getLogger(__name__)

if not logging.getLogger().hasHandlers():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


# Script
import argparse
import base64
import copy
import glob
import itertools
import lzma
import os
import sys
import webbrowser

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>codeBoot links</title>
<style>
body {{
  font-family: sans-serif;
  font-size: 20px;
}}
li {{
  padding-top: 0.15em;
  padding-bottom: 0.15em;
}}
h1, h2, h3, h4, h5, h6 {{
  margin-top: 1em;
  margin-bottom: 0.5em;
}}
</style>
</head>
<body>
<ol>
{links}
</ol>
</body>
</html>
"""

ANIMATE_SPEEDS = {
    0: None,
    1: 'slow',
    2: 'normal',
    3: 'fast',
    4: 'ultra',
}

class UrlTooLong(Exception):
    def __init__(self, file=None):
        self.file = file

class NoFile(Exception):
    pass

class File:
    def __new__(cls, path, main=False, on_device=False, skip_on_exception=True):
        source = sys.stdin if path == "-" else open(path, 'r')
        with source as f:
            try:
                content = f.read()
            except Exception as e:
                if skip_on_exception:
                    logger.warning(f'{path} was skipped ({type(e).__name__})')
                    return None
                else:
                    raise
        
        self = super().__new__(cls)
        self._path = path
        self.content = content
        self.main = main
        self.on_device = on_device
        return self

    @staticmethod
    def is_hidden(path):
        return os.path.basename(path).startswith('.')

    @classmethod
    def from_paths(cls, paths, first_as_main=True, on_device=False):
        paths = list(paths)
        files = []

        for path in paths:
            if cls.is_hidden(path):
                logger.info(f'{path} was skipped (hidden)')
                continue
            if os.path.isdir(path):
                for subpath in os.listdir(path):
                    paths.append(os.path.join(path, subpath))
            elif os.path.isfile(path) or path == "-":
                file = cls(path, main=first_as_main, on_device=on_device)
                if file:
                    files.append(file)
                    first_as_main = False
            else:
                raise FileNotFoundError(path)

        return files

    @property
    def path(self):
        return "untitled.py" if self._path == "-" else self._path

    @property
    def basename(self):
        return os.path.basename(self.path)

    @property
    def encoded_content(self):
        compressed = lzma.compress(
            self.content.encode(),
            format=lzma.FORMAT_ALONE
        )
        return base64.urlsafe_b64encode(compressed).decode()

    def get_url_encoding(self, use_basename=False):
        cmd = 'f' if self.main else 'o'
        if self.on_device: cmd = cmd.upper()
        filename = self.basename if use_basename else self.path
        path = base64.urlsafe_b64encode(filename.encode()).decode()
        return f'{cmd}{path}~{self.encoded_content}'

    def as_main(self, main=True):
        new_file = copy.copy(self)
        new_file.main = main
        return new_file

    def __copy__(self):
        copy = super().__new__(type(self))
        copy._path = self._path
        copy.content = self.content
        copy.main = self.main
        copy.on_device = self.on_device
        return copy

    def __repr__(self):
        return f'<File {self.path!r}>'

def open_in_browser(url, args):
    if args.device:
        # Attempt to open with chrome for device
        chrome = None
        for browser in ("google-chrome", "chrome", "chromium", "chromium-browser"):
            try:
                chrome = webbrowser.get(browser)
            except webbrowser.Error:
                continue

            chrome.open_new_tab(url)
        else:
            logger.warning('executing on device, but could not find Chrome browser')

    webbrowser.open_new_tab(url)

def build_query_string(files, args, use_basename=False):
    return _build_query_string(
        files=files,
        exec=not args.no_exec,
        animate=args.animate,
        steps=args.step,
        large_font=args.large_font,
        line_numbers=args.line_numbers,
        webapp=args.webapp,
        floating=args.floating,
        use_basename=use_basename
    )


def _build_query_string(*, files, exec, steps, animate, large_font,
                          line_numbers, webapp, floating, sep='.',
                          use_basename=False):
    def param(key, value):
        return f'~{key}={value}'

    def url_bool(x):
        return str(bool(x)).lower()

    def add_flag(key, value):
        if value is not None:
            add_param(key, url_bool(value))

    def add_param(key, value):
        parts.append(param(key, value))

    parts = [f.get_url_encoding(use_basename) for f in files]
    add_param('lang', 'py-novice')
    add_flag('largeFont', large_font)
    add_flag('showLineNumbers', line_numbers)
    add_flag('hidden', webapp)
    add_flag('floating', floating)

    if exec:
        if animate is not None:
            speed = ANIMATE_SPEEDS[animate]
            if speed is not None:
                add_param('animationSpeed', speed)
            parts.append('a')
        else:
            parts.append('e' + ('' if steps is None else str(steps)))

    return sep.join(parts)

def make_url(*, domain, version, signature=None, qs="", max_url_size=8000, app_subdomain='app'):
    version = f'{version}/' if version else ''
    domain = f'{app_subdomain}.{domain}' if signature is None and app_subdomain else domain
    query = f'?init={signature if signature else ""}.{qs}' if qs else ''
    url = f'https://{domain}/{version}{query}'

    if len(url) > max_url_size:
        raise UrlTooLong

    return url

def make_html_page(args, files):
    def make_html_link(file):
        qs = build_query_string([file.as_main()], args, use_basename=True)

        try:
            url = make_url(domain=args.domain, version=args.version, qs=qs)
        except UrlTooLong:
            raise UrlTooLong(file)

        return f'<li><a href="{url}">{file.basename}</a></li>'

    output_file = 'index.html'

    files = sorted(files, key=lambda file: file.path)

    parts = []

    for directory, group in itertools.groupby(files, key=lambda f: os.path.dirname(f.path)):

        parts.append(f"<h3>{directory}</h3>")

        for file in files:
            parts.append(make_html_link(file))

    content = TEMPLATE.format(links='\n'.join(parts))

    output_file = os.path.abspath(output_file)

    with open(output_file, 'w') as f:
        f.write(content)

    if args.link_only:
        print(output_file)
    else:
        open_in_browser(f"file://{output_file}", args)

def main(args):
    # Get files
    paths = []

    if not args.paths:
        logger.info('no file given, open codeboot ignoring the query string')
        codeboot_url = make_url(
            domain=args.domain,
            version=args.version,
            app_subdomain=None)
        if args.link_only:
            print(codeboot_url)
        else:
            open_in_browser(codeboot_url, args)
        return
    
    for path in args.paths:
        if glob.has_magic(path):
            paths.extend(glob.glob(path))
        else:
            paths.append(path)

    if not paths:
        raise NoFile

    has_dir = any(os.path.isdir(p) for p in paths)
    files = File.from_paths(paths, first_as_main=True, on_device=args.device)

    # Get codeBoot execution mode
    if has_dir:
        return make_html_page(args, files)

    qs = build_query_string(files, args)

    url = make_url(domain=args.domain, version=args.version, qs=qs)

    if args.link_only:
        print(url)
    else:
        open_in_browser(url, args)

def cli_main():
    formatter = lambda prog: argparse.HelpFormatter(prog, max_help_position=40)
    parser = argparse.ArgumentParser(
        formatter_class=formatter,
        description=(
            f'Execute Python scripts in the browser with codeBoot.\n'
            f'Learn more about codeBoot here: https://codeboot.org.\n'
            f'Version {__version__}.'),
        usage="%(prog)s [FILES]... [OPTIONS]...",
        add_help=False,
    )

    files_group = parser.add_argument_group('positional arguments',
        description=('A list of files or a directory to open in codeBoot.\n'
                     'When a list of files is given, these are opened in codeBoot.\n'
                     'When a directory is given, an html page that contains codeBoot links '
                     'to all files in the directory is generated and opened.'))
    files_group.add_argument(
        'paths',
        nargs="*",
        metavar='path',
        help=argparse.SUPPRESS
    )

    # Execution modes
    exec_group = parser.add_argument_group("execution options")
    parser_mode = exec_group.add_mutually_exclusive_group()
    parser_mode.add_argument(
        '-x', '--exec',
        action='store_true',
        help='execute in browser (default)'
    )
    parser_mode.add_argument('-s', '--step',
        type=int,
        metavar='N',
        help='single-step in browser up to N steps'
    )
    parser_mode.add_argument('-a', '--animate',
        nargs='?',
        const=0,
        type=int,
        choices=[k for k, v in ANIMATE_SPEEDS.items() if v is not None],
        help='single-step animation in browser with given step speed (1=slow, 2=normal, 3=fast, 4=ultra-fast)'
    )
    parser_mode.add_argument('-n', '--no-exec',
        action='store_true',
        help='open in browser without executing'
    )
    exec_group.add_argument('-w', '--webapp',
        action='store_true',
        default=None,
        help='open as a webapp with editor hidden'
    )
    exec_group.add_argument('-e', '--device',
        action='store_true',
        default=None,
        help='execute on external device through codeBoot'
    )
    exec_group.add_argument('-l', '--link-only',
        action='store_true',
        help='print a hyperlink instead of opening in browser'
    )

    # Debug settings
    debug_options = parser.add_argument_group("help options")
    debug_options.add_argument('-h', '--help',
        action='help',
        help='show this help message and exit')
    debug_options.add_argument('--version-info', action='version', version=__version__)
    debug_options.add_argument('--warnings',
        action='store_true',
        help='show warnings, including files that were skipped'
    )
    debug_options.add_argument('--debug', action='store_true', help=argparse.SUPPRESS)
    
    # Link creation settings
    link_group = parser.add_argument_group("server options")
    link_group.add_argument('-d', '--domain',
        type=str,
        default='codeboot.org',
        metavar='D',
        help='use given domain (default to codeboot.org)'
    )
    link_group.add_argument('-v', '--version',
        type=str,
        metavar='V',
        help='use given codeBoot version (default to latest)'
    )


    # codeBoot settings
    misc_options = parser.add_argument_group("editor options")
    misc_options.add_argument("--large-font",
        dest="large_font",
        default=None,
        action=argparse.BooleanOptionalAction,
        help="Enable/disable large font")
    misc_options.add_argument("--line-numbers",
        dest="line_numbers",
        default=None,
        action=argparse.BooleanOptionalAction,
        help="Enable/disable line numbers")
    misc_options.add_argument("--floating",
        dest="floating",
        default=None,
        action=argparse.BooleanOptionalAction,
        help="Enable/disable floating window")

    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)
        cli_args = '\n'.join(f'{k}={v}' for k, v in vars(args).items())
        logger.debug(f"command-line arguments:\n{cli_args}")
    elif args.warnings:
        logger.setLevel(logging.WARNING)
    else:
        logger.setLevel(logging.ERROR)

    def error(msg):
        print(msg, file=sys.stderr)
        exit(1)

    try:
        main(args)
    except UrlTooLong as e:
        if e.file is None:
            error("ERROR: Resulting url is too long.")
        else:
            error(f"ERROR: Resulting url for file {e.file.path!r} is too long.")
    except FileNotFoundError as e:
        filename = e.args[0] if e.args else '<unknown>'
        error(f"ERROR: Could not find {filename!r}.")
    except NoFile:
        error(f"ERROR: Given pattern matches no file.")
    else:
        exit(0)

if __name__ == "__main__":
    cli_main()