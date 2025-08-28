from dotenv import load_dotenv
import os
load_dotenv()
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_experimental.tools import PythonREPLTool
from langchain_experimental.agents import create_csv_agent
from langchain.agents import Tool
# from langchain.tools import PythonREPLTool

def main():
    print("start...")
    instructions = """
        You are a Python coding assistant.

        - You can write and run Python code using the PythonREPL tool.  
        - Use PythonREPL whenever a user asks you to calculate, simulate, analyze, or verify something that requires execution.  
        - Always explain what you are doing before running code.  
        - If the answer can be given directly without running code, still you should execute the code.  
        - After running code, summarize the result in plain English so it’s easy to understand.  
        - Make sure the code you write is clean, readable, and correct.  
        - Never execute dangerous operations (like file deletion, system shutdown, or network access).
        - If it does not seem like you can write the code to answer the question, just say you don't know.
        - You can use the Python_REPL tool to execute Python code.
        - You ARE allowed to write to files (e.g., save images, text, or data) and read files when needed.
    """

    from langchain.prompts import PromptTemplate

    # ✅ Updated base prompt with {tools} and {tool_names}
    base_prompt = PromptTemplate(
        input_variables=["input", "agent_scratchpad", "tools", "tool_names"],
        template="""
    You are a Python coding assistant. You can execute Python code in a safe REPL environment. 

    {instructions}

    You have access to the following tools:
    {tools}

    When you use a tool, follow this format strictly:

    Question: the input question you must answer
    Thought: your reasoning about what to do
    Action: the action to take, must be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action

    (You can repeat Thought/Action/Observation as needed)

    Final Answer: the final result of the question.

    Begin!

    Question: {input}
    {agent_scratchpad}
    """
    )

    # Keep your partial usage for injecting `instructions`
    prompt = base_prompt.partial(instructions=instructions)

    tools = [PythonREPLTool()]
    python_agent = create_react_agent(
        llm=ChatOpenAI(temperature=0, model="gpt-4-turbo"), 
        tools=tools,
        prompt=prompt
    )

    """NOTE: Higher models like "gpt-5 does not support stop" parameter yet. so avpid using them here 
    Error code: 400 - {'error': {'message': "Unsupported parameter: 'stop' is not supported with this model.",
      'type': 'invalid_request_error', 'param': 'stop', 'code': 'unsupported_parameter'}}"""
    
    python_agent_executor = AgentExecutor(agent=python_agent, 
                                   tools=tools, 
                                   verbose=True,
                                handle_parsing_errors=True)
    # python_agent_executor.invoke(input={"input": """Generate and save in current working directory 3 QR codes that points to the following URLs: https://chinmaynayak.cnresearchs.in/
    #                              you have qrcode package installed."""})
    
    # Be aware of using this type of code on Priduction as it can be dangerous
    csv_agent_executor: AgentExecutor = create_csv_agent(
        llm=ChatOpenAI(temperature=0, model="gpt-4-turbo"), 
        path="episode_info.csv", 
        verbose=True,
        allow_dangerous_code=True
    )

    # csv_agent_executor.invoke(input={"input": "What is the series name we are analyzing?"}) # We dont need it anymore as we have router agent now

    ## ROUTER AGENT ##
    tools = [
        Tool(
        name="Python Agent",
        func=lambda x: python_agent_executor.invoke({"input": x}),
        description="Useful for when you need to run Python code to answer questions or perform calculations. DOES NOT ACCEPT CODE AS DIRECT INPUT"
        ),
        Tool(
        name="CSV Agent",
        func=lambda x: csv_agent_executor.invoke({"input": x}),
        description="Useful for when you need to analyze or extract information from CSV files."
        )]

    prompt = base_prompt.partial(instructions="")
    router_agent = create_react_agent(
        llm=ChatOpenAI(temperature=0, model="gpt-4-turbo"), 
        tools=tools,
        prompt=prompt
    )

    router_agent_executor = AgentExecutor(agent=router_agent, 
                                            tools=tools, 
                                            verbose=True,
                                            handle_parsing_errors=True)

    # router_agent_executor.invoke(input={"input": """What is the series name we are analyzing in episode_info.csv? 
    #                                     If not found the answer directly from file then try to infer it by analysing the writer name of the episodes in csv."""})

    # router_agent_executor.invoke(input={"input": """Calculate the 1-10 Fibonacci numbers and their sum."""})

if __name__ == "__main__":
    main()