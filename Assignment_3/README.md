# Assignment 3 - ShieldMail Web Application

**Standalone full-stack spam detection application with packaged AI model from Assignment 2.**

## Overview

Assignment 3 is a complete, standalone web application that includes:
- **FastAPI backend** with AI model integration
- **React.js frontend** with interactive visualizations
- **Packaged AI model** from Assignment 2 (included in `models/` directory)
- **Standalone dependencies** - no dependency on Assignment 2

The application runs independently and does not require Assignment 2 to be present.

## Prerequisites

- **Python 3.8+**
- **Node.js 16+** and npm
- **AI model** in `models/spam_detection_model.pkl` (should already be packaged)

## Quick Start

### 1. Setup Python Environment

```bash
cd assignment_3

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

**Note:** Frontend dependencies (npm packages) will be automatically installed when you run `python main.py`. No need to run `npm install` manually!

### 2. Verify Model

The AI model should already be packaged in `models/` from Assignment 2:

```bash
ls models/spam_detection_model.pkl
```

If the model is missing, copy it from Assignment 2:
```bash
# From Assignment 2's outputs/models/ to assignment_3/models/
cp ../Assignment_2/outputs/models/spam_detection_model.pkl models/
cp ../Assignment_2/outputs/models/model_metadata.json models/
```

**Note:** `main.py` will automatically check if the model exists before starting the application.

### 3. Start Application

Start both backend and frontend with a single command:

```bash
cd assignment_3
source venv/bin/activate
python main.py
```

This will start:
- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:5173

Press `Ctrl+C` to stop both servers.

**Alternative: Start separately (if needed)**

If you prefer to run them separately:

**Terminal 1 (Backend):**
```bash
cd assignment_3
source venv/bin/activate
cd backend
uvicorn main:app --reload --port 8000
```

**Terminal 2 (Frontend):**
```bash
cd assignment_3/frontend
npm run dev
```

### 4. Use the Application

1. Open http://localhost:5173 in your browser
2. Enter email text in the input field
3. Click "Predict" to get spam detection results
4. View statistics dashboard and prediction history in other tabs

## Project Structure

```
assignment_3/
├── backend/                    # FastAPI backend
│   ├── main.py                # API endpoints
│   ├── model_service.py       # AI model loader (packaged from Assignment 2)
│   └── prediction_store.py    # In-memory prediction storage
├── frontend/                   # React.js frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── App.jsx           # Main application
│   │   └── main.jsx          # Entry point
│   ├── package.json
│   └── vite.config.js
├── models/                     # Packaged AI model from Assignment 2
│   ├── spam_detection_model.pkl
│   └── model_metadata.json
├── main.py                     # Main entry point (starts both servers)
└── requirements.txt            # Python dependencies (standalone)
```

## API Endpoints

- `POST /api/predict` - Predict spam for single email
- `POST /api/batch-predict` - Predict spam for multiple emails
- `GET /api/predictions` - Get all predictions
- `GET /api/predictions/{id}` - Get specific prediction
- `PUT /api/predictions/{id}` - Update prediction feedback
- `DELETE /api/predictions/{id}` - Delete prediction
- `GET /api/stats` - Get statistics
- `GET /api/health` - Health check
- `GET /api/model/info` - Model information

See http://localhost:8000/docs for interactive API documentation.

## Dependencies

### Python (requirements.txt)

- **FastAPI** - Web framework for API
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
- **scikit-learn** - Machine learning (for model loading)
- **joblib** - Model serialization
- **numpy** - Numerical operations
- **pandas** - Data processing (for optional model training)

### Node.js (package.json)

Dependencies are managed in `frontend/package.json`. They are **automatically installed** when you run `python main.py` - no manual `npm install` needed!

## Troubleshooting

### Backend Issues

- **Model not found**: Ensure `models/spam_detection_model.pkl` exists
- **Import errors**: Activate virtual environment and run `pip install -r requirements.txt`
- **Port 8000 in use**: Change port: `uvicorn main:app --reload --port 8001`

### Frontend Issues

- **npm install fails**: Check Node.js version (16+ required). If automatic installation fails, try manually:
  ```bash
  cd assignment_3/frontend
  npm install
  ```
- **Vite plugin errors**: Try cleaning and reinstalling:
  ```bash
  cd assignment_3/frontend
  rm -rf node_modules package-lock.json
  npm cache clean --force
  npm install
  ```
- **Port 5173 in use**: Vite will automatically use next available port
- **Cannot connect to backend**: Ensure backend is running on port 8000

### General Issues

- **No UI appears**: Make sure both backend AND frontend are running
- **Predictions fail**: Check backend logs for model loading errors
- **CORS errors**: Backend CORS is configured for localhost:5173 and localhost:3000

## Important Notes

1. **Single command startup**: Use `python main.py` to start both servers at once
2. **Automatic npm install**: Frontend dependencies are automatically installed if missing - no manual `npm install` needed!
3. **Backend shows text/JSON**: This is normal - it's an API server, not a UI
4. **Frontend shows the UI**: Open the URL (http://localhost:5173) in your browser
5. **Standalone execution**: Assignment 3 runs independently - no Assignment 2 needed
6. **Model packaging**: The AI model from Assignment 2 is packaged in `models/` directory
7. **Own dependencies**: Assignment 3 has its own `requirements.txt` - no dependency on Assignment 2
8. **Graceful shutdown**: Press `Ctrl+C` to stop both servers cleanly

## Development

### Start Both Servers (Recommended)

```bash
cd assignment_3
source venv/bin/activate
python main.py
```

### Start Servers Separately (for debugging)

**Backend only:**
```bash
cd assignment_3/backend
uvicorn main:app --reload --port 8000
```

**Frontend only:**
```bash
cd assignment_3/frontend
npm run dev
```

### Model Verification

The model is automatically verified when you start the application with `python main.py`. If the model is missing, you'll see an error message with instructions.

To manually check if the model exists:
```bash
ls assignment_3/models/spam_detection_model.pkl
```

## Requirements Compliance

- ✅ **Standalone execution**: No dependency on Assignment 2 at runtime
- ✅ **Standalone dependencies**: Own `requirements.txt` - no reference to Assignment 2
- ✅ **Packaged AI model**: Model from Assignment 2 included in `models/` directory
- ✅ **FastAPI backend**: RESTful API with multiple HTTP methods (GET, POST, PUT, DELETE)
- ✅ **React.js frontend**: Interactive UI with data visualizations
- ✅ **Error handling**: Comprehensive error handling and input validation
- ✅ **API integration**: AI model integrated into FastAPI backend
