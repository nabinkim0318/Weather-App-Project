"""
Module: services.export_service
-------------------------------

This module provides functionality for exporting application data into various
formats such as CSV, JSON, and PDF. It handles the transformation of internal data
structures into user-friendly, standardized file formats that can be downloaded,
shared, or archived.

Key Responsibilities:
- Convert weather data, user preferences, and other relevant application data
  into exportable formats while preserving data integrity and readability.
- Support multiple output formats:
    - CSV: Generate comma-separated value files suitable for spreadsheet
      applications and data analysis.
    - JSON: Produce well-formatted JSON files for interoperability with other
      systems or APIs.
    - PDF: Create formatted PDF documents for printing and presentation,
      including styled tables and charts where applicable.
- Manage file generation in-memory or via temporary storage to optimize performance
  and resource usage.
- Handle large datasets efficiently, including pagination or streaming exports if
  necessary.
- Ensure proper encoding, escaping, and formatting to prevent data corruption.
- Provide customizable export options, such as selecting date ranges, data fields,
  and output file naming conventions.
- Integrate with web framework response mechanisms to facilitate seamless file
  downloads in API endpoints.
- Log export activities for auditing and debugging purposes.

Error Handling:
- Validate input data before export and handle serialization errors gracefully.
- Manage file generation errors, such as disk write failures or memory constraints.
- Return meaningful error messages or codes to calling APIs or services.

Integration Points:
- Internal data sources, including database query results and in-memory objects.
- File system or cloud storage for temporary file handling (if applicable).
- Web framework response objects to stream or send files to clients.

This module abstracts the complexities of data export and ensures consistent,
reliable, and performant generation of exportable content across supported formats.
"""
import io
import csv
import json
from typing import List, Dict
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def export_to_csv(data: List[Dict]) -> io.StringIO:
    """Generate CSV content from list of dictionaries."""
    if not data:
        raise ValueError("No data available for CSV export.")
    
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)
    output.seek(0)
    return output


def export_to_json(data: List[Dict], pretty: bool = False) -> str:
    """Generate JSON string from list of dictionaries."""
    if not data:
        raise ValueError("No data available for JSON export.")
    
    return json.dumps(data, indent=4 if pretty else None)


def export_to_pdf(data: List[Dict]) -> io.BytesIO:
    """Generate a basic PDF summary from list of dictionaries."""
    if not data:
        raise ValueError("No data available for PDF export.")
    
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    y = height - 40
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y, "Weather Data Export")
    p.setFont("Helvetica", 10)
    y -= 30

    for row in data:
        line = ", ".join(f"{key}: {value}" for key, value in row.items())
        p.drawString(50, y, line)
        y -= 15
        if y < 50:
            p.showPage()
            y = height - 40

    p.save()
    buffer.seek(0)
    return buffer