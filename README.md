# AgendaFácil

Agenda de atendimentos para uma clínica médica. Permite **marcar**, **remarcar** e **listar** atendimentos, validando expediente, duração, formato de data e prevenindo conflitos e sobreposição de horários entre profissionais e pacientes. Os dados são mantidos em memória.

Projeto da Unidade 1 da disciplina **DIM0501 — Boas Práticas de Programação (DIMAp/UFRN)**, versão refatorada do código-base `agenda_base.py`.

---

## 📋 Pré-requisitos

O projeto foi desenvolvido e homologado utilizando o **Python 3.12**.

### Como instalar o Python 3.12

<details>
<summary><b>macOS (via Homebrew)</b></summary>

```bash
# Instalar o Homebrew (caso não possua):
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar o Python 3.12:
brew install python@3.12
```
</details>

<details>
<summary><b>Linux (Ubuntu/Debian)</b></summary>

```bash
sudo apt update
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-dev -y
```
</details>

<details>
<summary><b>Windows</b></summary>

* Baixe e instale o instalador oficial do [Python 3.12 em python.org](https://www.python.org/downloads/).
* **Importante:** Marque a opção **"Add python.exe to PATH"** durante a instalação.
* Ou instale via terminal (PowerShell/Winget):
  ```powershell
  winget install Python.Python.3.12
  ```
</details>

Verifique a instalação executando:
```bash
python3.12 --version
# ou no Windows:
python --version
```

---

## 🚀 Instalação e Configuração do Ambiente Virtual (`venv`)

Recomenda-se o uso de um ambiente virtual isolado para não poluir os pacotes globais do sistema.

### 1. Clonar ou acessar o diretório do projeto:
```bash
cd boas_praticas
```

### 2. Criar o ambiente virtual com Python 3.12:
* **Linux / macOS:**
  ```bash
  python3.12 -m venv .venv
  ```
* **Windows:**
  ```powershell
  py -3.12 -m venv .venv
  ```

### 3. Ativar o ambiente virtual:
* **Linux / macOS:**
  ```bash
  source .venv/bin/activate
  ```
* **Windows (PowerShell):**
  ```powershell
  .venv\Scripts\Activate.ps1
  ```
* **Windows (CMD):**
  ```cmd
  .venv\Scripts\activate.bat
  ```

*(Após a ativação, você verá `(.venv)` indicado no início da linha de comando).*

### 4. Instalar as dependências:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 💻 Executando o Projeto

O arquivo principal contém rotinas de demonstração e validação de casos de sucesso e de erro:

```bash
python agenda_facil.py
```

### Exemplo de saída:
```text
Atendimento marcado para Ana
Horario ocupado
Atendimento marcado para Carla
Remarcado
14 Carla Dra. Souza MARCADO
```

---

## 📚 Documentação com `pdoc`

A documentação da API foi estruturada seguindo o padrão **Google Style Docstrings** (`Args`, `Returns`, `Raises`) e compilada utilizando o **`pdoc`**.

A pasta [`docs/`](./docs) já contém a versão compilada em HTML.

### 1. Visualizar a documentação no navegador (com Live Reload):
Para navegar interativamente pela documentação local:
```bash
pdoc agenda_facil.py
```
Acesse o endereço exibido no terminal (geralmente [http://localhost:8080](http://localhost:8080)).

### 2. Recompilar a documentação estática na pasta `docs/`:
```bash
pdoc agenda_facil.py -o docs/
```
Os arquivos HTML atualizados serão salvos em `docs/index.html` e `docs/agenda_facil.html`.

---

## 🛡️ Regras de Validação e Tratamento de Exceções

O módulo implementa práticas defensivas e não permite falhas silenciosas:

1. **Cláusulas de Guarda (Guard Clauses):** Todas as funções públicas (`marcar_consulta`, `remarcar_consulta`, `listar_atendimentos_do_dia`) validam pré-condições no topo antes de executar qualquer lógica.
2. **Exceções Específicas com Valores:** Entradas inválidas não passam despercebidas e apontam explicitamente qual valor causou a falha:
   * `ValueError`: Nomes vazios, formatos de data incorretos, durações não-positivas ($\le 0$) ou horas fora do intervalo $[0, 23]$.
   * `HorarioInvalidoError`: Atendimentos que começam ou terminam fora do horário de funcionamento (08:00 às 17:00).
   * `ConflitoHorarioError`: Tentativas de marcação em horários com sobreposição de consultas para o mesmo profissional ou mesmo paciente.
   * `ConsultaNaoEncontradaError`: Tentativas de remarcação de consultas inexistentes.
3. **Ausência de Capturas Genéricas:** Não existem blocos `except:` vazios ou capturas de exceções genéricas não tratadas no código.
