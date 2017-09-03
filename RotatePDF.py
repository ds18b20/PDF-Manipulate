#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Rotate Pdf in input folder"""

from pdfrw import PdfReader, PdfWriter
from os import path, listdir


class PdfRotate(object):
    def __init__(self, input_path: str, output_path: str, rotate_degree: str):
        self.__input_path = input_path
        self.__output_path = output_path

        self.__rotate_degree = rotate_degree

    def rotate(self):
        input_pdf = PdfReader(self.__input_path)
        page_count = int(input_pdf.Root.Pages.Count)
        pages = input_pdf.pages

        assert self.__rotate_degree.isdigit()
        assert int(self.__rotate_degree) % 90 == 0

        for page_num in range(page_count):
            pages[page_num - 1].Rotate = int(self.__rotate_degree)
            out_data = PdfWriter()
            out_data.trailer = input_pdf
            out_data.write(self.__output_path)

if __name__ == "__main__":
    input_folder = 'input'
    input_file_list = [x for x in listdir(input_folder) if x.endswith('.pdf')]
    output_folder = 'output'

    input_rotate_degree = input('Input rotate degree here:\n' + 'Input must be (90*n)\n->')

    for input_file in input_file_list:
        pdf_input_path = path.join(input_folder, input_file)
        pdf_output_path = path.join(output_folder, u'Rotated-' + input_file)
        pdf_obj = PdfRotate(pdf_input_path, pdf_output_path, input_rotate_degree)
        pdf_obj.rotate()

    print(u'SUCCEED!')
