from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
import json
from datetime import datetime
import requests
from typing import Dict, Any
from decouple import config


app = FastAPI(
    title="WhatsApp Business API Integration",
    description="Backend para integração com WhatsApp Business API"
)

META_API_URL = 'https://graph.facebook.com/v22.0/' + config('PHONE_NUMBER_ID')

class Mensagem(BaseModel):
    numero_destino: str
    # mensagem: str


@app.post("/mensagens/enviar")
async def enviar_mensagem(mensagem: Mensagem):
    """Endpoint para enviar mensagem via WhatsApp"""
    auth_token = config("AUTH_TOKEN")
    
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
    
    # Não posso mandar mensagem de texto, só template
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
    
    response = requests.post(
        f"{META_API_URL}/messages",
        headers=headers,
        json=payload
    )
    
    if response.status_code == 200:
        _registrar_log(f"Mensagem enviada com sucesso para {mensagem.numero_destino}")
        return {"status": "sucesso"}
    else:
        _registrar_log(f"Erro ao enviar mensagem: {response.status_code} - {response.text}")
        raise HTTPException(status_code=response.status_code, detail=response.text)

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
            verify_token = config("WEBHOOK_VERIFY_TOKEN")
            
            if hub_mode == "subscribe" and hub_verify_token == verify_token:
                return PlainTextResponse(hub_challenge)
            else:
                raise HTTPException(status_code=403, detail="Token de verificação inválido")

        # Processamento de mensagens (POST)
        elif request.method == "POST":
            data = await request.json()
            try:
                _registrar_log(f"Mensagem recebida: {data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']}")
            except KeyError:
                status = data['entry'][0]['changes'][0]['value']['statuses'][0]['status']
                if status == 'delivered':
                    _registrar_log(f"Mensagem entregue: {data['entry'][0]['changes'][0]['value']['statuses'][0]['id']}")
                elif status == 'read':
                    _registrar_log(f"Mensagem lida: {data['entry'][0]['changes'][0]['value']['statuses'][0]['id']}")

            return {"status": "sucesso"}

    except Exception as e:
        _registrar_log(f"Erro no webhook: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno")

def _registrar_log(mensagem: str):
    """Função auxiliar para registro de logs"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("logs/whatsapp_api.log", "a") as f:
        f.write(f"[{timestamp}] {mensagem}\n")
