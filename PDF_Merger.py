from fileinput import filename
from logging import RootLogger
from ntpath import join
from pathlib import Path
from PyPDF2 import PdfFileMerger, PdfFileReader
import os
import PySimpleGUI as sg
from pathlib import Path



def mergPDF(pdf_files):
    #create an instance for PdfFileMerger
    merger = PdfFileMerger()

    #Merging PDF files
    for pdf_file in pdf_files:
       merger.append(pdf_file, "rb")
    merger.write("Merged PDF.pdf")
    merger.close()

filess = sg.popup_get_file('Perky PDF Merger: Please Select PDFs', multiple_files=True)

newfile = filess.replace(";",",")
pdf_files = newfile.split(",")
print(pdf_files)
mergPDF(pdf_files)



    
