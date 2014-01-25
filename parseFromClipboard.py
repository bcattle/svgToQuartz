#!/usr/bin/env python
import Tkinter

root = Tkinter.Tk()
root.withdraw()
clipboard_str = root.clipboard_get()

if clipboard_str:
    from parse import SvgStringParser
    parser = SvgStringParser()
    result = parser.parse_string(clipboard_str)

    print ''
    # If they have pygments, print it in color
    try:
        from pygments import highlight
        from pygments.lexers import ObjectiveCLexer
        from pygments.formatters import TerminalFormatter

        print highlight(result, ObjectiveCLexer(), TerminalFormatter())

    except ImportError:
        print result
else:
    print 'No SVG string found on the clipboard. Copy a <path d=""> attribute.'
    print 'Only include the part between the quotes.'
