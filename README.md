# Spotify Search Tool

Spotify Search Tool é uma aplicação Streamlit para buscar, exibir e salvar resultados musicais do Spotify.

## Objetivos
Esse repositório pretende documentar um projeto pessoal, resultado de alguns estudos intensivos. Nesse projeto, tive 
a oportunidade de exibir alguns conceitos importantes de desenvolvimento web, tais como consumo de API com todo o 
workflow envolvido (autorização > autenticação > obtenção de recursos), o desenvolvimento de uma aplicação web por 
um simples framework destinado à exibição de resultados e toda a lógica por trás desses componentes, inclusive a 
persistência dos dados, por um banco de dados SQL, gerenciado pelo ORM SQLAlchemy.

## Funcionalidades

- Busca de resultados musicais por nome do artista
- Exibição dos resultados em um DataFrame
- Download dos resultados como arquivo CSV

## Requisitos

- Python 3.7+
- Streamlit
- Pandas
- SQLAlchemy

## Instalação

### 1. Clone o repositório:

```
git clone https://github.com/LuanOliveira88/spotify_search_tool.git
cd spotify_search_tool
```

### 2. Crie um ambiente virtual e ative-o:

#### Linux
```
python -m venv venv
source venv/bin/activate
```
#### Windows

``` 
python -m venv venv
venv\Scripts\activate
```

### 3. Instale as dependências:

```
pip install -r requirements.txt
 ```

### 4. Configure as variáveis de ambiente no arquivo `.env`. 

Copie o exemplo abaixo e preencher `CLIENT_ID` e `CLIENT_SECRET` com suas credenciais da API do Spotify:

```
CLIENT_ID=your_spotify_client_id
CLIENT_SECRET=your_spotify_client_secret
DATABASE_URL=sqlite:///spotify_data.db
REDIRECT_URI=https://google.com
SPOTIFY_AUTH_URL=https://accounts.spotify.com/authorize
SPOTIFY_TOKEN_URL=https://accounts.spotify.com/api/token
SPOTIFY_API_URL=https://api.spotify.com/v1
```

Salve este conteúdo em um arquivo `.env` na raiz do projeto.

## Uso

1. Execute a aplicação localmente:

```
streamlit run app.py
```

2. No navegador, insira o nome do artista na barra lateral e clique no botão "Submit" para buscar os resultados.
3. Os resultados serão exibidos na área principal. Você pode baixar os resultados como arquivo CSV clicando e um dos
botões que surgem no canto superior direito do dataframe.

## Estrutura do Projeto

```
spotify_search_tool/
│
├── app.py
├── database.py
├── scripts.py
├── requirements.txt
├── .env
├── README.md
└── spotify_data.db
