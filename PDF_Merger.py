from ast import Break
from PyPDF2 import PdfFileMerger
import os
import PySimpleGUI as sg
import time
from fillpdf import fillpdfs

print('Welcome to Perky PDF!')
print('Features: Batch PDF merging/flatenning/conversion and batch printing')
print('\n')
print('How to set up: change your default printer as needed.')
print('Non-PDF Printing: Change your default printer to a physical printer of your choice.')
print('PDF Conversion: Change your default printer to a virtual printer -- Microsoft print to PDF.')
print('Press enter after you save a file to a PDF to continue.')
print('\n')
print('How to use: select your document(s) and click okay')
print('\n')

def flattenPDF(pdf_files):
    for pdf_fi in pdf_files:
        output1 = pdf_fi.find('.pdf')
        output2 = pdf_fi[:output1] + '_01' + pdf_fi[output1:]
        fillpdfs.flatten_pdf(pdf_fi, output2)
        print ('output = ' , output2)
        print ('Flattening PDF...')
        print ('Flatenned PDF(s)...')

     
def printPDF(pdf_files):
    for pdf_fil in pdf_files:
        os.startfile(pdf_fil,'open', '.')
        print('Opening...' + pdf_fil)
        time.sleep(1)
        os.startfile(pdf_fil,'print', '.')
        print('Printing...' + pdf_fil)
        time.sleep(1)
        print(f'Printed ' + pdf_fil)
        time.sleep(1)
        input("Press Enter to continue...")
        

def mergPDF(pdf_files):
    #create an instance for PdfFileMerger
    merger = PdfFileMerger()

    #Merging PDF files
    for pdf_file in pdf_files:
       merger.append(pdf_file, "rb")
    merger.write("Merged PDF.pdf")
    print('Merged Succesfully')
    print('Merged PDF.pdf is located at the location of the application.')
    merger.close()

    
#merge
filess = sg.popup_get_file('Perky PDF Merger: Please Select PDFs', multiple_files=True)
newfile = filess.replace(";",",")
pdf_files = newfile.split(",")

print('Selected Files: ', pdf_files)
for pdf_file in pdf_files:
    if pdf_file.endswith('1.pdf') == True:
        print('Flattened PDF. Merging in progress...')
        mergPDF(pdf_files)
        break
    elif len(pdf_files) == 1:
        print('Number of files = 1. Flattening in progress...')
        if pdf_file.endswith('.pdf') == True:
            print('Flattening PDF files...')
            flattenPDF(pdf_files)
            break
        else:
            print('Not a PDF file... Will print')
            printPDF(pdf_files)
            break
    else:
        print('Flattening and Merging in progress...')
        if pdf_file.endswith('.pdf') == True:
            print('PDF files: Flattening and Merging.')
            flattenPDF(pdf_files)
            mergPDF(pdf_files)
            break
        else:
            print ('Not PDF Files: Printing...')
            printPDF(pdf_files)
            Break
input("Press Enter to exit...")













    
