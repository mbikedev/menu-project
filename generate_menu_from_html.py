#!/usr/bin/env python3
"""
Generate a professional PDF menu from the HTML menu editor
"""

import os
import sys

try:
    from weasyprint import HTML, CSS
except ImportError:
    print("Installing weasyprint...")
    os.system("pip install weasyprint")
    from weasyprint import HTML, CSS

def generate_pdf():
    """Generate PDF from the HTML menu"""

    # Path to the HTML file
    html_file = os.path.join(os.path.dirname(__file__), 'menu_editor.html')

    # Path to the output PDF
    output_pdf = os.path.join(os.path.dirname(__file__), 'east_west_menu_final.pdf')

    if not os.path.exists(html_file):
        print(f"Error: HTML file not found at {html_file}")
        return False

    print(f"Reading HTML from: {html_file}")
    print(f"Generating PDF...")

    try:
        # Additional CSS for PDF optimization
        pdf_css = CSS(string='''
            @page {
                size: A4;
                margin: 0.5cm;
            }

            body {
                background: white !important;
            }

            .actions {
                display: none !important;
            }

            .menu-item input,
            .menu-item textarea {
                border: none !important;
                background: transparent !important;
                padding: 0 !important;
                pointer-events: none;
            }

            .item-name input {
                font-size: 16px !important;
                font-weight: bold !important;
                color: #1a5d3f !important;
            }

            .item-description textarea {
                font-size: 14px !important;
                color: #4b5563 !important;
                height: auto !important;
            }

            .item-price input {
                font-size: 18px !important;
                font-weight: bold !important;
                color: #d4af37 !important;
                text-align: right !important;
            }

            /* Page breaks */
            .section {
                page-break-inside: avoid;
            }

            .menu-item {
                page-break-inside: avoid;
            }
        ''')

        # Generate PDF
        HTML(filename=html_file).write_pdf(
            output_pdf,
            stylesheets=[pdf_css]
        )

        print(f"✓ PDF generated successfully!")
        print(f"✓ Saved to: {output_pdf}")
        return True

    except Exception as e:
        print(f"Error generating PDF: {e}")
        return False

if __name__ == "__main__":
    success = generate_pdf()
    sys.exit(0 if success else 1)
