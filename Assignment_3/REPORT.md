# Assignment 3 - ShieldMail Web Application Report

## 2. Frontend Implementation

The frontend of ShieldMail is built using React.js 18.2.0, providing an interactive single-page application (SPA) with comprehensive spam detection capabilities. The implementation focuses on user experience, data visualization, and seamless integration with the backend API.

### 2.1 User Input Form and Validation

The `EmailInputForm` component provides the primary interface for users to submit email text for spam analysis. The form includes several key features:

**Input Validation:**
The component implements client-side validation to ensure data quality before submission. The validation function is located in `frontend/src/components/EmailInputForm.jsx`:

```jsx
// File: frontend/src/components/EmailInputForm.jsx (lines 8-16)
const validateInput = (value) => {
  if (!value || !value.trim()) {
    return 'Email text cannot be empty'
  }
  if (value.length > 50000) {
    return 'Email text must be less than 50,000 characters'
  }
  return null
}
```

The validation checks ensure that:
- The input is not empty or whitespace-only
- The text length does not exceed 50,000 characters
- Validation errors are displayed immediately to the user

**User Interface Features:**
- **Textarea Input**: A large text area (10 rows) for pasting or typing email content
- **Character Counter**: Real-time display of character count (e.g., "1,234 / 50,000 characters")
- **Example Emails**: Quick-load buttons for spam and legitimate email examples to help users understand the system
- **Loading States**: The submit button displays "Analyzing..." during API calls and is disabled to prevent duplicate submissions
- **Error Display**: Both validation errors and API errors are clearly displayed to the user

**Form Submission:**
The form uses React's controlled component pattern, managing state through the `text` state variable and handling submission through the `handleSubmit` function. This code is in `frontend/src/components/EmailInputForm.jsx`:

```jsx
// File: frontend/src/components/EmailInputForm.jsx (lines 18-29)
const handleSubmit = async (e) => {
  e.preventDefault()
  setValidationError('')

  const validation = validateInput(text)
  if (validation) {
    setValidationError(validation)
    return
  }

  await onPredict(text)
}
```

### 2.2 Data Visualization

The application provides comprehensive data visualizations using the Recharts library, offering both aggregate analytics and individual prediction analysis.

**Statistics Dashboard** (`StatisticsDashboard` component) features two analysis modes:

1. **Aggregate Analysis**: Displays three interactive charts—a pie chart showing spam vs legitimate distribution, a bar chart illustrating probability distribution across ranges (0-20%, 20-40%, 40-60%, 60-80%, 80-100%), and a time series line chart with date range filtering for tracking predictions over time.

2. **Single Prediction Analysis**: Provides detailed analysis of individual predictions through a token impact bar chart (showing top 15 most influential words) and an in-text heatmap that color-codes words by their contribution to the classification (red for spam-indicating, green for legitimate-indicating).

All visualizations are responsive, include interactive tooltips, and support CSV export functionality. The pie chart implementation example is located in `frontend/src/components/StatisticsDashboard.jsx`:

```jsx
// File: frontend/src/components/StatisticsDashboard.jsx (lines 658-677)
<ResponsiveContainer width="100%" height={300}>
  <PieChart>
    <Pie
      data={chartData.pieData}
      cx="50%"
      cy="50%"
      labelLine={false}
      label={({ percent }) => `${(percent * 100).toFixed(0)}%`}
      outerRadius={100}
      fill="#8884d8"
      dataKey="value"
    >
      {chartData.pieData.map((entry, index) => (
        <Cell key={`cell-${index}`} fill={entry.color} />
      ))}
    </Pie>
    <Tooltip />
    <Legend />
  </PieChart>
</ResponsiveContainer>
```

**Prediction Results Display** (`PredictionResults` component) presents outcomes with color-coded status badges (SPAM/SAFE), probability bars showing spam and safe percentages, and model metadata including type, accuracy, F1 score, and timestamp.

### 2.3 HTTP Requests and Backend Integration

The frontend communicates with the backend API using the native `fetch` API, with all API calls centralized in the `App` component for state management and data flow coordination. The API base URL is configured via environment variables with a fallback to relative URLs for development (`frontend/src/App.jsx`, line 18).

**Prediction Request** (`handlePredict` function in `frontend/src/App.jsx`, lines 49-98) sends a POST request to `/api/predict` with comprehensive error handling, loading states, and automatic refresh of statistics and prediction history after successful predictions:

```jsx
// File: frontend/src/App.jsx (lines 49-98)
const handlePredict = async (text) => {
  setLoading(true)
  setError(null)
  try {
    const response = await fetch(`${API_BASE_URL}/api/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text }),
    })

    if (!response.ok) {
      let errorMessage = 'Prediction failed'
      try {
        const errorData = await response.json()
        errorMessage = errorData.detail || errorMessage
      } catch (e) {
        errorMessage = response.statusText || errorMessage
      }
      throw new Error(errorMessage)
    }

    const data = await response.json()
    setPrediction(data)
    
    // Refresh stats and predictions
    await Promise.all([fetchStats(), fetchPredictions()])
  } catch (err) {
    // Error handling for connection issues
    if (err.message.includes('Failed to fetch') || err.name === 'TypeError') {
      setError('Cannot connect to backend server. Please make sure the backend is running on http://localhost:8000')
    } else {
      setError(err.message)
    }
    setPrediction(null)
  } finally {
    setLoading(false)
  }
}
```

**Additional API Endpoints** include GET requests for statistics (`/api/stats`) and prediction history (`/api/predictions?limit=50`), and DELETE requests for prediction deletion (`/api/predictions/{id}`). All endpoints implement proper error handling and automatically refresh related data upon successful operations.

### 2.4 Component Architecture

The frontend follows a component-based architecture with clear separation of concerns:

**Main Components:**
- **App.jsx**: Main application component managing global state, API calls, and routing between tabs
- **EmailInputForm.jsx**: User input form with validation
- **PredictionResults.jsx**: Display of prediction results
- **StatisticsDashboard.jsx**: Comprehensive data visualizations
- **PredictionHistory.jsx**: List view of all predictions with management capabilities
- **Header.jsx**: Navigation header with tab switching

**State Management:**
- React hooks (`useState`, `useEffect`, `useMemo`) are used for state management
- State is lifted to the `App` component for shared data (predictions, stats, current prediction)
- Component-level state manages UI-specific concerns (form inputs, selected items, filters)

**Data Flow:**
1. User submits email text through `EmailInputForm`
2. `App` component handles the API request
3. Prediction results are stored in `App` state
4. Results are passed to `PredictionResults` for display
5. Statistics and history are automatically refreshed
6. Visualizations update based on new data

### 2.5 User Experience Features

**Navigation:**
- Tab-based navigation between Predict, Dashboard, and History views
- Active tab highlighting for clear user orientation
- Smooth scrolling to results after prediction

**Feedback and Error Handling:**
- Loading indicators during API calls
- Clear error messages for validation and API errors
- Success indicators through visual result displays
- Disabled states prevent duplicate submissions

**Data Management:**
- Automatic data refresh after predictions
- Export functionality for statistics and prediction history (CSV format)
- Sample data generation for testing and demonstration
- Prediction deletion with confirmation through UI

**Responsive Design:**
- Charts adapt to container size
- Mobile-friendly form layouts
- Accessible color schemes and contrast
- Clear typography and spacing

## 3. Backend Implementation

The backend of ShieldMail is built using FastAPI, a modern Python web framework that provides automatic API documentation, type validation, and asynchronous request handling. The server implements a RESTful API architecture for spam detection predictions and data management.

### 3.1 FastAPI Server Setup

The FastAPI application is initialized in `backend/main.py` with comprehensive configuration:

```python
# File: backend/main.py (lines 30-43)
app = FastAPI(
    title="ShieldMail API",
    description="Spam Detection API for ShieldMail Web Application",
    version="1.0.0"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Key Configuration Features:**
- **CORS Middleware**: Enables cross-origin requests from the React frontend running on ports 3000 and 5173
- **Automatic API Documentation**: FastAPI generates interactive API documentation at `/docs` endpoint
- **Type Validation**: Uses Pydantic models for request/response validation
- **Error Handling**: Global exception handler for consistent error responses
- **Service Integration**: Initializes `ModelService` for AI model operations and `PredictionStore` for in-memory prediction storage

**Service Architecture:**
- **ModelService**: Loads and manages the packaged AI model from Assignment 2, providing prediction functionality
- **PredictionStore**: In-memory storage for predictions with methods for CRUD operations and statistics calculation

### 3.2 API Endpoint Documentation

The backend provides multiple RESTful endpoints for spam detection and prediction management. The following sections document the four most critical endpoints. *Note: Due to page limitations, not all API endpoints are shown here. Additional endpoints include batch prediction, model information retrieval, health checks, and prediction updates.*

#### 3.2.1 POST /api/predict

Predicts whether an email text is spam or legitimate.

**Request:**
- **Method**: `POST`
- **URL**: `/api/predict`
- **Content-Type**: `application/json`
- **Request Body**:
```json
{
  "text": "Email text to analyze (1-50000 characters)"
}
```

**Response:**
- **Status Code**: `201 Created` (success) or `400 Bad Request` / `503 Service Unavailable` (error)
- **Response Body**:
```json
{
  "prediction_id": "uuid-string",
  "text": "Truncated email text...",
  "is_spam": true,
  "spam_probability": 0.85,
  "safe_probability": 0.15,
  "timestamp": "2024-11-06T12:00:00.000000",
  "model_metadata": {
    "model_type": "Naive Bayes",
    "accuracy": 0.92,
    "f1_score": 0.89
  }
}
```

**Implementation Location**: `backend/main.py` (lines 262-308)

#### 3.2.2 GET /api/predictions

Retrieves stored predictions with pagination support.

**Request:**
- **Method**: `GET`
- **URL**: `/api/predictions?limit=50&offset=0`
- **Query Parameters**:
  - `limit` (optional): Maximum number of predictions to return (default: 50, max: 500)
  - `offset` (optional): Number of predictions to skip (default: 0)

**Response:**
- **Status Code**: `200 OK` (success) or `500 Internal Server Error` (error)
- **Response Body**: Array of prediction objects
```json
[
  {
    "prediction_id": "uuid-string",
    "text": "Truncated email text...",
    "is_spam": false,
    "spam_probability": 0.25,
    "safe_probability": 0.75,
    "timestamp": "2024-11-06T11:00:00.000000",
    "model_metadata": {...}
  },
  ...
]
```

**Implementation Location**: `backend/main.py` (lines 372-393)

#### 3.2.3 GET /api/stats

Retrieves aggregate statistics about all predictions.

**Request:**
- **Method**: `GET`
- **URL**: `/api/stats`

**Response:**
- **Status Code**: `200 OK` (success) or `500 Internal Server Error` (error)
- **Response Body**:
```json
{
  "total_predictions": 150,
  "spam_count": 45,
  "safe_count": 105,
  "accuracy_feedback": 92.5,
  "recent_predictions": [
    {
      "prediction_id": "uuid-string",
      "text": "Truncated email text...",
      "is_spam": true,
      "spam_probability": 0.90,
      "safe_probability": 0.10,
      "timestamp": "2024-11-06T12:00:00.000000",
      "model_metadata": {...}
    },
    ...
  ]
}
```

**Implementation Location**: `backend/main.py` (lines 487-503)

#### 3.2.4 DELETE /api/predictions/{prediction_id}

Deletes a specific prediction by its unique identifier.

**Request:**
- **Method**: `DELETE`
- **URL**: `/api/predictions/{prediction_id}`
- **Path Parameters**:
  - `prediction_id`: Unique prediction identifier (UUID string)

**Response:**
- **Status Code**: `200 OK` (success), `404 Not Found` (prediction not found), or `500 Internal Server Error` (error)
- **Response Body**:
```json
{
  "message": "Prediction deleted successfully",
  "prediction_id": "uuid-string"
}
```

**Implementation Location**: `backend/main.py` (lines 456-484)

### 3.3 Data Models and Validation

The backend uses Pydantic models for request and response validation, ensuring type safety and data integrity:

**PredictionRequest** (`backend/main.py`, lines 50-57): Validates input text with constraints (1-50000 characters, non-empty after trimming)

**PredictionResponse** (`backend/main.py`, lines 59-66): Defines the structure of prediction responses including prediction ID, classification results, probabilities, timestamp, and model metadata

**Error Handling**: All endpoints implement comprehensive error handling with appropriate HTTP status codes (400 for validation errors, 404 for not found, 503 for service unavailable, 500 for server errors)

---

