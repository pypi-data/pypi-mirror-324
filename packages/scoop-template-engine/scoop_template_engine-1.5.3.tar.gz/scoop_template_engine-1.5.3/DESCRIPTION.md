The primary purpose of the SCOOP template engine (`ste`) is to facilitate the preparation of manuscripts in [LaTeX](https://www.latex-project.org/) for publication in scientific journals.
It allows the user to concentrate on the content, rather than the layout.
The layout, which depends on the journal, will be automatically generated.
An effort is made to achieve compatibility of a range of standard LaTeX packages with each supported journal.
In addition, a consistent set of theorem-like environments is provided across journals.

As of version 1.5.0, the SCOOP template engine also supports the creation of LaTeX letters.

## Installation
The SCOOP template engine requires Python 3.9 or newer.
To install the SCOOP template engine and initialize the journal resources, say
```python
pip3 install scoop-template-engine
ste init
```

## Getting Started
Please refer to the "Quick Start" section in the documentation
```python
ste doc
```
for more.

To create the files for a sample document in the current folder, say
```python
ste start amspreprint
```
To render this manuscript in a preprint layout, say
```python
ste prepare
```
Then compile the sample document `manuscript-amspreprint.tex`.

To see the list of supported journals, say
```python
ste list --template
```
