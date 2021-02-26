
## Melhor Envio - Data Engineer

### Tecnologias

- Python
- MySQL

--------------

### Instruções

O arquivo [logs.txt](https://drive.google.com/open?id=1GliYD4Q19_f6S88iFsn0dk8dGLhB9YXF) contém informações de log geradas por um sistema gateway, cada solicitação foi registrada em um objeto JSON separado por uma nova linha `\n`, com o seguinte formato:

![JSON](JSON.md)

***Algumas considerações sobre o objeto JSON acima:***

`latencies` contém alguns dados sobre as latências envolvidas:
- `proxy`  é o tempo levado pelo serviço final para processar a requisição.
- `kong`  é a latência referente a execução de todos os plugins pelo Kong (gateway).
- `request`  é o tempo decorrido entre o primeiro byte ser lido do cliente e o último byte ser enviado a ele. Útil para detectar clientes lentos.

--------------

### Requisitos

- Processar o arquivo de [log](JSON.md), extrair informações e salvá-las em um banco de dados.
- Estruturar esse [banco](DatabaseModel.md) de forma relacional.
- Buscar a normalização desse banco de dados.
- Gerar um relatório para cada descrição abaixo, em formato csv: 
	- [Requisições](Request.md) por [consumidor](TabelaConsumidor.md);
		- Principais caracteristicas de [Consumidor](Consumidor.md) 
	- Requisições por [serviço](TabelaServicos.md);
		- Principais caracteristicas de [servico](servico.md) 
	- Tempo médio de request, proxy e kong por serviço.
		- Principais caracteristicas de [Latencia](Latencia.md) 
- Documentar passo a passo de como executar o teste através de um arquivo [README.md](README.md).
- Efetue o `commit` de todos os passos do desenvolvimento em um ***git público*** de sua preferência e disponibilize apenas o link para o repositório.

