# Orbeon Stamped

Gera arquivos em .PDF A4 timbrado

## 1. Requirements dev

```bash
python -m pip install --upgrade pip
python -m pip install pip-tools
pip-compile --strip-extras
pip install -r requirements-dev.txt
```

```bash
python -m pip install --upgrade pip && python -m pip install pip-tools && pip-compile --strip-extras && pip install -r requirements-dev.txt
```

## Update on PyPI

```bash
# Install this library if it hasn't been installed yet
pip install twine
# Prepare the packages
python setup.py sdist bdist_wheel
# Upload with Twine
twine upload dist/*
```
