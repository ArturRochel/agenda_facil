# Análise de anomalias do código

## 1. Adequação e lógica

### Anomalia 01 — Múltiplas responsabilidades nas funções

**Onde:** Funções de marcação e remarcação de consultas.

**Por que é um problema:** As funções normalmente realizam a verificação da disponibilidade de horário antes de adicionar ou remarcar uma consulta, aumentando a complexidade ciclomática e a repetição de código.

### Anomalia 02 — Uso de arrays com acesso por índice

**Onde:** Linha 8.

**Por que é um problema:** Em vez de utilizar uma classe para gerar os objetos que representam os atendimentos, o código utiliza um array sem validação estrutural. É necessário lembrar a posição e o significado de cada informação, dificultando a leitura, a interação e a manutenção.

### Anomalia 03 — Comentário que identifica incorretamente o comportamento

**Onde:** Função de listagem.

**Por que é um problema:** O comentário não corresponde corretamente ao comportamento da função, podendo induzir o desenvolvedor ao erro durante a leitura e a manutenção do código.

---

## 2. Manutenibilidade

### Anomalia 01 — Nomenclatura inadequada

**Onde:** Variáveis e funções espalhadas pelo código.

**Por que é um problema:** A nomenclatura inadequada dificulta a identificação das responsabilidades e a compreensão da lógica, prejudicando a leitura, a interpretação e a manutenção do código.

### Anomalia 02 — Repetição da lógica de verificação de disponibilidade

**Onde:** Linhas 10 e 29, nas funções de marcar e remarcar consultas.

**Por que é um problema:** As duas funções repetem o bloco de código que verifica a disponibilidade do horário. Essa lógica poderia ser centralizada em uma função específica, reduzindo a duplicação.

### Anomalia 03 — Valores de horário espalhados pelo código

**Onde:** Verificações dos horários permitidos.

**Por que é um problema:** Os horários de funcionamento da clínica estão definidos diretamente nas verificações, dificultando a compreensão e a alteração desses valores.

---

## 3. Organização e estética

### Anomalia 01 — Histórico de alterações no cabeçalho

**Onde:** Linhas 1 a 6.

**Por que é um problema:** O histórico de alterações não agrega valor ao código, pois o Git e outras plataformas de versionamento já registram essas mudanças. Além disso, esse tipo de comentário pode ficar desatualizado.

### Anomalia 02 — Código morto

**Onde:** Linha 45.

**Por que é um problema:** Existe uma função chamada `desmarcar` que foi iniciada e posteriormente comentada. Esse código não executável polui a base de código e dificulta sua leitura.

### Anomalia 03 — Comentários que descrevem ações, mas não justificam decisões

**Onde:** Linhas 11, 30 e 52.

**Por que é um problema:** Os comentários descrevem o que as funções fazem, mas não explicam a motivação ou as decisões tomadas. Se a nomenclatura fosse clara, esses comentários seriam dispensáveis.

---

## 4. Programação defensiva e segurança

### Anomalia 01 — Exceção ignorada com `except: pass`

**Onde:** Linha 26.

**Por que é um problema:** O tratamento de exceção não realiza nenhuma ação. Quando ocorre um erro, ele é ignorado, sem aviso ou tratamento adequado, dificultando a identificação e a correção de falhas.

### Anomalia 02 — Ausência de validação da duração máxima do atendimento

**Onde:** Funções de marcação e remarcação de consultas.

**Por que é um problema:** Não existe uma verificação da duração máxima permitida de 120 minutos. Essa falha na validação da regra de negócio permite o agendamento de consultas com duração superior ao limite estabelecido.

---

## 5. Desempenho e recursos

### Anomalia 01 — Complexidade ciclomática elevada

**Onde:** Arquivo inteiro.

**Por que é um problema:** A soma da complexidade ciclomática das funções resulta em 23, indicando uma quantidade significativa de caminhos de execução a considerar nos testes. A função de adicionar um agendamento contribui consideravelmente para esse valor devido à quantidade de estruturas `if` e operadores `&&` presentes.