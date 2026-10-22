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

---

# Correções

Todas as correções foram aplicadas no arquivo `agenda_facil.py`, que substitui o `agenda_base.py`.

## 1. Adequação e lógica

### Anomalia 01 — Múltiplas responsabilidades nas funções

**Correção:** A lógica que ficava misturada dentro de `add` e `rem` foi separada em funções auxiliares com uma única responsabilidade cada: `_validar_data`, `_dentro_do_expediente`, `_ha_sobreposicao`, `_buscar_consulta`, `_verificar_disponibilidade` e `_imprimir_mensagem`. As funções públicas `marcar_consulta` e `remarcar_consulta` passaram a apenas orquestrar: validam as entradas, consultam as auxiliares e efetivam a operação.

### Anomalia 02 — Uso de arrays com acesso por índice

**Correção:** A lista `ag` de listas posicionais (`a[2]`, `a[3]`...) foi substituída pela lista `agenda: list[Atendimento]`, onde `Atendimento` é uma `dataclass` com os campos nomeados `paciente`, `profissional`, `data`, `hora`, `duracao` e `status`. O acesso passou a ser por nome (`consulta.data`), eliminando a necessidade de memorizar posições. Foram adicionadas também as propriedades `inicio` e `fim`, que calculam o intervalo real do atendimento.

### Anomalia 03 — Comentário que identifica incorretamente o comportamento

**Correção:** O comentário "lista os atendimentos do mes" foi removido. A função foi renomeada para `listar_atendimentos_do_dia`, e sua docstring descreve corretamente que ela lista os atendimentos de uma data específica, em ordem cronológica, e retorna essa lista.

---

## 2. Manutenibilidade

### Anomalia 01 — Nomenclatura inadequada

**Correção:** Funções, parâmetros e variáveis receberam nomes que expressam sua responsabilidade: `add` → `marcar_consulta`, `rem` → `remarcar_consulta`, `lst` → `listar_atendimentos_do_dia`, `ag` → `agenda`, `p` → `paciente`, `pr` → `profissional`, `d` → `data`, `h` → `hora`, `dur` → `duracao`, `nd`/`nh` → `nova_data`/`nova_hora`. As funções internas usam o prefixo `_`.

### Anomalia 02 — Repetição da lógica de verificação de disponibilidade

**Correção:** O bloco duplicado foi centralizado em `_verificar_disponibilidade`, usada tanto por `marcar_consulta` quanto por `remarcar_consulta`. O parâmetro `consulta_ignorada` permite que a remarcação desconsidere o próprio atendimento que está sendo movido. A verificação passou a comparar intervalos reais de tempo (`_ha_sobreposicao`), e não apenas horários de início idênticos, e considera conflito tanto do profissional quanto do paciente.

### Anomalia 03 — Valores de horário espalhados pelo código

**Correção:** Os valores de funcionamento da clínica foram extraídos para as constantes `HORARIO_INICIO = 8` e `HORARIO_FIM = 17`, usadas por `_dentro_do_expediente` e nas mensagens de erro. Para alterar o expediente, basta mudar as constantes em um único lugar.

---

## 3. Organização e estética

### Anomalia 01 — Histórico de alterações no cabeçalho

**Correção:** O cabeçalho com autores e datas de alteração foi removido e substituído por uma docstring de módulo que descreve o propósito do arquivo. O histórico fica a cargo do Git.

### Anomalia 02 — Código morto

**Correção:** A função `desmarcar` comentada e o `TODO` antigo foram removidos.

### Anomalia 03 — Comentários que descrevem ações, mas não justificam decisões

**Correção:** Os comentários redundantes ("adiciona na lista", "remarca o atendimento"...) foram removidos, já que os novos nomes deixam a ação clara. A documentação passou a ser feita por docstrings com argumentos, retorno e exceções. Os comentários que restaram apenas sinalizam as cláusulas de guarda (pré-condições).

---

## 4. Programação defensiva e segurança

### Anomalia 01 — Exceção ignorada com `except: pass`

**Correção:** O `try/except` que engolia qualquer erro foi removido. No lugar, foram criadas cláusulas de guarda que validam paciente e profissional vazios, duração menor ou igual a zero, data inválida e hora fora de 0 a 23, levantando `ValueError` com mensagem clara, incluindo o valor informado. Foram criadas as exceções específicas `ErroAgenda`, `HorarioInvalidoError` (fora do expediente) e `ConsultaNaoEncontradaError` (remarcação de consulta inexistente, que antes falhava silenciosamente). Além disso, o aninhamento de `if` foi substituído por essas cláusulas de guarda.

### Anomalia 02 — Ausência de validação da duração máxima do atendimento

**Situação:** Não corrigida. A nova versão valida que a duração seja maior que zero e que o atendimento termine dentro do expediente (o que limita indiretamente a duração a 9 horas), mas ainda não existe a verificação do limite de 120 minutos. Correção pendente: criar a constante `DURACAO_MAXIMA = 120` e validá-la em `marcar_consulta` com `ValueError`.

---

## 5. Desempenho e recursos

### Anomalia 01 — Complexidade ciclomática elevada

**Correção:** A complexidade que estava concentrada na antiga função `add` (quatro `if` aninhados, `try/except` e laço com condição composta) foi distribuída entre funções pequenas e cláusulas de guarda, e a condição composta de conflito foi encapsulada em `_ha_sobreposicao` e `_verificar_disponibilidade`. Assim, cada função tem poucos caminhos de execução e é mais simples de testar. O valor numérico da nova complexidade ainda não foi medido; recomenda-se calculá-lo com uma ferramenta como `radon cc` para registrar o resultado.

---

## Observação sobre mudança de comportamento

No código original, uma consulta podia começar até as 17h, mesmo que terminasse depois das 18h. Na nova versão, o atendimento inteiro (início e fim) precisa caber entre 08:00 e 17:00. Esse é um ajuste intencional na regra de expediente, mas vale confirmar se `HORARIO_FIM = 17` é o valor desejado.