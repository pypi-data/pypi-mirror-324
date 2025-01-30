# langchain_payman_tool/payman_tools.py

import os
from typing import Optional, Dict, Any, List, Type
from typing_extensions import Literal

from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool

from paymanai import Paymanai

########################################
# 1) Initialize the Payman client
########################################
PAYMAN_API_SECRET = os.getenv("PAYMAN_API_SECRET")
PAYMAN_ENVIRONMENT = os.getenv("PAYMAN_ENVIRONMENT")

client = Paymanai(
    x_payman_api_secret=PAYMAN_API_SECRET,
    environment=PAYMAN_ENVIRONMENT
)

########################################
# 2) Send Payment Tool
########################################

class SendPaymentInput(BaseModel):
    """Pydantic input schema for sending a payment."""
    amount_decimal: float = Field(..., description="Amount to send in decimal format (e.g. 10.00)")
    payment_destination_id: Optional[str] = Field(
        None, description="ID of an existing payment destination to send to"
    )
    payment_destination: Optional[Dict[str, Any]] = Field(
        None, 
        description="Optional dictionary describing a new payment destination (if not using payment_destination_id)"
    )
    customer_id: Optional[str] = Field(None, description="An optional customer ID if sending on behalf of a customer")
    customer_email: Optional[str] = Field(None, description="Customer email if available")
    customer_name: Optional[str] = Field(None, description="Customer name if available")
    memo: Optional[str] = Field(None, description="Optional note or memo for the payment")

class SendPaymentTool(BaseTool):
    """A LangChain tool that calls Payman.ai's 'send_payment'."""
    name: str = "send_payment"
    description: str = (
        "Send funds from an agent's wallet to a payee. "
        "Takes amount_decimal, payment_destination_id or payment_destination, customer info, etc."
    )
    args_schema: Type[BaseModel] = SendPaymentInput

    def _run(self, **kwargs: Any) -> str:
        try:
            response = client.payments.send_payment(**kwargs)
            return f"Payment sent successfully. Response: {response}"
        except Exception as e:
            return f"Error in send_payment: {str(e)}"


########################################
# 3) Search Payees Tool
########################################

class SearchPayeesInput(BaseModel):
    """Pydantic input schema for searching payees."""
    name: Optional[str] = Field(None, description="Optional name filter for the payee")
    contact_email: Optional[str] = Field(None, description="Optional email filter")
    type: Optional[str] = Field(None, description="Optional type filter (CRYPTO_ADDRESS or US_ACH, etc.)")

class SearchPayeesTool(BaseTool):
    """A LangChain tool that calls Payman.ai's 'search_payees'."""
    name: str = "search_payees"
    description: str = (
        "Search for existing payment destinations (payees). "
        "Can filter by name, email, type, etc."
    )
    args_schema: Type[BaseModel] = SearchPayeesInput

    def _run(self, **kwargs: Any) -> str:
        try:
            response = client.payments.search_payees(**kwargs)
            return f"Payees search returned: {response}"
        except Exception as e:
            return f"Error in search_payees: {str(e)}"


########################################
# 4) Add Payee (Create Payee) Tool
########################################

class AddPayeeInput(BaseModel):
    """Pydantic input schema for adding a new payee."""
    type: Literal["CRYPTO_ADDRESS", "US_ACH"] = Field(..., description="Type of payment destination")
    name: Optional[str] = Field(None, description="Optional name for the payee")
    contact_details: Optional[Dict[str, Any]] = Field(None, description="Optional contact info dictionary")
    account_holder_name: Optional[str] = Field(None, description="Required if type == 'US_ACH'")
    account_number: Optional[str] = Field(None, description="Required if type == 'US_ACH'")
    account_type: Optional[str] = Field(None, description="Required if type == 'US_ACH', e.g. 'checking'")
    routing_number: Optional[str] = Field(None, description="Required if type == 'US_ACH'")
    address: Optional[str] = Field(None, description="Required if type == 'CRYPTO_ADDRESS'")
    currency: Optional[str] = Field(None, description="The blockchain currency (if CRYPTO_ADDRESS)")
    tags: Optional[List[str]] = Field(None, description="Optional labels for this payee")

class AddPayeeTool(BaseTool):
    """A LangChain tool that calls Payman.ai's 'create_payee' (add a new payment destination)."""
    name: str = "add_payee"
    description: str = (
        "Add a new payee (payment destination). "
        "Can be US_ACH or CRYPTO_ADDRESS with the appropriate fields."
    )
    args_schema: Type[BaseModel] = AddPayeeInput

    def _run(self, **kwargs: Any) -> str:
        try:
            response = client.payments.create_payee(**kwargs)
            return f"Payee created successfully. Response: {response}"
        except Exception as e:
            return f"Error in add_payee: {str(e)}"


########################################
# 5) Ask for Money (Customer Deposit) Tool
########################################

class AskForMoneyInput(BaseModel):
    """Pydantic input schema for generating a checkout link (customer deposit)."""
    amount_decimal: float = Field(..., description="Amount to request in decimal format (e.g. 10.00 for USD)")
    customer_id: str = Field(..., description="ID of the customer from whom you want to request money")
    customer_email: Optional[str] = Field(None, description="Optional email for the customer")
    customer_name: Optional[str] = Field(None, description="Optional name of the customer")
    memo: Optional[str] = Field(None, description="Optional memo for the deposit request")

class AskForMoneyTool(BaseTool):
    """A tool for requesting money (initiate_customer_deposit) from a customer."""
    name: str = "ask_for_money"
    description: str = (
        "Generate a checkout link to request money from a customer. "
        "Customer can then complete the deposit on Payman's hosted page."
    )
    args_schema: Type[BaseModel] = AskForMoneyInput

    def _run(self, **kwargs: Any) -> str:
        try:
            response = client.payments.initiate_customer_deposit(**kwargs)
            checkout_url = response.checkout_url
            return f"Checkout URL for deposit: {checkout_url}"
        except Exception as e:
            return f"Error in ask_for_money: {str(e)}"


########################################
# 6) Get Balance Tool
########################################

class GetBalanceInput(BaseModel):
    """Pydantic input schema for retrieving balance information."""
    customer_id: Optional[str] = Field(
        None, description="If specified, get the balance for that customer. Otherwise returns agent's balance."
    )
    currency: str = Field("USD", description="Which currency to get the balance for (default USD)")

class GetBalanceTool(BaseTool):
    """Retrieve the balance of your AI Agents wallet."""
    name: str = "get_balance"
    description: str = (
        "Get the spendable balance for either the agent (if customer_id not provided) "
        "or a specific customer (if customer_id provided)."
    )
    args_schema: Type[BaseModel] = GetBalanceInput

    def _run(self, customer_id: Optional[str] = None, currency: str = "USD", **kwargs: Any) -> str:
        try:
            if customer_id and customer_id.lower() != "none":
                resp = client.balances.get_customer_balance(
                    customer_id=customer_id,
                    currency=currency
                )
            else:
                resp = client.balances.get_spendable_balance(
                    currency=currency
                )
            return f"Balance info: {resp}"
        except Exception as e:
            return f"Error in get_balance: {str(e)}"
