import tempfile
import win32api
import win32print


def print_ticket_number(ticket_number: int):
    filename = tempfile.mktemp(".txt")
    open(filename, "w").write(str(ticket_number))
    win32api.ShellExecute(
      0,
      "print",
      filename,
      '/d:"%s"' % win32print.GetDefaultPrinter(),
      ".",
      0
    )
