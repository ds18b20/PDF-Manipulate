#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
# from PyQt4.QtCore import *
# from PyQt4.QtGui import *
from PySide.QtCore import *
from PySide.QtGui import *
from SplitPDF import SplitPDF
from MergePDF import MergePDF
from AddText2PDF import add_text
from RotatePDF import PdfRotate
from functools import reduce


class CentralWidget(QWidget):
    def __init__(self, parent=None):
        super(CentralWidget, self).__init__(parent)

        self.__input_file_path = ''
        self.__input_file_path_list = []
        self.__output_file_path = ''
        self.input_text = QLineEdit(self)
        self.output_text = QLineEdit(self)
        self.sb_text = QLineEdit(self)
        self.sb_text.setText('SB-')
        self.start_page_text = QLineEdit(self)
        self.page_count_text = QLineEdit(self)
        self.rotate_degree_text = QLineEdit(self)

        self.__radio_status = "SB"

        grid = QGridLayout()
        grid.addWidget(self.function_select_group())
        grid.addWidget(self.create_input_group())
        grid.addWidget(self.create_output_group())
        # grid.addWidget(self.function_select_group())
        grid.addWidget(self.create_option_group())
        # grid.addLayout(self.create_option_group(), 4, 0)
        grid.addWidget(self.create_run_group())
        self.setLayout(grid)
    
    def radio_status_1(self):
        self.__radio_status = "SB"

    def radio_status_2(self):
        self.__radio_status = "Instruction"

    def radio_status_3(self):
        self.__radio_status = "Split"

    def radio_status_4(self):
        self.__radio_status = "Merge"

    def radio_status_5(self):
        self.__radio_status = "Rotate"

    def function_select_group(self):
        group_box = QGroupBox("Select function")

        radio1 = QRadioButton("SB(A4)")
        radio1.toggled.connect(self.radio_status_1)
        radio2 = QRadioButton("Instruction(A3)")
        radio2.toggled.connect(self.radio_status_2)
        radio3 = QRadioButton("Split")
        radio3.toggled.connect(self.radio_status_3)
        radio4 = QRadioButton("Merge")
        radio4.toggled.connect(self.radio_status_4)
        radio5 = QRadioButton("Rotate")
        radio5.toggled.connect(self.radio_status_5)
        # self.rb.setFocusPolicy(Qt.NoFocus)
        radio1.setChecked(True)

        h_box = QHBoxLayout()
        h_box.addStretch(1)
        h_box.addWidget(radio1)
        h_box.addWidget(radio2)
        h_box.addWidget(radio3)
        h_box.addWidget(radio4)
        h_box.addWidget(radio5)

        group_box.setLayout(h_box)

        return group_box

    def create_input_group(self):
        group_box = QGroupBox("Input file")

        # input_text = QLineEdit(self)
        input_button = QPushButton('Browse', self)
        input_button.clicked.connect(self.input_click_method)

        h_box = QHBoxLayout()
        h_box.addWidget(self.input_text)
        h_box.addWidget(input_button)

        group_box.setLayout(h_box)

        return group_box

    def create_output_group(self):
        group_box = QGroupBox("Output file")

        # output_text = QLineEdit()
        output_button = QPushButton('Browse', self)
        output_button.clicked.connect(self.output_click_method)

        h_box = QHBoxLayout()
        h_box.addWidget(self.output_text)
        h_box.addWidget(output_button)
        group_box.setLayout(h_box)

        return group_box

    def create_option_group(self):

        group_box = QGroupBox("Option")

        label_sb = QLabel('SB:')
        label_start_page = QLabel('StartPage:')
        label_page_count = QLabel('PageCount:')
        label_rotate_degree = QLabel('RotateDegree:')

        h_box = QHBoxLayout()
        h_box.addStretch(1)

        h_box.addWidget(label_sb)
        h_box.addWidget(self.sb_text)
        h_box.addWidget(label_start_page)
        h_box.addWidget(self.start_page_text)
        h_box.addWidget(label_page_count)
        h_box.addWidget(self.page_count_text)
        h_box.addWidget(label_rotate_degree)
        h_box.addWidget(self.rotate_degree_text)

        group_box.setLayout(h_box)

        return group_box

    def create_run_group(self):
        group_box = QGroupBox("Run")

        run_button = QPushButton('Run', self)
        run_button.clicked.connect(self.run_click_method)
        close_button = QPushButton('Close', self)
        close_button.clicked.connect(self.close_click_method)

        h_box = QHBoxLayout()
        h_box.addStretch(1)
        h_box.addWidget(run_button)
        h_box.addWidget(close_button)

        group_box.setLayout(h_box)

        return group_box
        
    def open_file_name_dialog(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(parent=self,
                                                   caption="QFileDialog.getOpenFileNames()",
                                                   directory="",
                                                   filter="PDF Files (*.pdf);;All Files (*)",
                                                   options=options)
        return file_path

    def open_file_names_dialog(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        file_path_list, _ = QFileDialog.getOpenFileNames(parent=self,
                                                         caption="QFileDialog.getOpenFileNames()",
                                                         directory="",
                                                         filter="PDF Files (*.pdf);;All Files (*)",
                                                         options=options)
        return file_path_list

    def save_file_dialog(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getSaveFileName(parent=self,
                                                   caption="QFileDialog.getOpenFileNames()",
                                                   directory="",
                                                   filter="PDF Files (*.pdf);;All Files (*)",
                                                   options=options)
        return file_path
            
    def input_click_method(self):
        # print(self.radio_status)
        if self.__radio_status == "Merge":
            self.__input_file_path_list = self.open_file_names_dialog()
            if self.__input_file_path_list:
                file_list = [os.path.basename(x) for x in self.__input_file_path_list]
                list2string = reduce(lambda x, y: x + ',' + y, file_list)
                self.input_text.setText(list2string)
                # print(list2string)
            # print(self.__input_file_path_list)

        else:
            self.__input_file_path = self.open_file_name_dialog()
            if self.__input_file_path:
                base_name = os.path.basename(self.__input_file_path)
                self.input_text.setText(base_name)
        # print('Input Clicked')

    def output_click_method(self):
        self.__output_file_path = self.save_file_dialog()
        if self.__output_file_path:
            base_name = os.path.basename(self.__output_file_path)
            if base_name.split('.')[-1] != 'pdf':
                base_name = base_name + '.pdf'
                self.__output_file_path = self.__output_file_path + '.pdf'
            self.output_text.setText(base_name)
        # print('Output Clicked')
        
    def run_click_method(self):
        # print('Run Clicked')
        # print(self.input_text.text() == '')
        # print(self.output_text.text() == '')

        if self.input_text.text() and self.output_text.text():
            self.select_function()
        else:
            show_message("Select INPUT & OUTPUT")

    def close_click_method(self):
        self.dummy()
        quit_app()
        # print('Close Clicked')

    def select_function(self):
        if self.__radio_status == "SB":
            add_text(self.__input_file_path, self.__output_file_path, '1', self.start_page_text.text(),
                     self.sb_text.text())
            show_message("SB Finished!")
        elif self.__radio_status == "Instruction":
            add_text(self.__input_file_path, self.__output_file_path, '2', self.start_page_text.text(),
                     self.page_count_text.text())
            show_message("Instruction Finished!")
        elif self.__radio_status == 'Split':
            pdf = SplitPDF(self.__input_file_path, self.__output_file_path)
            pdf.split()
            show_message("Split Finished!")
        elif self.__radio_status == "Merge":
            pdf = MergePDF(self.__input_file_path_list, self.__output_file_path)
            pdf.merge()
            show_message("Merge Finished!")
        elif self.__radio_status == "Rotate":
            pdf = PdfRotate(self.__input_file_path, self.__output_file_path, self.rotate_degree_text.text())
            pdf.rotate()
            show_message("Rotate Finished!")
        else:
            pass

    def dummy(self):
        pass


def show_message(msg: str):
        QMessageBox.information(None, "message", msg, QMessageBox.Ok)


def quit_app():
    QCoreApplication.instance().quit()


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("PDF manipulate")
        self.setWindowIcon(QIcon('ebr.png')) 
        self.resize(600, 300)
        
        """file menu"""
        # Create open action
        open_action = QAction(QIcon('open.png'), '&Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('Open document')
        open_action.triggered.connect(self.open_call)

        # Create exit action
        exit_action = QAction(QIcon('exit.png'), '&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(self.exit_call)
        # Create menu bar and add action
        # /file_menu/
        menu_bar = self.menuBar()
        self.file_menu = menu_bar.addMenu('&File')
        self.file_menu.addAction(open_action)
        self.file_menu.addAction(exit_action)
        
        """about_menu"""
        # Create new action
        help_action = QAction(QIcon('help.png'), '&Help', self)
        help_action.setShortcut('F1')
        help_action.setStatusTip('Get help')
        help_action.triggered.connect(self.help_call)

        # Create exit action
        info_action = QAction(QIcon('info.png'), '&Info', self)
        info_action.setShortcut('Ctrl+I')
        info_action.setStatusTip('Get info')
        info_action.triggered.connect(self.info_call)
        
        # Create menu bar and add action
        # /about_menu/
        self.about_menu = menu_bar.addMenu('&About')
        self.about_menu.addAction(help_action)
        self.about_menu.addAction(info_action)

        # Central Widget
        self.setCentralWidget(CentralWidget(self))

        # Status Bar
        self.status_bar = QStatusBar(self)
        self.status_bar.showMessage("Here is Status Bar", 5000)
        self.setStatusBar(self.status_bar)

    def open_call(self):
        self.dummy()
        # print('open')
        # self.editor.setPlainText(self.__file_path)

    def exit_call(self):
        self.dummy()
        QCoreApplication.instance().quit()
        # print('Exit')
        
    def help_call(self):
        self.dummy()
        # print('Help')
        
    def info_call(self):
        self.dummy()
        # print('Info')

    def dummy(self):
        pass


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
