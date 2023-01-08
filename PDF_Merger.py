from ast import Break
from logging import root
import os
import PySimpleGUI as sg
import time
from fillpdf import fillpdfs
from pdfrw import PdfReader, PdfWriter, PdfName


print('Welcome to Perky PDF!')
print('Features: Batch PDF merging/flattenning/conversion and batch printing')
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
        output2 = pdf_fi[:output1] + '_01' + pdf_fi[output1:] #adding _01 at the end of the filename
        fillpdfs.flatten_pdf(pdf_fi, output2) #flattening
        print ('output = ' , output2)
        print ('Flattening PDF...')
        print ('Flatenned PDF(s)...')

     
def printPDF(pdf_files):
    for pdf_fil in pdf_files:
        os.startfile(pdf_fil,'open', '.') #opening the file to give user a reference to what file they're printing
        print('Opening...' + pdf_fil)
        time.sleep(1)
        os.startfile(pdf_fil,'print', '.') #printing and opening up a container for saving output file. Will send to the default printer
        print('Printing...' + pdf_fil)
        time.sleep(1)
        print(f'Printed ' + pdf_fil)
        time.sleep(1)
        input("Press Enter to continue...")
        
#due to an issue with the previous merger function unable to add the AcroForm node to the merged file hence all the fields are empty in the merged file, 
#the solution: https://stackoverflow.com/questions/57008782/pypdf2-pdffilemerger-loosing-pdf-module-in-merged-file is temporarily being used to add the Acroform to the merged file
#Currently working on another way to add the acroform. Credits for this portion of code: A_E.
def mergPDF(pdf_files):
  merger = PdfWriter()
  num = 0
  output_acroform = None
  for pdf_file in pdf_files:
      input = PdfReader(pdf_file,verbose=False)
      merger.addpages(input.pages)
      if PdfName('AcroForm') in input[PdfName('Root')].keys():  # Not all PDFs have an AcroForm node
          source_acroform = input[PdfName('Root')][PdfName('AcroForm')] #declaring the source acroform
          if PdfName('Fields') in source_acroform:
              output_formfields = source_acroform[PdfName('Fields')] #declaring the formfield
          else:
              output_formfields = []
          num2 = 0
          for form_field in output_formfields:
              key = PdfName('T') #declaring the key 't'. Key 't' is for  Edit document text tool/text recognition to allow the document to be editable
              old_name = form_field[key].replace('(','').replace(')','')  # Field names are in the "(name)" format, so renaming form fields so they're not all the same
              form_field[key] = 'FILE_{n}_FIELD_{m}_{on}'.format(n=num, m=num2, on=old_name)
              num2 += 1
          if output_acroform == None:
              # copy the first AcroForm node to the merged PDF
              output_acroform = source_acroform
          else:
              for key in source_acroform.keys():
                  # Add new AcroForms keys if output_acroform already existing
                  if key not in output_acroform:
                      output_acroform[key] = source_acroform[key]
              # Add missing font entries in /DR node of source file
              if (PdfName('DR') in source_acroform.keys()) and (PdfName('Font') in source_acroform[PdfName('DR')].keys()):
                  if PdfName('Font') not in output_acroform[PdfName('DR')].keys():
                      # if output_acroform is missing entirely the /Font node under an existing /DR, simply add it
                      output_acroform[PdfName('DR')][PdfName('Font')] = source_acroform[PdfName('DR')][PdfName('Font')]
                  else:
                      # else add new fonts only
                      for font_key in source_acroform[PdfName('DR')][PdfName('Font')].keys():
                          if font_key not in output_acroform[PdfName('DR')][PdfName('Font')]:
                              output_acroform[PdfName('DR')][PdfName('Font')][font_key] = source_acroform[PdfName('DR')][PdfName('Font')][font_key]
          if PdfName('Fields') not in output_acroform:
              output_acroform[PdfName('Fields')] = output_formfields
          else:
              # Add new fields
              output_acroform[PdfName('Fields')] += output_formfields
      num +=1
  merger.trailer[PdfName('Root')][PdfName('AcroForm')] = output_acroform
  merger.write("Merged PDF.pdf")

  print('Merged Succesfully')
  print('Merged PDF.pdf is located at the location of the application.')
    

    
#getting files
filess = sg.popup_get_file('Perky PDF Merger: Please Select PDFs', multiple_files=True)
newfile = filess.replace(";",",") #turning the list format from user input into a working python list 
pdf_files = newfile.split(",")

print('Selected Files: ', pdf_files)
for pdf_file in pdf_files:
    if pdf_file.endswith('_01.pdf') == True: #if pdf ends with _01.pdf that was added to flattened pdf files, the application will know to only merge it
        print('Flattened PDF. Merging in progress...')
        mergPDF(pdf_files)
        break
    elif len(pdf_files) == 1:
        print('Number of files = 1. Flattening in progress...') 
        if pdf_file.endswith('.pdf') == True: #if there is only 1 pdf file, then it will flatten. currently, you can't batch print PDFs.
            print('Flattening PDF files...')
            flattenPDF(pdf_files)
            break
        else:
            print('Not a PDF file... Will print') #if there is only 1 non pdf file, then it will give print option to convert to PDF
            printPDF(pdf_files)
            break
    else:
        print('Flattening and Merging in progress...')
        if pdf_file.endswith('.pdf') == True: #if there are more than one pdf files, then it will flatten and merge
            print('PDF files: Flattening and Merging.')
            flattenPDF(pdf_files)
            mergPDF(pdf_files)
            break
        else:
            print ('Not PDF Files: Printing...')
            printPDF(pdf_files) # if there are more than one non pdf files, then it will give print option
            break
input("Press Enter to exit...")










    
