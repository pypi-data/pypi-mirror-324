from setuptools import setup

setup(
    name='codeboot',
    version='0.0.1',
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
