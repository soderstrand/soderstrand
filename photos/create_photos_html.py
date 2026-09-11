#!/usr/bin/env python3
from pathlib import Path
import sys
from html import escape
from openpyxl import load_workbook
EXCEL_FILE='PDF_Files.xlsx'
TEMPLATE_FILE='photos_placeholder.html'
OUTPUT_FILE='photos.html'
PDFJS_VIEWER='https://mozilla.github.io/pdf.js/web/viewer.html?file='
def read_excel(path):
    print('Reading Excel File')
    try:
        wb=load_workbook(path, read_only=True, data_only=True); ws=wb.active; rows=[]
        for r in ws.iter_rows(min_row=2, values_only=True):
            vals=list(r)+[None]*5; year,month,day,title,filename=vals[:5]
            if all(v is None or str(v).strip()=='' for v in vals[:5]): continue
            if filename is None or not str(filename).strip(): raise ValueError('A row has no file name in column E.')
            rows.append((title if title is not None else str(filename), str(filename).strip()))
        wb.close(); print('Excel File Read Successfully'); return rows
    except Exception as e:
        print(f'Error reading Excel file: {e}'); return None
def create(rows, template, output):
    try:
        text=Path(template).read_text(encoding='utf-8'); a=text.find('<main class="placeholder-page">'); b=text.find('</main>',a)
        if a<0 or b<0: raise ValueError('Could not find placeholder main section.')
        b+=7
        items=[]
        for title,fn in rows:
            t=escape(str(title).strip() or fn); f=escape(fn,quote=True)
            items.append(f'    <li><a href="{PDFJS_VIEWER}./{f}" target="_blank" rel="noopener">{t}</a> <a href="{f}" download>[Download]</a></li>')
        main='<main class="photos-page">\n  <h2>Photos</h2>\n  <p>Select a title to view the PDF. It opens in PDF.js and can be read or downloaded.</p>\n  <ul>\n'+"\n".join(items)+'\n  </ul>\n</main>'
        Path(output).write_text(text[:a]+main+text[b:],encoding='utf-8'); print('photos.html created'); return True
    except Exception as e: print(f'Error creating photos.html: {e}'); return False
def main():
    d=Path(__file__).resolve().parent; rows=read_excel(d/EXCEL_FILE)
    if rows is None: input('Press Enter to exit...'); sys.exit(1)
    if not (d/TEMPLATE_FILE).exists(): print(f'Error: {TEMPLATE_FILE} not found.'); input('Press Enter to exit...'); sys.exit(1)
    if not create(rows,d/TEMPLATE_FILE,d/OUTPUT_FILE): input('Press Enter to exit...'); sys.exit(1)
    input('Press Enter to exit...')
if __name__=='__main__': main()
