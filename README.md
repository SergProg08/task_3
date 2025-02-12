# RESTful-API-for-Authentication-with-simplejwt

## REST API for a user authentication and authorization system using Django and Django REST Framework.

### Objective

REST API for a user authentication and authorization system using Django and Django REST Framework. The system should support user registration, authentication, token refresh, logout, and allow users to retrieve and update their personal information.

Authentication should utilize Access and Refresh tokens.

Refresh Token – A UUID stored in the database, issued for 30 days by default. Access Token – A JSON Web Token with a default lifespan of 30 seconds.

Clients may request an Access Token refresh at any time, for instance, upon Access Token expiry by providing a valid Refresh Token. In this case, the service returns a new valid pair of Access and Refresh Tokens, resetting their lifespans.

#### Implementation Requirements

1. RESTful API must be developed with Django and Django REST Framework.
2. Access Token is not stored in the database; it’s verified in authentication endpoints without database calls, using the SimpleJWT library.
3. Refresh Token should be stored in the database with its expiry time and linked to a user. This allows for the token to be invalidated when necessary (e.g., when the user logs out).
4. Use the django-constance module for managing the lifetimes of Access and Refresh tokens.
5. API Documentation: Provide a browsable API with endpoint documentation.
6. Deployment: For demonstrating the API’s functionality, you can use free hosting platforms like Heroku, which offer convenient means for deploying Django applications.

### Required Endpoints Description

#### User Registration

[Endpoint: `/api/register/`
Method: `POST`
Body: `{"password": "password", "email": "user@example.com"}`
Response: `{"id": 1, "email": "user@example.com"}`  
curl -X POST (http://localhost:8000/api/register/) -d '{"password": "password", "email": "user@example.com"}' -H "Content-Type: application/json"]