import json
import os
from typing import Dict, List, Callable, Any

# Configuração de diretórios e arquivos
class Config:
    def __init__(self, project_path: str):
        self.FEATURES_DIR = os.path.join(project_path, "test/features/specs")
        self.STEPS_DIR = os.path.join(project_path, "test/features/steps")
        self.SERVICES_DIR = os.path.join(project_path, "test/features/services")
        self.UTILS_FEATURE = os.path.join(self.FEATURES_DIR, "utils_feature.feature")
        self.UTILS_STEPS = os.path.join(self.STEPS_DIR, "utils_steps.py")
        self.UTILS_SERVICE = os.path.join(self.SERVICES_DIR, "utils_service.py")

def create_utils_files(config: Config) -> None:
    """Cria os arquivos utils com conteúdo base."""
    utils_feature_content = """#language:pt
Funcionalidade: Utils
    Funcionalidade base com steps comuns

    Cenário: Setup básico
        Dado que configurei a solicitação
        Então recebo uma resposta válida"""

    utils_steps_content = """from behave import *

@given('que configurei a solicitação')
def setup_request(context):
    context.payload = {}

@then('recebo uma resposta válida')
def validate_response(context):
    assert context.response.status_code == 200"""

    utils_service_content = """import requests
from support.ambientes import *
from support.logger import *

class BaseService:
    def make_request(self, payload, method='GET', endpoint=''):
        try:
            response = getattr(requests, method.lower())(
                f"{BASE_URL_QA}{endpoint}",
                json=payload
            )
            return response
        except Exception as error:
            return logging.error(error)"""

    # Cria os diretórios se não existirem
    os.makedirs(os.path.dirname(config.UTILS_FEATURE), exist_ok=True)
    os.makedirs(os.path.dirname(config.UTILS_STEPS), exist_ok=True)
    os.makedirs(os.path.dirname(config.UTILS_SERVICE), exist_ok=True)

    # Cria os arquivos utils
    with open(config.UTILS_FEATURE, "w", encoding='utf-8') as f:
        f.write(utils_feature_content)
    print(f"Arquivo utils feature criado: {config.UTILS_FEATURE}")

    with open(config.UTILS_STEPS, "w", encoding='utf-8') as f:
        f.write(utils_steps_content)
    print(f"Arquivo utils steps criado: {config.UTILS_STEPS}")

    with open(config.UTILS_SERVICE, "w", encoding='utf-8') as f:
        f.write(utils_service_content)
    print(f"Arquivo utils service criado: {config.UTILS_SERVICE}")

def generate_file(
    endpoint: Dict,
    directory: str,
    utils_file: str,
    file_suffix: str,
    content_generator: Callable[[Dict, str], str],
    check_imports: bool = False
) -> None:
    """Função base para geração de arquivos com lógica comum."""
    if not endpoint.get('name') or not endpoint.get('request', {}).get('method'):
        print(f"Pulando item sem nome ou método: {endpoint}")
        return
        
    file_name = endpoint['name'].replace(' ', '_').lower()
    file_path = os.path.join(directory, f"{file_name}{file_suffix}")
    
    if not os.path.exists(file_path):
        content = content_generator(endpoint, file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding='utf-8') as f:
            f.write(content)
        print(f"Arquivo gerado: {file_path}")

def detect_duplicates(directory: str, utils_file: str, check_imports: bool = False) -> None:
    """Detecta e move conteúdo duplicado para arquivo de utilidades."""
    if not os.path.exists(directory):
        print(f"Diretório não existe: {directory}")
        return

    seen_content = {}
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and not file_path.endswith('utils_feature.feature'):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            if check_imports:
                lines = content.splitlines()
                for i, line in enumerate(lines):
                    if line.strip().startswith(("from behave import *", "import requests")):
                        lines[i] = f"# Duplicado: {line.strip()}"
                content = "\n".join(lines)
            
            if content in seen_content.values():
                with open(utils_file, "a", encoding="utf-8") as f:
                    f.write(content + "\n")
                os.remove(file_path)
                print(f"Conteúdo duplicado movido para {utils_file}")
            else:
                seen_content[filename] = content

def generate_gherkin_content(endpoint: Dict, file_name: str) -> str:
    """Gera conteúdo para arquivos .feature"""
    method = endpoint['request']['method']
    return f"""#language:pt
Funcionalidade: {endpoint['name']}
    @{endpoint['name']}
    Cenário: {endpoint['name']}
        Dado que configurei a solicitação
        Quando uma batida do tipo {method} na api de {file_name}
        Então recebo uma resposta válida"""

def generate_step_content(endpoint: Dict, file_name: str) -> str:
    """Gera conteúdo para arquivos _steps.py"""
    service_class_name = f"{endpoint['name'].replace(' ', '').capitalize()}Service"
    method = endpoint['request']['method']
    return f"""from behave import *
from services.{file_name}_service import {service_class_name}

@when('uma batida do tipo {method} na api de {file_name}')
def send_request(context):
    context.response = {service_class_name}().make_request(context.payload)"""

def generate_service_content(endpoint: Dict, file_name: str) -> str:
    """Gera conteúdo para arquivos _service.py"""
    method = endpoint['request']['method'].lower()
    class_name = endpoint['name'].replace(' ', '').capitalize()
    return f"""import requests
from support.ambientes import *
from support.logger import *
from services.utils_service import BaseService

class {class_name}Service(BaseService):
    def make_request(self, payload):
        return super().make_request(payload, '{method}')"""

def process_items(items: List[Dict], callback: Callable[[Dict], None]) -> None:
    """Processa recursivamente os itens da coleção."""
    if not isinstance(items, list):
        print(f"Items não é uma lista: {type(items)}")
        return

    for item in items:
        print(f"Processando item: {item.get('name', 'Sem nome')}")
        
        # Verifica se é um endpoint válido
        if item.get('request', {}).get('method'):
            print(f"Endpoint encontrado: {item['name']}")
            callback(item)
        
        # Processa subitens recursivamente
        if 'item' in item and isinstance(item['item'], list):
            print(f"Processando subitens de: {item.get('name', 'Sem nome')}")
            process_items(item['item'], callback)

def ensure_directories(config: Config) -> None:
    """Cria a estrutura de diretórios necessária."""
    for directory in [config.FEATURES_DIR, config.STEPS_DIR, config.SERVICES_DIR]:
        os.makedirs(directory, exist_ok=True)
        print(f"Diretório criado/verificado: {directory}")

def main():
    """Função principal que coordena a geração de testes."""
    collection_path = input("Digite o caminho da collection Postman: ").strip()
    project_path = input("Digite o caminho do projeto onde os testes serão gerados: ").strip()
    
    print(f"\nIniciando geração de testes...")
    print(f"Collection: {collection_path}")
    print(f"Projeto: {project_path}\n")
    
    config = Config(project_path)
    ensure_directories(config)
    
    # Cria os arquivos utils primeiro
    create_utils_files(config)
    
    try:
        with open(collection_path, "r") as f:
            collection = json.load(f)
            print("Collection carregada com sucesso")
    except Exception as e:
        print(f"Erro ao carregar collection: {e}")
        return
    
    if 'item' not in collection:
        print("Collection não contém items")
        return
    
    print("\nGerando arquivos .feature...")
    process_items(collection['item'], lambda item: generate_file(
        item,
        config.FEATURES_DIR,
        config.UTILS_FEATURE,
        ".feature",
        generate_gherkin_content
    ))
    detect_duplicates(config.FEATURES_DIR, config.UTILS_FEATURE)
    
    print("\nGerando arquivos _steps.py...")
    process_items(collection['item'], lambda item: generate_file(
        item,
        config.STEPS_DIR,
        config.UTILS_STEPS,
        "_steps.py",
        generate_step_content,
        check_imports=True
    ))
    detect_duplicates(config.STEPS_DIR, config.UTILS_STEPS, check_imports=True)
    
    print("\nGerando arquivos _service.py...")
    process_items(collection['item'], lambda item: generate_file(
        item,
        config.SERVICES_DIR,
        config.UTILS_SERVICE,
        "_service.py",
        generate_service_content
    ))
    detect_duplicates(config.SERVICES_DIR, config.UTILS_SERVICE)
    
    print("\nGeração de testes concluída!")

if __name__ == "__main__":
    main()