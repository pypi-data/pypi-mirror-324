import json
import os
from typing import Dict, List, Callable, Any

# Solicita os caminhos ao usuário
collection_path = input("Digite o caminho da collection Postman: ").strip()
project_path = input("Digite o caminho do projeto onde os testes serão gerados: ").strip()

# Diretórios de destino
FEATURES_DIR = os.path.join(project_path, "test/features/specs")
STEPS_DIR = os.path.join(project_path, "test/features/steps")
SERVICES_DIR = os.path.join(project_path, "test/features/services")
UTILS_FEATURE = os.path.join(FEATURES_DIR, "utils_feature.feature")
UTILS_STEPS = os.path.join(STEPS_DIR, "utils_steps.py")
UTILS_SERVICE = os.path.join(SERVICES_DIR, "utils_service.py")

def detect_duplicates(directory: str, utils_file: str, check_imports: bool = False) -> None:
    """Move arquivos duplicados para o arquivo de utilidades correspondente e verifica duplicações de imports."""
    seen_content = {}
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Verificar duplicação de imports
            if check_imports:
                lines = content.splitlines()
                for i, line in enumerate(lines):
                    if line.strip().startswith("from behave import *") or line.strip().startswith("import requests"):
                        lines[i] = f"# Duplicado: {line.strip()}"
                content = "\n".join(lines)
            
            if content in seen_content.values():
                with open(utils_file, "a", encoding="utf-8") as f:
                    f.write(content + "\n")
                os.remove(file_path)
            else:
                seen_content[filename] = content

def ensure_directories() -> None:
    """Cria a estrutura de diretórios necessária."""
    for directory in [FEATURES_DIR, STEPS_DIR, SERVICES_DIR]:
        os.makedirs(directory, exist_ok=True)

def generate_gherkin_files(collection: Dict) -> None:
    """Gera arquivos .feature."""
    def create_gherkin_file(endpoint: Dict) -> None:
        file_name = f"{endpoint['name'].replace(' ', '_').lower()}"
        feature_name = f"{file_name}.feature"
        feature_path = os.path.join(FEATURES_DIR, feature_name)
        # Quando envio uma solicitação {file_name}-{endpoint['request']['method']} para "{endpoint['request'].get('url', {}).get('raw', 'URL não especificada')}"
        gherkin_content = f"""#language:pt
Funcionalidade: {endpoint['name']}
    @{endpoint['name']}
    Cenário: {endpoint['name']}
        Dado que configurei a solicitação
        Quando uma batida do tipo {endpoint['request']['method']} na api de {file_name}
        Então recebo uma resposta válida
"""
        if not os.path.exists(feature_path):
            with open(feature_path, "w", encoding='utf-8') as f:
                f.write(gherkin_content)
    
    process_items(collection['item'], create_gherkin_file)
    detect_duplicates(FEATURES_DIR, UTILS_FEATURE)

def generate_step_files(collection: Dict) -> None:
    """Gera arquivos _steps.py sem duplicações, com imports corretos dos serviços."""
    common_step = """from behave import *

@given('que configurei a solicitação')
def setup_request(context):
    context.payload = {}

@then('recebo uma resposta válida')
def validate_response(context):
    assert context.response.status_code == 200
"""
    
    # Verificar se o common_step já existe no arquivo de utilitários
    if not os.path.exists(UTILS_STEPS):
        with open(UTILS_STEPS, "w", encoding='utf-8') as f:
            f.write(common_step)
    else:
        with open(UTILS_STEPS, "r", encoding='utf-8') as f:
            existing_content = f.read()
        
        # Só escrever o common_step se ele não estiver no arquivo
        if common_step not in existing_content:
            with open(UTILS_STEPS, "a", encoding='utf-8') as f:
                f.write(common_step)
    
    def create_step_file(endpoint: Dict) -> None:
        file_name = f"{endpoint['name'].replace(' ', '_').lower()}"
        service_name = f"{file_name}_service"
        service_class_name = f"{endpoint['name'].replace(' ', '').capitalize()}Service"
        step_name = f"{file_name}_steps.py"
        step_path = os.path.join(STEPS_DIR, step_name)
        
        # Construir a importação do serviço específico
        step_content = f"""from behave import *
from services.{service_name} import {service_class_name}

@when('uma batida do tipo {endpoint['request']['method']} na api de {file_name}')
def send_request(context):
    context.response = {service_class_name}().make_request(context.payload)
    
"""
        if not os.path.exists(step_path):
            with open(step_path, "w", encoding='utf-8') as f:
                f.write(step_content)
    
    process_items(collection['item'], create_step_file)
    detect_duplicates(STEPS_DIR, UTILS_STEPS, check_imports=True)

def generate_service_classes(collection: Dict) -> None:
    """Gera arquivos _service.py sem duplicações."""
    common_service = """import requests
from support.ambientes import *
from support.logger import *

class ApiService:
    def make_request(self, payload):
        try:
            response = requests.post(f"{BASE_URL_QA}", json=payload)
            return response
        except Exception as error:
            return logging.error(error)

"""
    
    if not os.path.exists(UTILS_SERVICE):
        with open(UTILS_SERVICE, "w", encoding='utf-8') as f:
            f.write(common_service)
    
    def create_service_class(endpoint: Dict) -> None:
        service_file = f"{endpoint['name'].replace(' ', '_').lower()}_service.py"
        service_path = os.path.join(SERVICES_DIR, service_file)
        method = endpoint['request']['method'].lower()
        # Alteração: Criando a classe de forma independente, sem herança
        service_content = f"""import requests
from support.ambientes import *
from support.logger import *

class {endpoint['name'].replace(' ', '').capitalize()}Service:
    def make_request(self, payload):
        try:
            response = requests.{method}(f"{{BASE_URL_QA}}", json=payload)
            return response
        except Exception as error:
            return logging.error(error)

"""
        if not os.path.exists(service_path):
            with open(service_path, "w", encoding='utf-8') as f:
                f.write(service_content)
    
    process_items(collection['item'], create_service_class)
    detect_duplicates(SERVICES_DIR, UTILS_SERVICE)

def process_items(items: List[Dict], callback: Callable[[Dict], None]) -> None:
    """Processa os itens da coleção."""
    for item in items:
        if 'request' in item and 'method' in item['request']:
            callback(item)
        elif 'item' in item:
            process_items(item['item'], callback)

def main():
    """Executa o processo de geração de testes."""
    ensure_directories()
    with open(collection_path, "r") as f:
        collection = json.load(f)
    generate_gherkin_files(collection)
    generate_step_files(collection)
    generate_service_classes(collection)
    print("Geração de testes concluída!")

if __name__ == "__main__":
    main()
