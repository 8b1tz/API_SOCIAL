# API Social
Este projeto demonstra uma **API Social** completa utilizando:

- **FastAPI** para criação de rotas e serviços de forma rápida e eficiente  
- **SQLAlchemy** (com SQLite como exemplo local, mas pode ser PostgreSQL/MySQL em produção)  
- **JWT com jti** para invalidação de tokens no servidor (logout real)  
- **Passlib (bcrypt)** para hashing de senhas  
- **Pydantic** para validação de dados

## Estrutura do Projeto

```
API_SOCIAL/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── utils.py
│   └── routers/
│       ├── auth.py
│       ├── feed.py
│       ├── posts.py
│       ├── profile.py
│       └── friends.py
├── requirements.txt
└── README.md
```

- **`app/main.py`**: Inicia a aplicação FastAPI, cria as tabelas e inclui os routers.  
- **`app/database.py`**: Configura a conexão com o banco de dados via SQLAlchemy.  
- **`app/models.py`**: Define as tabelas/entidades (Users, Posts, Comments, Likes, Friendships, SessionToken).  
- **`app/schemas.py`**: Classes Pydantic para validação das requisições e formatação das respostas.  
- **`app/utils.py`**: Funções auxiliares (hash de senha, criação/decodificação de token JWT, invalidação de sessão).  
- **`app/routers/`**: Pastas de rotas, separadas por domínio (auth, feed, posts, profile, friends).  

## Como Executar

1. **Instale as dependências**:

  ```bash
  python -m venv venv
  ```
  ```bash
  venv/Scripts/activate
   ```
   ```bash
   pip install -r requirements.txt
   ```

2. **Inicie a aplicação** (na raiz do projeto):

   ```bash
   uvicorn app.main:app --reload
   ```

3. **Acesse a documentação**:

   - [Swagger UI](http://127.0.0.1:8000/docs)
   - [Redoc](http://127.0.0.1:8000/redoc)

## Principais Endpoints

- **Autenticação**  
  - `POST /auth/register`: Cria usuário novo.  
  - `POST /auth/login`: Retorna token JWT se credenciais corretas.  
  - `POST /auth/logout`: Invalida o token no servidor, efetivando logout real.

- **Feed**  
  - `GET /feed`: Lista posts (pode ser público ou privado, conforme necessidade).  
  - `POST /feed`: Cria um post (somente se estiver autenticado).

- **Posts**  
  - `GET /posts/{post_id}/comments`: Lista comentários de um post.  
  - `POST /posts/{post_id}/comments`: Cria comentário (restrito a usuários logados).  
  - `GET /posts/{post_id}/likes`: Mostra quantidade de likes.  
  - `POST /posts/{post_id}/likes`: Dá like em um post (restrito a usuários logados).

- **Perfil**  
  - `GET /profile`: Mostra dados do usuário logado.  
  - `PUT /profile`: Atualiza dados do perfil.  
  - `DELETE /profile`: Exclui a conta do usuário logado.

- **Amigos**  
  - `GET /friends`: Lista as amizades do usuário logado.  
  - `POST /friends/{friend_id}`: Adiciona amizade com outro usuário.  
  - `DELETE /friends/{friendship_id}`: Remove amizade.

## Logout Real

Esta API implementa logout real via **tabela de sessões** (`SessionToken`). Cada token JWT emitido possui um `jti` único salvo no banco. Quando o usuário faz logout:

1. **Decodifica** o token para encontrar o `jti`.  
2. **Marca** a sessão correspondente como `inativa` (`is_active = False`).  

Qualquer requisição posterior com o mesmo token retornará `401 Unauthorized`, pois a sessão foi invalidada.

## Observações

- Utilize um **banco de dados robusto** (ex.: PostgreSQL em produção).  
- **Guarde a SECRET_KEY** e outras configurações sensíveis em variáveis de ambiente.  
- Para suporte a **múltiplos logins simultâneos**, basta permitir que o usuário tenha várias sessões ativas ou invalidar todas no logout, conforme a política de segurança desejada.

---
