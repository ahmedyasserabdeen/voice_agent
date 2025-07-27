# gradio_interface.py
import gradio as gr
from typing import Tuple
from audio_services import speech_to_text, text_to_speech
from chat_agent import run_agent, clear_conversation, get_order_history, get_backend_orders

def process_voice_input(audio_file, user_id: str = "default_user") -> Tuple[str, str, str]:
    """Process voice input and return conversation history, status, and audio response"""
    
    if audio_file is None:
        return "", "❌ لم يتم رفع ملف صوتي", None
    
    try:
        # Convert speech to text
        user_text = speech_to_text(audio_file)
        
        if not user_text:
            return "", "❌ لم أتمكن من فهم الصوت، حاول مرة أخرى", None
        
        # Process through agent
        agent_response = run_agent(user_id, user_text)
        
        if "error" in agent_response:
            return "", f"❌ خطأ: {agent_response['error']}", None
        
        # Generate audio response
        response_for_audio = agent_response["clean_response"]
        audio_file_path = text_to_speech(response_for_audio)
        
        # Build conversation display
        conversation = f"👤 **أنت:** {user_text}\n\n🤖 **المساعد:** {response_for_audio}\n\n"
        
        # Add order status if applicable
        status = ""
        if agent_response.get("function_call"):
            order_id = agent_response.get("order_id", "غير متوفر")
            eta = agent_response.get("eta_minutes", "غير محدد")
            backend_msg = agent_response.get("backend_message", "تم تأكيد الطلب")
            
            status = f"✅ {backend_msg}\n"
            status += f"🆔 رقم الطلب: {order_id}\n"
            status += f"⏰ الوقت المتوقع: {eta} دقيقة\n"
            status += f"📋 الاسم: {agent_response['name']}\n"
            status += f"🍽️ الطلبات: {', '.join(agent_response['items'])}"
        else:
            status = "💬 جاري المحادثة..."
        
        return conversation, status, audio_file_path
        
    except Exception as e:
        return "", f"❌ خطأ في معالجة الصوت: {str(e)}", None

def process_text_input(text_input: str, conversation_history: str, user_id: str = "default_user") -> Tuple[str, str, str]:
    """Process text input and return updated conversation, status, and audio response"""
    
    if not text_input.strip():
        return conversation_history, "❌ الرجاء كتابة رسالة", None
    
    try:
        # Process through agent
        agent_response = run_agent(user_id, text_input)
        
        if "error" in agent_response:
            return conversation_history, f"❌ خطأ: {agent_response['error']}", None
        
        # Generate audio response
        response_for_audio = agent_response["clean_response"]
        audio_file_path = text_to_speech(response_for_audio)
        
        # Update conversation display
        new_conversation = f"👤 **أنت:** {text_input}\n\n🤖 **المساعد:** {response_for_audio}\n\n"
        updated_conversation = conversation_history + new_conversation
        
        # Add order status if applicable
        status = ""
        if agent_response.get("function_call"):
            order_id = agent_response.get("order_id", "غير متوفر")
            eta = agent_response.get("eta_minutes", "غير محدد")
            backend_msg = agent_response.get("backend_message", "تم تأكيد الطلب")
            
            status = f"✅ {backend_msg}\n"
            status += f"🆔 رقم الطلب: {order_id}\n"
            status += f"⏰ الوقت المتوقع: {eta} دقيقة\n"
            status += f"📋 الاسم: {agent_response['name']}\n"
            status += f"🍽️ الطلبات: {', '.join(agent_response['items'])}"
        else:
            status = "💬 جاري المحادثة..."
        
        return updated_conversation, status, audio_file_path
        
    except Exception as e:
        return conversation_history, f"❌ خطأ في معالجة النص: {str(e)}", None

def clear_conversation_ui() -> Tuple[str, str]:
    """Clear conversation history"""
    user_id = "default_user"
    clear_conversation(user_id)
    return "", "🔄 تم مسح المحادثة"

def create_gradio_interface():
    """Create and configure the Gradio interface"""
    
    with gr.Blocks(
        theme=gr.themes.Soft(),
        title="مساعد المطعم الصوتي",
        css="""
        .main-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .conversation-box {
            max-height: 400px;
            overflow-y: auto;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 10px;
            background-color: #f9f9f9;
        }
        .status-box {
            padding: 10px;
            border-radius: 8px;
            margin: 10px 0;
        }
        .arabic-text {
            font-family: 'Arial', sans-serif;
            font-size: 16px;
            line-height: 1.6;
            text-align: right;
            direction: rtl;
        }
        """
    ) as demo:
        
        gr.Markdown(
            """
            # 🎤 مساعد المطعم الصوتي السوري
            ### تحدث أو اكتب باللغة العربية السورية لطلب الطعام
            
            **المميزات:**
            - 🎤 تحدث مباشرة مع المساعد
            - ✍️ أو اكتب رسالتك
            - 🔊 استمع للردود الصوتية
            - 📋 تأكيد الطلبات قبل الإرسال
            """,
            elem_classes=["arabic-text"]
        )
        
        with gr.Row():
            with gr.Column(scale=2):
                # Voice Input Section
                gr.Markdown("## 🎤 الإدخال الصوتي")
                voice_input = gr.Audio(
                    sources=["microphone", "upload"],
                    type="filepath",
                    label="🎙️ تحدث أو ارفع ملف صوتي"
                )
                voice_submit = gr.Button("🎤 إرسال الصوت", variant="primary")
                
                # Text Input Section
                gr.Markdown("## ✍️ الإدخال النصي")
                text_input = gr.Textbox(
                    label="💬 اكتب رسالتك هنا",
                    placeholder="مثال: أهلاً، بدي أطلب أكل...",
                    lines=2,
                    elem_classes=["arabic-text"]
                )
                text_submit = gr.Button("📤 إرسال النص", variant="secondary")
                
                # Controls
                gr.Markdown("## ⚙️ التحكم")
                with gr.Row():
                    clear_btn = gr.Button("🗑️ مسح المحادثة", variant="stop")
                    orders_btn = gr.Button("📋 عرض الطلبات المحلية", variant="secondary")
                    backend_orders_btn = gr.Button("🗄️ طلبات النظام", variant="secondary")
            
            with gr.Column(scale=3):
                # Conversation Display
                gr.Markdown("## 💬 المحادثة")
                conversation_display = gr.Markdown(
                    value="",
                    label="المحادثة",
                    elem_classes=["conversation-box", "arabic-text"]
                )
                
                # Status Display
                status_display = gr.Markdown(
                    value="🔄 اضغط على الزر أو تحدث للبدء",
                    label="الحالة",
                    elem_classes=["status-box", "arabic-text"]
                )
                
                # Audio Output
                gr.Markdown("## 🔊 الرد الصوتي")
                audio_output = gr.Audio(
                    label="استمع للرد",
                    autoplay=True
                )
                
                # Order History (Hidden by default)
                order_history_display = gr.Markdown(
                    value="",
                    visible=False,
                    elem_classes=["arabic-text"]
                )
        
        # Event handlers
        voice_submit.click(
            fn=process_voice_input,
            inputs=[voice_input],
            outputs=[conversation_display, status_display, audio_output]
        )
        
        text_submit.click(
            fn=process_text_input,
            inputs=[text_input, conversation_display],
            outputs=[conversation_display, status_display, audio_output]
        ).then(
            fn=lambda: "",  # Clear text input after submit
            outputs=[text_input]
        )
        
        # Enter key support for text input
        text_input.submit(
            fn=process_text_input,
            inputs=[text_input, conversation_display],
            outputs=[conversation_display, status_display, audio_output]
        ).then(
            fn=lambda: "",
            outputs=[text_input]
        )
        
        clear_btn.click(
            fn=clear_conversation_ui,
            outputs=[conversation_display, status_display]
        )
        
        orders_btn.click(
            fn=get_order_history,
            outputs=[order_history_display]
        ).then(
            fn=lambda: gr.update(visible=True),
            outputs=[order_history_display]
        )
        
        backend_orders_btn.click(
            fn=get_backend_orders,
            outputs=[order_history_display]
        ).then(
            fn=lambda: gr.update(visible=True),
            outputs=[order_history_display]
        )
    
    return demo