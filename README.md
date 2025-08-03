# Sistema ETL e Dashboard Analítico de Indicadores Macroeconômicos

Este projeto foi desenvolvido como parte do Trabalho de Conclusão de Curso do MBA em Engenharia de Software – USP ESALQ. O sistema tem como objetivo automatizar o processo de extração, tratamento, armazenamento e visualização de dados econômicos provenientes de fontes oficiais brasileiras.

## 🧩 Componentes do Sistema

- **`extrair_dados.py`**: Script responsável por extrair dados de APIs públicas (BACEN, IBGE, IPEA), realizar transformação e persistência no banco PostgreSQL.
- **`app.py`**: Aplicação web desenvolvida com Dash e Plotly para visualização interativa de séries temporais e análise macroeconômica.

## 🔧 Tecnologias Utilizadas

- Python
- Dash e Plotly
- pandas
- SQLAlchemy
- PostgreSQL
- APIs públicas: Banco Central do Brasil, IBGE, IPEA

## 🚀 Como Executar

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 2. Configure o ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### 3. Execute o script de extração de dados

```bash
python extrair_dados.py
```

### 4. Inicie o dashboard analítico

```bash
python app.py
```

## 📈 Exemplo de Visualização

A aplicação Dash exibe gráficos interativos que facilitam a identificação de marcos econômicos relevantes, como recessões ou picos inflacionários.

## 📚 Licença

Este projeto é distribuído sob a licença MIT. Sinta-se livre para usar e adaptar.

## 👨‍💻 Autor

Pedro Henrique da Silva Carneiro  
MBA em Engenharia de Software – USP ESALQ