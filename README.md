# Projeto 02 Estuda+

### Integrantes:
#### Anna Alyssia Dantas de Medeiros
#### Joeslyany Luanda da Silva Lopes
---
# Descrição:
O Estuda+ é uma aplicação web desenvolvida para ajudar estudantes a organizarem melhor sua rotina acadêmica e acompanharem suas atividades de forma prática e eficiente.
A ideia do projeto surgiu a partir das dificuldades que muitos alunos enfrentam para administrar tarefas, prazos, trabalhos e horários de estudo no dia a dia.

A plataforma permite que o usuário crie uma conta, realize login e tenha acesso ao seu próprio ambiente de estudos, onde poderá cadastrar, visualizar, editar e excluir tarefas.
Além disso, o sistema utiliza sessões em Flask e banco de dados SQLite3, permitindo um armazenamento mais seguro e organizado das informações dos usuários.
Com isso, o Estuda+ busca reunir em um único ambiente as principais atividades acadêmicas do estudante, facilitando o acompanhamento da rotina e contribuindo para uma melhor organização dos estudos.

---
# Objetivo: 
O objetivo do Estuda+ é desenvolver uma aplicação web simples, acessível e eficiente para auxiliar estudantes na organização de suas atividades acadêmicas e rotina de estudos. A plataforma contará com funcionalidades como cadastro de usuários, sistema de login, controle de sessões, área individual para cada usuário e gerenciamento de tarefas, permitindo adicionar, editar, excluir e visualizar atividades cadastradas. 

O desenvolvimento da aplicação será realizado utilizando Python com o framework Flask no back-end, além de HTML, CSS e JavaScript na construção da interface da plataforma. Já o SQLite3 será utilizado para armazenar os dados dos usuários e das atividades cadastradas no sistema. Ao final do desenvolvimento, espera-se que a aplicação contribua para uma rotina de estudos mais organizada, ajudando os estudantes no controle de suas tarefas e no gerenciamento do tempo.

---
# Justificativa
A organização da rotina de estudos é uma dificuldade comum entre muitos estudantes, principalmente devido à grande quantidade de atividades, conteúdos e prazos que precisam ser administrados ao mesmo tempo. Muitas vezes, a falta de planejamento pode causar atrasos, acúmulo de tarefas, dificuldade de concentração e queda no desempenho acadêmico. Pensando nisso, o Estuda+ foi desenvolvido com a proposta de oferecer uma ferramenta simples e prática que ajude os estudantes a manterem suas atividades organizadas em um único ambiente. 

A utilização do banco de dados SQLite3 permite armazenar as informações dos usuários e das tarefas de forma segura, enquanto o sistema de sessões em Flask possibilita um acesso mais organizado e personalizado dentro da plataforma. Além de facilitar o acompanhamento das atividades, o sistema também contribui para uma rotina mais produtiva e planejada, incentivando hábitos de estudo mais organizados e eficientes. Dessa forma, o Estuda+ busca auxiliar os estudantes no desenvolvimento de hábitos mais organizados, proporcionando maior controle sobre suas atividades acadêmicas e contribuindo para uma rotina de estudos mais eficiente.

---
# Principais problemas técnicos encontrados e soluções
Durante o desenvolvimento do projeto foram encontrados alguns desafios técnicos.
O primeiro foi a migração do banco de dados de SQLite3 utilizando comandos SQL para o SQLAlchemy, exigindo a criação dos modelos, relacionamentos e chaves estrangeiras entre as entidades Usuário, Tarefa e Matéria.

Outro problema ocorreu durante a alteração da estrutura da tabela de tarefas, quando foi adicionada a chave estrangeira materia_id. Como o banco de dados antigo não possuía essa coluna, foi necessário recriar o arquivo database.db para que a nova estrutura fosse criada corretamente.

Além disso, foram realizados ajustes nos templates HTML para substituir campos de texto por listas de seleção (select), permitindo que o usuário escolha uma matéria cadastrada ao criar ou editar uma tarefa.


# 📚 Referéncia
- SQLAIchemy -- https://www.sqlalchemy.org/
- Flask-login -- https://flask-login.readthedocs.io/en/latest/
