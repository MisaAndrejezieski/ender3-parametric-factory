# ender3-parametric-factory

Projeto de estudo para gerar cases técnicos paramétricos com build123d e explorar projeções de renda com impressão 3D.

## Ambiente

No Windows, crie e ative o ambiente virtual e instale as dependências:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Testes

```powershell
pytest -v
```

## Gerador

```powershell
python src\main.py
# ou
python -m src.main
```

O arquivo STL será criado em `output/`.
