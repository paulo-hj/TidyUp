# views.py
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import os
import re
import subprocess

def home(request):
    return render(request, 'app/home.html')

def gerarScript(request):
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

        # Caminho para o script de geração do executável
        gerar_executavel_script = os.path.join(settings.BASE_DIR, 'scripts', 'gerar_executavel.py')
        
        # Executa o script para gerar o executável
        try:
            subprocess.run(['python', gerar_executavel_script], check=True)
        except subprocess.CalledProcessError as e:
            return HttpResponse(f"Erro ao gerar o executável: {str(e)}", status=500)
        
        # Caminho para o executável gerado
        executable_path = os.path.join(settings.BASE_DIR, 'static', 'download', 'executavel', 'main-run')

        # Verifica se o executável foi criado
        if not os.path.isfile(executable_path):
            return HttpResponse("Executável não encontrado.", status=404)
        
        # Teste
        #txt_file_path = os.path.join(settings.BASE_DIR, 'static', 'download', 'executavel', 'variaveis.txt')
        #with open(txt_file_path, 'w') as txt_file:
        #    txt_file.write(f"Quantidade de dígitos: {num_digitos}\n")
        #    txt_file.write(f"Indicador de Revisão: {indicador_revisao}\n")
        #    txt_file.write(f"Conteúdo do script:\n{script_content}\n")
        
        # Crie uma resposta HTTP com o executável
        with open(executable_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename="main-run.exe"'
        
        return response
    else:
        return HttpResponse("Método não permitido", status=405)

def sobre(request):
    return render(request, 'sobre.html')

def tutorial(request):
    return render(request, 'tutorial.html')

def ferramentas(request):
    return render(request, 'ferramentas.html')
