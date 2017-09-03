#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pdfrw import PdfReader, PdfWriter
from os import path

"""Split PDF to single-pages PDF"""
class SplitPDF(object):
    def __init__(self, input_path: str, output_path: str):
        self.__input_path = input_path
        self.__output_path = output_path
        self.__output_file = path.basename(self.__output_path)
        self.__output_folder = path.dirname(self.__output_path)

    def split(self):
        input_pdf = PdfReader(self.__input_path)
        for i, p in enumerate(input_pdf.pages):
            temp = self.__output_file.split('.')[0] + "-page_%03d.pdf" % (i+1)
            PdfWriter().addpage(p).write(path.join(self.__output_folder, temp))

if __name__ == "__main__":
    x = SplitPDF('input.pdf', 'output.pdf')
    x.split()
