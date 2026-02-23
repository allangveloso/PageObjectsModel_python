"""O QUE É UMA FIXTURE (ACESSÓRIO)
Uma fixture é um conjunto de recursos que um teste pode usar.
Pense nisso como preparar o ambiente para um teste, como abrir um navegador, configurar um banco de dados ou criar dados de teste.

Em pytest, fixtures são funções que:

1. Configuram recursos (bancos de dados, arquivos, instâncias de navegador, etc.)
2. Fornecem esses recursos aos testes que precisam deles
3. Limpam/desmontam os recursos após a conclusão dos testes
4. Podem ser reutilizadas em vários testes
5. Garantem que cada teste comece com um estado conhecido e limpo

Exemplos comuns de fixtures:
Conexões de banco de dados com dados de teste
Arquivos ou diretórios temporários
Objetos ou serviços simulados
Instâncias de navegador (como este driver do Chrome)
Clientes de API ou tokens de autenticação
"""

"""
conftest.py é um arquivo de configuração especial do pytest que define fixtures, hooks e plugins compartilhados para arquivos de teste. 
Quando pytest executa, ele automaticamente descobre e carrega arquivos conftest.py do diretório de teste e seus diretórios pai.
 
PRINCIPAIS RECURSOS
-Fixtures definidas aqui são automaticamente disponibilizadas para todos os arquivos de testes do mesmo diretório e subdiretórios (sem necessidade de importação).
-Age como um local central para setup de testes comuns e configuações.
-Pode conter hooks do pytest para personalizar o comportamento do framework de testes.
-Múltiplos arquivos conftest.py podem existir em diferentes níveis de diretórios, cada um afetando apenas os testes naquele diretório e seus subdiretórios.
-Segue um escopo hierárquico: fixtures definidas em conftest.py mais próximos ao arquivo de teste têm precedência sobre as mais distantes.

NOTA: Este driver fixture poderá ser tipicamente colocado em um conftest.py para estar automaticamente disponível para todos os testes de sua suite.
"""

import pytest
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env

@pytest.fixture(scope="function")
def driver():
    """
    Este arquivo está configurado para capturar um print automático da tela toda vez que um teste falhar
    Setup: Abre o navegador antes de cada teste.
    Scope='function' garante um navegador limpo para cada teste.
    """
    chrome_options = webdriver.ChromeOptions()
    # options.add_argument("--headless") # Rodar ocultando janelas
    # chrome_options.add_argument("--disable-password-manager") # Desabilitar gerenciador de senha
    # chrome_options.add_argument("--disable-password-manager-reauthentication") # Desabilitar reautenticação do gerenciador de senha
    # chrome_options.add_argument("--disable-save-password-bubble") # Desabilitar popups de senha
    # chrome_options.add_argument("--disable-password-autofill-public-suffix-domain-matching") # Desabilitar preenchimento automático de senha
    # chrome_options.add_argument("--disable-password-generation") # Desabilitar geração de senha
    ##(... outras opções de configuração do Chrome, se necessário)


    #Preferências de inicialização do Chrome
    # prefs = {
    #     "profile.password_manager_enabled": False, # Desabilitar gerenciador de senhas
    #     "profile.default_content_setting_values.popups": 0, # Bloquear pop-ups
    #     "profile.default_content_setting_values.notifications": 2, # Bloquear notificações
    #     "profile.manger_default_content_settings.notifications": 2, # Bloquear notificações
    #     "credentials_enable_service": False, # Desabilitar serviço de credenciais
    #     "profile.password_manager_enabled": False, # Desabilitar gerenciador de senhas
    #     #(... outras preferências, se necessário)
    # }
    # chrome_options.add_experimental_option("prefs", prefs)

    #configurações adicionais para evitar pop-ups e notificações
    # chrome_options.add_argument("--disable-extensions") # Desabilitar extensões
    # chrome_options.add_argument("--disable-infobars") # Desabilitar infobars
    # chrome_options.add_argument("--disable-notifications") # Desabilitar notificações
    # chrome_options.add_argument("--disable-popup-blocking") # Desabilitar bloqueio de pop-ups
    # chrome_options.add_argument("--disable-translate") # Desabilitar tradução automática
    # chrome_options.add_argument("--no-first-run") # Evitar tela de boas-vindas
    # chrome_options.add_argument("--disable-default-apps") # Desabilitar aplicativos padrão
    ##chrome_options.add_argument("--disable-automation") # Desabilitar automação para evitar det
    # chrome_options.add_argument("--disable-background-mode")    # Desabilitar modo de fundo

    
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.implicitly_wait(10) # Espera até 10s por elementos antes de dar erro
    
    
    #O yield driver "empresta" o navegador para o seu teste, que roda todas as ações necessárias (cliques, preenchimento de campos, etc.).
    #Assim que o teste termina (passando ou falhando), o Python volta para a função e executa o que estiver abaixo do yield.
    #Mesmo que o seu teste dê um erro crítico (crash), o Pytest garante que o código após o yield seja executado, fechando o processo do Chrome e liberando memória RAM.
    yield driver    

    
    # Teardown: Fecha após o término do teste
    driver.quit()



@pytest.fixture
def base_url():
    return os.getenv("BASE_URL")
    

@pytest.fixture
def credentials():
    return {
        "username": os.getenv("USERNAME"),  #estão no arquivo .evn
        "password": os.getenv("PASSWORD")   #estão no arquivo .evn
    }


"""
# Hook para capturar falhas
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Executa o passo do teste
    outcome = yield
    rep = outcome.get_result()

    # Verifica se o teste falhou durante a execução (call)
    if rep.when == "call" and rep.failed:
        try:
            # Pega a fixture 'driver' usada no teste
            driver = item.funcargs['driver']
            
            # Cria uma pasta para os prints se não existir
            if not os.path.exists("screenshots"):
                os.makedirs("screenshots")
            
            # Salva o print com o nome do teste
            nome_arquivo = f"screenshots/{item.name}.png"
            driver.save_screenshot(nome_arquivo)
            print(f"\n[EVIDÊNCIA] Print salvo em: {nome_arquivo}")
            
        except Exception as e:
            print(f"Falha ao capturar screenshot: {e}")
"""