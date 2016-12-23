# Probability of software failure detection

O objectivo do presente documento trata-se de avaliar a efectividade da utilização de *test suites* de variadas complexidades na deteção de falhas em blocos de software.

O procedimento aplicado baseou-se na seleção de um conjunto de blocos de software e, utilizando o injetor de falhas *ucXception*, na aplicação de diferentes tipos de erros nos códigos submetidos. Para estes blocos de software, foram utilizados códigos na linguagem C e com tamanhos médios de 150 linhas de código. Submetendo *test suites* previamente elaborados e testados no código original, avaliou-se a efectividade dos referidos *test suites* na deteção da falha injetada em cada código alterado, através da comparação dos *outputs* gerados ou de falhas de qualquer ordem durante a execução. De realçar o método de *testing* de *black box*, visto as nossas atenções se centrarem nos inputs e outputs.

Referindo a hipótese que deu azo ao presente estudo experimental, *É possível considerar, com 95% de certeza, que os nossos test suites detetam todo o conjunto de falhas injetadas no dataset de blocos de software considerado?*. Foi então possível de avaliar através do cálculo do intervalo de confiança associado à taxa de deteção de falhas injetadas em todos os blocos de software constituites do *dataset* original.

Como conclusão, podemos averiguar que a referida hipótese mencionada se verificaria falsa, aprensentando um intervalo de confiança bastante satisfatório, na ordem dos 84,55% +- 1,82%.
