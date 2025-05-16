#!/usr/bin/env python
import sys
import warnings
from AgentDocumentsManager.crew import Agentdocumentsmanager
import os

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the crew.
    """
    inputs = {
        "content": "bản Báo cáo năng suất lao động được tạo ngày nào? Hiện nó đang ở đâu",
    }
    try:
        Agentdocumentsmanager().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
# def run():
#     """
#     Run the crew in a loop.
#     """
#     agent = Agentdocumentsmanager().crew()

#     while True:
#         question = input("Question : ")
#         if question.strip().lower() == 'exit':
#             break
#         inputs = {"content": question}
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
        "content": "bản Báo cáo năng suất lao động được tạo ngày nào? Hiện nó đang ở đâu",
    }
    try:
        Agentdocumentsmanager().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Agentdocumentsmanager().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "content": "bản Báo cáo năng suất lao động được tạo ngày nào? Hiện nó đang ở đâu",
    }
    try:
        Agentdocumentsmanager().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")