# Trabalha Brasil Apply Bot
Realiza candidaturas nos resultados de uma busca dado as keywords e a localização

## Requisitos
- Mozilla Firefox

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
    "location": "rio de janeiro rj"
}
```
- O seu cpf deve ser passado com somente os números
- A sua data de nascimento deve ser passada com somente os números
- location deve ser passada como no formato acima, cidade sigla, como em: rio de janeiro rj, são paulo sp, rio grande do sul rs

## Observações
- É possível que o firefox use muita memória, então cuidado se o seu computador tiver pouca memória, eu reinicio o webdriver de tempos em tempos para diminuir o consumo de memória.
- Pode ser que em algum momento o bot pare de funcionar já que a página web pode mudar e assim vai mudar a forma como o bot seleciona as tags, então se esse for o caso abra um issue.
