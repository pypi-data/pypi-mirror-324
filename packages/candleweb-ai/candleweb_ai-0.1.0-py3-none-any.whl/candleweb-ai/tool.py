from crewai.tools import BaseTool
from typing import Type, Optional
from pydantic import BaseModel, Field
import requests
import uuid
import json


class PlaceOrderInput(BaseModel):
    """Input schema for the PlaceOrderTool."""
    ai: str = Field(..., description="The AI model (e.g., BINANCE-ETHDEMO)")
    exchange: str = Field(..., description="Exchange name (e.g., BINANCE)")
    pair: str = Field(..., description="Trading pair (e.g., ETHUSDT)")
    mode: str = Field(..., description="Mode (e.g., DEMO or LIVE)")
    side: str = Field(..., description="Order side (BUY or SELL)")
    api_key: str = Field(..., description="Bearer api key for authentication")
    environment: Optional[str] = Field(None, description="Bearer token for authentication (optional)")

class PlaceOrderTool(BaseTool):
    name: str = "Place Order Tool"
    description: str = "Tool to place BUY or SELL orders on the endpoint and retrieve a response."
    args_schema: Type[BaseModel] = PlaceOrderInput

    def _run(self, ai: str, exchange: str, pair: str, mode: str, side: str, api_key: str, enviroment: Optional[str] = None) -> str:
        context = {}

        # Generate a unique idempotency key
        idempotency_key = str(uuid.uuid4())

        # Choose enviroment
        enviroment = 'api' if enviroment == 'live' else 'sandboxapi'

        # Define the API endpoint
        url = f"https://{enviroment}.candleweb.io/api/bot/place/order/?ai={ai}&exchange={exchange}&pair={pair}&mode={mode}&side={side}"

        # Headers with idempotency and authorization token
        headers = {
            'Content-Type': 'application/json',
            'Idempotency-Key': idempotency_key,
            'Authorization': f'Bearer {api_key}'
        }

        try:
            # Make the GET request
            response = requests.get(url, headers=headers)

            # Return the response text or handle errors
            if response.status_code == 200:
                return json.loads(response.text)
            else:
                context['status'] = 'error'
                context['message'] = f"Error: {response.status_code} - {response.text}"
                return context

        except Exception as e:
            context['status'] = 'error'
            context['message'] = f"Request failed: {str(e)}"
            return context
