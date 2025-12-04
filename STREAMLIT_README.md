# VECTOR - Streamlit Integration Guide

## 🚀 Quick Start

### Option 1: Run both services locally
```bash
# Install dependencies
uv sync

# Run both FastAPI backend and Streamlit frontend
python run_app.py
```

### Option 2: Run services separately
```bash
# Terminal 1 - Start FastAPI backend
uvicorn src.api.main:app --reload --port 8000

# Terminal 2 - Start Streamlit frontend
streamlit run streamlit_app.py --server.port 8501
```

### Option 3: Docker deployment
```bash
# Build and run with Docker
docker build -t vector-app .
docker run -p 8000:8000 -p 8501:8501 vector-app
```

## 🌐 Access Points

- **Streamlit Frontend**: http://localhost:8501
- **FastAPI Backend**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📋 Environment Setup

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
EXA_API_KEY=your_exa_api_key_here
```

## 🎯 Features

### Streamlit Frontend
- **Interactive UI**: Clean, user-friendly interface for product search
- **Real-time Search**: Connect to your FastAPI backend for live results
- **Visual Analytics**: Price comparisons, rating distributions, and metrics
- **Product Cards**: Detailed product information with pros/cons
- **AI Recommendations**: Smart suggestions based on your requirements
- **Example Queries**: Pre-built examples to get started quickly

### Key Components
- **VectorUI**: Main UI components and styling
- **ProductDisplay**: Product card rendering and formatting
- **RecommendationDisplay**: AI recommendation visualization
- **Analytics Dashboard**: Charts and metrics for product comparison

## 🔧 Configuration

### Streamlit Configuration
The app automatically configures:
- Wide layout for better product display
- Custom CSS for professional styling
- Responsive design for different screen sizes

### API Integration
- Configurable API endpoint in sidebar
- Error handling for connection issues
- JSON response formatting and display

## 📱 Usage Examples

### Basic Product Search
```
"Lightweight laptop under $1200 for programming"
```

### Advanced Search
```
"Gaming headset under $200 with noise cancellation, prefer wireless, for competitive gaming"
```

### Specific Requirements
```
"Smartphone under $800 with excellent camera for photography, prefer Android, good battery life"
```

## 🛠 Development

### Project Structure
```
src/
├── frontend/
│   └── components.py    # Streamlit UI components
├── api/
│   └── main.py         # FastAPI backend
├── graph/
│   └── main_graph.py   # LangGraph workflow
└── ...

streamlit_app.py        # Main Streamlit application
run_app.py             # Launcher script
docker-entrypoint.sh   # Docker startup script
```

### Adding New Features

1. **New UI Components**: Add to `src/frontend/components.py`
2. **API Endpoints**: Modify `src/api/main.py`
3. **Styling**: Update CSS in `components.py`
4. **Charts**: Use Plotly for new visualizations

## 🐛 Troubleshooting

### Common Issues

1. **API Connection Failed**
   - Ensure FastAPI server is running on port 8000
   - Check if the API URL in sidebar is correct
   - Verify your API keys are set in `.env`

2. **Dependencies Missing**
   - Run `uv sync` to install all dependencies
   - Check Python version (requires >=3.13)

3. **Docker Issues**
   - Make sure both ports 8000 and 8501 are available
   - Check if `.env` file is properly configured

### Debug Mode

Enable debug information by expanding the "Raw API Response" section at the bottom of the results.

## 🔮 Future Enhancements

- [ ] User authentication and preferences
- [ ] Product comparison side-by-side
- [ ] Export results to PDF/Excel
- [ ] Price tracking and alerts
- [ ] Multi-language support
- [ ] Mobile-optimized layouts
- [ ] Integration with more e-commerce APIs