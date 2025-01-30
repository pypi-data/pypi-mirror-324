#!/usr/bin/env python3

import argparse
import base64
import copy
import itertools
import logging
import lzma
import os
import sys
import webbrowser

logger = logging.Logger(__name__)

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

class File:
    def __new__(cls, path, main=False, skip_on_exception=True):
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
        return self

    @staticmethod
    def is_hidden(path):
        return os.path.basename(path).startswith('.')

    @classmethod
    def from_paths(cls, paths, first_as_main=True):
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
                file = cls(path, first_as_main)
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

    @property
    def url_encoding(self):
        cmd = 'f' if self.main else 'o'
        path = base64.urlsafe_b64encode(self.path.encode()).decode()
        return f'{cmd}{path}~{self.encoded_content}'

    def as_main(self, main=True):
        new_file = copy.copy(self)
        new_file.main = main
        return new_file

    def __copy__(self):
        copy = super().__new__(type(self))
        copy.path = self.path
        copy.content = self.content
        copy.main = self.main
        return copy

    def __repr__(self):
        return f'<File {self.path!r}>'

def build_query_string(*, files, exec, steps=None, large_font=None, line_numbers=None, webapp=None, sep='.'):
    def param(key, value):
        return f'~{key}={value}'

    def url_bool(x):
        return str(bool(x)).lower()

    parts = [f.url_encoding for f in files]
    parts.append(param('lang', 'py-novice'))

    if large_font is not None:
        parts.append(param('largeFont', url_bool(large_font)))

    if line_numbers is not None:
        parts.append(param('showLineNumbers', url_bool(line_numbers)))

    if webapp is not None:
        parts.append(param('hidden', url_bool(webapp)))

    if exec:
        parts.append('e' + '' if steps is None else str(steps))

    return sep.join(parts)

def make_url(*, domain, version, signature=None, qs):
    version = f'{version}/' if version else ''
    domain = f'app.{domain}' if signature is None else domain
    return f'https://{domain}/{version}?init={signature if signature else ""}.{qs}'



def make_html_page(args, files):
    def make_html_link(file):
        url = make_url(domain=args.domain, version=args.version, qs=qs)
        return f'<li><a href="{url}">{file.basename}</a></li>'

    output_file = args.page or 'index.html'

    files = sorted(files, key=lambda file: file.path)

    parts = []

    for directory, group in itertools.groupby(files, key=lambda f: os.path.dirname(f.path)):

        parts.append(f"<h3>{directory}</h3>")

        for file in files:
            qs = build_query_string(
                files=[file],
                exec=False,
                large_font=args.large_font,
                line_numbers=args.line_numbers,
                webapp=args.webapp
            )

            parts.append(make_html_link(file))

    content = TEMPLATE.format(links='\n'.join(parts))

    output_file = os.path.abspath(output_file)

    with open(output_file, 'w') as f:
        f.write(content)

    if args.link:
        print(output_file)
    else:
        webbrowser.open_new_tab(f"file://{output_file}")

def main(args):
    # Get files
    paths = args.paths
    has_dir = any(os.path.isdir(p) for p in paths)
    files = File.from_paths(paths, first_as_main=True)

    # Get codeBoot execution mode
    if has_dir or args.page is not None:
        return make_html_page(args, files)

    qs = build_query_string(
        files=files,
        exec=not args.stop,
        steps=args.step,
        large_font=args.large_font,
        line_numbers=args.line_numbers,
        webapp=args.webapp
    )

    url = make_url(domain=args.domain, version=args.version, qs=qs)

    if args.link:
        print(url)
    else:
        webbrowser.open_new(url)

def cli_main():
    parser = argparse.ArgumentParser(
        prog='codeBoot linker',
        description=(
            'Generate links to executable Python scripts in the browser with codeBoot.\n'
            'Learn more about codeBoot here: https://codeboot.org'),
    )

    parser.add_argument(
        'paths',
        nargs="+",
        metavar='path',
        help='path to a script or directory'
    )

    parser_mode = parser.add_mutually_exclusive_group()

    parser_mode.add_argument(
        '-x', '--exec',
        action='store_true',
        help='execute first given .py file in browser. This is the default if given a single .py file.'
    )
    parser_mode.add_argument('-s', '--step',
        type=int,
        metavar='N',
        help='single-step first given .py file in browser up to step N.'
    )
    parser_mode.add_argument('-t', '--stop',
        action='store_true',
        help='open first given .py file in browser without executing.'
    )
    parser_mode.add_argument('-p', '--page',
        nargs='?',
        metavar='path',
        default=argparse.SUPPRESS,
        help=('open an html page with execution links for each .py file.\n'
              'The html file is written at the given path (index.html by default).\n'
              'This is the default when a directory is given.')
    )

    parser.add_argument('-a', '--webapp',
        action='store_true',
        default=None,
        help='execute as a webapp.'
    )
    parser.add_argument('-f', '--large-font',
        action='store_true',
        default=None,
        help='use large font.'
    )
    parser.add_argument('-n', '--line-numbers',
        action='store_true',
        default=None,
        help='show line numbers.'
    )
    parser.add_argument('-v', '--version',
        type=str,
        metavar='V',
        help='force the use of codeBoot version V.'
    )
    parser.add_argument('-d', '--domain',
        type=str,
        default='codeboot.org',
        metavar='D',
        help='use domain D for links (default to codeboot.org).'
    )
    parser.add_argument('-l', '--link',
        action='store_true',
        help='print a hyperlink instead of opening in browser.'
    )
    parser.add_argument('-w', '--show-warnings',
        action='store_true',
        help='show warnings, including files that were skipped.'
    )

    args = parser.parse_args()

    if args.show_warnings:
        logger.setLevel(logging.WARNING)
    else:
        logger.setLevel(logging.ERROR)

    if "page" not in args:
        args.page = None
    elif not args.page:
        args.page = ""

    main(args)

if __name__ == "__main__":
    cli_main()