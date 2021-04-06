import re

class DocxDocument:
    def __init__(self, text):
        self.text = text
        self.numline = len(text)

    def extractCorpName(self):
       reg = re.compile(r'\[(.+)\](.+)')

       m = reg.match(self.text[0])
       if m is None:
           self.corpName = self.text[0]
           return self.corpName

       self.corpName = m.group(1).strip()

       return self.corpName

    def extractTask(self):  
        if len(self.text) >= 2:
            idx = self.text[1].find(':')
            self.task = self.text[1][idx+1:].strip()
        
            return self.task
        
        return self.text

    def extractQAList(self):
        self.content = self.text[2:]

        reg = re.compile(r'^\d+\.\s')
        questions = []
        answers = []
        answer = ''

        for line in self.content:
            m = reg.match(line)

            if m is None:
                answer += (line + ' ')
            else:
                if len(questions) > 0:
                    answers.append(answer)
                    answer = ''
                questions.append(line)

        answers.append(answer)
        self.questions = questions
        self.answers = answers

        return (self.questions, self.answers)