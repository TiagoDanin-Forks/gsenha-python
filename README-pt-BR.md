# GSenha Cliente Python
[![Build Status](https://travis-ci.com/globocom/gsenha-python.svg?branch=master)](https://travis-ci.com/globocom/gsenha-python)

Cliente para [gsenha-api](https://github.com/globocom/gsenha-api)

## Instalação
```bash
pip install gsenha
```

## Uso
```python
from gsenha import PasswordManager
pm = PasswordManager(GSENHA_ENDPOINT, GSENHA_USER, GSENHA_PASS, GSENHA_KEY|GSENHA_KEY_PATH, verify='path_to_your_private_cert')
pm.get_passwords(folder, name1, name2, name*)
```

* GSENHA_ENDPOINT: Endpoint para [gsenha-api](https://github.com/globocom/gsenha-api)
* GSENHA_USER: Usuário para [gsenha-api](https://github.com/globocom/gsenha-api)
* GSENHA_PASS: Senha para [gsenha-api](https://github.com/globocom/gsenha-api)
* GSENHA_KEY: Chave privada de usuário para [gsenha-api](https://github.com/globocom/gsenha-api)
* GSENHA\_KEY\_PATH: Caminho da chave privada de usuário para [gsenha-api](https://github.com/globocom/gsenha-api)

GSenha deve usar chave privada bruta como string ou carregar arquivo do sistema de arquivos.

Você pode usar essas *variáveis de ambiente* e não passar todas elas ao inicializar o **PasswordManager**:

```python
from gsenha import PasswordManager
pm = PasswordManager()
pm.get_passwords(folder, name1, name2, name*)
```

## Contribuição

Para desenvolvimento e contribuição, por favor veja o [Guia de Contribuição](https://github.com/globocom/gsenha-python/blob/master/CONTRIBUTING.md) e SEMPRE respeite o [Código de Conduta](https://github.com/globocom/gsenha-python/blob/master/CODE_OF_CONDUCT.md)

*Este artigo foi traduzido do [Inglês](README.md) para [Português (Brasil)](README-pt-BR.md).*
