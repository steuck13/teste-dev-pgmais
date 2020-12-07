# teste-dev-pgmais
Esse repositório contém o código referente ao teste prático tal qual descrito em https://github.com/pgmais/teste-dev e foi desenvolvido utilizando a linguagem Python.

## Execução
```
$ python3 broker-messaging.py messages_file
```
## Testes
Todos os testes unitários encontram-se no arquivo `message_test.py` e podem ser executados com o seguinte comando:
```
$ python3 -m unittest message_test.py
```

## Bibliotecas e ferramentas
Algumas bibliotecas inclusas com a linguagem foram utilizadas nesse projeto:
* `unittest` - para criação de tests unitários
* `re` - para validação do número (sem ddd) de telefone
* `requests` - para verificar se um dado número consta ou não em uma blacklist
* `datetime` - para validação do horário de envio da mensagem
* `argparse` - para gerenciar os argumentos do script `broker-messaging.py`

O desenvolvimento foi feito utilizando o editor `VSCodium` (versão totalmente aberta do VSCode), em sistema operacional CentOS Linux 8.