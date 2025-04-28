from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
import os
import json
from datetime import datetime
import requests
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="WhatsApp Business API Integration",
    description="Backend para integração com WhatsApp Business API"
)

META_API_URL = 'https://graph.facebook.com/v22.0/' + os.getenv('PHONE_NUMBER_ID')

class Mensagem(BaseModel):
    numero_destino: str
    mensagem: str

# @app.post("/auth/token")
# async def obter_token():
#     """Endpoint para obtenção do token de acesso"""
#     try:
#         url = f"https://graph.facebook.com/v20.0/oauth/access_token"
#         params = {
#             "client_id": os.getenv("META_APP_ID"),
#             "client_secret": os.getenv("META_APP_SECRET"),
#             "grant_type": "client_credentials"
#         }
        
#         response = requests.post(url, params=params)
#         return response.json()
#     except Exception as e:
#         _registrar_log(f"Erro ao obter token: {str(e)}")
#         raise HTTPException(status_code=500, detail="Erro na autenticação")

@app.post("/mensagens/enviar")
async def enviar_mensagem(mensagem: Mensagem):
    """Endpoint para enviar mensagem via WhatsApp"""
    try:
        auth_token = os.getenv("AUTH_TOKEN")
        print(f"Auth Token: {auth_token}")
        
        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json"
        }
        
        # payload = {
        #     "messaging_product": "whatsapp",
        #     "to": mensagem.numero_destino,
        #     "type": "text",
        #     "text": {
        #         "body": mensagem.mensagem
        #     }
        # }
        payload = {
            "messaging_product": "whatsapp",
            "to": mensagem.numero_destino,
            "type": "template",
            "template": {
                "name": "hello_world",
                "language": {
                    "code": "en_US"
                },
            }
        }
        print(f"Payload: {json.dumps(payload)}")
        
        response = requests.post(
            f"{META_API_URL}/messages",
            headers=headers,
            json=payload
        )
        print(f"Response: {response.status_code} - {response.text}")
        
        if response.status_code == 200:
            _registrar_log(f"Mensagem enviada com sucesso para {mensagem.numero_destino}")
            return {"status": "sucesso"}
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
            
    except Exception as e:
        _registrar_log(f"Erro ao enviar mensagem: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao enviar mensagem")

@app.api_route("/webhooks/receber", methods=["GET", "POST"])
async def receber_mensagem(
    request: Request,
    hub_mode: str = Query(None, alias="hub.mode", description="Modo de verificação do webhook (deve ser 'subscribe')"),
    hub_challenge: str = Query(None, alias="hub.challenge", description="Desafio a ser retornado para validação"),
    hub_verify_token: str = Query(None, alias="hub.verify_token", description="Token de verificação do webhook"),
):
    """
    Webhook para receber mensagens do WhatsApp Business API.
    - **GET**: Validação inicial do webhook (Meta envia um desafio).
    - **POST**: Recebe mensagens enviadas pelos usuários.
    """
    try:
        # Verificação do webhook (GET)
        if request.method == "GET":
            verify_token = os.getenv("WEBHOOK_VERIFY_TOKEN")
            print('\nverify_token', verify_token, 'hub_mode', hub_mode, 'hub_verify_token', hub_verify_token)
            
            if hub_mode == "subscribe" and hub_verify_token == verify_token:
                print('here')
                return PlainTextResponse(hub_challenge)
            else:
                print('lá')
                raise HTTPException(status_code=403, detail="Token de verificação inválido")

        # Processamento de mensagens (POST)
        elif request.method == "POST":
            data = await request.json()
            _registrar_log(f"Mensagem recebida: {json.dumps(data, indent=2)}")
            return {"status": "sucesso"}

    except Exception as e:
        _registrar_log(f"Erro no webhook: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno")

def _registrar_log(mensagem: str):
    """Função auxiliar para registro de logs"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("logs/whatsapp_api.log", "a") as f:
        f.write(f"[{timestamp}] {mensagem}\n")