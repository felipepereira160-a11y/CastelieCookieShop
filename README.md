# Casteli? Cookie Shop

App Streamlit para catalogo, pedidos e area admin.

## Rodar local

```powershell
cd "c:\Users\felipe.silva\Downloads\Cookie's Shop"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

## Pastas

- `assets/products`: imagens dos produtos (use o mesmo id do catalogo)
- `data/catalog.json`: catalogo editavel
- `data/orders.csv` e `data/orders.xlsx`: pedidos salvos

## Admin

Defina a senha admin com a variavel de ambiente:

```powershell
$env:ADMIN_PASS="sua_senha"
```

## Email automatico (Gmail)

Crie uma senha de app no Gmail e configure as variaveis:

```powershell
$env:SMTP_HOST="smtp.gmail.com"
$env:SMTP_PORT="587"
$env:SMTP_USER="seu_email@gmail.com"
$env:SMTP_PASS="sua_senha_de_app"
$env:SMTP_TO="destino@gmail.com"
```

## GitHub push automatico

O app faz `git add/commit/push` quando o pedido e finalizado.

Localmente, use o Git Credential Manager.
Em servidores (Render), configure variaveis:

```powershell
$env:GIT_USERNAME="felipepereira160-a11y"
$env:GIT_REPO="CastelieCookieShop"
$env:GIT_TOKEN="seu_token_do_github"
$env:GIT_BRANCH="main"
```

## Render (deploy)

O `render.yaml` ja esta configurado. Basta conectar o repo no Render.
