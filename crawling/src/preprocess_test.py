import os
import docx2txt
import pandas as pd

# customize
from docPreprocessor import DocxDocument
from pdfPreprocessor import PdfDocument

path = "/Users/nahyeonan/Downloads/incruit"

task_list = []
corp_list = []
question_list = []

for file in os.listdir(path):
    ext = file[-3:]
    tmp_qst = []
    tmp_ans = []

    if ext == 'pdf':
        pdObj = PdfDocument(path + "/" + file)
        q, a = pdObj.extractQAList()

        for i in range(len(q)):
            tmp_qst.append(q[i])
            tmp_ans.append(a[i])

    if len(tmp_qst) == 0:
        continue
    question_list.append(tmp_qst)

print(question_list)
    # task_list.append(task)
    # corp_list.append(corpName)
    # question_list.append(q)

# task_df = pd.DataFrame(task_list, columns=['name'])
# task_df.to_csv('task.csv')
#
# corp_df = pd.DataFrame(corp_list, columns=['name'])
# corp_df.to_csv('company.csv')
#
# question_df = pd.DataFrame(question_list, columns=['name'])
# question_df.to_csv('question.csv')