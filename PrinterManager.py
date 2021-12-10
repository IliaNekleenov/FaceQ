import os

import win32api
import win32print
from docxtpl import DocxTemplate


template_filename = 'template.docx'


def print_ticket_number(ticket_number: int):
    number = format_number(ticket_number)
    doc = DocxTemplate(template_filename)
    context = {'n': number}
    doc.render(context)
    filename = f'tmp.docx'
    doc.save(filename)
    print_file(filename)
    # os.remove(filename)


def print_file(filename):
    win32api.ShellExecute(
      0,
      "print",
      filename,
      '/d:"%s"' % win32print.GetDefaultPrinter(),
      ".",
      0
    )


def format_number(n):
    str_n = str(n)
    if str_n[-1] == '6' or str_n[-1] == '9':
        str_n += '.'
    return str_n
