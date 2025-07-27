# 🎤 Syrian Arabic Voice Restaurant Assistant

A sophisticated voice-enabled restaurant ordering system that supports Syrian Arabic dialect with speech-to-text, text-to-speech, and intelligent order processing.

## 🌟 Features

- **🎤 Voice Input**: Speak directly to the assistant in Syrian Arabic
- **✍️ Text Input**: Type your messages in Arabic
- **🔊 Audio Response**: Listen to AI-generated voice responses
- **📋 Order Management**: Complete order processing with confirmation
- **🗄️ Backend API**: RESTful API for order management
- **💾 Persistent Storage**: Orders saved to JSON file

## 📁 Project Structure

```
restaurant-voice-assistant/
├── config.py              # Configuration and API keys
├── backend_api.py          # Flask backend API
├── audio_services.py       # Speech-to-text and text-to-speech
├── chat_agent.py          # LLM chat agent with LangChain
├── gradio_interface.py    # Gradio UI interface
├── main.py               # Main application entry point
├── requirements.txt      # Python dependencies
├── README.md            # Project documentation
└── orders.json          # Persistent order storage (generated)
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

Edit `config.py` and add your API keys:

```python
GOOGLE_API_KEY = "your_google_api_key_here"
ELEVENLABS_API_KEY = "your_elevenlabs_api_key_here"
HUGGINGFACE_API_KEY = "your_huggingface_api_key_here"
```

### 3. Run the Application

```bash
python main.py
```

This will start:
- 📡 Backend API on `http://localhost:5000`
- 🎤 Gradio Interface on `http://localhost:7860`

## 🔧 Components Overview

### 1. `config.py`
Central configuration file containing:
- API keys for external services
- Backend and frontend settings
- Voice and LLM configurations

### 2. `backend_api.py`
Flask-based REST API providing:
- `POST /submit-order` - Submit new orders
- `GET /orders` - Retrieve all orders
- `GET /orders/<id>` - Get specific order details

### 3. `audio_services.py`
Audio processing services:
- **Speech-to-Text**: Using Hugging Face Whisper API
- **Text-to-Speech**: Using ElevenLabs API

### 4. `chat_agent.py`
LangChain-powered conversational AI:
- Intent detection (order, complaint, question, other)
- Order processing with confirmation
- Backend integration for order submission

### 5. `gradio_interface.py`
Web-based user interface:
- Voice and text input options
- Real-time conversation display
- Audio response playback
- Order history management

### 6. `main.py`
Application entry point that:
- Starts the backend API in a separate thread
- Launches the Gradio interface
- Handles application lifecycle

## 🔄 Order Processing Flow

1. **Input**: User speaks or types in Syrian Arabic
2. **Processing**: 
   - Audio converted to text (if voice input)
   - Text processed by LLM agent
   - Intent detection and response generation
3. **Order Handling**:
   - Collect name and items
   - Offer upsells and modifications
   - Request final confirmation
   - Submit to backend API
4. **Response**:
   - Generate Arabic text response
   - Convert to speech audio
   - Display order confirmation with ID and ETA

## 🛠️ API Endpoints

### Submit Order
```http
POST /submit-order
Content-Type: application/json

{
  "name": "محمد أحمد",
  "items": ["شاورما دجاج", "عصير برتقال", "بطاطا مقلية"]
}
```

### Get All Orders
```http
GET /orders
```

### Get Specific Order
```http
GET /orders/{order_id}
```

## 🎯 Supported Intents

- **Order**: Food ordering with confirmation flow
- **Complaint**: Empathetic customer service responses
- **Question**: Information and help requests
- **Other**: General conversation and clarification

## 🌐 External Services

- **Google Gemini**: LLM for conversational AI
- **ElevenLabs**: Text-to-speech conversion
- **Hugging Face**: Speech-to-text (Whisper model)

## 📝 Development Notes

### Adding New Features
1. Update relevant component files
2. Modify `config.py` for new settings
3. Update `requirements.txt` for new dependencies
4. Test integration through `main.py`

### Customization
- Modify the system prompt in `chat_agent.py` for different behaviors
- Update voice settings in `config.py`
- Customize UI styling in `gradio_interface.py`

## 🔒 Security Considerations

- **API Keys**: Keep API keys secure and use environment variables in production
- **Input Validation**: Validate all user inputs
- **Rate Limiting**: Implement rate limiting for production use
- **Authentication**: Add user authentication for production deployment

## 🐛 Troubleshooting

### Common Issues
1. **Audio not working**: Check ElevenLabs API key and quota
2. **Speech recognition failing**: Verify Hugging Face API key
3. **Backend connection errors**: Ensure Flask server is running
4. **Order submission failing**: Check backend API endpoint availability

### Logs and Debugging
- Enable debug mode in `config.py`
- Check console output for error messages
- Verify API key validity and quotas

## 📈 Future Enhancements

- Multi-user support with session management
- Menu integration with pricing
- Payment processing integration
- Order tracking and status updates
- Analytics and reporting dashboard
- Mobile app development
- Multi-language support

## 📄 License

This project is for educational and demonstration purposes. Please ensure you have proper licenses for all external APIs and services used.