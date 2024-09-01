import subprocess
import os

# Caminho para o script Python
script_path = os.path.join('static', 'download', 'main-run.py')
output_dir = os.path.join('static', 'download', 'executavel')

# Crie o diretório de saída se não existir
os.makedirs(output_dir, exist_ok=True)

# Comando para criar o executável
subprocess.run([
    'pyinstaller',
    '--onefile',
    '--distpath', output_dir,
    '--workpath', 'build',
    '--specpath', 'build',
    script_path
], check=True)
