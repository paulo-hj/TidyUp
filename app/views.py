# views.py
from django.shortcuts import render
from django.http import HttpResponse
import re

def home(request):
    return render(request, 'app/home.html')


def generate_script(request):
    if request.method == 'POST':
        num_digitos = request.POST.get('num_digitos')
        if not re.match(r'^\d{1,4}$', num_digitos):
            return HttpResponse("Número de dígitos inválido. Insira entre 1 e 4 dígitos numéricos.", status=400)
        
        script_content = f"""import os
# Seu código aqui
"""
        response = HttpResponse(script_content, content_type='application/force-download')
        response['Content-Disposition'] = f'attachment; filename="script_organizar.py"'
        return response
    else:
        return HttpResponse("Método não permitido", status=405)

def sobre(request):
    return render(request, 'sobre.html')

def tutorial(request):
    return render(request, 'tutorial.html')

def ferramentas(request):
    return render(request, 'ferramentas.html')