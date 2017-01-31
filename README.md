# Probability of software failure detection

O objetivo do presente documento trata-se de avaliar a efectividade da utilização de *test suites* de variadas complexidades na deteção de falhas em blocos de *software*.

O método aplicado consistiu na aplicação de um cenário experimental, baseado numa técnica de *black testing*, centrando as nossas atenções na relação *input/output*. O procedimento aplicado baseou-se na seleção de um conjunto de blocos de *software* e, utilizando o injetor de falhas *ucXception*, na aplicação de diferentes tipos de erros nos códigos seleccionados. Estes programas consistiram em códigos na linguagem *C* e com tamanhos médios de 150 linhas de código. Através da submissão de *test suites* previamente elaborados e testados no código original, avaliou-se a efectividade dos referidos *test suites* na deteção da falha injetada em cada código alterado, através da comparação dos *outputs* gerados. A ocorrência de falhas de uma qualquer outra ordem durante a execução, é descartada, visto tratarem-se de um consequência de uma falha provocada pela injeção de falhas e não de uma verificação através do uso de *test suites*.

Após a execução do cenário experimental desenhado, foi possível analisar os resultados e qual foi a capacidade demonstrada pelos *test suites* no processo de deteção de falhas em blocos de *software*.

Como conclusão, foram executados alguns testes de hipótese que nos permitiram fazer uma previsão do que poderia acontecer caso o cenário experimental fosse repetido.
