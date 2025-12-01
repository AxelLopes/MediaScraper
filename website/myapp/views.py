from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponseRedirect
from .models import TodoItem
from .forms import SearchKeywordsForm
from django.http import JsonResponse
from .scraper_linkedin import scrape_linkedin, run_script
#from .text_analysis import analyze
import subprocess
import pandas as pd


# Create your views here.
"""
def home(request):
    # Exemple de DataFrame
    data = {
        'Nom': ['Alice', 'Bob', 'Charlie'],
        'Age': [24, 30, 22],
        'Ville': [' ParisParisParisParisParisParisParisParisParisParisParisParisParisParisParisParisParisParisParisParisParisParisParisParisParisParisParisParisParisParisParisParisParisParisParisParisParis Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris <br> Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris ParisParis Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris<br><br><br><br><br> Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris ParisParis Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris Paris ', 'Lyon', 'Marseille']
    }
    df = pd.DataFrame(data)

    # Convertir le DataFrame en HTML
    df_html = df.to_html(classes='table table-striped', border=0, escape=False)
    df_html = df_html.replace('<td>', '<td><div class=scrollable>').replace('</td>', '</div></td>')

    # Renvoyer le DataFrame HTML à la template
    return render(request, 'home.html', {'df_html': df_html})
"""
def home(request):
    return render(request,'home.html')

"""
#22-08-2025 working?
def process_keywords(request):
    if request.method == 'POST':
        keywords = request.POST.get('keywords')
        # Call Python script here with the keywords
        result = scrape_linkedin(keywords)
        #print('printing result :')
        #print(result)
        print("Rendering df to html")
        
        #result_analyzed = analyze(result)

        data = {
        'Nom': ['Alice', 'Bob', 'Charlie'],
        'Age': [24, 30, 22],
        'Ville': ['Paris', 'Paris Lyon', 'Paris Marseille']
                }
        df = pd.DataFrame(data)
    # Convertir le DataFrame en HTML
        result.reset_index(drop=True, inplace=True)
        df_html = result.to_html(classes='table table-striped', border=0, escape=False)
        df_html = df_html.replace('<td>', '<td><div class=scrollable>').replace('</td>', '</div></td>')
        return HttpResponse(df_html)
    return render(request,'home.html')
"""
#proposé par windsurf le 22-08-2025
def process_keywords(request):
    if request.method == 'POST':
        try:
            keywords = request.POST.get('keywords')
            if not keywords:
                return JsonResponse({'error': 'No keywords provided'}, status=400)
                
            result = scrape_linkedin(keywords)
            if result is None:
                return JsonResponse({'error': 'Failed to scrape data'}, status=500)
                
            result.reset_index(drop=True, inplace=True)
            df_html = result.to_html(classes='table table-striped', border=0, escape=False)
            df_html = df_html.replace('<td>', '<td><div class=scrollable>').replace('</td>', '</div></td>')
            return HttpResponse(df_html)
            
        except Exception as e:
            print(f"Error in process_keywords: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def test_script(request):
    if request.method == 'POST':
        # Call Python script here with the keywords
        result = run_script()
        return JsonResponse({'result': result})
    return JsonResponse({'error': 'Invalid request method'}, status=400)


def todos(request):
    items = TodoItem.objects.all()
    return render(request,'todos.html',{"todos":items})


