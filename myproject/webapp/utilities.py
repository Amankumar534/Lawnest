# from langchain_core.runnables import RunnableLambda
# from langgraph.prebuilt import ToolNode
# from langchain_core.messages import ToolMessage, SystemMessage, AIMessage, HumanMessage
# from .email_sender import EmailSender


# def handle_tool_error(state) -> dict:
#     error = state.get("error")
#     tool_calls = state["messages"][-1].tool_calls
#     return {
#         "messages": [
#             ToolMessage(
#                 content=f"Error: {repr(error)}\n please fix your mistakes.",
#                 tool_call_id=tc["id"],
#             )
#             for tc in tool_calls
#         ]
#     }

# def create_tool_node_with_fallback(tools: list) -> dict:
#     return ToolNode(tools).with_fallbacks(
#         [RunnableLambda(handle_tool_error)], exception_key="error"
#     )


# def convert_messages(messages):
#     converted_messages = []
#     for message in messages:
#         if message.content:
#             if isinstance(message, SystemMessage):
#                 converted_messages.append(("system", message.content))
#             elif isinstance(message, AIMessage) or isinstance(message, ToolMessage):
#                 converted_messages.append(("ai", message.content))
#             elif isinstance(message, HumanMessage):
#                 converted_messages.append(("human", message.content))
#     return converted_messages


# def write_email(event_details, summary):
#     summary_html = "".join(f"<li>{item}</li>" for item in summary)
#     html_content = f'''
#     <html>
#     <body style="font-family: Arial, sans-serif;">
#         <h2 style="color: #2d89ef;">Thank you for using Vinove Customer Support Chatbot</h2>
#         <p>Your meeting has been successfully booked.</p>
#         <h3>Event Details:</h3>
#         <table border="1" cellspacing="0" cellpadding="8" style="border-collapse: collapse;">
#             <tr><th style="background-color: #f2f2f2;">Title</th><td>{event_details['title']}</td></tr>
#             <tr><th style="background-color: #f2f2f2;">Start Time</th><td>{event_details['start_time']}</td></tr>
#             <tr><th style="background-color: #f2f2f2;">End Time</th><td>{event_details['end_time']}</td></tr>
#             <tr><th style="background-color: #f2f2f2;">Description</th><td>{event_details['description']}</td></tr>
#             <tr><th style="background-color: #f2f2f2;">Link</th><td><a href="{event_details['link']}">Join Meeting</a></td></tr>
#         </table>
#         <h3>Summary of Your Conversation with Our Chatbot:</h3>
#         <ul>{summary_html}</ul>
#         <p>Best Regards,<br>Team Vinove</p>
#     </body>
#     </html>
#     '''
#     return html_content


# def send_email(event_details: dict, messages: list, email: str):
#     all_messages = []
#     for message in messages:
#         if hasattr(message, "content"):
#             all_messages.append(message.content)
#     all_messages.pop()

#     send_email_obj = EmailSender()
#     send_email_obj.send_email(email, "Thanks for using Vinove Chatbot", write_email(event_details))

