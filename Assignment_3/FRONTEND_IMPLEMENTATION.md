# Front-End Implementation

## Overview

The ShieldMail frontend is built using React.js and provides an interactive user interface for spam detection. The application features three main sections: email prediction, statistics dashboard, and prediction history. The frontend communicates with the FastAPI backend through HTTP requests to send email text and retrieve prediction results.

## Key Features

### 1. User Input Form with Validation

The `EmailInputForm` component provides a user-friendly interface for entering email text. It includes:

- **Text Input Area**: A large textarea for pasting or typing email content
- **Character Counter**: Real-time display of character count (0-50,000 characters)
- **Input Validation**: Client-side validation to ensure:
  - Email text is not empty
  - Text length does not exceed 50,000 characters
- **Example Emails**: Quick-load buttons for spam and legitimate email examples
- **Error Handling**: Displays validation errors and API errors to the user
- **Loading States**: Disables form submission during prediction requests

**Code Snippet 1: EmailInputForm Component with Validation**

```jsx
// frontend/src/components/EmailInputForm.jsx
import React, { useState } from 'react'
import './EmailInputForm.css'

const EmailInputForm = ({ onPredict, loading, error }) => {
  const [text, setText] = useState('')
  const [validationError, setValidationError] = useState('')

  const validateInput = (value) => {
    if (!value || !value.trim()) {
      return 'Email text cannot be empty'
    }
    if (value.length > 50000) {
      return 'Email text must be less than 50,000 characters'
    }
    return null
  }

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

  const handleChange = (e) => {
    const value = e.target.value
    setText(value)
    setValidationError('')
  }

  return (
    <div className="email-input-form-container">
      <div className="card">
        <h2>Email Spam Detection</h2>
        <p className="subtitle">Enter email text to analyze for spam</p>

        <form onSubmit={handleSubmit} className="form">
          <div className="form-group">
            <label htmlFor="email-text">Email Text</label>
            <textarea
              id="email-text"
              value={text}
              onChange={handleChange}
              placeholder="Paste or type the email text here..."
              rows={10}
              className={validationError ? 'error' : ''}
              disabled={loading}
            />
            <div className="char-count">
              {text.length} / 50,000 characters
            </div>
            {validationError && (
              <div className="error-message">{validationError}</div>
            )}
          </div>

          {error && (
            <div className="error-message api-error">{error}</div>
          )}

          <button
            type="submit"
            className="submit-btn"
            disabled={loading || !text.trim()}
          >
            {loading ? 'Analyzing...' : 'Analyze Email'}
          </button>
        </form>
      </div>
    </div>
  )
}

export default EmailInputForm
```

### 2. Data Visualization

The frontend includes comprehensive data visualization features implemented using the Recharts library:

#### 2.1 Prediction Results Display
- **Probability Bars**: Visual representation of spam and safe probabilities
- **Status Badges**: Color-coded indicators (SPAM/SAFE)
- **Model Information**: Displays model metadata including accuracy and F1 score
- **Timestamp Display**: Shows when the prediction was made

**Code Snippet 2: PredictionResults Component**

```jsx
// frontend/src/components/PredictionResults.jsx
import React from 'react'
import './PredictionResults.css'

const PredictionResults = ({ prediction }) => {
  if (!prediction) return null

  const spamPercentage = (prediction.spam_probability * 100).toFixed(2)
  const safePercentage = (prediction.safe_probability * 100).toFixed(2)
  const isSpam = prediction.is_spam

  return (
    <div className="prediction-results">
      <div className={`card result-card ${isSpam ? 'spam' : 'safe'}`}>
        <div className="result-header">
          <h2 className={isSpam ? 'spam-title' : 'safe-title'}>
            {isSpam ? 'Spam Detected' : 'Legitimate Email'}
          </h2>
          <div className={`status-badge ${isSpam ? 'spam-badge' : 'safe-badge'}`}>
            {isSpam ? 'SPAM' : 'SAFE'}
          </div>
        </div>

        <div className="probability-bar-container">
          <div className="probability-info">
            <div className="prob-item spam-prob">
              <span className="prob-label">Spam Probability</span>
              <span className="prob-value">{spamPercentage}%</span>
            </div>
            <div className="prob-item safe-prob">
              <span className="prob-label">Safe Probability</span>
              <span className="prob-value">{safePercentage}%</span>
            </div>
          </div>
          
          <div className="probability-bar">
            <div 
              className="prob-bar-spam" 
              style={{ width: `${spamPercentage}%` }}
            />
            <div 
              className="prob-bar-safe" 
              style={{ width: `${safePercentage}%` }}
            />
          </div>
        </div>
      </div>
    </div>
  )
}

export default PredictionResults
```

#### 2.2 Statistics Dashboard
The `StatisticsDashboard` component provides multiple visualization types:

- **Pie Chart**: Distribution of spam vs legitimate emails
- **Bar Chart**: Probability distribution histogram
- **Line Chart**: Time series of predictions over time with date filtering
- **Token Impact Analysis**: Bar chart showing feature contributions (words that influence predictions)
- **Text Heatmap**: In-text visualization highlighting spam-indicating and legitimate-indicating words

**Code Snippet 3: Statistics Dashboard with Charts**

```jsx
// frontend/src/components/StatisticsDashboard.jsx
import React, { useMemo, useState, useEffect, useRef } from 'react'
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  PieChart, Pie, Cell, LineChart, Line
} from 'recharts'
import './StatisticsDashboard.css'

const StatisticsDashboard = ({ stats, predictions }) => {
  const chartData = useMemo(() => {
    if (!predictions || predictions.length === 0) return null

    // Pie chart data
    const spamCount = predictions.filter(p => p.is_spam).length
    const safeCount = predictions.filter(p => !p.is_spam).length
    const pieData = [
      { name: 'Spam', value: spamCount, color: '#e74c3c' },
      { name: 'Legitimate', value: safeCount, color: '#27ae60' }
    ]

    // Probability distribution histogram
    const probabilityRanges = [
      { range: '0-20%', spam: 0, safe: 0 },
      { range: '20-40%', spam: 0, safe: 0 },
      { range: '40-60%', spam: 0, safe: 0 },
      { range: '60-80%', spam: 0, safe: 0 },
      { range: '80-100%', spam: 0, safe: 0 }
    ]

    predictions.forEach(pred => {
      const spamProb = pred.spam_probability * 100
      let rangeIndex = Math.floor(spamProb / 20)
      if (rangeIndex >= 5) rangeIndex = 4
      
      if (pred.is_spam) {
        probabilityRanges[rangeIndex].spam++
      } else {
        probabilityRanges[rangeIndex].safe++
      }
    })

    return { pieData, probabilityRanges, spamCount, safeCount }
  }, [predictions])

  return (
    <div className="dashboard-container">
      <div className="stats-grid">
        {/* Pie Chart */}
        <div className="chart-card">
          <h3>Spam vs Legitimate Distribution</h3>
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
        </div>

        {/* Bar Chart */}
        <div className="chart-card">
          <h3>Spam Probability Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData.probabilityRanges}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="range" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="spam" fill="#e74c3c" name="Spam" />
              <Bar dataKey="safe" fill="#27ae60" name="Legitimate" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Line Chart - Time Series */}
        <div className="chart-card full-width">
          <h3>Predictions Over Time</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData.timeSeriesArray}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line 
                type="monotone" 
                dataKey="spam" 
                stroke="#e74c3c" 
                name="Spam"
                strokeWidth={2}
              />
              <Line 
                type="monotone" 
                dataKey="safe" 
                stroke="#27ae60" 
                name="Legitimate"
                strokeWidth={2}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  )
}

export default StatisticsDashboard
```

#### 2.3 Prediction History
- **Summary Statistics**: Cards showing total predictions, spam count, and legitimate count
- **Prediction List**: Detailed view of all predictions with filtering and export capabilities
- **CSV Export**: Functionality to export prediction history to CSV format

### 3. HTTP Requests and Backend Communication

The frontend communicates with the FastAPI backend using HTTP requests. While Axios is included in the dependencies, the implementation uses the native `fetch` API for HTTP requests. All API calls are centralized in the main `App.jsx` component.

**Code Snippet 4: HTTP Request Implementation (App.jsx)**

```jsx
// frontend/src/App.jsx
import React, { useState, useEffect } from 'react'
import './App.css'
import EmailInputForm from './components/EmailInputForm'
import PredictionResults from './components/PredictionResults'
import StatisticsDashboard from './components/StatisticsDashboard'
import PredictionHistory from './components/PredictionHistory'
import Header from './components/Header'

function App() {
  const [prediction, setPrediction] = useState(null)
  const [predictions, setPredictions] = useState([])
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [activeTab, setActiveTab] = useState('predict')

  // API base URL from environment variable or default to empty string for relative URLs
  const API_BASE_URL = import.meta.env.VITE_API_URL || ''

  useEffect(() => {
    fetchStats()
    fetchPredictions()
  }, [])

  // Fetch statistics from backend
  const fetchStats = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/stats`)
      if (response.ok) {
        const data = await response.json()
        setStats(data)
      }
    } catch (err) {
      console.error('Error fetching stats:', err)
    }
  }

  // Fetch all predictions from backend
  const fetchPredictions = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/predictions?limit=50`)
      if (response.ok) {
        const data = await response.json()
        setPredictions(data)
      }
    } catch (err) {
      console.error('Error fetching predictions:', err)
    }
  }

  // Send email text to backend for prediction
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
      
      // Refresh stats and predictions after successful prediction
      await Promise.all([fetchStats(), fetchPredictions()])
      
      // Scroll to results
      setTimeout(() => {
        const resultsElement = document.querySelector('.prediction-results')
        if (resultsElement) {
          resultsElement.scrollIntoView({ behavior: 'smooth', block: 'start' })
        }
      }, 100)
    } catch (err) {
      // Handle connection errors
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

  // Delete a prediction
  const handleDeletePrediction = async (predictionId) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/predictions/${predictionId}`, {
        method: 'DELETE',
      })

      if (response.ok) {
        await Promise.all([fetchStats(), fetchPredictions()])
        // Clear current prediction if it was deleted
        if (prediction && prediction.prediction_id === predictionId) {
          setPrediction(null)
        }
      }
    } catch (err) {
      console.error('Error deleting prediction:', err)
    }
  }

  return (
    <div className="App">
      <Header activeTab={activeTab} setActiveTab={setActiveTab} />
      
      <div className="container">
        {activeTab === 'predict' && (
          <div className="tab-content">
            <EmailInputForm 
              onPredict={handlePredict} 
              loading={loading}
              error={error}
            />
            {prediction && (
              <PredictionResults prediction={prediction} />
            )}
          </div>
        )}

        {activeTab === 'dashboard' && (
          <div className="tab-content">
            <StatisticsDashboard 
              stats={stats}
              predictions={predictions}
            />
          </div>
        )}

        {activeTab === 'history' && (
          <div className="tab-content">
            <PredictionHistory 
              predictions={predictions}
              onDelete={handleDeletePrediction}
              onRefresh={fetchPredictions}
              loading={loading}
              stats={stats}
            />
          </div>
        )}
      </div>
    </div>
  )
}

export default App
```

### 4. API Endpoints Used

The frontend makes HTTP requests to the following backend endpoints:

- **POST `/api/predict`**: Submit email text for spam prediction
- **GET `/api/predictions`**: Retrieve all predictions (with optional limit query parameter)
- **GET `/api/stats`**: Get statistics about predictions
- **DELETE `/api/predictions/{id}`**: Delete a specific prediction
- **POST `/api/generate-sample-data`**: Generate sample prediction data (for testing)

### 5. Error Handling

The frontend implements comprehensive error handling:

- **Validation Errors**: Client-side validation before submitting requests
- **API Errors**: Displays error messages from backend responses
- **Connection Errors**: Detects and displays friendly messages when backend is unavailable
- **Loading States**: Shows loading indicators during API requests
- **Error State Management**: Maintains error state and clears it appropriately

### 6. State Management

The application uses React's built-in state management with `useState` and `useEffect` hooks:

- **Prediction State**: Stores the current prediction result
- **Predictions List**: Maintains a list of all predictions
- **Statistics**: Stores aggregated statistics from the backend
- **Loading States**: Tracks loading status for async operations
- **Error States**: Manages error messages and display
- **Active Tab**: Tracks the currently selected navigation tab

### 7. Data Flow

1. **User Input**: User enters email text in the `EmailInputForm` component
2. **Validation**: Client-side validation checks input validity
3. **HTTP Request**: Valid input is sent to backend via POST request to `/api/predict`
4. **Response Handling**: Backend response is parsed and stored in state
5. **UI Update**: Prediction results are displayed in `PredictionResults` component
6. **Data Refresh**: Statistics and prediction history are refreshed from backend
7. **Visualization**: Updated data is rendered in charts and dashboards

## Technical Implementation Details

### Dependencies

The frontend uses the following key dependencies:

- **React 18.2.0**: UI framework
- **Recharts 2.10.0**: Chart library for data visualization
- **Axios 1.6.0**: HTTP client library (available but uses fetch API in implementation)
- **Vite 5.0.0**: Build tool and development server

### Component Structure

```
frontend/src/
├── App.jsx                 # Main application component with state management
├── components/
│   ├── EmailInputForm.jsx  # User input form with validation
│   ├── PredictionResults.jsx # Prediction results display
│   ├── StatisticsDashboard.jsx # Data visualization dashboard
│   ├── PredictionHistory.jsx # Prediction history and management
│   └── Header.jsx          # Navigation header
└── main.jsx                # Application entry point
```

### Key Design Patterns

1. **Component Composition**: Modular components that can be reused and composed
2. **Props Drilling**: State and handlers passed down through component hierarchy
3. **Controlled Components**: Form inputs are controlled by React state
4. **Conditional Rendering**: UI elements conditionally rendered based on state
5. **Async/Await**: Modern JavaScript async patterns for HTTP requests
6. **Memoization**: `useMemo` hook used for expensive computations in visualizations

## Summary

The frontend implementation provides a comprehensive, user-friendly interface for spam detection. It features robust input validation, rich data visualizations, and seamless communication with the backend API through HTTP requests. The use of React hooks for state management and the Recharts library for visualizations creates an interactive and responsive user experience.

