# prova 22/09/26
prova 22/09/26

# SafeFactory: Inteligência Artificial para Segurança Industrial e Inclusão (HSE)

O **SafeFactory** é uma solução para o chão de fábrica baseada em Inteligência Artificial. Ele resolve simultaneamente dois gargalos críticos da indústria de manufatura: o monitoramento falho do uso de Equipamentos de Proteção Individual (EPIs) e a falta de acessibilidade para colaboradores com deficiência auditiva em zonas de maquinário pesado.

## 🚀 O Problema e o Impacto Industrial

O projeto aborda duas frentes estruturais essenciais:
1. **Segurança Proativa:** Substitui a fiscalização humana falha por monitoramento automatizado, prevenindo acidentes severos, paradas de produção e custos com sinistros ou multas trabalhistas (alinhado às normas **NR-6** e **NR-12**).
2. **Inclusão Acessível:** Transforma alertas de emergência essencialmente sonoros (sirenes) em eventos digitais instantâneos para visualização tátil ou luminosa, garantindo a autonomia de operadores PcD auditivos.

### Personas do Sistema
* **Carlos (42 anos) - Gestor de HSE:** Precisa de dados preditivos consolidados para antecipar sinistros industriais, auditorias e relatórios automatizados de conformidade.
* **Mateus (28 anos) - Operador de Maquinário (Surdo):** Precisa trabalhar em áreas de alto risco com total confiança de que será alertado de emergências em tempo real.

---

## 🧠 O Core de Inteligência Artificial

A arquitetura lógica do sistema divide-se em dois motores de IA paralelos:
* **Visão Computacional (YOLOv8):** Processamento de vídeo em tempo real integrado ao circuito de CFTV. Identifica os operadores humanos (`Person`) e calcula a sobreposição espacial (**Intersection over Union - IoU**) com as classes de EPI vinculadas à zona de risco (`Helmet`, `Vest`, etc.). Caso detecte um operador sem a proteção adequada, um gatilho de infração é disparado.
* **Classificação de Áudio (YAMNet / CNNs 1D):** Monitoramento contínuo do ambiente para isolar frequências e ritmos característicos de sirenes industriais de incêndio ou evacuação, distinguindo-as de ruídos comuns de furadeiras ou motores. Ao classificar o perigo, realiza a tradução digital imediata.

---

## 🏗️ Estrutura do Repositório

```text
industria-segura/
├── data/                      # Amostras e mídias de testes locais
├── models/                    # Pesos e artefatos de IA (.pt)
├── src/
│   ├── database/              # Persistência em ORM (SQLAlchemy) e logs preditivos
│   │   ├── __init__.py
│   │   └── connection.py
│   └── vision/                # Pipeline de processamento de Visão Computacional
│       ├── __init__.py
│       └── inference.py
├── .gitignore                 # Arquivo de exclusão de arquivos binários e caches
├── README.md                  # Documentação principal da solução
└── requirements.txt           # Dependências estritas do projeto
```

---

## 🛠️ Instalação Passo a Passo

### Pré-requisitos
* Python **3.10+** instalado.
* Gerenciador de pacotes `pip` atualizado.

### 1. Clonar e Acessar o Projeto
```bash
git clone https://github.com
cd industria-segura
```

### 2. Configurar o Ambiente Virtual (`venv`)
Crie e ative o ambiente virtual isolado para evitar conflitos de dependências globais:
* **Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
* **Linux / macOS:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Instalar Dependências do Projeto
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## ⚙️ Como Executar a Solução

Com o ambiente virtual (`venv`) ativado e na raiz do projeto, execute o script do pipeline de visão computacional:

```bash
python -m src.vision.inference
```
*Nota: Na primeira execução, o motor YOLOv8 fará o download do arquivo de pesos inteligentes oficial (`yolov8n.pt`) para o diretório `models/` de forma totalmente automatizada. O script iniciará sua WebCam ou mídia configurada em tempo real. Pressione a tecla **'q'** com a janela ativa para encerrar.*

---

## 📂 Modelagem de Dados Relacional (DER)

O banco de dados relacional (gerenciado via SQLAlchemy com SQLite para homologação) foi projetado para registrar os eventos com precisão cirúrgica de tempo e espaço, permitindo a construção de dashboards preditivos:

* **Tabela `log_infracao_epi`:** Guarda a estampa de tempo (`data_hora`), a identificação da câmera e setor, o tipo exato do EPI ausente detectado pela IA e a métrica de confiabilidade (`confianca_ia`) para geração de relatórios de conformidade.

---

## 📌 Histórico de Commits Semânticos

O desenvolvimento deste squad segue o padrão de mensagens de commit atômicas e padronizadas:
* `feat: setup initial architecture with yolo vision pipeline and db connection`
* `fix: correct database path resolution inside inference pipeline`
* `docs: create comprehensive production-ready readme documentation`
