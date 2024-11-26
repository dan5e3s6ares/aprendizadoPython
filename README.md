# aprendizadoPython

## Descrição
Desafio LangChain com DB Vetorial

## Requisitos
- Docker
- docker compose

### API KEY

Atualize o campo COHERE_API_KEY com a sua própria API Key da [Cohere](https://dashboard.cohere.com/welcome/login)

### Rode o Sistema

```sh
docker compose up --build -d
```

### Visualize os logs

Visualize os logs do container e aguarde o aviso : Application startup complete.

```sh
docker logs -f aprendizadopython
```

### Chat

Acesse o chat para realizar suas perguntas [chat](http://localhost:8000/chat)

Sempre que você fizer uma afirmação verdadeira e formal, ela será salva no Banco de Dados.

> O tema escolhido como estudo para a conversa é "sci.space" </p>
> O tema está todo em Inglês, portanto a conversa deve ser realizada toda em Inglês


### Atalho para Afirmações feitas pelo usuário

Acesse o endpoint [lista](http://localhost:8000/learned) para verificar o que foi salvo de informações fornecida pelo usuário



