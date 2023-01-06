from fileinput import filename
from logging import RootLogger
from ntpath import join
from pathlib import Path
from PyPDF2 import PdfFileMerger, PdfFileReader
import os
import PySimpleGUI as sg
from pathlib import Path
import win32print as wp
from subprocess import call
import time

def flattenPDF(pdf_files):
    for pdf_fil in pdf_files:
        printer = wp.OpenPrinter('Microsoft Print to PDF')
        os.startfile(pdf_fil,'open', '.')
        print('Opening...' + pdf_fil)
        time.sleep(1)
        os.startfile(pdf_fil,'print', '.')
        print('Printing...' + pdf_fil)
        time.sleep(2)
        print(f'Printed ' + pdf_fil)
        time.sleep(2)

def mergPDF(pdf_files):
    #create an instance for PdfFileMerger
    merger = PdfFileMerger()

    #Merging PDF files
    for pdf_file in pdf_files:
       merger.append(pdf_file, "rb")
    merger.write("Merged PDF.pdf")
    print('Merged Succesfully')
    merger.close()
    
#merge
filess = sg.popup_get_file('Perky PDF Merger: Please Select PDFs', multiple_files=True)
newfile = filess.replace(";",",")
pdf_files = newfile.split(",")

#flatten
#newfile1 = filess.replace(";","z")
#newstring = newfile1.replace('C:/Users/parke/Desktop/', '')
#newpdfilesh = newstring.split("z")

print(pdf_files)
#print(newpdfilesh)
for pdf_file in pdf_files:
    if pdf_file.endswith('1.pdf') == True:
        print('Flattened PDF. Merging in progress...')
        mergPDF(pdf_files)
        break
    elif len(pdf_files) == 1:
        print('Number of files = 1. Flattening in progress...')
        flattenPDF(pdf_files)
        break
    else:
        print('Flattening and Merging in progress...')
        flattenPDF(pdf_files)
        mergPDF(pdf_files)
        break












    
