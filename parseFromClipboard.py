#!/usr/bin/env python
import Tkinter

root = Tkinter.Tk()
root.withdraw()
clipboard_str = root.clipboard_get()

if clipboard_str:
    from parse import SvgStringParser
    parser = SvgStringParser()
    parser.parse_string(clipboard_str)
else:
    print 'No SVG string found on the clipboard. Copy a <path d=""> attribute.'
    print 'Only include the part between the quotes.'
