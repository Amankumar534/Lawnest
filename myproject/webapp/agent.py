from langgraph.graph import StateGraph, END
from dotenv import load_dotenv
from typing import TypedDict, Annotated
from langgraph.prebuilt import tools_condition
from langgraph.graph.message import AnyMessage, add_messages
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from .utilities import create_tool_node_with_fallback, convert_messages
# from .calendar_tools import book_event
from langchain_core.prompts import ChatPromptTemplate
import sqlite3, datetime
from langchain_groq import ChatGroq

load_dotenv()

ist_timezone = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
now = datetime.datetime.now(ist_timezone).isoformat()

class ChatbotAgent:
    def __init__(self, prompt):
        self.prompt = prompt      
        
        self.workflow = self.build_workflow()

    class UserState(TypedDict):
        messages: Annotated[list[AnyMessage], add_messages]
        last_user_input: str | None
        options: list[str]

    def final_node(self, state: UserState) -> UserState:
        tool_response: str = state["messages"][-1].content
        print("Tool Response in final_node:", tool_response)

        if tool_response.startswith("[{") and tool_response.endswith("}]"):
            ans = "Would you like to schedule a call with one of our agents \n to discuss available options?"
        elif tool_response == "Event Booked Successfully":  
            ans = "Excellent! We have successfully scheduled your call. Is there anything else I can help you with?"
        elif "time slot already booked" in tool_response:
            ans = "Oops! this slot is already booked. Please provide a different date and time."
        else:
            ans = "Calendar Token Expired! Please contact the developer."
        
        return {**state, "messages": AIMessage(content=ans)}
    
    def generate_response(self, state: UserState) -> dict:          
        messages = convert_messages(state["messages"])

        assistant_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.prompt),
                ("placeholder", "{conversation}"),
            ]
        ).partial(time=now,)

        llm = ChatGroq(llm_name="llama-4-scout", temp=0.6)
        runnable_llm = assistant_prompt | llm.bind_tools(self.tool_to_use)

        response = runnable_llm.invoke({"conversation": messages})  

        return {"messages": response}
    
    def build_workflow(self):
        graph = StateGraph(self.UserState)
        graph.add_node("generate_response", self.generate_response)
        graph.add_node("final_node", self.final_node)
        graph.add_node("tools", create_tool_node_with_fallback(self.tool_to_use))

        graph.set_entry_point("generate_response")

        graph.add_conditional_edges("generate_response", tools_condition)
        graph.add_edge("tools", "final_node")
        graph.add_edge("final_node", END)
    
        conn = sqlite3.connect("checkpoints.sqlite", check_same_thread=False)
        memory = SqliteSaver(conn)
        return graph.compile(checkpointer=memory)
    
    
    def run_query(self, user_input: str, thread_id: str = None,):
        # exists = check_conversation_exists(thread_id)
        messages = []
        
        messages.append(HumanMessage(content=user_input))
        initial_state = {
            "messages": messages,
            "last_user_input": user_input
        }
        config = { "configurable": { "thread_id": thread_id} }
        state = self.workflow.invoke(initial_state, config)
        return state['messages'][-1].content