from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource
from crewai.memory import LongTermMemory, ShortTermMemory, EntityMemory
from crewai.memory.storage.rag_storage import RAGStorage
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage
from .tools import DocumentQueryTool, LocationQueryTool, UserInfoQueryTool

# from crewai_tools import (
#     DirectoryReadTool,
#     FileReadTool,
#     SerperDevTool,
#     WebsiteSearchTool
# )

@CrewBase
class DocumentsManager():
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    text_source = TextFileKnowledgeSource(
            file_paths=["csv_info.txt","csv_schema.txt"]
    )

    @agent
    def data_analyst_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['data_analyst_agent'],
            verbose=True,
            tools=[DocumentQueryTool(), LocationQueryTool(), UserInfoQueryTool()],
            max_iter=5 # Vòng lặp tối đa khi thực hiện task
        )
    
    @task
    def data_analyst_task(self) -> Task:
        return Task(
            config=self.tasks_config['data_analyst_task'],
        )
    
    @crew
    def crew(self) -> Crew:
        """"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            memory=True,
            verbose=True,
            # embedder={
            #     "provider": "openai",
            #     "config": {
            #         "model": 'text-embedding-3-small'
            #     }
            # },
            # Long-term memory for persistent storage across sessions
            long_term_memory = LongTermMemory(
                storage=LTMSQLiteStorage(
                    db_path="memories/long_term_memory_storage.db"
                )
            ),
            # external_memory=ExternalMemory(
            #         embedder_config={
            #             "provider": "mem0", 
            #             "config": {"user_id": "truong.bit-8686"}} # you can provide an entire Mem0 configuration
            # ),
            # Short-term memory for current context using RAG
            short_term_memory = ShortTermMemory(
                storage = RAGStorage(
                        embedder_config={
                            "provider": "openai",
                            "config": {
                                "model": 'text-embedding-3-small'
                            }
                        },
                        type="short_term",
                        path="memories/"
                )
            ),
            # # Entity memory for tracking key information about entities
            entity_memory = EntityMemory(
                storage=RAGStorage(
                    embedder_config={
                        "provider": "openai",
                        "config": {
                            "model": 'text-embedding-3-small'
                        }
                    },
                    type="short_term",
                    path="memories/"
                )
            ),
            knowledge_sources=[self.text_source], # Dùng chung cho mọi agent
            # chat_llm="gpt-4o-mini",
        )
