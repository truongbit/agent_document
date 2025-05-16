#!/usr/bin/env python
import sys
import warnings
from AgentDocumentsManager.crew import Agentdocumentsmanager
import os

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# def run():
#     """
#     Run the crew.
#     """
#     inputs = [
#         {
#             "question" : "anh dũng đã thêm những tài liệu nào vào hệ thống?"
#         },
#          {
#             "question" : "bản tài liệu đầu tiên được thêm ngày nào"
#         },
#         {
#             "question" : "hiện giờ nó đang ở đâu"
#         }
#     ]
#     # inputs = {
#     #     "question": "bản Báo cáo năng suất lao động được tạo ngày nào? Hiện nó đang ở đâu",
#     # }
    
#     try:
#         Agentdocumentsmanager().crew().kickoff_for_each(inputs=inputs)
#     except Exception as e:
#         raise Exception(f"An error occurred while running the crew: {e}")
def run():
    """
    Run the crew in a loop.
    """
    agent = Agentdocumentsmanager().crew()

    while True:
        question = input("Question : ")
        if question.strip().lower() == 'exit':
            break
        inputs = {"content": question}
        try:
            result = agent.kickoff(inputs=inputs)
            print('\033[94mAnswer : \033[0m',result)
        except Exception as e:
            print(f"Answer error: {e}")