#!/usr/bin/env python3

"""
Create photos.html from PDF_Files.xlsx.

Files expected in the same directory as this program:
    PDF_Files.xlsx
    photos_placeholder.html
    all PDF files

Excel columns:
    A = Year
    B = Month
    C = Day
    D = Title
    E = File Name
"""

from pathlib import Path
from urllib.parse import quote
from html import escape
import sys

from openpyxl import load_workbook


EXCEL_FILE = "PDF_Files.xlsx"
TEMPLATE_FILE = "photos_placeholder.html"
OUTPUT_FILE = "photos.html"

# The directory containing photos.html and the PDF files.
PDF_DIRECTORY_URL = "https://soderstrand.com/photos/"

# Mozilla-hosted PDF.js viewer.
PDFJS_VIEWER = "https://mozilla.github.io/pdf.js/web/viewer.html?file="


def read_excel(excel_path):
    print("Reading Excel File")

    try:
        workbook = load_workbook(
            filename=excel_path,
            read_only=True,
            data_only=True
        )
        worksheet = workbook.active

        rows = []

        for excel_row in worksheet.iter_rows(min_row=2, values_only=True):
            values = list(excel_row) + [None] * 5
            year, month, day, title, filename = values[:5]

            # Ignore completely blank rows.
            if all(
                value is None or str(value).strip() == ""
                for value in (year, month, day, title, filename)
            ):
                continue

            if filename is None or str(filename).strip() == "":
                raise ValueError(
                    "A row has no PDF file name in column E."
                )

            if title is None or str(title).strip() == "":
                display_title = str(filename).strip()
            else:
                display_title = str(title).strip()

            rows.append({
                "year": year,
                "month": month,
                "day": day,
                "title": display_title,
                "filename": str(filename).strip()
            })

        workbook.close()
        print("Excel File Read Successfully")
        return rows

    except Exception as exc:
        print(f"Error reading Excel file: {exc}")
        return None


def create_photos_html(rows, template_path, output_path):
    try:
        template = Path(template_path).read_text(encoding="utf-8")

        # Replace only the placeholder <main> section. This preserves
        # the site's existing CSS, JavaScript, header, navigation,
        # and footer.
        start_marker = '<main class="placeholder-page">'
        end_marker = "</main>"

        start = template.find(start_marker)
        if start == -1:
            raise ValueError(
                'Could not find <main class="placeholder-page"> '
                "in the placeholder HTML file."
            )

        end = template.find(end_marker, start)
        if end == -1:
            raise ValueError(
                "Could not find the closing </main> tag."
            )

        end += len(end_marker)

        html_items = []

        for row in rows:
            title = row["title"]
            filename = row["filename"]

            # Encode the filename for use in an HTTP URL.
            # This handles spaces and other special characters.
            encoded_filename = quote(filename, safe="")

            # IMPORTANT: PDF.js is hosted on mozilla.github.io.
            # Therefore "./filename.pdf" would be relative to the
            # PDF.js website, not to soderstrand.com. Give PDF.js
            # the complete URL of the PDF instead.
            pdf_url = PDF_DIRECTORY_URL + encoded_filename

            # Encode the complete PDF URL for the PDF.js file parameter.
            pdfjs_url = PDFJS_VIEWER + quote(pdf_url, safe="")

            safe_title = escape(title)
            safe_filename = escape(filename, quote=True)
            safe_pdfjs_url = escape(pdfjs_url, quote=True)

            html_items.append(
                '    <li>\n'
                f'      <a href="{safe_pdfjs_url}" target="_blank" rel="noopener">\n'
                f'        {safe_title}\n'
                '      </a>\n'
                f'      <a href="{safe_filename}" download>[Download]</a>\n'
                '    </li>'
            )

        main_section = (
            '<main class="photos-page">\n'
            '  <h2>Photos</h2>\n'
            '  <p>Select a title to view the PDF. It opens in PDF.js and can be read or downloaded.</p>\n'
            '  <ul>\n'
            + "\n".join(html_items)
            + '\n  </ul>\n'
            '</main>'
        )

        new_html = template[:start] + main_section + template[end:]

        Path(output_path).write_text(
            new_html,
            encoding="utf-8"
        )

        print("photos.html created")
        return True

    except Exception as exc:
        print(f"Error creating photos.html: {exc}")
        return False


def main():
    script_directory = Path(__file__).resolve().parent

    excel_path = script_directory / EXCEL_FILE
    template_path = script_directory / TEMPLATE_FILE
    output_path = script_directory / OUTPUT_FILE

    rows = read_excel(excel_path)

    if rows is None:
        input("Press Enter to exit...")
        sys.exit(1)

    if not template_path.exists():
        print(
            f"Error: placeholder HTML file not found: "
            f"{TEMPLATE_FILE}"
        )
        input("Press Enter to exit...")
        sys.exit(1)

    if not create_photos_html(
        rows,
        template_path,
        output_path
    ):
        input("Press Enter to exit...")
        sys.exit(1)

    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
