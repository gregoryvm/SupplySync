# SupplySync
SupplySync is a full-stack inventory management system designed to assist users with manage their products. 

We're currently hosted at:
- https://supplysync-er1f.onrender.com/

## Tech Stack
### Backend:
- Python
- Django
- Django REST Framework

### Frontend
- HTML
- CSS

### Database
-  PostgreSQL

### Deployment
-  Render
-  Supabase

## API Overview

### Products
| Method | Endpoint           | Description |
| ------ | ------------------ | ----------- |
| GET    | /inventory         | View a user's inventory dashboard |
| GET    | /create            | Show product creation form |
| POST   | /create            | Create a new product |
| POST   | /delete/<str:name>/<str:sku> | Delete product |
| POST   | /edit/<str:name>/<str:sku> | Edit product |

### Users
| Method | Endpoint           | Description |
| ------ | ------------------ | ----------- |
| POST   | /signup            | Registers a new user |
| POST   | /login             | Log in a user |
| POST   | /logout            | Logs out a user |
| GET    | /account           | View user account page |
| POST   | /delete/<str:username> | Deletes a user account |

### General
| Method | Endpoint           | Description |
| ------ | ------------------ | ----------- |
| GET    | /                  | View home page |

