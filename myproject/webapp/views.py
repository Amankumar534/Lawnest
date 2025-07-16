from django.shortcuts import render
from .models import Attorney,News
from .agent import ChatbotAgent
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Create your views here.
def home(request):
    attorney = Attorney.objects.all()
    news = News.objects.all()
    return render(request, 'home.html', {'attorney': attorney, 'news': news})


@csrf_exempt
def chatbot_agent(request):    
    if request.method == 'POST':
        try:            
            data = json.loads(request.body)
            user_input = data['curr_input']
            session_id = data['conversation_id']              

            agent_graph = ChatbotAgent()            
            result = agent_graph.run_query(user_input, session_id)

            # conversation = Conversation.objects.get(id=session_id)

            # message1 = Message(
            #     conversation=conversation,
            #     role="user",
            #     content=user_input,
            # )
            # message1.save()

            # message2 = Message(
            #     conversation=conversation,
            #     role="assistant",
            #     content=result,
            # )
            # message2.save()

            return JsonResponse(result, safe=False)
        except Exception as e:
            return JsonResponse({'error': e}, status=404)