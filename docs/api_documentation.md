# Travel Application API Documentation

This document provides a comprehensive overview of the William Travel application API endpoints, including request
parameters and response models.

## Table of Contents

1. [Authentication](#authentication)
2. [Users](#users)
3. [Roles](#roles)
4. [Permissions](#permissions)
5. [Locations](#locations)
    - [Continents](#continents)
    - [Countries](#countries)
    - [Regions](#regions)
    - [Districts](#districts)
    - [Wards](#wards)
    - [Location Categories](#location-categories)
6. [Accommodations](#accommodations)
7. [Foods](#foods)
8. [Media](#media)
9. [Articles](#articles)
10. [Events](#events)
11. [Community Posts](#community-posts)
12. [Ratings](#ratings)

---

## Authentication

Authentication endpoints for user login and token management.

### Login

Authenticate a user and get an access token.

**Endpoint:** `POST /api/v1/auth/login`

**Request Body:**

```json
{
  "username": "user@example.com",
  // Email is used as username
  "password": "yourpassword"
}
```

**Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Status Codes:**

- 200: Success
- 401: Authentication failed (Incorrect email or password)
- 400: Inactive user

### Request Password Reset

Request a password reset token to be sent to the user's email.

**Endpoint:** `POST /api/v1/auth/password-reset`

**Request Body:**

```json
{
  "email": "user@example.com"
}
```

**Response:**

```json
{
  "message": "If a user with this email exists, a password reset link has been sent."
}
```

**Status Codes:**

- 200: Success (even if email doesn't exist, for security reasons)

### Reset Password

Reset password using the token received via email.

**Endpoint:** `POST /api/v1/auth/password-reset/confirm`

**Request Body:**

```json
{
  "token": "reset-token-from-email",
  "password": "new-password"
}
```

**Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Status Codes:**

- 200: Success
- 400: Invalid or expired token

---

## Users

User management endpoints.

### Get Current User

Get the profile of the currently authenticated user.

**Endpoint:** `GET /api/v1/users/me`

**Headers:**

- Authorization: Bearer {access_token}

**Response:**

```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "role": "user",
  "is_superuser": false,
  "created_at": "2025-05-18T15:30:45",
  "updated_at": "2025-05-18T15:30:45"
}
```

### Update Current User

Update the profile of the currently authenticated user.

**Endpoint:** `PUT /api/v1/users/me`

**Headers:**

- Authorization: Bearer {access_token}

**Request Body:**

```json
{
  "email": "newemail@example.com",
  // Optional
  "full_name": "New Name",
  // Optional
  "is_active": true
  // Optional
}
```

**Response:** Updated user object (same format as GET response)

### Update Password

Change the password of the currently authenticated user.

**Endpoint:** `PUT /api/v1/users/me/password`

**Headers:**

- Authorization: Bearer {access_token}

**Request Body:**

```json
{
  "current_password": "currentpassword",
  "new_password": "newpassword"
}
```

**Response:** User object (same format as GET response)

**Status Codes:**

- 200: Success
- 400: Current password is incorrect

### Get User by ID

Get a specific user by ID.

**Endpoint:** `GET /api/v1/users/{user_id}`

**Headers:**

- Authorization: Bearer {access_token}

**Response:** User object (same format as GET /api/v1/users/me response)

**Status Codes:**

- 200: Success
- 404: User not found

### List All Users

Get a list of all users (superuser only).

**Endpoint:** `GET /api/v1/users/`

**Headers:**

- Authorization: Bearer {access_token}

**Query Parameters:**

- skip: int (default: 0)
- limit: int (default: 100)

**Response:**

```json
[
  {
    "id": 1,
    "email": "admin@example.com",
    "full_name": "Admin User",
    "is_active": true,
    "role": "admin",
    "is_superuser": true,
    "created_at": "2025-05-18T15:30:45",
    "updated_at": "2025-05-18T15:30:45"
  },
  {
    "id": 2,
    "email": "user@example.com",
    "full_name": "Regular User",
    "is_active": true,
    "role": "user",
    "is_superuser": false,
    "created_at": "2025-05-18T15:30:45",
    "updated_at": "2025-05-18T15:30:45"
  }
]
```

### Create User

Create a new user (superuser only).

**Endpoint:** `POST /api/v1/users/`

**Headers:**

- Authorization: Bearer {access_token}

**Request Body:**

```json
{
  "email": "newuser@example.com",
  "password": "securepassword",
  "full_name": "New User",
  "role": "user",
  "is_superuser": false,
  "is_active": true
}
```

**Response:** Created user object (same format as in List All Users)

---

## Roles

Role management endpoints for access control.

### List Roles

Get list of all roles with their permissions.

**Endpoint:** `GET /api/v1/roles/`

**Headers:**

- Authorization: Bearer {access_token}

**Query Parameters:**

- skip: int (default: 0)
- limit: int (default: 100)

**Response:**

```json
[
  {
    "id": 1,
    "name": "Admin",
    "description": "Administrator with full access",
    "is_default": false,
    "permissions": [
      {
        "id": 1,
        "name": "Create User",
        "code": "user:create",
        "description": "Can create new users"
      },
      {
        "id": 2,
        "name": "Delete User",
        "code": "user:delete",
        "description": "Can delete users"
      }
    ],
    "created_at": "2025-05-18T15:30:45",
    "updated_at": "2025-05-18T15:30:45"
  },
  {
    "id": 2,
    "name": "User",
    "description": "Standard user",
    "is_default": true,
    "permissions": [
      {
        "id": 3,
        "name": "Create Post",
        "code": "post:create",
        "description": "Can create posts"
      }
    ],
    "created_at": "2025-05-18T15:30:45",
    "updated_at": "2025-05-18T15:30:45"
  }
]
```

### Get Role

Get a specific role by ID.

**Endpoint:** `GET /api/v1/roles/{role_id}`

**Headers:**

- Authorization: Bearer {access_token}

**Response:** Same as a single role object from the list endpoint

**Status Codes:**

- 200: Success
- 404: Role not found

### Create Role

Create a new role with permissions.

**Endpoint:** `POST /api/v1/roles/`

**Headers:**

- Authorization: Bearer {access_token}

**Request Body:**

```json
{
  "name": "Content Manager",
  "description": "Manages content across the platform",
  "is_default": false,
  "permission_ids": [
    3,
    4,
    5
  ]
}
```

**Response:** Created role object with permissions

**Status Codes:**

- 201: Created
- 400: Bad request (e.g., role name already exists)
- 403: Forbidden (not authorized)

### Update Role

Update an existing role.

**Endpoint:** `PUT /api/v1/roles/{role_id}`

**Headers:**

- Authorization: Bearer {access_token}

**Request Body:**

```json
{
  "name": "Updated Role Name",
  // Optional
  "description": "Updated role description",
  // Optional
  "is_default": false,
  // Optional
  "permission_ids": [
    1,
    2,
    3,
    4
  ]
  // Optional - replaces existing permissions
}
```

**Response:** Updated role object with permissions

**Status Codes:**

- 200: Success
- 404: Role not found
- 400: Bad request (e.g., role name already exists)
- 403: Forbidden (not authorized)

### Delete Role

Delete a role if it's not assigned to any users.

**Endpoint:** `DELETE /api/v1/roles/{role_id}`

**Headers:**

- Authorization: Bearer {access_token}

**Status Codes:**

- 200: Success
- 400: Bad Request (role is assigned to users)
- 404: Role not found
- 403: Forbidden (not authorized)

---

## Permissions

Permission management endpoints for access control.

### List Permissions

Get list of all permissions.

**Endpoint:** `GET /api/v1/permissions/`

**Headers:**

- Authorization: Bearer {access_token}

**Query Parameters:**

- skip: int (default: 0)
- limit: int (default: 100)

**Response:**

```json
[
  {
    "id": 1,
    "name": "Create User",
    "code": "user:create",
    "description": "Can create new users",
    "created_at": "2025-05-18T15:30:45",
    "updated_at": "2025-05-18T15:30:45"
  },
  {
    "id": 2,
    "name": "Delete User",
    "code": "user:delete",
    "description": "Can delete users",
    "created_at": "2025-05-18T15:30:45",
    "updated_at": "2025-05-18T15:30:45"
  }
]
```

### Get Permission

Get a specific permission by ID.

**Endpoint:** `GET /api/v1/permissions/{permission_id}`

**Headers:**

- Authorization: Bearer {access_token}

**Response:** Same as a single permission object from the list endpoint

**Status Codes:**

- 200: Success
- 404: Permission not found

### Create Permission

Create a new permission.

**Endpoint:** `POST /api/v1/permissions/`

**Headers:**

- Authorization: Bearer {access_token}

**Request Body:**

```json
{
  "name": "Manage Articles",
  "code": "article:manage",
  "description": "Can manage all articles"
}
```

**Response:** Created permission object

**Status Codes:**

- 201: Created
- 400: Bad request (e.g., permission code already exists)
- 403: Forbidden (not authorized)

### Update Permission

Update an existing permission.

**Endpoint:** `PUT /api/v1/permissions/{permission_id}`

**Headers:**

- Authorization: Bearer {access_token}

**Request Body:**

```json
{
  "name": "Updated Permission Name",
  // Optional
  "code": "updated:code",
  // Optional
  "description": "Updated description"
  // Optional
}
```

**Response:** Updated permission object

**Status Codes:**

- 200: Success
- 404: Permission not found
- 400: Bad request (e.g., permission code already exists)
- 403: Forbidden (not authorized)

### Delete Permission

Delete a permission.

**Endpoint:** `DELETE /api/v1/permissions/{permission_id}`

**Headers:**

- Authorization: Bearer {access_token}

**Status Codes:**

- 200: Success
- 404: Permission not found
- 403: Forbidden (not authorized)

---

## Locations

Endpoints for managing geographic location data.

### Continents

#### List Continents

Get list of all continents.

**Endpoint:** `GET /api/v1/locations/continents/`

**Query Parameters:**

- skip: int (default: 0)
- limit: int (default: 100)

**Response:**

```json
[
  {
    "id": 1,
    "name": "Asia",
    "code": "AS",
    "name_code": "asia",
    "background_image": "https://example.com/asia.jpg",
    "logo": "https://example.com/asia-logo.png",
    "description": "Largest and most populous continent",
    "description_code": "asia_desc",
    "status": 1,
    "created_at": "2025-05-01T00:00:00",
    "updated_at": "2025-05-01T00:00:00"
  }
]
```

#### Get Continent

Get a specific continent by ID.

**Endpoint:** `GET /api/v1/locations/continents/{continent_id}`

**Response:** Same as a single continent object from the list endpoint

**Status Codes:**

- 200: Success
- 404: Continent not found

#### Create Continent

Create a new continent (superuser only).

**Endpoint:** `POST /api/v1/locations/continents/`

**Headers:**

- Authorization: Bearer {access_token}

**Request Body:**

```json
{
  "name": "North America",
  "code": "NA",
  "name_code": "north_america",
  "background_image": "https://example.com/na.jpg",
  "logo": "https://example.com/na-logo.png",
  "description": "North America continent description",
  "description_code": "na_desc",
  "status": 1
}
```

**Response:** Created continent object

#### Update Continent

Update an existing continent (superuser only).

**Endpoint:** `PUT /api/v1/locations/continents/{continent_id}`

**Headers:**

- Authorization: Bearer {access_token}

**Request Body:**

```json
{
  "name": "Updated Continent Name",
  // Optional
  "code": "UC",
  // Optional
  "name_code": "updated_continent",
  // Optional
  "background_image": "https://example.com/updated-continent.jpg",
  // Optional
  "logo": "https://example.com/updated-logo.png",
  // Optional
  "description": "Updated description",
  // Optional
  "description_code": "updated_desc",
  // Optional
  "status": 1
  // Optional
}
```

**Response:** Updated continent object

**Status Codes:**

- 200: Success
- 404: Continent not found

### Countries

#### Update Country

Update an existing country (superuser only).

**Endpoint:** `PUT /api/v1/locations/countries/{country_id}`

**Headers:**

- Authorization: Bearer {access_token}

**Request Body:**

```json
{
  "name": "Updated Country Name",
  // Optional
  "code": "UC",
  // Optional
  "name_code": "updated_country",
  // Optional
  "description": "Updated description",
  // Optional
  "description_code": "updated_country_desc",
  // Optional
  "background_image": "https://example.com/updated-country.jpg",
  // Optional
  "logo": "https://example.com/updated-country-logo.png",
  // Optional
  "status": 1,
  // Optional
  "continent_id": 1
  // Optional
}
```

**Response:** Updated country object

**Status Codes:**

- 200: Success
- 404: Country not found

### Regions

#### Update Region

Update an existing region (superuser only).

**Endpoint:** `PUT /api/v1/locations/regions/{region_id}`

**Headers:**

- Authorization: Bearer {access_token}

**Request Body:**

```json
{
  "name": "Updated Region Name",
  // Optional
  "code": "UR",
  // Optional
  "name_code": "updated_region",
  // Optional
  "description": "Updated region description",
  // Optional
  "description_code": "updated_region_desc",
  // Optional
  "background_image": "https://example.com/updated-region.jpg",
  // Optional
  "logo": "https://example.com/updated-region-logo.png",
  // Optional
  "status": 1,
  // Optional
  "country_id": 1
  // Optional
}
```

**Response:** Updated region object

**Status Codes:**

- 200: Success
- 404: Region not found

### Districts

#### List Districts

Get list of all districts.

**Endpoint:** `GET /api/v1/locations/districts/`

**Query Parameters:**

- skip: int (default: 0)
- limit: int (default: 100)
- region_id: int (optional)

**Response:**

```json
[
  {
    "id": 1,
    "name": "Ba Dinh",
    "code": "BD",
    "name_code": "ba_dinh",
    "description": "Historical district in Hanoi",
    "description_code": "ba_dinh_desc",
    "status": 1,
    "region_id": 1,
    "created_at": "2025-05-01T00:00:00",
    "updated_at": "2025-05-01T00:00:00"
  }
]
```

#### Get District

Get a specific district by ID.

**Endpoint:** `GET /api/v1/locations/districts/{district_id}`

**Response:** Same as a single district object from the list endpoint

**Status Codes:**

- 200: Success
- 404: District not found

### Wards

#### List Wards

Get list of all wards.

**Endpoint:** `GET /api/v1/locations/wards/`

**Query Parameters:**

- skip: int (default: 0)
- limit: int (default: 100)
- district_id: int (optional)

**Response:**

```json
[
  {
    "id": 1,
    "name": "Phuc Xa",
    "code": "PX",
    "name_code": "phuc_xa",
    "status": 1,
    "district_id": 1,
    "created_at": "2025-05-01T00:00:00",
    "updated_at": "2025-05-01T00:00:00"
  }
]
```

#### Get Ward

Get a specific ward by ID.

**Endpoint:** `GET /api/v1/locations/wards/{ward_id}`

**Response:** Same as a single ward object from the list endpoint

**Status Codes:**

- 200: Success
- 404: Ward not found

### Location Categories

#### List Location Categories

Get list of all location categories.

**Endpoint:** `GET /api/v1/locations/location-categories/`

**Response:**

```json
[
  {
    "id": 1,
    "name": "Tourist Attraction",
    "code": "attraction",
    "status": 1,
    "created_at": "2025-05-01T00:00:00",
    "updated_at": "2025-05-01T00:00:00"
  },
  {
    "id": 2,
    "name": "Beach",
    "code": "beach",
    "status": 1,
    "created_at": "2025-05-01T00:00:00",
    "updated_at": "2025-05-01T00:00:00"
  }
]
```

#### Get Location Category

Get a specific location category by ID.

**Endpoint:** `GET /api/v1/locations/location-categories/{category_id}`

**Response:** Same as a single location category object from the list endpoint

**Status Codes:**

- 200: Success
- 404: Location category not found

---

## Accommodations

Endpoints for managing accommodation information.

### Accommodation Categories

#### List Accommodation Categories

Get list of all accommodation categories.

**Endpoint:** `GET /api/v1/accommodations/categories/`

**Response:**

```json
[
  {
    "id": 1,
    "name": "Hotel",
    "description": "Professional accommodation with various amenities",
    "status": 1,
    "created_at": "2025-05-01T00:00:00",
    "updated_at": "2025-05-01T00:00:00"
  },
  {
    "id": 2,
    "name": "Homestay",
    "description": "Stay with locals in their homes",
    "status": 1,
    "created_at": "2025-05-01T00:00:00",
    "updated_at": "2025-05-01T00:00:00"
  }
]
```

#### Get Accommodation Category

Get a specific accommodation category by ID.

**Endpoint:** `GET /api/v1/accommodations/categories/{category_id}`

**Response:** Same as a single category object from the list endpoint

**Status Codes:**

- 200: Success
- 404: Category not found

#### Create Accommodation Category

Create a new accommodation category (superuser only).

**Endpoint:** `POST /api/v1/accommodations/categories/`

**Headers:**

- Authorization: Bearer {access_token}

**Request Body:**

```json
{
  "name": "Resort",
  "description": "Luxury accommodation with full recreational amenities",
  "status": 1
}
```

**Response:** Created accommodation category object

#### Update Accommodation Category

Update an existing accommodation category (superuser only).

**Endpoint:** `PUT /api/v1/accommodations/categories/{category_id}`

**Headers:**

- Authorization: Bearer {access_token}

**Request Body:**

```json
{
  "name": "Updated Category Name",
  // Optional
  "description": "Updated description",
  // Optional
  "status": 1
  // Optional
}
```

**Response:** Updated category object

**Status Codes:**

- 200: Success
- 404: Category not found

### List Accommodations

Get list of accommodations with pagination.

**Endpoint:** `GET /api/v1/accommodations/`

**Query Parameters:**

- page: int (default: 1)
- limit: int (default: 10, max: 100)
- search: string (optional)
- category_id: int (optional)
- country_id: int (optional)
- region_id: int (optional)
- district_id: int (optional)
- min_price: float (optional)
- max_price: float (optional)

**Response:**

```json
{
  "items": [
    {
      "id": 1,
      "name": "Luxury Hotel & Spa",
      "description": "5-star luxury accommodation",
      "address": "123 Example Street",
      "category_id": 1,
      "price_range": "200-500",
      "rating": 4.8,
      "facilities": [
        "pool",
        "spa",
        "gym"
      ],
      "contacts": {
        "phone": "+84123456789",
        "email": "info@luxuryhotel.com",
        "website": "https://luxuryhotel.com"
      },
      "location": {
        "latitude": 21.0285,
        "longitude": 105.8542
      },
      "region_id": 1,
      "images": [
        "https://example.com/luxuryhotel1.jpg",
        "https://example.com/luxuryhotel2.jpg"
      ],
      "created_at": "2025-05-01T00:00:00",
      "updated_at": "2025-05-01T00:00:00"
    }
  ],
  "total": 50,
  "page": 1,
  "size": 10,
  "pages": 5
}
```

### Get Accommodation

Get a specific accommodation by ID.

**Endpoint:** `GET /api/v1/accommodations/{accommodation_id}`

**Response:** Same as a single accommodation object from the items array in the list endpoint

**Status Codes:**

- 200: Success
- 404: Accommodation not found

### Create Accommodation

Create a new accommodation.

**Endpoint:** `POST /api/v1/accommodations/`

**Headers:**

- Authorization: Bearer {access_token}

**Request Body:**

```json
{
  "name": "Beachside Resort",
  "description": "Beautiful resort by the beach",
  "address": "456 Beach Road",
  "category_id": 3,
  "price_range": "300-700",
  "facilities": [
    "beach_access",
    "pool",
    "restaurant"
  ],
  "contacts": {
    "phone": "+84987654321",
    "email": "info@beachresort.com",
    "website": "https://beachresort.com"
  },
  "location": {
    "latitude": 10.7456,
    "longitude": 106.7631
  },
  "region_id": 2
}
```

**Response:** Created accommodation object

### Update Accommodation

Update an existing accommodation.

**Endpoint:** `PUT /api/v1/accommodations/{accommodation_id}`

**Headers:**

- Authorization: Bearer {access_token}

**Request Body:**

```json
{
  "name": "Updated Resort Name",
  // Optional
  "description": "Updated description",
  // Optional
  "address": "Updated address",
  // Optional
  "category_id": 2,
  // Optional
  "price_range": "400-800",
  // Optional
  "facilities": [
    "updated",
    "facilities",
    "list"
  ],
  // Optional
  "contacts": {
    // Optional
    "phone": "+84111222333",
    "email": "updated@example.com",
    "website": "https://updated-example.com"
  },
  "location": {
    // Optional
    "latitude": 10.7789,
    "longitude": 106.7012
  },
  "region_id": 3
  // Optional
}
```

**Response:** Updated accommodation object

**Status Codes:**

- 200: Success
- 404: Accommodation not found
- 403: Forbidden (not the owner or superuser)

### Delete Accommodation

Delete an accommodation.

**Endpoint:** `DELETE /api/v1/accommodations/{accommodation_id}`

**Headers:**

- Authorization: Bearer {access_token}

**Status Codes:**

- 200: Success
- 404: Accommodation not found
- 403: Forbidden (not the owner or superuser)

---

## Foods

Endpoints for managing food-related information.

### Food Categories

#### List Food Categories

Get list of all food categories.

**Endpoint:** `GET /api/v1/foods/categories/`

**Response:**

```json
[
  {
    "id": 1,
    "name": "Restaurant",
    "description": "Full service dining establishment",
    "status": 1,
    "created_at": "2025-05-01T00:00:00",
    "updated_at": "2025-05-01T00:00:00"
  },
  {
    "id": 2,
    "name": "Street Food",
    "description": "Local food served from vendors on the street",
    "status": 1,
    "created_at": "2025-05-01T00:00:00",
    "updated_at": "2025-05-01T00:00:00"
  }
]
```

#### Get Food Category

Get a specific food category by ID.

**Endpoint:** `GET /api/v1/foods/categories/{category_id}`

**Response:** Same as a single category object from the list endpoint

**Status Codes:**

- 200: Success
- 404: Category not found

#### Create Food Category

Create a new food category (superuser only).

**Endpoint:** `POST /api/v1/foods/categories/`

**Headers:**

- Authorization: Bearer {access_token}

**Request Body:**

```json
{
  "name": "Café",
  "description": "Coffee shop with light food options",
  "status": 1
}
```

**Response:** Created food category object

#### Update Food Category

Update an existing food category (superuser only).

**Endpoint:** `PUT /api/v1/foods/categories/{category_id}`

**Headers:**

- Authorization: Bearer {access_token}

**Request Body:**

```json
{
  "name": "Updated Category Name",
  // Optional
  "description": "Updated description",
  // Optional
  "status": 1
  // Optional
}
```

**Response:** Updated category object

**Status Codes:**

- 200: Success
- 404: Category not found

### List Foods

Get list of foods with pagination.

**Endpoint:** `GET /api/v1/foods/`

**Query Parameters:**

- page: int (default: 1)
- limit: int (default: 10, max: 100)
- search: string (optional)
- category_id: int (optional)
- country_id: int (optional)
- region_id: int (optional)
- district_id: int (optional)
- min_price: float (optional)
- max_price: float (optional)

**Response:**

```json
{
  "items": [
    {
      "id": 1,
      "name": "Pho Restaurant",
      "description": "Traditional Vietnamese pho restaurant",
      "address": "789 Food Street",
      "category_id": 1,
      "cuisine": "vietnamese",
      "price_range": "$",
      "signature_dishes": [
        "Pho Bo",
        "Bun Cha"
      ],
      "operating_hours": "7:00 AM - 10:00 PM",
      "contacts": {
        "phone": "+84123456789",
        "email": "info@phorestaurant.com"
      },
      "location": {
        "latitude": 21.0277,
        "longitude": 105.8341
      },
      "region_id": 1,
      "images": [
        "https://example.com/pho1.jpg",
        "https://example.com/pho2.jpg"
      ],
      "rating": 4.7,
      "created_at": "2025-05-01T00:00:00",
      "updated_at": "2025-05-01T00:00:00"
    }
  ],
  "total": 42,
  "page": 1,
  "size": 10,
  "pages": 5
}
```

### Get Food

Get a specific food by ID.

**Endpoint:** `GET /api/v1/foods/{food_id}`

**Response:** Same as a single food object from the items array in the list endpoint

**Status Codes:**

- 200: Success
- 404: Food not found

### Create Food

Create a new food/restaurant entry (admin or moderator only).

**Endpoint:** `POST /api/v1/foods/`

**Headers:**

- Authorization: Bearer {access_token}

**Request Body:**

```json
{
  "name": "Seafood Restaurant",
  "description": "Fresh seafood directly from the ocean",
  "address": "101 Ocean Drive",
  "category_id": 1,
  "cuisine": "seafood",
  "price_range": "$$",
  "signature_dishes": [
    "Grilled Lobster",
    "Seafood Hotpot"
  ],
  "operating_hours": "11:00 AM - 11:00 PM",
  "contacts": {
    "phone": "+84987654321",
    "email": "info@seafoodrestaurant.com"
  },
  "location": {
    "latitude": 10.7789,
    "longitude": 106.7012
  },
  "region_id": 2
}
```

**Response:** Created food object

### Update Food

Update an existing food/restaurant entry (admin or content manager only).

**Endpoint:** `PUT /api/v1/foods/{food_id}`

**Headers:**

- Authorization: Bearer {access_token}

**Request Body:**

```json
{
  "name": "Updated Restaurant Name",
  // Optional
  "description": "Updated description",
  // Optional
  "address": "Updated address",
  // Optional
  "category_id": 2,
  // Optional
  "cuisine": "updated_cuisine",
  // Optional
  "price_range": "$$$",
  // Optional
  "signature_dishes": [
    "Updated",
    "Signature",
    "Dishes"
  ],
  // Optional
  "operating_hours": "10:00 AM - 11:00 PM",
  // Optional
  "contacts": {
    // Optional
    "phone": "+84111222333",
    "email": "updated@example.com"
  },
  "location": {
    // Optional
    "latitude": 10.7789,
    "longitude": 106.7012
  },
  "region_id": 3
  // Optional
}
```

**Response:** Updated food object

**Status Codes:**

- 200: Success
- 404: Food not found
- 403: Forbidden (not authorized)

### Delete Food

Delete a food/restaurant entry (admin or content manager only).

**Endpoint:** `DELETE /api/v1/foods/{food_id}`

**Headers:**

- Authorization: Bearer {access_token}

**Status Codes:**

- 200: Success
- 404: Food not found
- 403: Forbidden (not authorized)

---

## Media

Endpoints for managing media files.

### Media Types

#### List Media Types

Get list of all media types.

**Endpoint:** `GET /api/v1/media/types/`

**Response:**

```json
[
  {
    "id": 1,
    "name": "Image",
    "code": "image",
    "status": 1,
    "created_at": "2025-05-01T00:00:00",
    "updated_at": "2025-05-01T00:00:00"
  },
  {
    "id": 2,
    "name": "Video",
    "code": "video",
    "status": 1,
    "created_at": "2025-05-01T00:00:00",
    "updated_at": "2025-05-01T00:00:00"
  }
]
```

#### Get Media Type

Get a specific media type by ID.

**Endpoint:** `GET /api/v1/media/types/{type_id}`

**Response:** Same as a single media type object from the list endpoint

**Status Codes:**

- 200: Success
- 404: Media type not found

#### Create Media Type

Create a new media type (superuser only).

**Endpoint:** `POST /api/v1/media/types/`

**Headers:**

- Authorization: Bearer {access_token}

**Request Body:**

```json
{
  "name": "Document",
  "code": "document",
  "status": 1
}
```

**Response:** Created media type object

### Media Categories

#### List Media Categories

Get list of all media categories.

**Endpoint:** `GET /api/v1/media/categories/`

**Response:**

```json
[
  {
    "id": 1,
    "name": "Accommodation Photos",
    "code": "accommodation_photos",
    "status": 1,
    "created_at": "2025-05-01T00:00:00",
    "updated_at": "2025-05-01T00:00:00"
  },
  {
    "id": 2,
    "name": "Food Photos",
    "code": "food_photos",
    "status": 1,
    "created_at": "2025-05-01T00:00:00",
    "updated_at": "2025-05-01T00:00:00"
  }
]
```

#### Get Media Category

Get a specific media category by ID.

**Endpoint:** `GET /api/v1/media/categories/{category_id}`

**Response:** Same as a single media category object from the list endpoint

**Status Codes:**

- 200: Success
- 404: Media category not found

#### Create Media Category

Create a new media category (superuser only).

**Endpoint:** `POST /api/v1/media/categories/`

**Headers:**

- Authorization: Bearer {access_token}

**Request Body:**

```json
{
  "name": "Attraction Videos",
  "code": "attraction_videos",
  "status": 1
}
```

**Response:** Created media category object

### List Media Files

Get list of media files.

**Endpoint:** `GET /api/v1/media/`

**Query Parameters:**

- skip: int (default: 0)
- limit: int (default: 20)
- type_id: int (optional)
- category_id: int (optional)
- entity_type: string (optional) - e.g., "accommodation", "food", "article"
- entity_id: int (optional)

**Response:**

```json
[
  {
    "id": 1,
    "file_name": "hotel_facade.jpg",
    "file_path": "/media/images/accommodations/hotel_facade.jpg",
    "file_url": "https://example.com/media/images/accommodations/hotel_facade.jpg",
    "mime_type": "image/jpeg",
    "file_size": 1024568,
    "type_id": 1,
    "category_id": 1,
    "entity_type": "accommodation",
    "entity_id": 5,
    "created_at": "2025-05-20T15:30:45",
    "updated_at": "2025-05-20T15:30:45"
  }
]
```

### Get Media File

Get a specific media file by ID.

**Endpoint:** `GET /api/v1/media/{media_id}`

**Response:** Same as a single media object from the list endpoint

**Status Codes:**

- 200: Success
- 404: Media not found

### Upload Media File

Upload a new media file.

**Endpoint:** `POST /api/v1/media/`

**Headers:**

- Authorization: Bearer {access_token}
- Content-Type: multipart/form-data

**Form Data:**

- file: binary data (the actual file)
- type_id: int (ID of the media type)
- category_id: int (ID of the media category)
- entity_type: string (optional) - e.g., "accommodation", "food", "article"
- entity_id: int (optional)
- title: string (optional)
- description: string (optional)

**Response:** Created media object

**Status Codes:**

- 201: Created
- 400: Bad request (invalid file type, etc.)
- 401: Unauthorized

### Delete Media File

Delete a specific media file.

**Endpoint:** `DELETE /api/v1/media/{media_id}`

**Headers:**

- Authorization: Bearer {access_token}

**Status Codes:**

- 204: No content (successful deletion)
- 404: Media not found
- 403: Forbidden (not authorized)

---

## Articles

Endpoints for managing articles.

### Article Categories

#### List Article Categories

Get list of all article categories.

**Endpoint:** `GET /api/v1/articles/categories/`

**Response:**

```json
[
  {
    "id": 1,
    "name": "Travel Guide",
    "description": "Comprehensive travel guides for destinations",
    "status": 1,
    "created_at": "2025-05-01T00:00:00",
    "updated_at": "2025-05-01T00:00:00"
  },
  {
    "id": 2,
    "name": "Travel Tips",
    "description": "Useful tips and tricks for travelers",
    "status": 1,
    "created_at": "2025-05-01T00:00:00",
    "updated_at": "2025-05-01T00:00:00"
  }
]
```

#### Get Article Category

Get a specific article category by ID.

**Endpoint:** `GET /api/v1/articles/categories/{category_id}`

**Response:** Same as a single category object from the list endpoint

**Status Codes:**

- 200: Success
- 404: Category not found

#### Create Article Category

Create a new article category (admin or content manager only).

**Endpoint:** `POST /api/v1/articles/categories/`

**Headers:**

- Authorization: Bearer {access_token}

**Request Body:**

```json
{
  "name": "Food Reviews",
  "description": "Reviews of local cuisine and restaurants",
  "status": 1
}
```

**Response:** Created article category object

### Article Tags

#### List Article Tags

Get list of all article tags.

**Endpoint:** `GET /api/v1/articles/tags/`

**Response:**

```json
[
  {
    "id": 1,
    "name": "Vietnam",
    "status": 1,
    "created_at": "2025-05-01T00:00:00",
    "updated_at": "2025-05-01T00:00:00"
  },
  {
    "id": 2,
    "name": "Budget Travel",
    "status": 1,
    "created_at": "2025-05-01T00:00:00",
    "updated_at": "2025-05-01T00:00:00"
  }
]
```

#### Get Article Tag

Get a specific article tag by ID.

**Endpoint:** `GET /api/v1/articles/tags/{tag_id}`

**Response:** Same as a single tag object from the list endpoint

**Status Codes:**

- 200: Success
- 404: Tag not found

#### Create Article Tag

Create a new article tag (admin or content manager only).

**Endpoint:** `POST /api/v1/articles/tags/`

**Headers:**

- Authorization: Bearer {access_token}

**Request Body:**

```json
{
  "name": "Adventure",
  "status": 1
}
```

**Response:** Created article tag object

### List Articles

Get list of articles with pagination.

**Endpoint:** `GET /api/v1/articles/`

**Query Parameters:**

- page: int (default: 1)
- limit: int (default: 10, max: 50)
- search: string (optional)
- category_id: int (optional)
- tag_id: int (optional)
- author_id: int (optional)
- published: bool (optional)

**Response:**

```json
{
  "items": [
    {
      "id": 1,
      "title": "Top 10 Things to Do in Hanoi",
      "slug": "top-10-things-to-do-in-hanoi",
      "summary": "A quick guide to the best attractions in Hanoi",
      "content": "Full article content with markdown formatting...",
      "category_id": 1,
      "tags": [
        {
          "id": 1,
          "name": "Vietnam"
        },
        {
          "id": 3,
          "name": "City Guide"
        }
      ],
      "author": {
        "id": 2,
        "full_name": "Travel Writer"
      },
      "cover_image": "https://example.com/hanoi-guide.jpg",
      "reading_time": 5,
      "related_locations": [
        {
          "id": 1,
          "name": "Hanoi"
        }
      ],
      "published": true,
      "published_at": "2025-05-15T10:30:00",
      "created_at": "2025-05-14T15:30:45",
      "updated_at": "2025-05-15T10:30:00"
    }
  ],
  "total": 42,
  "page": 1,
  "size": 10,
  "pages": 5
}
```

### Get Article

Get a specific article by ID or slug.

**Endpoint:** `GET /api/v1/articles/{article_id}` or `GET /api/v1/articles/slug/{slug}`

**Response:** Same as a single article object from the items array in the list endpoint

**Status Codes:**

- 200: Success
- 404: Article not found

### Create Article

Create a new article (requires authentication).

**Endpoint:** `POST /api/v1/articles/`

**Headers:**

- Authorization: Bearer {access_token}

**Request Body:**

```json
{
  "title": "Travel Guide to Ho Chi Minh City",
  "summary": "Everything you need to know before visiting HCMC",
  "content": "Full article content with markdown formatting...",
  "category_id": 1,
  "tag_ids": [
    1,
    4,
    6
  ],
  "cover_image": "https://example.com/hcmc-guide.jpg",
  "related_location_ids": [
    2
  ],
  "published": false
}
```

**Response:** Created article object

### Update Article

Update an existing article (only author, editor or admin).

**Endpoint:** `PUT /api/v1/articles/{article_id}`

**Headers:**

- Authorization: Bearer {access_token}

**Request Body:**

```json
{
  "title": "Updated: Travel Guide to Ho Chi Minh City",
  // Optional
  "summary": "Updated summary about HCMC",
  // Optional
  "content": "Updated article content...",
  // Optional
  "category_id": 2,
  // Optional
  "tag_ids": [
    1,
    5,
    8
  ],
  // Optional
  "cover_image": "https://example.com/updated-hcmc-guide.jpg",
  // Optional
  "related_location_ids": [
    2,
    5
  ],
  // Optional
  "published": true
  // Optional
}
```

**Response:** Updated article object

**Status Codes:**

- 200: Success
- 404: Article not found
- 403: Forbidden (not authorized)

### Delete Article

Delete an article (only author, editor or admin).

**Endpoint:** `DELETE /api/v1/articles/{article_id}`

**Headers:**

- Authorization: Bearer {access_token}

**Status Codes:**

- 204: No content (successful deletion)
- 404: Article not found
- 403: Forbidden (not authorized)

---

## Events

Endpoints for managing events.

### Event Organizers

#### List Event Organizers

Get list of organizers created by the current user.

**Endpoint:** `GET /api/v1/events/organizers/`

**Headers:**

- Authorization: Bearer {access_token}

**Response:**

```json
[
  {
    "id": 1,
    "name": "Local Tours Company",
    "description": "Local tour operator in Hanoi",
    "logo": "https://example.com/localtours-logo.png",
    "website": "https://localtours.com",
    "email": "info@localtours.com",
    "phone": "+84123456789",
    "user_id": 5,
    "created_at": "2025-05-01T00:00:00",
    "updated_at": "2025-05-01T00:00:00"
  }
]
```

#### Get Event Organizer

Get a specific organizer by ID.

**Endpoint:** `GET /api/v1/events/organizers/{organizer_id}`

**Headers:**

- Authorization: Bearer {access_token}

**Response:** Same as a single organizer object from the list endpoint

**Status Codes:**

- 200: Success
- 404: Organizer not found

#### Create Event Organizer

Create a new event organizer.

**Endpoint:** `POST /api/v1/events/organizers/`

**Headers:**

- Authorization: Bearer {access_token}

**Request Body:**

```json
{
  "name": "Culture Events Organization",
  "description": "Organization hosting cultural events in Vietnam",
  "logo": "https://example.com/culture-logo.png",
  "website": "https://cultureevents.com",
  "email": "info@cultureevents.com",
  "phone": "+84987654321"
}
```

**Response:** Created organizer object

#### Update Event Organizer

Update an existing event organizer (only owner or superuser).

**Endpoint:** `PUT /api/v1/events/organizers/{organizer_id}`

**Headers:**

- Authorization: Bearer {access_token}

**Request Body:**

```json
{
  "name": "Updated Organization Name",
  // Optional
  "description": "Updated description",
  // Optional
  "logo": "https://example.com/updated-logo.png",
  // Optional
  "website": "https://updated-website.com",
  // Optional
  "email": "updated@example.com",
  // Optional
  "phone": "+84111222333"
  // Optional
}
```

**Response:** Updated organizer object

**Status Codes:**

- 200: Success
- 404: Organizer not found
- 403: Forbidden (not the owner or superuser)

### Event Categories

#### List Event Categories

Get list of all event categories.

**Endpoint:** `GET /api/v1/events/categories/`

**Response:**

```json
[
  {
    "id": 1,
    "name": "Festival",
    "description": "Cultural and traditional festivals",
    "status": 1,
    "created_at": "2025-05-01T00:00:00",
    "updated_at": "2025-05-01T00:00:00"
  },
  {
    "id": 2,
    "name": "Food Event",
    "description": "Food and culinary events",
    "status": 1,
    "created_at": "2025-05-01T00:00:00",
    "updated_at": "2025-05-01T00:00:00"
  }
]
```

#### Get Event Category

Get a specific event category by ID.

**Endpoint:** `GET /api/v1/events/categories/{category_id}`

**Response:** Same as a single category object from the list endpoint

**Status Codes:**

- 200: Success
- 404: Category not found

#### Create Event Category

Create a new event category (admin or content manager only).

**Endpoint:** `POST /api/v1/events/categories/`

**Headers:**

- Authorization: Bearer {access_token}

**Request Body:**

```json
{
  "name": "Music Concert",
  "description": "Live music performances and concerts",
  "status": 1
}
```

**Response:** Created event category object

### List Events

Get list of events with pagination.

**Endpoint:** `GET /api/v1/events/`

**Query Parameters:**

- page: int (default: 1)
- limit: int (default: 10, max: 100)
- search: string (optional)
- category_id: int (optional)
- organizer_id: int (optional)
- country_id: int (optional)
- region_id: int (optional)
- district_id: int (optional)

**Response:**

```json
{
  "items": [
    {
      "id": 1,
      "name": "Lantern Festival",
      "description": "Annual lantern festival in Hoi An",
      "category_id": 1,
      "organizer_id": 3,
      "start_date": "2025-06-15",
      "end_date": "2025-06-16",
      "start_time": "18:00:00",
      "end_time": "23:00:00",
      "location": {
        "address": "Hoi An Ancient Town",
        "latitude": 15.8800,
        "longitude": 108.3380
      },
      "region_id": 3,
      "cover_image": "https://example.com/lantern-festival.jpg",
      "ticket_price": "Free",
      "website": "https://hoian-festival.com",
      "created_at": "2025-05-01T00:00:00",
      "updated_at": "2025-05-01T00:00:00"
    }
  ],
  "total": 25,
  "page": 1,
  "size": 10,
  "pages": 3
}
```

### Get Event

Get a specific event by ID.

**Endpoint:** `GET /api/v1/events/{event_id}`

**Response:** Same as a single event object from the items array in the list endpoint

**Status Codes:**

- 200: Success
- 404: Event not found

### Create Event

Create a new event.

**Endpoint:** `POST /api/v1/events/`

**Headers:**

- Authorization: Bearer {access_token}

**Request Body:**

```json
{
  "name": "Food and Culture Festival",
  "description": "Festival celebrating Vietnamese food and culture",
  "category_id": 1,
  "organizer_id": 2,
  "start_date": "2025-07-20",
  "end_date": "2025-07-22",
  "start_time": "10:00:00",
  "end_time": "22:00:00",
  "location": {
    "address": "September 23 Park, Ho Chi Minh City",
    "latitude": 10.7721,
    "longitude": 106.6926
  },
  "region_id": 2,
  "ticket_price": "$10",
  "website": "https://foodfestival.com"
}
```

**Response:** Created event object

### Update Event

Update an existing event (only organizer or admin).

**Endpoint:** `PUT /api/v1/events/{event_id}`

**Headers:**

- Authorization: Bearer {access_token}

**Request Body:**

```json
{
  "name": "Updated Festival Name",
  // Optional
  "description": "Updated description",
  // Optional
  "category_id": 3,
  // Optional
  "start_date": "2025-07-21",
  // Optional
  "end_date": "2025-07-23",
  // Optional
  "start_time": "11:00:00",
  // Optional
  "end_time": "23:00:00",
  // Optional
  "location": {
    // Optional
    "address": "Updated Address",
    "latitude": 10.7725,
    "longitude": 106.6930
  },
  "region_id": 3,
  // Optional
  "ticket_price": "$15",
  // Optional
  "website": "https://updated-website.com"
  // Optional
}
```

**Response:** Updated event object

**Status Codes:**

- 200: Success
- 404: Event not found
- 403: Forbidden (not authorized)

### Delete Event

Delete an event (only organizer or admin).

**Endpoint:** `DELETE /api/v1/events/{event_id}`

**Headers:**

- Authorization: Bearer {access_token}

**Status Codes:**

- 204: No content (successful deletion)
- 404: Event not found
- 403: Forbidden (not authorized)

---

## Community Posts

Endpoints for managing community posts.

### List Community Posts

Get list of community posts with pagination.

**Endpoint:** `GET /api/v1/community-posts/`

**Query Parameters:**

- page: int (default: 1)
- limit: int (default: 10, max: 50)
- user_id: int (optional)
- location_id: int (optional)

**Response:**

```json
{
  "items": [
    {
      "id": 1,
      "title": "My Experience in Sapa",
      "content": "I just returned from an amazing trip to Sapa...",
      "user": {
        "id": 3,
        "full_name": "John Traveler"
      },
      "location": {
        "id": 5,
        "name": "Sapa"
      },
      "images": [
        "https://example.com/sapa1.jpg",
        "https://example.com/sapa2.jpg"
      ],
      "likes_count": 24,
      "comments_count": 5,
      "created_at": "2025-05-18T09:45:12",
      "updated_at": "2025-05-18T09:45:12"
    }
  ],
  "total": 86,
  "page": 1,
  "size": 10,
  "pages": 9
}
```

### Get Community Post

Get a specific community post by ID.

**Endpoint:** `GET /api/v1/community-posts/{post_id}`

**Response:** Same as a single post object from the items array in the list endpoint, plus comments:

```json
{
  "id": 1,
  "title": "My Experience in Sapa",
  "content": "I just returned from an amazing trip to Sapa...",
  "user": {
    "id": 3,
    "full_name": "John Traveler"
  },
  "location": {
    "id": 5,
    "name": "Sapa"
  },
  "images": [
    "https://example.com/sapa1.jpg",
    "https://example.com/sapa2.jpg"
  ],
  "likes_count": 24,
  "comments": [
    {
      "id": 5,
      "content": "Great post! I'm planning to visit next month.",
      "user": {
        "id": 7,
        "full_name": "Jane Doe"
      },
      "created_at": "2025-05-19T14:22:36"
    }
  ],
  "created_at": "2025-05-18T09:45:12",
  "updated_at": "2025-05-18T09:45:12"
}
```

**Status Codes:**

- 200: Success
- 404: Post not found

### Create Community Post

Create a new community post.

**Endpoint:** `POST /api/v1/community-posts/`

**Headers:**

- Authorization: Bearer {access_token}

**Request Body:**

```json
{
  "title": "Hidden Gems in Da Nang",
  "content": "During my recent trip to Da Nang, I discovered some amazing places that aren't in most guidebooks...",
  "location_id": 4,
  "image_ids": [
    15,
    16,
    17
  ]
}
```

**Response:** Created post object

### Update Community Post

Update an existing community post (only author or admin).

**Endpoint:** `PUT /api/v1/community-posts/{post_id}`

**Headers:**

- Authorization: Bearer {access_token}

**Request Body:**

```json
{
  "title": "Updated: Hidden Gems in Da Nang",
  // Optional
  "content": "Updated content...",
  // Optional
  "location_id": 4,
  // Optional
  "image_ids": [
    15,
    18,
    20
  ]
  // Optional
}
```

**Response:** Updated post object

**Status Codes:**

- 200: Success
- 404: Post not found
- 403: Forbidden (not authorized)

### Delete Community Post

Delete a community post (only author or admin).

**Endpoint:** `DELETE /api/v1/community-posts/{post_id}`

**Headers:**

- Authorization: Bearer {access_token}

**Status Codes:**

- 204: No content (successful deletion)
- 404: Post not found
- 403: Forbidden (not authorized)

### Like/Unlike Post

Toggle like status for a post.

**Endpoint:** `POST /api/v1/community-posts/{post_id}/like`

**Headers:**

- Authorization: Bearer {access_token}

**Response:**

```json
{
  "liked": true,
  "likes_count": 25
}
```

### Add Comment

Add a comment to a community post.

**Endpoint:** `POST /api/v1/community-posts/{post_id}/comments`

**Headers:**

- Authorization: Bearer {access_token}

**Request Body:**

```json
{
  "content": "Great post! I'm planning to visit Da Nang next month."
}
```

**Response:**

```json
{
  "id": 12,
  "content": "Great post! I'm planning to visit Da Nang next month.",
  "user": {
    "id": 5,
    "full_name": "Jane Doe"
  },
  "created_at": "2025-05-21T14:35:22"
}
```

---

## Ratings

Endpoints for managing ratings and reviews.

### Create Rating

Create a new rating or update existing rating.

**Endpoint:** `POST /api/v1/ratings/`

**Headers:**

- Authorization: Bearer {access_token}

**Request Body:**

```json
{
  "reference_id": 3,
  "reference_type": "accommodation",
  "rating": 4.5,
  "comment": "Excellent service and beautiful views. Highly recommended!"
}
```

**Response:**

```json
{
  "id": 8,
  "reference_id": 3,
  "reference_type": "accommodation",
  "rating": 4.5,
  "comment": "Excellent service and beautiful views. Highly recommended!",
  "user_id": 5,
  "created_at": "2025-05-21T12:30:15",
  "updated_at": "2025-05-21T12:30:15"
}
```

### Get Ratings

Get ratings for a specific item.

**Endpoint:** `GET /api/v1/ratings/`

**Query Parameters:**

- reference_id: int (required) - ID of the item being rated
- reference_type: string (required) - Type of item being rated (location, accommodation, food, etc.)
- skip: int (default: 0)
- limit: int (default: 100)

**Response:**

```json
[
  {
    "id": 8,
    "reference_id": 3,
    "reference_type": "accommodation",
    "rating": 4.5,
    "comment": "Excellent service and beautiful views. Highly recommended!",
    "user": {
      "id": 5,
      "full_name": "Jane Doe"
    },
    "created_at": "2025-05-21T12:30:15"
  },
  {
    "id": 12,
    "reference_id": 3,
    "reference_type": "accommodation",
    "rating": 5.0,
    "comment": "Perfect stay, couldn't ask for more!",
    "user": {
      "id": 7,
      "full_name": "Maria Garcia"
    },
    "created_at": "2025-05-18T09:12:33"
  }
]
```

### Get Average Rating

Get the average rating for a specific item.

**Endpoint:** `GET /api/v1/ratings/average`

**Query Parameters:**

- reference_id: int (required) - ID of the item being rated
- reference_type: string (required) - Type of item being rated (location, accommodation, food, etc.)

**Response:**

```json
{
  "average_rating": 4.75,
  "ratings_count": 2
}
```

### Get User Rating

Get the current user's rating for a specific item.

**Endpoint:** `GET /api/v1/ratings/mine`

**Headers:**

- Authorization: Bearer {access_token}

**Query Parameters:**

- reference_id: int (required) - ID of the item being rated
- reference_type: string (required) - Type of item being rated (location, accommodation, food, etc.)

**Response:**

```json
{
  "id": 8,
  "reference_id": 3,
  "reference_type": "accommodation",
  "rating": 4.5,
  "comment": "Excellent service and beautiful views. Highly recommended!",
  "created_at": "2025-05-21T12:30:15",
  "updated_at": "2025-05-21T12:30:15"
}
```

**Status Codes:**

- 200: Success
- 404: Rating not found (user has not rated this item)

