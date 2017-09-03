#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from io import BytesIO
from pdfrw import PdfReader, PdfWriter, PageMerge
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm, inch
from reportlab.lib.pagesizes import A4, A3, landscape
from reportlab.lib.colors import black, white, blue, red, whitesmoke
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from configparser import ConfigParser
from os import path, listdir
from sys import exit


def get_canvas_data(selection: str, sb_or_count: str, page_num: int, ini_object) -> BytesIO:
    # SB rect info
    sb_rect_props = ini_object.get_sb_rect_props()

    # Ins rect info
    ins_rect_props = ini_object.get_ins_rect_props()

    # sb info
    sb_props = ini_object.get_sb_props()

    # instruction info
    instruction_props = ini_object.get_instruction_props()

    # Read SB RECT
    sb_rect_start_x = float(sb_rect_props['x'])
    sb_rect_start_y = float(sb_rect_props['y'])
    sb_rect_width = float(sb_rect_props['width'])
    sb_rect_height = float(sb_rect_props['height'])

    # Read SB RECT
    ins_rect_start_x = float(ins_rect_props['x'])
    ins_rect_start_y = float(ins_rect_props['y'])
    ins_rect_width = float(ins_rect_props['width'])
    ins_rect_height = float(ins_rect_props['height'])
    
    # Read SB
    sb_start_x = float(sb_props["x"])
    sb_start_y = float(sb_props["y"])
    sb_font_size = int(sb_props["font_size"])

    # Read Instruction
    ins_start_x = float(instruction_props["x"])
    ins_start_y = float(instruction_props["y"])
    ins_font_size = int(instruction_props["font_size"])

    # Draw String
    font_name = "IPA Gothic"
    font_path = u'C:/Windows/Fonts/msgothic.ttc'
    pdfmetrics.registerFont(TTFont(font_name, font_path))

    # SB or Instruction usage
    if selection == '1':
        # Create a new PDF with reportlab
        data = BytesIO()
        can = canvas.Canvas(data, pagesize=A4)

        # String for print
        string = u"管理番号：{}                          P.{}".format(sb_or_count, page_num)

        # Set SB RECT
        rect_start_x = sb_rect_start_x * mm
        rect_start_y = sb_rect_start_y * mm
        rect_width = sb_rect_width * mm
        rect_height = sb_rect_height * mm

        # Draw a rectangle
        can.setFillColor(white)
        can.rect(rect_start_x, rect_start_y, rect_width, rect_height, fill=True, stroke=False)

        # Draw String
        can.setFillColor(black)
        can.setFont(font_name, sb_font_size)
        can.drawString(sb_start_x * mm, sb_start_y * mm, string)

        can.showPage()
        can.save()
        data.seek(0)
        return data

    elif selection == '2':
        # Create a new PDF with reportlab
        data = BytesIO()
        can = canvas.Canvas(data, pagesize=landscape(A3))

        # String for print
        string = u"別紙({}／{})".format(page_num, sb_or_count)

        # Set SB RECT
        rect_start_x = ins_rect_start_x * mm
        rect_start_y = ins_rect_start_y * mm
        rect_width = ins_rect_width * mm
        rect_height = ins_rect_height * mm

        # Draw a rectangle
        can.setFillColor(white)
        can.rect(rect_start_x, rect_start_y, rect_width, rect_height, fill=True, stroke=False)
        # Draw String
        can.setFillColor(black)
        can.setFont(font_name, ins_font_size)
        can.drawString(ins_start_x * mm, ins_start_y * mm, string)

        can.showPage()
        can.save()
        data.seek(0)
        return data
    else:
        pass


class IniInfo(object):
    def __init__(self, ini_path: str):
        self.__ini_path = ini_path

    def get_input_folder(self):
        input_folder = self.read_config_file('INPUT', 'folder')
        return input_folder

    def get_output_folder(self):
        input_folder = self.read_config_file('OUTPUT', 'folder')
        return input_folder

    def get_sb_rect_props(self):
        rect_x = self.read_config_file('SB_RECT', 'x')
        rect_y = self.read_config_file('SB_RECT', 'y')
        rect_width = self.read_config_file('SB_RECT', 'width')
        rect_height = self.read_config_file('SB_RECT', 'height')
        return {'x': rect_x, 'y': rect_y, 'width': rect_width, 'height': rect_height}

    def get_ins_rect_props(self):
        rect_x = self.read_config_file('INS_RECT', 'x')
        rect_y = self.read_config_file('INS_RECT', 'y')
        rect_width = self.read_config_file('INS_RECT', 'width')
        rect_height = self.read_config_file('INS_RECT', 'height')
        return {'x': rect_x, 'y': rect_y, 'width': rect_width, 'height': rect_height}

    def get_sb_props(self):
        sb_x = self.read_config_file('SB', 'x')
        sb_y = self.read_config_file('SB', 'y')
        sb_font_size = self.read_config_file('SB', 'font_size')
        return {'x': sb_x, 'y': sb_y, 'font_size': sb_font_size}

    def get_instruction_props(self):
        instruction_x = self.read_config_file('INSTRUCTION', 'x')
        instruction_y = self.read_config_file('INSTRUCTION', 'y')
        instruction_font_size = self.read_config_file('INSTRUCTION', 'font_size')
        return {'x': instruction_x, 'y': instruction_y, 'font_size': instruction_font_size}

    # read ini file method
    def read_config_file(self, section: str, key: str) ->str:
        conf = ConfigParser()
        conf.read(self.__ini_path)
        return conf.get(section, key)


def io_check():
    selection = input(u"対象PDFの種類を選択してください：\n1：購入仕様書　2：改造指示書\n")
    if selection == '1':
        start_page_num = input(u"購入仕様書のスタートページ番号を入力してください：\n")
        if start_page_num.isdigit():
            sb_doc_num = input(u"SB番号を入力してください：\n")
            return selection, start_page_num, sb_doc_num
        else:
            print(u"正しく入力してください。")
            exit(0)
    elif selection == '1':
        start_page_num = input(u"改造指示書のスタートページ番号を入力してください：\n")
        if start_page_num.isdigit():
            page_count = input(u"ページ数を入力してください：\n")
            if page_count.isdigit():
                return selection, start_page_num, page_count
            else:
                print(u"正しく入力してください。")
                exit(0)
        else:
            print(u"正しく入力してください。")
            exit(0)
    else:
        print(u"正しく入力してください。")
        exit(0)


def add_text(input_path: str, output_path: str, selection: str, start_page_num: str, sb_or_count: str):
    assert path.exists('conf.ini')
    ini_file = 'conf.ini'
    ini_object = IniInfo(ini_file)
    source_pdf = PdfReader(input_path)
    total_page_num = int(source_pdf.Root.Pages.Count)
    for page_num in range(total_page_num):
        canvas_data = get_canvas_data(selection, sb_or_count, page_num + int(start_page_num), ini_object)
        wm_pdf = PdfReader(canvas_data)
        wm_obj = PageMerge().add(wm_pdf.pages[0])[0]
        PageMerge(source_pdf.pages[page_num]).add(wm_obj).render()
    output_data = BytesIO()
    PdfWriter().write(output_data, source_pdf)
    output_data.seek(0)

    save2pdf(output_data, output_path)


def save2pdf(data: BytesIO, filename: str):
    with open(filename, 'wb') as f:
        f.write(data.read())


def main():
    selection, start_page_num, sb_or_count = io_check()
    print(u"稼動中...\n")
    print(u"AddText2PDF by WEN")

    assert path.exists('conf.ini')
    ini_file = 'conf.ini'
    ini_object = IniInfo(ini_file)

    # IO
    input_folder = ini_object.get_input_folder()
    input_file_list = [x for x in listdir(input_folder) if x.endswith('.pdf')]
    input_file = input_file_list[0]
    input_path = path.join(input_folder, input_file)

    output_folder = ini_object.get_output_folder()
    output_file = u'編集済み-' + input_file
    output_path = path.join(output_folder, output_file)

    source_pdf = PdfReader(input_path)
    total_page_num = int(source_pdf.Root.Pages.Count)
    for page_num in range(total_page_num):
        canvas_data = get_canvas_data(selection, sb_or_count, page_num + int(start_page_num), ini_object)
        wm_pdf = PdfReader(canvas_data)
        wm_obj = PageMerge().add(wm_pdf.pages[0])[0]
        PageMerge(source_pdf.pages[page_num]).add(wm_obj).render()
    output_data = BytesIO()
    PdfWriter().write(output_data, source_pdf)
    output_data.seek(0)

    save2pdf(output_data, output_path)

if __name__ == "__main__":
    main()
