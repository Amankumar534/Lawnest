from django.shortcuts import render
from .models import Attorney
# from .agent import ChatbotAgent
import json, os
# from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import requests

# Create your views here.
def home(request):
    attorney = Attorney.objects.all()
    MEDIA_API_KEY=os.getenv("MEDIA_API_KEY")
    news_url = f"https://api.mediastack.com/v1/news?access_key={MEDIA_API_KEY}&categories=general&countries=in"
    response = requests.get(news_url)
    news_list = []
    if response.status_code == 200:
        data = response.json()  
        articles = data.get('data', [])      
        for article in articles:
            news_list.append({
                "title": article.get("title"),
                "date": article.get("published_at"),
                "image": article.get("image"),
                "link": article.get("url"),
            })
        news_list = news_list[:4]
    return render(request, 'home.html', {'attorney': attorney, 'news': news_list})


# @csrf_exempt
# def chatbot_agent(request):    
#     if request.method == 'POST':
#         try:            
#             data = json.loads(request.body)
#             user_input = data['curr_input']
#             thread_id = data['thread_id'] if 'thread_id' in data else None   

#             agent_graph = ChatbotAgent()  
#             print("+++++++++++=====")         
#             result = agent_graph.run_query(thread_id, user_input)
#             print("result", result)

#             return JsonResponse(result, safe=False)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=404)
        

def news(request):
    MEDIA_API_KEY=os.getenv("MEDIA_API_KEY")
    news_url = f"https://api.mediastack.com/v1/news?access_key={MEDIA_API_KEY}&categories=general&countries=in"
    response = requests.get(news_url)
    news_list = []
    if response.status_code == 200:
        data = response.json()  
        articles = data.get('data', [])      
        for article in articles:
            news_list.append({
                "title": article.get("title"),
                "date": article.get("published_at"),
                "image": article.get("image"),
                "link": article.get("url"),
            })
            news_list = news_list[:24]
    return render(request, 'news.html', {'news': news_list})
