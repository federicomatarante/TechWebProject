import os
import tempfile
from io import BytesIO

import pdfkit
from django.http import FileResponse


def send_pdf(html_content, file_name):
    pdf_data = pdfkit.from_string(html_content, False)
    buffer = BytesIO(pdf_data)
    response = FileResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{file_name}.pdf"'
    return response
