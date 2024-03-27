# Trabalha Brasil Apply Bot
Realiza candidaturas nos resultados de uma busca dado as keywords e a localização

## Requisitos
- Mozilla Firefox
- Sqlite3

## Instalação
1. insira no terminal: python3 -m venv env
2. insira no terminal: source ./env/bin/activate ou \env\Scripts\activate no windows
3. insira no terminal: pip install -r requirements.txt

## Instruções
1. Passe as informações no arquivo params.json como veja o exemplo:
```
{
    "cpf": "01234567890",
    "data_nascimento": "01012001",
    "keywords": "programador",
    "location": "rio de janeiro rj",
    "home-office": false,
    "ordenacao": 1
}
```
- O seu cpf deve ser passado com somente os números
- A sua data de nascimento deve ser passada com somente os números
- location deve ser passada como no formato acima, [cidade] [sigla do estado], como em: rio de janeiro rj, são paulo sp, duque de caxias rj. Se não quiser passar uma localização, basta tirar o campo location do params.json 
- home-office é true quando as vagas a serem procuradas são somente em home office e false caso contrário
- ordenacao: 1 se for sem filtro, 2 se for ordenado pelas últimas vagas e 3 se for pelos maiores salários
2. Rode o código bot.py

## Observações
- Pode ser que em algum momento o bot pare de funcionar já que a página web pode mudar e assim vai mudar a forma como o bot seleciona as tags, então se esse for o caso abra um issue.
