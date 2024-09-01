# views.py
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import os
import re  # Adicione esta linha para importar o módulo 're'

def home(request):
    return render(request, 'app/home.html')

def generate_script(request):
    if request.method == 'POST':
        # Recebe o valor do campo Quantidade de dígitos
        num_digitos = request.POST.get('num_digitos')
        indicador_revisao = request.POST.get('indicador_revisao')
        
        # Caminho para o arquivo no diretório estático
        file_path = os.path.join(settings.BASE_DIR, 'static', 'download', 'main-run.py')
        
        # Verifique se o arquivo existe
        if not os.path.isfile(file_path):
            return HttpResponse("Arquivo não encontrado.", status=404)
        
        # Leia o conteúdo do arquivo
        with open(file_path, 'r') as f:
            script_content = f.read()
        
        # Substitua a variável no script com os valores fornecidos
        script_content = re.sub(r'self\.quantoDigitos\s*=\s*\d+', f'self.quantoDigitos = {num_digitos}', script_content)
        script_content = re.sub(r'self\.indicadorRev\s*=\s*["\'].*?["\']', f'self.indicadorRev = "{indicador_revisao}"', script_content)
        
        # Crie uma resposta HTTP com o conteúdo modificado
        response = HttpResponse(script_content, content_type='application/octet-stream')
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
