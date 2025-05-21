# William Travel API - Frontend Integration Guide

## Introduction

This document provides comprehensive guidelines for frontend developers integrating with the William Travel API. It
includes authentication flows, API endpoints, data models, and code examples specifically designed for frontend
applications.

## API Base URL

- **Development**: `http://localhost:8000/api/v1`
- **Production**: `https://api.williamtravel.com/api/v1`

## Authentication

The API uses JWT (JSON Web Token) authentication.

### Authentication Flow

1. **User Login**

```javascript
// Using fetch API
async function login(email, password) {
    const response = await fetch('http://localhost:8000/api/v1/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: email,
            password: password
        })
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Login failed');
    }

    const data = await response.json();

    // Store token in localStorage or secure storage
    localStorage.setItem('accessToken', data.access_token);

    return data;
}
```

2. **User Registration**

```javascript
async function register(email, password, fullName) {
    const response = await fetch('http://localhost:8000/api/v1/auth/signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: email,
            password: password,
            full_name: fullName
        })
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Registration failed');
    }

    return await response.json();
}
```

3. **Adding Authentication to Requests**

```javascript
// API client utility
const apiClient = {
    async request(endpoint, options = {}) {
        const token = localStorage.getItem('accessToken');

        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                ...(token ? {Authorization: `Bearer ${token}`} : {})
            }
        };

        const mergedOptions = {
            ...defaultOptions,
            ...options,
            headers: {
                ...defaultOptions.headers,
                ...options.headers
            }
        };

        const response = await fetch(`http://localhost:8000/api/v1${endpoint}`, mergedOptions);

        // Handle token expiration
        if (response.status === 401) {
            localStorage.removeItem('accessToken');
            // Redirect to login page or refresh token
            window.location.href = '/login';
            throw new Error('Session expired');
        }

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || `API request failed with status ${response.status}`);
        }

        return response.json();
    },

    get(endpoint) {
        return this.request(endpoint, {method: 'GET'});
    },

    post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },

    put(endpoint, data) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    },

    delete(endpoint) {
        return this.request(endpoint, {method: 'DELETE'});
    }
};
```

## Error Handling

The API returns standardized error responses with the following structure:

```json
{
  "error": "ERROR_CODE",
  "message": "User-friendly error message",
  "details": {
    // Additional error details
  }
}
```

Example of handling errors in frontend code:

```javascript
try {
    const data = await apiClient.get('/users/me');
    // Process data
} catch (error) {
    // Handle error
    console.error('API Error:', error.message);

    // Show appropriate UI notification
    showNotification({
        type: 'error',
        message: error.message
    });
}
```

## Common Error Codes

| Error Code         | Description             | Frontend Handling                   |
|--------------------|-------------------------|-------------------------------------|
| `UNAUTHORIZED`     | User not authenticated  | Redirect to login page              |
| `FORBIDDEN`        | User lacks permission   | Show permission error message       |
| `NOT_FOUND`        | Resource not found      | Show 404 message or redirect        |
| `VALIDATION_ERROR` | Input validation failed | Display field validation errors     |
| `INTERNAL_ERROR`   | Server-side error       | Show generic error and retry option |

## Core API Endpoints

### User Management

#### Get Current User Profile

```javascript
// Get current user profile
const userProfile = await apiClient.get('/users/me');

// Example response:
// {
//   "id": 1,
//   "email": "user@example.com",
//   "full_name": "User Name",
//   "is_active": true,
//   "created_at": "2023-01-01T12:00:00"
// }
```

#### Update User Profile

```javascript
const updatedProfile = await apiClient.put('/users/me', {
    full_name: "Updated Name",
    // other fields to update
});
```

### Location Endpoints

#### Get All Locations

```javascript
// Fetch locations with pagination
const getLocations = async (page = 1, limit = 10) => {
    return apiClient.get(`/locations?skip=${(page - 1) * limit}&limit=${limit}`);
};

// Example usage
const locationsData = await getLocations(1, 10);
// locationsData contains an array of location objects
```

#### Get Location Details

```javascript
const locationDetails = await apiClient.get(`/locations/${locationId}`);
```

#### Get Featured Locations

```javascript
const featuredLocations = await apiClient.get('/locations/featured');
```

#### Get Locations by Country

```javascript
const locationsByCountry = await apiClient.get(`/locations/country/${countryName}`);
```

### Accommodation Endpoints

#### Get All Accommodations

```javascript
const accommodations = await apiClient.get('/accommodations');
```

#### Get Accommodation Details

```javascript
const accommodationDetails = await apiClient.get(`/accommodations/${accommodationId}`);
```

#### Get Accommodations by Location

```javascript
const accommodationsByLocation = await apiClient.get(`/accommodations/location/${locationId}`);
```

#### Get Top-Rated Accommodations

```javascript
const topAccommodations = await apiClient.get('/accommodations/top');
```

### Foods & Restaurants

#### Get All Food Places

```javascript
const foodPlaces = await apiClient.get('/foods');
```

#### Get Food Places by Location

```javascript
const foodsByLocation = await apiClient.get(`/foods/location/${locationId}`);
```

#### Get Food Categories

```javascript
const foodCategories = await apiClient.get('/foods/categories');
```

### Articles & Travel Guides

#### Get All Articles

```javascript
const articles = await apiClient.get('/articles');
```

#### Get Article Details

```javascript
const articleDetails = await apiClient.get(`/articles/${articleId}`);
```

#### Get Articles by Location

```javascript
const articlesByLocation = await apiClient.get(`/articles/location/${locationId}`);
```

### Events

#### Get Upcoming Events

```javascript
const upcomingEvents = await apiClient.get('/events/upcoming');
```

#### Get Events by Location

```javascript
const eventsByLocation = await apiClient.get(`/events/location/${locationId}`);
```

### Community Posts

#### Get Community Posts

```javascript
const communityPosts = await apiClient.get('/community');
```

#### Create a Community Post

```javascript
const newPost = await apiClient.post('/community', {
    title: "My Amazing Trip",
    content: "It was a wonderful experience...",
    location_id: 1,
    media_ids: [1, 2, 3] // Optional
});
```

#### Get User's Posts

```javascript
const userPosts = await apiClient.get('/community/user/me');
```

### Media Uploads

```javascript
// Helper function for file uploads
async function uploadMedia(file, description = '') {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('description', description);

    const token = localStorage.getItem('accessToken');

    const response = await fetch('http://localhost:8000/api/v1/media/upload', {
        method: 'POST',
        headers: {
            Authorization: `Bearer ${token}`
        },
        body: formData
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Upload failed');
    }

    return await response.json();
}

// Example usage:
const fileInput = document.querySelector('input[type="file"]');
const uploadButton = document.querySelector('#uploadButton');

uploadButton.addEventListener('click', async () => {
    if (fileInput.files.length > 0) {
        try {
            const uploadResult = await uploadMedia(
                fileInput.files[0],
                "My vacation photo"
            );
            console.log('Upload successful:', uploadResult);
        } catch (error) {
            console.error('Upload failed:', error);
        }
    }
});
```

## Data Models & TypeScript Types

Here are TypeScript interfaces for the main entities:

```typescript
interface User {
    id: number;
    email: string;
    full_name: string;
    is_active: boolean;
    created_at: string;
}

interface Location {
    id: number;
    name: string;
    description: string;
    country: string;
    region: string;
    continent?: string;
    latitude: number;
    longitude: number;
    is_featured: boolean;
    is_active: boolean;
    created_at: string;
}

interface Accommodation {
    id: number;
    name: string;
    description: string;
    address: string;
    price_range: string; // "$", "$$", "$$$", "$$$$"
    location_id: number;
    amenities: string[];
    rating: number;
    is_active: boolean;
    created_at: string;
}

interface FoodPlace {
    id: number;
    name: string;
    description: string;
    address: string;
    price_range: string;
    cuisine_type: string;
    location_id: number;
    rating: number;
    is_active: boolean;
    created_at: string;
}

interface Article {
    id: number;
    title: string;
    content: string;
    location_id: number;
    author_id: number;
    published_at: string;
    is_active: boolean;
    created_at: string;
}

interface Event {
    id: number;
    name: string;
    description: string;
    location_id: number;
    start_date: string;
    end_date: string;
    is_active: boolean;
    created_at: string;
}

interface CommunityPost {
    id: number;
    title: string;
    content: string;
    user_id: number;
    location_id: number;
    created_at: string;
    is_active: boolean;
    media?: Media[];
}

interface Media {
    id: number;
    filename: string;
    url: string;
    mime_type: string;
    size: number;
    description?: string;
    user_id: number;
    created_at: string;
}

interface PaginatedResponse<T> {
    items: T[];
    total: number;
    page: number;
    size: number;
    pages: number;
}
```

## Authentication State Management

### React Example with Context API

```jsx
import React, {createContext, useState, useEffect, useContext} from 'react';

// Create Auth Context
const AuthContext = createContext();

// Auth Provider Component
export const AuthProvider = ({children}) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // Check for existing token and validate on mount
    useEffect(() => {
        const checkAuth = async () => {
            const token = localStorage.getItem('accessToken');

            if (!token) {
                setLoading(false);
                return;
            }

            try {
                // Verify token and get user
                const response = await fetch('http://localhost:8000/api/v1/users/me', {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                });

                if (!response.ok) {
                    throw new Error('Invalid token');
                }

                const userData = await response.json();
                setUser(userData);
            } catch (error) {
                console.error('Authentication error:', error);
                localStorage.removeItem('accessToken'); // Clear invalid token
            } finally {
                setLoading(false);
            }
        };

        checkAuth();
    }, []);

    // Login function
    const login = async (email, password) => {
        setError(null);

        try {
            const response = await fetch('http://localhost:8000/api/v1/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({username: email, password})
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Login failed');
            }

            const data = await response.json();
            localStorage.setItem('accessToken', data.access_token);

            // Get user profile
            const userResponse = await fetch('http://localhost:8000/api/v1/users/me', {
                headers: {
                    Authorization: `Bearer ${data.access_token}`
                }
            });

            if (!userResponse.ok) {
                throw new Error('Failed to get user profile');
            }

            const userData = await userResponse.json();
            setUser(userData);

            return userData;
        } catch (err) {
            setError(err.message);
            throw err;
        }
    };

    // Logout function
    const logout = () => {
        localStorage.removeItem('accessToken');
        setUser(null);
    };

    // Register function
    const register = async (email, password, fullName) => {
        setError(null);

        try {
            const response = await fetch('http://localhost:8000/api/v1/auth/signup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({email, password, full_name: fullName})
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Registration failed');
            }

            return await response.json();
        } catch (err) {
            setError(err.message);
            throw err;
        }
    };

    return (
        <AuthContext.Provider value={{
            user,
            loading,
            error,
            isAuthenticated: !!user,
            login,
            logout,
            register
        }}>
            {children}
        </AuthContext.Provider>
    );
};

// Auth Hook for easy access to auth context
export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};

// Usage Example:
// In your app:
// <AuthProvider>
//   <App />
// </AuthProvider>
//
// In your components:
// const { user, login, logout, isAuthenticated } = useAuth();
```

## Example Frontend Components

### Login Form Component (React)

```jsx
import React, {useState} from 'react';
import {useAuth} from '../context/AuthContext';
import {useNavigate} from 'react-router-dom';

const LoginForm = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [error, setError] = useState('');

    const {login} = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsSubmitting(true);
        setError('');

        try {
            await login(email, password);
            navigate('/dashboard'); // Redirect after login
        } catch (err) {
            setError(err.message);
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <div className="login-form">
            <h2>Login to William Travel</h2>

            {error && (
                <div className="error-message">
                    {error}
                </div>
            )}

            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="email">Email</label>
                    <input
                        id="email"
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="password">Password</label>
                    <input
                        id="password"
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>

                <button
                    type="submit"
                    disabled={isSubmitting}
                    className="btn btn-primary"
                >
                    {isSubmitting ? 'Logging in...' : 'Login'}
                </button>
            </form>

            <div className="signup-link">
                Don't have an account? <a href="/register">Sign up</a>
            </div>
        </div>
    );
};

export default LoginForm;
```

### Listing Locations Component (React)

```jsx
import React, {useState, useEffect} from 'react';
import {Link} from 'react-router-dom';
import {apiClient} from '../utils/apiClient';

const LocationsList = () => {
    const [locations, setLocations] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [page, setPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);

    useEffect(() => {
        const fetchLocations = async () => {
            try {
                setLoading(true);
                const data = await apiClient.get(`/locations?skip=${(page - 1) * 10}&limit=10`);
                setLocations(data.items || data);

                if (data.total && data.size) {
                    setTotalPages(Math.ceil(data.total / data.size));
                }
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchLocations();
    }, [page]);

    if (loading) return <div className="loading">Loading locations...</div>;
    if (error) return <div className="error-message">Error: {error}</div>;

    return (
        <div className="locations-list">
            <h2>Explore Destinations</h2>

            <div className="location-grid">
                {locations.map(location => (
                    <div key={location.id} className="location-card">
                        <div className="location-image">
                            {/* Placeholder for location image */}
                            <img src={location.image_url || '/placeholder-location.jpg'} alt={location.name}/>
                        </div>

                        <div className="location-info">
                            <h3>{location.name}</h3>
                            <p className="location-country">{location.country}</p>
                            <p className="location-description">{location.description.substring(0, 100)}...</p>

                            <Link to={`/locations/${location.id}`} className="btn btn-view">
                                View Details
                            </Link>
                        </div>
                    </div>
                ))}
            </div>

            {/* Pagination */}
            <div className="pagination">
                <button
                    onClick={() => setPage(prev => Math.max(prev - 1, 1))}
                    disabled={page === 1}
                >
                    Previous
                </button>

                <span>Page {page} of {totalPages}</span>

                <button
                    onClick={() => setPage(prev => prev + 1)}
                    disabled={page >= totalPages}
                >
                    Next
                </button>
            </div>
        </div>
    );
};

export default LocationsList;
```

### Location Detail Component (React)

```jsx
import React, {useState, useEffect} from 'react';
import {useParams} from 'react-router-dom';
import {apiClient} from '../utils/apiClient';

const LocationDetail = () => {
    const {locationId} = useParams();
    const [location, setLocation] = useState(null);
    const [accommodations, setAccommodations] = useState([]);
    const [foods, setFoods] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchLocationData = async () => {
            try {
                setLoading(true);

                // Fetch location details and related data in parallel
                const [locationData, accommodationsData, foodsData] = await Promise.all([
                    apiClient.get(`/locations/${locationId}`),
                    apiClient.get(`/accommodations/location/${locationId}`),
                    apiClient.get(`/foods/location/${locationId}`)
                ]);

                setLocation(locationData);
                setAccommodations(accommodationsData);
                setFoods(foodsData);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchLocationData();
    }, [locationId]);

    if (loading) return <div className="loading">Loading location details...</div>;
    if (error) return <div className="error-message">Error: {error}</div>;
    if (!location) return <div className="not-found">Location not found</div>;

    return (
        <div className="location-detail">
            <div className="location-header">
                <h1>{location.name}</h1>
                <p className="location-region">{location.country}, {location.region}</p>
            </div>

            <div className="location-body">
                <div className="location-description">
                    <h2>About {location.name}</h2>
                    <p>{location.description}</p>
                </div>

                {/* Map view */}
                <div className="location-map">
                    {/* Integrate with a map library like Google Maps or Leaflet */}
                    <div className="map-container">
                        Map view with coordinates: {location.latitude}, {location.longitude}
                    </div>
                </div>

                {/* Accommodations */}
                <div className="location-accommodations">
                    <h2>Where to Stay</h2>
                    <div className="accommodations-grid">
                        {accommodations.slice(0, 3).map(accommodation => (
                            <div key={accommodation.id} className="accommodation-card">
                                <h3>{accommodation.name}</h3>
                                <p className="price-range">{accommodation.price_range}</p>
                                <p>{accommodation.description.substring(0, 100)}...</p>
                                <p className="rating">Rating: {accommodation.rating}/5</p>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Restaurants */}
                <div className="location-foods">
                    <h2>Where to Eat</h2>
                    <div className="foods-grid">
                        {foods.slice(0, 3).map(food => (
                            <div key={food.id} className="food-card">
                                <h3>{food.name}</h3>
                                <p className="cuisine-type">{food.cuisine_type}</p>
                                <p>{food.description.substring(0, 100)}...</p>
                                <p className="rating">Rating: {food.rating}/5</p>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default LocationDetail;
```

## Websocket Integration (Real-time Features)

If your application supports WebSockets for real-time updates:

```javascript
// WebSocket client for real-time updates
class TravelWebSocketClient {
    constructor(authToken) {
        this.socket = null;
        this.authToken = authToken;
        this.listeners = {};
    }

    connect() {
        this.socket = new WebSocket(`wss://api.williamtravel.com/ws?token=${this.authToken}`);

        this.socket.onopen = () => {
            console.log('WebSocket connection established');
        };

        this.socket.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                const eventType = data.type;

                if (this.listeners[eventType]) {
                    this.listeners[eventType].forEach(callback => callback(data.payload));
                }
            } catch (error) {
                console.error('WebSocket message error:', error);
            }
        };

        this.socket.onerror = (error) => {
            console.error('WebSocket error:', error);
        };

        this.socket.onclose = () => {
            console.log('WebSocket connection closed');

            // Attempt to reconnect after a delay
            setTimeout(() => this.connect(), 5000);
        };
    }

    on(eventType, callback) {
        if (!this.listeners[eventType]) {
            this.listeners[eventType] = [];
        }

        this.listeners[eventType].push(callback);
    }

    off(eventType, callback) {
        if (this.listeners[eventType]) {
            this.listeners[eventType] = this.listeners[eventType]
                .filter(cb => cb !== callback);
        }
    }

    disconnect() {
        if (this.socket) {
            this.socket.close();
        }
    }
}

// Usage example
const token = localStorage.getItem('accessToken');
const wsClient = new TravelWebSocketClient(token);
wsClient.connect();

// Listen for new messages
wsClient.on('new_message', (message) => {
    console.log('New message received:', message);
    // Update UI with new message
});

// Listen for new community posts
wsClient.on('new_community_post', (post) => {
    console.log('New community post:', post);
    // Update community feed
});

// Clean up on component unmount
// wsClient.disconnect();
```

## Performance Optimization

1. **Data Caching**

```javascript
// Simple cache implementation
const cache = {
    data: {},

    get(key) {
        const item = this.data[key];

        // Check if item exists and is not expired
        if (item && item.expiry > Date.now()) {
            return item.value;
        }

        // Remove expired item
        delete this.data[key];
        return null;
    },

    set(key, value, ttlSeconds = 300) {
        this.data[key] = {
            value,
            expiry: Date.now() + (ttlSeconds * 1000)
        };
    },

    invalidate(key) {
        delete this.data[key];
    },

    clear() {
        this.data = {};
    }
};

// Example usage with API client
const cachedApiClient = {
    async get(endpoint, options = {}) {
        const {skipCache = false, cacheTTL = 300} = options;
        const cacheKey = `get:${endpoint}`;

        // Try to get from cache unless skipCache is true
        if (!skipCache) {
            const cachedData = cache.get(cacheKey);
            if (cachedData) {
                return cachedData;
            }
        }

        // If not in cache or skipCache is true, fetch from API
        const data = await apiClient.get(endpoint);

        // Store in cache
        cache.set(cacheKey, data, cacheTTL);

        return data;
    },

    // Cache invalidation when data changes
    invalidateRelated(entity, id = null) {
        if (id) {
            cache.invalidate(`get:/${entity}/${id}`);
        }
        cache.invalidate(`get:/${entity}`);
    }
};

// Usage
const getLocations = async (forceRefresh = false) => {
    return cachedApiClient.get('/locations', {skipCache: forceRefresh});
};
```

2. **Infinite Scrolling Example**

```jsx
import React, {useState, useEffect, useRef} from 'react';
import {apiClient} from '../utils/apiClient';

const InfiniteScroll = ({endpoint, renderItem}) => {
    const [items, setItems] = useState([]);
    const [loading, setLoading] = useState(false);
    const [hasMore, setHasMore] = useState(true);
    const [page, setPage] = useState(1);
    const observer = useRef();
    const limit = 10;

    // Setup intersection observer to detect when user scrolls to bottom
    const lastItemRef = useRef();

    useEffect(() => {
        observer.current = new IntersectionObserver(entries => {
            if (entries[0].isIntersecting && hasMore && !loading) {
                setPage(prev => prev + 1);
            }
        });

        if (lastItemRef.current) {
            observer.current.observe(lastItemRef.current);
        }

        return () => {
            if (observer.current) {
                observer.current.disconnect();
            }
        };
    }, [hasMore, loading]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                const skip = (page - 1) * limit;
                const data = await apiClient.get(`${endpoint}?skip=${skip}&limit=${limit}`);

                if (page === 1) {
                    setItems(data.items || data);
                } else {
                    setItems(prev => [...prev, ...(data.items || data)]);
                }

                // Check if there are more items to load
                if (data.items && data.items.length < limit) {
                    setHasMore(false);
                }
            } catch (error) {
                console.error('Failed to fetch data:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [endpoint, page]);

    return (
        <div className="infinite-scroll-container">
            <div className="items-list">
                {items.map((item, index) => (
                    <div
                        key={item.id}
                        ref={index === items.length - 1 ? lastItemRef : null}
                    >
                        {renderItem(item)}
                    </div>
                ))}
            </div>

            {loading && <div className="loading-indicator">Loading...</div>}
            {!hasMore && <div className="end-message">No more items to load</div>}
        </div>
    );
};

// Usage
const ArticlesList = () => {
    const renderArticle = (article) => (
        <div className="article-card">
            <h3>{article.title}</h3>
            <p>{article.content.substring(0, 200)}...</p>
            <a href={`/articles/${article.id}`}>Read more</a>
        </div>
    );

    return <InfiniteScroll endpoint="/articles" renderItem={renderArticle}/>;
};
```

## Best Practices for Frontend Integration

1. **Centralize API Calls**
    - Use a centralized API client module for all requests
    - Implement consistent error handling and retrying

2. **Handle Authentication Properly**
    - Store tokens securely (preferably in memory or httpOnly cookies)
    - Implement automatic token refresh
    - Clear tokens and redirect on authentication errors

3. **Implement Loading States**
    - Show appropriate loading indicators during API calls
    - Implement skeleton screens for better UX

4. **Error Handling**
    - Display user-friendly error messages
    - Provide appropriate actions for error recovery

5. **Performance Considerations**
    - Implement efficient caching strategies
    - Use pagination or infinite scrolling for large data sets
    - Consider implementing data prefetching for critical views

6. **Security**
    - Never store sensitive data in localStorage
    - Sanitize all user-generated content before rendering
    - Implement CSRF protection if using cookie-based authentication

## Support

For API integration assistance, contact:

- Email: frontend-support@williamtravel.com
- Developer Slack Channel: #frontend-api-help

## Changelog

### API v1.0.0 (May 2025)

- Initial API release supporting all core travel features
