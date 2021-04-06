import re

class PdfDocument:
    def __init__(self, path):
        self.text = self.readPdf(path)
        self.numLine = len(self.text)

    def readPdf(self, pdf):
        from pdfminer.converter import TextConverter
        from pdfminer.layout import LAParams
        from pdfminer.pdfdocument import PDFDocument
        from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
        from pdfminer.pdfpage import PDFPage
        from pdfminer.pdfparser import PDFParser
        from io import StringIO

        ret = StringIO()
        with open(pdf, 'rb') as f:
            parser = PDFParser(f)
            doc = PDFDocument(parser)
            rsrcmr = PDFResourceManager()
            device = TextConverter(rsrcmr, ret, laparams=LAParams())
            interpreter = PDFPageInterpreter(rsrcmr, device)
            for page in PDFPage.create_pages(doc):
                interpreter.process_page(page)

        temp = str(ret.getvalue())
        lines = []
        for line in temp.splitlines():
            line = line.strip()
            if line == '\n' or line == '' or line == ' ':
                continue
            lines.append(line)
        return lines

    def extractCorpName(self):
        if self.text[0][-3:] == '모음편':
            print('모음편')
        else:
            print(self.text[0][-3:])
        return self.text[0][-3:]

    def extractQAList(self):
        reg = re.compile(r'^\d+\.\s')

        ans = ''
        question = []
        answer = []
        for line in self.text:
            m = reg.match(line)

            if m is None:
                ans += (line + ' ')
            else:
                if len(question) > 0:
                    answer.append(ans)
                    ans = ''
                question.append(line)

        answer.append(ans)

        self.question = question
        self.answer = answer

        return (self.question, self.answer)