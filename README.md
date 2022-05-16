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

- SSH configurado devidamente com a porta 22 aberta

## Rodando em Docker

1. Variáveis precisam ser definidas:

```bash
export RSA=(RSA path)
export OLD_ORIGIN_API=(example: https://gitlab.com/api/v4/)
export OLD_ORIGIN_TOKEN=(old origin access token)
export ORIGIN_API=(example: http://localhost:8080/api/v4/projects)
export ORIGIN_TOKEN=(origin access token)
```

2. Rodando o Docker:

```bash
docker build \
--build-arg RSA=RSA \
--build-arg OLD_ORIGIN_API='https://gitlab.com/api/v4/' \
--build-arg OLD_ORIGIN_TOKEN=OLD_ORIGIN_TOKEN \
--build-arg ORIGIN_API=ORIGIN_API \
--build-arg ORIGIN_TOKEN=ORIGIN_TOKEN \
-t gitlab-export .
```

## Utilização

Para fazer
