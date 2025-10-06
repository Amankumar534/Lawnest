from langgraph.graph import StateGraph, END
from dotenv import load_dotenv
from typing import TypedDict, Annotated
from langgraph.prebuilt import tools_condition
from langgraph.graph.message import AnyMessage, add_messages
from langchain_core.messages import HumanMessage, AIMessage
from .utilities import create_tool_node_with_fallback, convert_messages
from .calendar_tools import book_event
from langchain_core.prompts import ChatPromptTemplate
import datetime
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
import os

load_dotenv()

ist_timezone = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
now = datetime.datetime.now(ist_timezone).isoformat()

class ChatbotAgent:
    def __init__(self):  
        self.tool_to_use = [book_event]      
        self.workflow = self.build_workflow()
        self.memory = ConversationBufferMemory(return_messages=True)

    class UserState(TypedDict):
        messages: Annotated[list[AnyMessage], add_messages]
        last_user_input: str | None
        options: list[str]

    def final_node(self, state: UserState) -> UserState:
        print("final node")
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
        
        # Corrected line: Return a dictionary with the 'messages' key
        # containing a list with the new AIMessage.
        return {"messages": [AIMessage(content=ans)]}
    
    def generate_response(self, state: UserState) -> dict:  
        print("generate response node")

        messages = convert_messages(state["messages"])
        print(messages)

        prompt = '''You are a polite and helpful virtual assistant on a law firm's website. Your primary role is to assist users in booking legal appointments.

                    If the user says "hi", "hello", "good morning", or similar, respond warmly and ask how you can assist.
                    If user ask to book appointment kindly ask the user for the following three details one by one
                    Date of the appointment 
                    Preferred time 
                    email address

                    Once all three details are collected:
                    Confirm the details back to the user
                    Then call the book_event tool to create the appointment.

                    If the user provides only partial information, gently prompt them to complete the missing details.

                    Current time: {time}

                    Additional Context:
                    {info}'''

        assistant_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", prompt),
                ("placeholder", "{conversation}"),
            ]
        ).partial(time=now)

        llm = ChatGroq(llm_name="llama3-70b-8192", temp=0.6, api_key=os.getenv("GROQ_API_KEY"))
        runnable_llm = assistant_prompt | llm.bind_tools(self.tool_to_use)

        response = runnable_llm.invoke({"conversation": messages}) 
        print(response) 

        return {"messages": [response]}
    
    def build_workflow(self):
        print("building workflow")
        graph = StateGraph(self.UserState)
        graph.add_node("generate_response", self.generate_response)
        graph.add_node("final_node", self.final_node)
        graph.add_node("tools", create_tool_node_with_fallback(self.tool_to_use))

        graph.set_entry_point("generate_response")

        graph.add_conditional_edges("generate_response", tools_condition)
        graph.add_edge("tools", "final_node")
        graph.add_edge("final_node", END)

        return graph.compile()
    
    
    def run_query(self, thread_id: str, user_input: str): 
        print("query running")       
        self.memory.chat_memory.add_user_message(user_input)

        past_messages = self.memory.chat_memory.messages

        initial_state = {
            "messages": past_messages,
            "last_user_input": user_input
        }
        
        print("initial state:", initial_state)
        config = { "configurable": { "thread_id": thread_id} }
        state = self.workflow.invoke(initial_state, config)
        print("final state:", state)
        final_response = state['messages'][-1].content
        print("Final Response:", final_response)
        self.memory.chat_memory.add_ai_message(final_response)
        
        return final_response