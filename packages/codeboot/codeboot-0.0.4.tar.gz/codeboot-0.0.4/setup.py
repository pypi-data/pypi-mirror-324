from setuptools import setup
import os

import codeboot

# Sanity check that we are not importing a globally installed codeboot.py
script_dir = os.path.dirname(codeboot.__file__)
this_dir = os.path.dirname(__file__)
assert script_dir == this_dir, f"imported codeboot.py from wrong dir {script_dir!r}"

setup(
    name='codeboot',
    version=codeboot.__version__,
    description='Some tools to control codeBoot from Python and the shell',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author='Olivier Melançon',
    author_email='olivier.melancon.1@umontreal.ca',
    url="https://github.com/udem-dlteam/codeboot-tools",
    py_modules=["codeboot"],
    packages=[],classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "codeboot=codeboot:cli_main"
        ]
    }
)
