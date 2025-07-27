# main.py
import threading
import time
from backend_api import run_backend
from gradio_interface import create_gradio_interface
from config import BACKEND_PORT, GRADIO_CONFIG

def start_backend():
    """Start the Flask backend in a separate thread"""
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    time.sleep(2)  # Give Flask time to start
    return backend_thread

def main():
    """Main application entry point"""
    print("🚀 Starting Voice Assistant with Backend API...")
    print(f"📡 Backend API running on: http://localhost:{BACKEND_PORT}")
    print(f"🎤 Gradio Interface will be available on: http://localhost:{GRADIO_CONFIG['server_port']}")
    print("\n📋 API Endpoints:")
    print("   POST /submit-order - Submit new order")
    print("   GET  /orders - Get all orders")
    print("   GET  /orders/<id> - Get specific order")
    
    # Start backend API
    backend_thread = start_backend()
    
    # Create and launch Gradio interface
    demo = create_gradio_interface()
    
    try:
        demo.launch(
            share=GRADIO_CONFIG["share"],
            debug=GRADIO_CONFIG["debug"],
            server_port=GRADIO_CONFIG["server_port"]
        )
    except KeyboardInterrupt:
        print("\n🛑 Shutting down application...")
    except Exception as e:
        print(f"❌ Error starting application: {e}")

if __name__ == "__main__":
    main()