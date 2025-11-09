# Front-End Implementation

## Overview

The ShieldMail frontend is built using React.js and provides an interactive user interface for spam detection. The application features a user input form with validation, data visualizations, and communicates with the FastAPI backend through HTTP requests to send email text and retrieve prediction results.

## Key Features

### 1. User Input Form with Validation

The `EmailInputForm` component provides a user-friendly interface for entering email text with client-side validation. It validates that the email text is not empty and does not exceed 50,000 characters. The form includes real-time character counting, error message display, and loading states during API requests.

**Code Snippet 1: EmailInputForm with Validation**

```jsx
// frontend/src/components/EmailInputForm.jsx
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

  return (
    <form onSubmit={handleSubmit}>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        className={validationError ? 'error' : ''}
        disabled={loading}
      />
      <div className="char-count">{text.length} / 50,000 characters</div>
      {validationError && <div className="error-message">{validationError}</div>}
      <button type="submit" disabled={loading || !text.trim()}>
        {loading ? 'Analyzing...' : 'Analyze Email'}
      </button>
    </form>
  )
}
```

### 2. Data Visualization

The frontend includes data visualization features using the Recharts library. The `StatisticsDashboard` component displays prediction statistics through pie charts, bar charts, and line charts. It visualizes the distribution of spam vs legitimate emails, probability distributions, and predictions over time.

**Code Snippet 2: Statistics Dashboard with Visualization**

```jsx
// frontend/src/components/StatisticsDashboard.jsx
import { BarChart, Bar, XAxis, YAxis, PieChart, Pie, Cell, ResponsiveContainer } from 'recharts'

const StatisticsDashboard = ({ predictions }) => {
  const chartData = useMemo(() => {
    const spamCount = predictions.filter(p => p.is_spam).length
    const safeCount = predictions.filter(p => !p.is_spam).length
    
    const pieData = [
      { name: 'Spam', value: spamCount, color: '#e74c3c' },
      { name: 'Legitimate', value: safeCount, color: '#27ae60' }
    ]

    const probabilityRanges = [
      { range: '0-20%', spam: 0, safe: 0 },
      { range: '20-40%', spam: 0, safe: 0 },
      { range: '40-60%', spam: 0, safe: 0 },
      { range: '60-80%', spam: 0, safe: 0 },
      { range: '80-100%', spam: 0, safe: 0 }
    ]

    predictions.forEach(pred => {
      const spamProb = pred.spam_probability * 100
      const rangeIndex = Math.min(Math.floor(spamProb / 20), 4)
      if (pred.is_spam) {
        probabilityRanges[rangeIndex].spam++
      } else {
        probabilityRanges[rangeIndex].safe++
      }
    })

    return { pieData, probabilityRanges }
  }, [predictions])

  return (
    <div className="dashboard-container">
      {/* Pie Chart - Spam vs Legitimate Distribution */}
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={chartData.pieData}
            cx="50%"
            cy="50%"
            label={({ percent }) => `${(percent * 100).toFixed(0)}%`}
            outerRadius={100}
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

      {/* Bar Chart - Probability Distribution */}
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData.probabilityRanges}>
          <XAxis dataKey="range" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="spam" fill="#e74c3c" name="Spam" />
          <Bar dataKey="safe" fill="#27ae60" name="Legitimate" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
```

### 3. HTTP Requests and Backend Communication

The frontend communicates with the FastAPI backend using HTTP requests via the native `fetch` API. Data is sent to the backend as JSON in POST requests, and predictions are retrieved through GET requests. The main API communication is handled in the `App.jsx` component.

**Code Snippet 3: HTTP Request Implementation**

```jsx
// frontend/src/App.jsx
function App() {
  const [prediction, setPrediction] = useState(null)
  const [predictions, setPredictions] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const API_BASE_URL = import.meta.env.VITE_API_URL || ''

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
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Prediction failed')
      }

      const data = await response.json()
      setPrediction(data)
      
      // Refresh predictions after successful prediction
      await fetchPredictions()
    } catch (err) {
      setError(err.message)
      setPrediction(null)
    } finally {
      setLoading(false)
    }
  }

  // Retrieve predictions from backend
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

  // Retrieve statistics from backend
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

  return (
    <div className="App">
      <EmailInputForm 
        onPredict={handlePredict} 
        loading={loading}
        error={error}
      />
      {prediction && <PredictionResults prediction={prediction} />}
      <StatisticsDashboard predictions={predictions} />
    </div>
  )
}
```

## Summary

The frontend implementation provides a user-friendly interface with input validation, data visualizations using Recharts, and HTTP-based communication with the backend. Email text is validated client-side, then sent to the backend via POST requests to `/api/predict`. Predictions are retrieved through GET requests to `/api/predictions` and `/api/stats`, and the results are displayed in interactive charts and visualizations.
