# constrained-counterpoint
Generate your own first-species counterpoint harnessing the power of `python-constraint`!

## Prerequisites
- Python3
- LilyPond (http://lilypond.org/download.html)
- Notation software that can open MIDI files (MuseScore for example)
- python-constraint
- venv

## Setup
#### Create a virtual environment.
`python3 -m venv venv`
<br>

#### Activate it.
`source venv/bin/activate`
<br>

#### Install python-constraint.
`pip3 install python-constraint`
<br>

#### Run script.
`python3 counterpoint.py`
<br><br>

TODO:
- Add "max 3 consecutive 3rd/6ths" rule
- Enforce 'arc' shape
- Add variance constraint
<br><br>

Don't tell your music professors!
