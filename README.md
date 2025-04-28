# WhatsApp Business API Integration

Este projeto é uma integração com a API do WhatsApp Business, permitindo o envio de mensagens e o recebimento de eventos via webhook. Ele foi desenvolvido utilizando o framework FastAPI.

## Funcionalidades

- **Envio de mensagens**: Envia mensagens de template para números de telefone via API do WhatsApp Business.
- **Recebimento de mensagens e eventos**: Recebe mensagens e eventos de status (entregue, lida, etc.) via webhook.
- **Registro de logs**: Registra logs de mensagens enviadas, recebidas e eventos em um arquivo de log.

---

## Requisitos

- Python 3.6.15 (definido no arquivo `.python-version`)
- Conta no WhatsApp Business com acesso à API
- Token de autenticação e ID do número de telefone fornecidos pela Meta
- Arquivo `.env` configurado com as variáveis de ambiente necessárias

---

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/meta_api_whatsapp_test.git
   cd meta_api_whatsapp_test
   ```

2. Crie um ambiente virtual e ative-o:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure o arquivo `.env` com as seguintes variáveis:
   ```env
   AUTH_TOKEN=<seu_token_de_autenticacao>
   PHONE_NUMBER_ID=<id_do_numero_de_telefone>
   TO_PHONE_NUMBER=<numero_destino>
   WEBHOOK_VERIFY_TOKEN=<token_de_verificacao_do_webhook>
   ```

---

## Uso

### Iniciar o servidor

Execute o servidor FastAPI:
```bash
uvicorn main:app --reload
```

O servidor estará disponível em `http://127.0.0.1:8000`.

---

### Endpoints

#### **1. Enviar mensagem**
- **URL**: `/mensagens/enviar`
- **Método**: `POST`
- **Descrição**: Envia uma mensagem de template para um número de telefone.
- **Exemplo de payload**:
  ```json
  {
    "numero_destino": "5586995610997"
  }
  ```
- **Resposta de sucesso**:
  ```json
  {
    "status": "sucesso"
  }
  ```

#### **2. Webhook**
- **URL**: `/webhooks/receber`
- **Métodos**: `GET`, `POST`
- **Descrição**:
  - `GET`: Valida o webhook com o token fornecido pela Meta.
  - `POST`: Recebe mensagens e eventos enviados pelo WhatsApp Business API.
- **Parâmetros de Query (GET)**:
  - `hub.mode`: Deve ser `subscribe`.
  - `hub.challenge`: Desafio retornado para validação.
  - `hub.verify_token`: Token de verificação configurado no `.env`.

---

## Estrutura do Projeto

- `main.py`: Código principal da aplicação FastAPI.
- `test2.py`: Script de exemplo para envio de mensagens usando a biblioteca `requests`.
- `test1.sh`: Script de exemplo para envio de mensagens usando `curl`.
- `requirements.txt`: Dependências do projeto.
- `.env`: Arquivo de configuração com variáveis de ambiente.
- `logs/`: Diretório onde os logs são armazenados.

---

## Logs

Os logs são armazenados no arquivo `logs/whatsapp_api.log` e incluem informações sobre mensagens enviadas, recebidas e eventos de status.

---

## Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).
