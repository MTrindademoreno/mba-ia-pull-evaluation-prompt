**A) Seção "Técnicas Aplicadas (Fase 2)":**

## Técnicas de Prompt Engineering Aplicadas

### 1. Role Prompting

Usei Role Prompting porque percebi que o modelo precisava de um ponto de referência claro para saber *com que nível de qualidade* gerar o output. Sem uma persona definida, o modelo respondia como um assistente genérico — produzia User Stories simples que tecnicamente estavam corretas, mas não tinham o nível de detalhe que um time ágil esperaria em um refinamento real.

Ao definir a persona como especialista em Engenharia de Requisitos com experiência como Product Owner e Tech Lead, o modelo passou a adotar implicitamente critérios que eu não precisaria descrever um a um — como saber quando incluir contexto técnico, quando usar a perspectiva do sistema como persona, ou como estruturar critérios de aceitação testáveis. A persona carrega esse conhecimento de domínio embutido.

**Trecho do prompt:**
```
Você é um especialista em Engenharia de Requisitos, Product Discovery e Gestão de Backlog,
com experiência atuando como Product Owner e Tech Lead em equipes ágeis.

Sua responsabilidade é transformar relatos de bugs escritos por usuários em User Stories
bem estruturadas, prontas para refinamento técnico.
```

### 2. Chain of Thought

Adicionei o Chain of Thought porque o problema de converter um bug em User Story não é trivial — envolve múltiplas decisões sequenciais: entender o bug, identificar quem é afetado, classificar a complexidade, decidir quais seções incluir. Sem guiar esse raciocínio, o modelo tendia a pular etapas e gerar outputs incompletos.

O "Processo de Análise" com 10 passos força o modelo a raciocinar antes de escrever. Instruí que esse raciocínio não aparecesse no output final, porque quero apenas o artefato gerado — mas o processo interno melhora significativamente a qualidade do resultado. Foi essa técnica que resolveu os casos em que o modelo escolhia a persona errada ou omitia seções relevantes para a complexidade do bug.

**Trecho do prompt:**
```
## Processo de Análise

Antes de gerar a resposta, siga internamente o processo abaixo:

1. Compreenda o relato do usuário.
2. Identifique a funcionalidade afetada.
3. Identifique o comportamento observado e o comportamento esperado.
4. Identifique qual necessidade do usuário deixou de ser atendida.
5. Defina a persona correta: se o bug afeta o sistema como ator principal
   (webhooks, validações de estoque, integrações), use "Como o sistema";
   se afeta um perfil de usuário específico, use aquele perfil.
6. Classifique a complexidade do bug: simples, médio ou complexo.
7. Extraia todos os detalhes técnicos do relato: endpoints, códigos HTTP, logs,
   tempos de resposta, limites numéricos, componentes afetados —
   preserve-os sem filtrar ou resumir.
8. Identifique todos os cenários que precisam de critérios próprios: cenário principal,
   cenários de prevenção, edge cases, acessibilidade, múltiplos componentes.
9. Para bugs críticos com impacto quantificado, inclua uma seção "Métricas de Sucesso"
   com os valores atuais vs esperados.
10. Estruture a User Story com todas as seções adequadas ao nível de complexidade.

Não exponha essa análise na resposta final.
```

### 3. Few-shot Learning

Usei Few-shot Learning porque descrições em prosa de "o que fazer" não eram suficientes para o modelo entender o formato exato esperado — especialmente para bugs complexos, onde o output tem múltiplas seções com nomes específicos.

Construí 4 exemplos cobrindo os 3 níveis de complexidade (simples, médio e complexo), cada um demonstrando o formato correto de saída. O exemplo de bug complexo foi o mais crítico: sem ele, o modelo não sabia que devia usar seções `=== ===`, incluir "Múltiplos Componentes Afetados" ou "Métricas de Sucesso". Ver um exemplo concreto foi mais eficaz do que qualquer instrução textual que eu pudesse escrever.

**Trecho do prompt (Exemplo 2 — demonstrando persona "Como o sistema" e Critérios de Prevenção):**
```
Relato de Bug:
Carrinho permite finalizar compra mesmo com produto fora de estoque.

User Story:
Como o sistema de e-commerce,
eu quero validar disponibilidade de estoque antes de permitir finalização de compra,
para que não sejam criados pedidos que não podem ser atendidos.

Critérios de Aceitação:
- Dado que um produto está no carrinho
- Quando o cliente tenta finalizar a compra
- Então o sistema deve validar estoque disponível em tempo real
- E se o produto estiver fora de estoque, deve bloquear a compra

Critérios de Prevenção:
- Quando produto ficar sem estoque
- E houver itens em carrinhos de outros clientes
- Então deve exibir aviso "estoque limitado" ao adicionar
- E deve reservar estoque temporariamente (15 minutos) ao ir para checkout
```

### 4. Structured Output

Usei Structured Output porque a avaliação automática compara a resposta gerada com uma referência usando F1-Score — e para o Recall ser alto, o output precisa cobrir as mesmas seções que a referência. Se o modelo gerasse o conteúdo certo em uma estrutura diferente, o avaliador não reconheceria as informações e penalizaria o Recall.

Defini templates de saída explícitos para cada nível de complexidade, mostrando o esqueleto antes dos exemplos. Para bugs complexos, o template lista exatamente as seções esperadas com seus nomes. Isso eliminou a variação de formato entre execuções e garantiu que o modelo sempre produzisse um output estruturalmente compatível com o que o dataset de avaliação esperava.

**Trecho do prompt (template para bugs complexos):**
```
=== USER STORY PRINCIPAL ===

Título: [título descritivo do problema geral]

Descrição:
Como [persona detalhada], eu quero [ação completa], para que [benefício de negócio].

=== CRITÉRIOS DE ACEITAÇÃO ===

A. [Nome do Problema 1] - [descrição curta]:
- Dado que [contexto]
- Quando [ação]
- Então [resultado]

=== CRITÉRIOS TÉCNICOS ===

[Área 1]:
- [detalhe técnico extraído do relato, com valores exatos]

=== CONTEXTO DO BUG ===

Severidade: [CRÍTICA / ALTA / MÉDIA]

Múltiplos Componentes Afetados:
- [componente]: [o que está impactado]

=== TASKS TÉCNICAS SUGERIDAS ===

[Sprint/Fase 1] - [nome] ([tempo estimado]):
1. [ÁREA] descrição da task

=== MÉTRICAS DE SUCESSO ===

Antes vs Depois:
- [métrica atual extraída do relato] → [meta esperada]
```

**B) Seção "Resultados Finais":**

- Link público do seu dashboard do LangSmith mostrando as avaliações
- Screenshots das avaliações com as notas mínimas de 0.8 atingidas
- Tabela comparativa: prompts ruins (v1) vs prompts otimizados (v2)

**C) Seção "Como Executar":**

- Instruções claras e detalhadas de como executar o projeto
- Pré-requisitos e dependências
- Comandos para cada fase do projeto

**3. Evidências no LangSmith:**

- Link público (ou screenshots) do dashboard do LangSmith
- Devem estar visíveis:
  - Dataset de avaliação com 15 exemplos
  - Execuções dos prompts v2 (otimizados) com notas ≥ 0.8
  - Tracing detalhado de pelo menos 3 exemplos

---
