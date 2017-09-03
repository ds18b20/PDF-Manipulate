#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from pdfrw import PdfReader, PdfWriter


class MergePDF(object):
    """Merge PDFs to one PDF"""
    def __init__(self, input_path_list: list, output_path: str):
        self.__input_path_list = input_path_list
        self.__output_path = output_path
    
    def merge(self):
        writer = PdfWriter()
        for _path in sorted(self.__input_path_list):
            writer.addpages(PdfReader(_path).pages)
        writer.write(self.__output_path)

if __name__ == "__main__":
    x = MergePDF(['a.pdf', 'b.pdf'], 'output.pdf')
    x.merge()
