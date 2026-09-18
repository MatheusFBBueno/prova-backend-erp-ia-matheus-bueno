# Instruções de execução
# Respostas teóricas
## Questão 1
Para o módulo ERP descrito, criaria microserviços para lidar com a entrada de pedidos, com a contagem de estoque e com o registro de movimentações.
Assumindo que o módulo de clientes se refere à plataforma por são agregados os pedidos de clientes, e que o módulo financeiro refere-se à plataforma de onde são gerados relatórios financeiros, usaria uma API gateway para direcionar as requisições e realizar controle de permissões com base na sessão do usuário (ex. impedir que uma requisição vinda do módulo de clientes faça pedidos de relatórios financeiros).
Idealmente, um domínio diferente para ambos seria mais apropriado, na minha opinião. No entanto, dado as configurações corretas do gateway, esta estrutura poderia ser usada de forma segura e utilizar um mesmo domínio.

Para comunicação entre módulos referindo aos pedidos de clientes, utilizaria filas de mensagens assíncronas, como no diagrama, para disparar as chamadas necessárias para verificar se o pedido é válido (se o item pedido está em estoque, e atualizar o mesmo caso o pedido prossiga). As filas serão configuradas para que sejam persistentes, de forma que se um dos microsserviços não responda imediatamente ou esteja temporariamente offline, os pedidos sejam armazenados para serem processados quando possível. As filas seguem o modelo de um produtor e múltiplos consumidores, pois as requisições disparam tanto solicitações de consulta de estoque e de registro de transações, que são separados em bancos diferentes para que a carga entre eles possa ser distribuída de forma mais eficiente (E para que consultas pesadas de relatórios financeiros não gere atrasos de leitura para operações de estoque).

As requisições vindas do módulo financeiro seguem um padrão síncrono REST, pois espero que o volume seja menor se comparado ao fluxo de clientes, e a espera do retorno de requisições não seja um fator de impedimento, diferentemente da área que interage com o cliente, que requer agilidade para processar os pedidos e gerar uma experiência de usuário fluida.

Além do registro de movimento de estoque, o serviço de logging também pode disponibilizar métricas coletadas dos pedidos para um graphana para facilitar observabilidade de possíveis gargalos na infraestrutura, com as mensagens coletadas das filas tendo o tempo de entrada de um pedido e da geração de uma resposta.
Finalmente, para otimizar tanto a consulta de estoque de itens frequentemente visualizados, e para reduzir o tempo de execução de relatórios frequentes, incluiria um cache Redis nas interfaces de ambos os bancos, considerando a quantidade de requisições.
![Diagrama de módulos ERP](anexos/Diagrama%20alto%20nivel%20ERP.svg)

## Questão 2
# Uso de IA