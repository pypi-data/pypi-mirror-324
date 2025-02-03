# Python CNPJ/CPF

[![Build Status](https://dev.azure.com/omorenodovale/pycnpj-cpf/_apis/build/status%2Fpycnpj-cpf?branchName=main)](https://dev.azure.com/omorenodovale/pycnpj-cpf/_build/latest?definitionId=5&branchName=main)
[![CI](https://github.com/carlos-moreno/pycnpj-cpf/actions/workflows/main.yml/badge.svg)](https://github.com/carlos-moreno/pycnpj-cpf/actions/workflows/main.yml)

Python CNPJ/CPF is a library created to validate the entered value, indicating whether it is a valid CNPJ or CPF.

## Installation

```py
pip install pycnpj-cpf
```


## Usage in CLI mode

```sh
$ #verify CNPJ
$ pycnpj-cpf validate --value="37.538.534/0001-86"
$
$ pycnpj-cpf validate --value="AB.2YW.3Z5/01DE-83"
$
$ pycnpj-cpf validate --value="37538534000186"
$ #verify CPF
$ pycnpj-cpf validate --value="237.491.140-30"
$
$ pycnpj-cpf validate --value="23749114030"
$
```

## Usage in Python file

```py
>>> from pycnpj_cpf.core import cnpj_or_cpf_is_valid
>>>
>>> cnpj_or_cpf_is_valid("31.851.707/0001-35")
True
>>>
>>> cnpj_or_cpf_is_valid("12.2HI.345/01DE-40")
True
>>>
>>> cnpj_or_cpf_is_valid("492.711.290-08")
True
>>>
>>> cnpj_or_cpf_is_valid("49271129008")
True
>>>
>>> cnpj_or_cpf_is_valid("31851707000135")
True
>>>
>>> cnpj_or_cpf_is_valid("12ABC34501DE35")
True
>>>
>>> cnpj_or_cpf_is_valid("31.851.707/0001-40")
False
>>>
>>> cnpj_or_cpf_is_valid("31.851.707/000140")
False
>>>
>>> cnpj_or_cpf_is_valid("31.851.707/0001-40a")
False
>>>
>>> cnpj_or_cpf_is_valid("12.2HI.345/01DY-40")
False
>>>
>>> cnpj_or_cpf_is_valid("31.851.707/0001-40 ")
False
>>>
>>> cnpj_or_cpf_is_valid("37537026000106")
False
>>>
>>> cnpj_or_cpf_is_valid("37538036000106")
False
>>>
```
