import sys
import pdfquery

fname = sys.argv[1]
pdf = pdfquery.PDFQuery(fname + ".pdf")
pdf.load()
pdf.tree.write(fname + ".xml", pretty_print=True, encoding="utf-8")