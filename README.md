# Orders System

Sistema legado para gerenciamento de pedidos desenvolvido em Python, utilizando persistência em arquivos JSON.

## Funcionalidades

O sistema permite:

* Cadastro e leitura de pedidos armazenados em JSON;
* Cálculo de subtotal, impostos, descontos e frete;
* Geração de relatório de pedidos;
* Aprovação automática de pedidos pendentes;
* Alteração controlada do status dos pedidos;
* Persistência automática das alterações.

---

# Evolução implementada (TP2)

Como parte do Trabalho Prático 2 da disciplina de Evolução de Software, foi implementada uma evolução relacionada ao controle do ciclo de vida dos pedidos.

A nova funcionalidade permite alterar manualmente o status de um pedido, respeitando regras de negócio previamente definidas.

## Fluxo de status

As seguintes transições são permitidas:

```text
pending
 ├── paid
 └── cancelled

paid
 ├── shipped
 └── cancelled

shipped
 └── delivered

delivered
 └── (estado final)

cancelled
 └── (estado final)
```

Os estados **approved** e **manual_review** continuam sendo utilizados exclusivamente pela rotina automática de aprovação existente no sistema legado.

---

# Validações implementadas

A evolução adicionou as seguintes validações:

* Verificação da existência do pedido;
* Validação do novo status informado;
* Controle das transições permitidas entre estados;
* Persistência automática da alteração no arquivo JSON;
* Mensagens claras de sucesso ou erro para o usuário.

---

# Estrutura do projeto

```
orders_system/
│
├── app.py
├── config.py
├── data/
│   └── orders.json
├── services/
├── utils/
├── tests/
│   └── test_order_status.py
└── README.md
```

---

# Como executar

Executar o sistema:

```bash
python app.py
```

---

# Executar os testes

```bash
python -m unittest discover -s tests -v
```

---

# Tecnologias utilizadas

* Python 3
* JSON
* unittest
* Git
* GitHub

---

# Organização da evolução

A implementação foi desenvolvida utilizando uma branch específica:

```
feature/tp2-alteracao-status-pedido
```

A evolução foi registrada por meio de commits incrementais, contemplando:

1. Implementação da lógica de negócio para alteração controlada de status;
2. Integração da funcionalidade ao menu e aos relatórios;
3. Criação de testes automatizados;
4. Atualização da documentação;
5. Geração da versão final (Release v2.0-tp2).

---

# Autor

Projeto desenvolvido para a disciplina de Evolução de Software como atividade prática de manutenção e evolução de sistemas legados.

Camila Eduarda Servat, Jayne Thaís Budny, Júlia Bourscheid