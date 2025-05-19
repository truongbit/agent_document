#!/usr/bin/env python
import sys
import warnings
from documents_manager.crew import DocumentsManager
import os

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the crew.
    """
    inputs = {
        "question": "Bạn là ai. Đây là hệ thống gì?",
    }
    try:
        DocumentsManager().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
# def run():
#     """
#     Run the crew in a loop.
#     """
#     agent = DocumentsManager().crew()

#     while True:
#         question = input("Question : ")
#         if question.strip().lower() == 'exit':
#             break
#         inputs = {"question": question}
#         try:
#             result = agent.kickoff(inputs=inputs)
#             print('\033[94mAnswer : \033[0m',result)
#         except Exception as e:
#             print(f"Answer error: {e}")

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "question": "",
    }
    try:
        DocumentsManager().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        DocumentsManager().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "question": "",
    }
    try:
        DocumentsManager().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")