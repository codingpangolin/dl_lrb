# dl_lrb

Python CLI that can generate an epub of an issue of the London Review of Books based on the articles on its website.

## Setup

1. For the tool to work Pandoc must be installed and added to PATH. See installation instructions [here](https://pandoc.org/installing.html).
2. Install modules from requirements.txt

## Usage

Create an epub of the latest issue of the magazine:

```
Python dl_lrb.py
```

Create an epub of a specific issue of the magazine by supplying full URL of the issue from the London Review of Books website as an argument:

```
python dl_lrb.py "https://www.lrb.co.uk/the-paper/v40/n23"
```

epub file will be saved to cwd with file named using issue number and date of magazine requested, e.g:

> Vol 40 No 23 6 December 2018.epub
