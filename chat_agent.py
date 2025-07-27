# chat_agent.py
import re
import datetime
import requests
from typing import Dict, Any
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from config import GOOGLE_API_KEY, LLM_CONFIG, BACKEND_URL

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model=LLM_CONFIG["model"], 
    temperature=LLM_CONFIG["temperature"], 
    google_api_key=GOOGLE_API_KEY
)

# Chat prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system",
    """You are a helpful and friendly voice assistant speaking in Syrian Arabic.
Your job is to detect the user's **intent**: one of these:
- 'order'
- 'complaint'
- 'question'
- 'other'

Behavior per intent:

1. If intent is **order**:
   - Ask for missing details: `name`, `items`.
   - Once you have both name and items, summarize the order and ask if they want to add anything else or modify something.
   - After they confirm they don't want changes, ask for final confirmation: "هل تريد تأكيد الطلب؟" (Do you want to confirm the order?)
   - ONLY when user confirms the order, then say: FUNCTION_CALL: submit_order(name="...", items=["...", "..."])
   - Always offer upsells before asking for confirmation (e.g., offer dessert, soft drink, fries).
   - Be friendly, warm, and conversational.

2. If intent is **complaint**:
   - Respond with empathy and apologize sincerely.
   - Show understanding and offer help.

3. If intent is **question**:
   - Answer clearly and politely.

4. If intent is **unclear or other**:
   - Respond kindly, ask for clarification or offer help.

🗣 Always reply in Syrian Arabic.
Start each turn with a warm greeting or polite phrase.
IMPORTANT: When you include FUNCTION_CALL in your response, add it at the END after your natural Arabic response.
"""
    ),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

# Global variables for session management
user_histories = {}
order_log = []

def extract_clean_response(full_response: str) -> str:
    """Extract the clean Arabic response without FUNCTION_CALL"""
    if "FUNCTION_CALL:" in full_response:
        clean_response = full_response.split("FUNCTION_CALL:")[0].strip()
        return clean_response
    return full_response

def submit_order_to_backend(name: str, items: list) -> Dict[str, Any]:
    """Submit order to backend API"""
    try:
        url = f"{BACKEND_URL}/submit-order"
        payload = {
            "name": name,
            "items": items
        }
        
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            error_msg = response.json().get('error', 'Unknown error')
            return {"error": f"Backend error: {error_msg}"}
            
    except requests.exceptions.ConnectionError:
        return {"error": "لا يمكن الاتصال بالخادم"}
    except requests.exceptions.Timeout:
        return {"error": "انتهت مهلة الاتصال"}
    except Exception as e:
        return {"error": f"خطأ في الإرسال: {str(e)}"}

def run_agent(user_id: str, user_input: str) -> Dict[str, Any]:
    """Process user input through the Syrian Arabic assistant"""
    if user_id not in user_histories:
        user_histories[user_id] = []

    history = user_histories[user_id]

    result = (prompt | llm).invoke(
        {"input": user_input, "chat_history": history},
        config=RunnableConfig()
    )

    response_text = result.content
    history.append(HumanMessage(content=user_input))
    history.append(AIMessage(content=response_text))

    clean_response = extract_clean_response(response_text)

    # Parse function call if present
    if "FUNCTION_CALL:" in response_text:
        try:
            match = re.search(r"submit_order\s*\(\s*name\s*=\s*['\"](.+?)['\"]\s*,\s*items\s*=\s*\[(.*?)\]\s*\)", response_text)
            if match:
                name = match.group(1)
                items_raw = match.group(2)
                items = [item.strip().strip("'\"") for item in items_raw.split(',') if item.strip()]
                
                # Submit to backend API
                backend_response = submit_order_to_backend(name, items)
                
                if "error" in backend_response:
                    return {
                        "response": response_text,
                        "clean_response": clean_response,
                        "error": backend_response["error"]
                    }
                
                # Log the order locally as well
                order_info = {
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "name": name,
                    "items": items,
                    "user_id": user_id,
                    "order_id": backend_response.get("order_id"),
                    "eta_minutes": backend_response.get("eta_minutes"),
                    "backend_response": backend_response
                }
                order_log.append(order_info)
                
                return {
                    "function_call": True, 
                    "name": name, 
                    "items": items, 
                    "response": response_text,
                    "clean_response": clean_response,
                    "order_id": backend_response.get("order_id"),
                    "eta_minutes": backend_response.get("eta_minutes"),
                    "backend_message": backend_response.get("message", "تم تأكيد الطلب")
                }
            else:
                return {"response": response_text, "clean_response": clean_response, "error": "Failed to parse function call"}
        except Exception as e:
            return {"response": response_text, "clean_response": clean_response, "error": str(e)}

    return {"response": response_text, "clean_response": clean_response, "function_call": False}

def clear_conversation(user_id: str = "default_user"):
    """Clear conversation history for a user"""
    if user_id in user_histories:
        user_histories[user_id] = []

def get_order_history() -> str:
    """Get formatted order history"""
    if not order_log:
        return "📋 لا توجد طلبات حتى الآن"
    
    history = "📋 **سجل الطلبات:**\n\n"
    for i, order in enumerate(order_log, 1):
        history += f"**طلب رقم {i}:**\n"
        history += f"⏰ الوقت: {order['timestamp']}\n"
        history += f"👤 الاسم: {order['name']}\n"
        history += f"🍽️ الطلبات: {', '.join(order['items'])}\n"
        
        # Add backend information if available
        if 'order_id' in order and order['order_id']:
            history += f"🆔 رقم الطلب: {order['order_id']}\n"
        if 'eta_minutes' in order and order['eta_minutes']:
            history += f"⏰ الوقت المتوقع: {order['eta_minutes']} دقيقة\n"
        
        history += "\n"
    
    return history

def get_backend_orders() -> str:
    """Get all orders from backend API"""
    try:
        response = requests.get(f"{BACKEND_URL}/orders", timeout=5)
        if response.status_code == 200:
            orders = response.json()
            if not orders:
                return "📋 لا توجد طلبات في النظام"
            
            history = "🗄️ **طلبات النظام (من الخادم):**\n\n"
            for order_id, order in orders.items():
                history += f"**🆔 {order_id}:**\n"
                history += f"👤 الاسم: {order['name']}\n"
                history += f"🍽️ الطلبات: {', '.join(order['items'])}\n"
                history += f"⏰ الوقت المتوقع: {order['eta_minutes']} دقيقة\n"
                history += f"📅 تاريخ الطلب: {order['created_at']}\n"
                history += f"📊 الحالة: {order['status']}\n\n"
            
            return history
        else:
            return "❌ خطأ في جلب الطلبات من الخادم"
    except Exception as e:
        return f"❌ خطأ في الاتصال بالخادم: {str(e)}"