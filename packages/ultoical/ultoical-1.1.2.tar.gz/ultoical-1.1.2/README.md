# ULToICAL
[ [English](README.fr.md) | [Francais](README.fr.md) ]

[ [Support my work](https://ko-fi.com/totorocodesoften) ]

ULToICAL is an easy way to convert your Universite de Lorraine Multi timetable to an ICAL format to store in Google Agenda, Apple Calendars etc...
## Installation
To use ULToICAL you will need `python>=3.10`

### From PIP

Run `pip install ultoical`

To use the program run `ultoical`

### From source

Simply run

```bash
pip install .
```

And start the program using:

```bash
ultoical
```

## Getting the UL Token (optional)
To get the token simply go to your timetable inside the UL Multi app and press `CTRL + Maj + I`

Click on `network` on the window that just oppened

Change weeks on the timetable until you see a `200 POST schedule json`

Click on it, navigate to `Requests` and copy the `authToken` field

## TODO
- [ ] Official secure public instance
- [x] Automatic temp file deletion
- [x] Add french support
- [x] Better error handeling
- [x] Tokenless auth
