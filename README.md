# Migração Gitlab

Uma ferramenta de migração automatizada usando [Gitlab API](https://docs.gitlab.com/ee/api/).

## Funcionalidades

### Estrutura

- [ ] Transferência de grupos
- [ ] Transferência de subgrupos
- [x] Transferência de projetos*
- [x] Exclusão de projetos
- [ ] Mantém a mesma organização estrutural do ambiente

### Conteúdo

- [x] Migração do conteúdo dos repositórios*
- [x] Migração das variáveis de ambiente para seus devidos projetos*
- [ ] Migração dos Runners* (nenhuma possibilidade encontrada)

### Usuários

- [x] Transferência de usuários*
  - [x] Nome
  - [x] Usuário
  - [x] Email (usuario@vertigo.com.br)

\* Salva seus respectivos arquivos em seus diretórios propriamente criados.

## Requisitos

### Client-side

- Máquina registrada com chave SSH em ambos ambientes no Gitlab
- Chave RSA
- Token de acesso de ambos ambientes no Gitlab
- Função de usuário do Gitlab como Dono
- Espaço para armazenamento de arquivos dos repositórios
- Python >= 3.8
  - colorama
  - requests
  - urllib3
  - chardet

`pip3 install colorama requests urllib3 chardet`

### Server-side

- SSH configurado devidamente na porta 22

## Rodando em Docker

Para fazer

## Utilização

Para fazer
