#!/usr/bin/python

# Boyer-Moore Library
class last_occurrence(object):
    """Last occurrence functor."""

    def __init__(self, pattern, alphabet):
        """Generate a dictionary with the last occurrence of each alphabet
        letter inside the pattern.

        Note: This function uses str.rfind, which already is a pattern
        matching algorithm. There are more 'basic' ways to generate this
        dictionary."""
        self.occurrences = dict()
        for letter in alphabet:
            self.occurrences[letter] = pattern.rfind(letter)

    def __call__(self, letter):
        """Return last position of the specified letter inside the pattern.
        Return -1 if letter not found in pattern."""
        return self.occurrences[letter]


def boyer_moore_match(text, pattern):
    """Find occurrence of pattern in text."""
    alphabet = set(text)
    last = last_occurrence(pattern, alphabet)
    m = len(pattern)
    n = len(text)
    i = m - 1  # text index
    j = m - 1  # pattern index
    while i < n:
        if text[i] == pattern[j]:
            if j == 0:
                return i
            else:
                i -= 1
                j -= 1
        else:
            l = last(text[i])
            i = i + m - min(j, 1 + l)
            j = m - 1
    return -1


### MAIN FUNCTION ###

if __name__ == '__main__':

    def show_match(text, pattern):
        # print 'Text:  %s' % text
        p = boyer_moore_match(text, pattern)
        if p > 0:
            return 'Tidak Baku: %s%s' % ('' * p, pattern)

import re
from tkinter import *

root = Tk()
root.title('Aplikasi Deteksi Kata Tidak Baku')
# Code to add widgets...

row1 = Frame(root)
row1.pack()
Label1 = Label(row1, text="Masukan Teks")
Label1.pack()
InsertText = Text(row1, height=20)
InsertText.pack()


def displayResult():
    ViewResult.delete("1.0", END)
    kamus = ["analisa", "praktek", "tehnik", "kwalitas", "aktifitas", "frase", "hakekat", "ijin", "karir", "lembab",
             "propinisi", "resiko", "silahkan", "subyek", "seksama", "rubah", "terlantar", "trampil", "pendeteksi",
             "masukkan", "input", "website", "file", "folder", "sistimatis"]
    hasil_cari = []
    index = 1
    for ptr in kamus:
        cek = show_match(InsertText.get("1.0", END), ptr)
        if cek is not None:
            hasil_cari.insert(index, cek)
        print
        cek
        index = index + 1

    if len(hasil_cari) > 0:
        hasil = "\n".join(hasil_cari)
    else:
        hasil = "Kata tidak baku tidak ditemukan"

    ViewResult.insert(INSERT, hasil)


def cleanResult():
    ViewResult.delete("1.0", END)
    InsertText.delete("1.0", END)


B = Button(row1, text="PERIKSA", command=displayResult)
B2 = Button(row1, text="ULANG", command=cleanResult)
B.pack()
B2.pack()

row2 = Frame(root)
row2.pack()
Label1 = Label(row1, text="Hasil")
Label1.pack()
ViewResult = Text(row2, height=10)
ViewResult.pack()

root.mainloop()