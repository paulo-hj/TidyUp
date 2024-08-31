# views.py
from django.shortcuts import render
from django.http import HttpResponse
import re
from django.conf import settings
import os

def home(request):
    return render(request, 'app/home.html')


def generate_script(request):
    if request.method == 'POST':
        # Caminho para o arquivo no diretório estático
        file_path = os.path.join(settings.BASE_DIR, 'static', 'download', 'main-run.py')
        
        # Verifique se o arquivo existe
        if not os.path.isfile(file_path):
            return HttpResponse("Arquivo não encontrado.", status=404)

        # Leia o conteúdo do arquivo
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename="main-run.py"'
            return response
    else:
        return HttpResponse("Método não permitido", status=405)

def sobre(request):
    return render(request, 'sobre.html')

def tutorial(request):
    return render(request, 'tutorial.html')

def ferramentas(request):
    return render(request, 'ferramentas.html')