# Castelie Cookie Shop

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

## GitHub push automatico

O app faz `git add/commit/push` quando o pedido e finalizado.

1. Configure o repositorio remoto:

```powershell
git init
git branch -M main
git remote add origin https://github.com/felipepereira160-a11y/CastelieCookieShop.git
```

2. Configure autenticacao:

- Opcao A: usar Git Credential Manager (recomendado no Windows).
- Opcao B: usar token pessoal do GitHub e fazer login no `git` quando pedir.

Se seu branch principal nao for `main`, defina:

```powershell
$env:GIT_BRANCH="master"
```
