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

---

