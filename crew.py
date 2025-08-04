import os
from crewai import Agent, Crew, Process, Task,LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import MCPServerAdapter
from typing import Union,Optional
from dotenv import load_dotenv
load_dotenv()

groq_api_key= os.getenv('GROQ_API_KEY')
os.environ['GROQ_API_KEY'] = "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"
llm = LLM(
    model='groq/llama-3.3-70b-versatile')

@CrewBase
class Dbcrew():
    """Dbcrew crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    mcp_server_params: Union[list[MCPServerAdapter | dict[str, str]], MCPServerAdapter, dict[str, str]]  = {
        "url": "http://127.0.0.1:8001/sse/",
        "transport": "sse",
    }
   
    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'], # type: ignore[index]
            verbose=True,
            llm=llm,
            tools=self.get_mcp_tools()
        )

    

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'], # type: ignore[index]
        )

   
    @crew
    def crew(self) -> Crew:
        """Creates the Dbcrew crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
