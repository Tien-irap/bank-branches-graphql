# Bank Branches GraphQL API

A FastAPI-based backend service that provides a GraphQL API for querying Indian bank branches data.

## 🏗️ Project Structure

```
root/
├── app/
│   ├── __init__.py
│   ├── main.py              # Entry point (initializes FastAPI + GraphQL)
│   │
│   ├── core/                # The "Plumbing"
│   │   ├── __init__.py
│   │   ├── config.py        # Env vars (DB path, Debug mode)
│   │   ├── database.py      # SQLite connection management
│   │   └── logger.py        # Logger configuration
│   │
│   ├── models/              # The "Database" (prepared for SQLAlchemy)
│   │   ├── __init__.py
│   │   └── sql_models.py    # Placeholder for future SQLAlchemy models
│   │
│   ├── schemas/             # The "Shape" (Strawberry/GraphQL)
│   │   ├── __init__.py
│   │   └── gql_types.py     # Defines 'BankType' and 'BranchType'
│   │
│   ├── repo/                # The "Data Access"
│   │   ├── __init__.py
│   │   └── repository.py    # Database query functions
│   │
│   ├── services/            # The "Logic" (Business layer)
│   │   ├── __init__.py
│   │   └── branch_service.py  # Functions like 'get_all_branches()'
│   │
│   └── routes/              # The "Doorway"
│       ├── __init__.py
│       └── views.py         # GraphQL Query definitions
│
├── data/                    # Data files (separate from code)
│   ├── bank_branches.csv
│   └── indian_banks.db
│
├── init_db.py               # Database initialization script (run once)
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (don't commit!)
└── README.md                # This file
```

## 📦 Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Environment
```bash
cp .env.example .env
```

Edit `.env` if needed to customize settings.

### 3. Initialize Database
```bash
python init_db.py
```

This will:
- Create `data/` folder
- Read `data/bank_branches.csv`
- Create `data/indian_banks.db` with tables:
  - `banks` (id, name)
  - `branches` (ifsc, branch, address, city, district, state, bank_id)

## 🚀 Run the Server

```bash
python app/main.py
```

Or using uvicorn directly:
```bash
uvicorn app.main:app --reload
```

The server will start at `http://localhost:8000`

## 🔍 GraphQL API

### Endpoint
`http://localhost:8000/graphql`

Access the **GraphiQL** interactive interface in your browser to explore and test queries.

### Sample Queries

#### 1. Get Branches
```graphql
query {
  branches {
    edges {
      node {
        branch
        bank {
          name
        }
        ifsc
      }
    }
  }
}
```

#### 2. Get Branches with Pagination
```graphql
query {
  branches(first: 10) {
    edges {
      node {
        ifsc
        branch
        city
        bank {
          name
        }
      }
      cursor
    }
    pageInfo {
      hasNextPage
      endCursor
    }
    totalCount
  }
}
```

#### 3. Get Branches with Filters
```graphql
query {
  branches(first: 5, filter: {city: "MUMBAI"}) {
    edges {
      node {
        ifsc
        branch
        address
        city
        bank {
          name
        }
      }
    }
    totalCount
  }
}
```

#### 4. Get Single Branch
```graphql
query {
  branch(ifsc: "ABHY0065001") {
    ifsc
    branch
    address
    city
    district
    state
    bank {
      id
      name
    }
  }
}
```

#### 5. Get All Banks
```graphql
query {
  banks(first: 10) {
    edges {
      node {
        id
        name
      }
    }
    pageInfo {
      hasNextPage
    }
    totalCount
  }
}
```

#### 6. Get Single Bank
```graphql
query {
  bank(id: 60) {
    id
    name
  }
}
```

## 📋 Features

- ✅ **GraphQL API** with Strawberry
- ✅ **Cursor-based pagination** (Relay-style)
- ✅ **Advanced filtering** (city, district, state, bank name, branch name, IFSC)
- ✅ **Nested queries** (branch → bank relationship)
- ✅ **Comprehensive logging** throughout all layers
- ✅ **Clean architecture** (separation of concerns)
- ✅ **GraphiQL interface** for testing
- ✅ **Health check endpoint**: `/health`
- ✅ **API statistics**: `/stats`

## 🛠️ Tech Stack

- **FastAPI**: Modern web framework
- **Strawberry GraphQL**: GraphQL library for Python
- **SQLite**: Lightweight database
- **Pandas**: CSV data processing
- **Uvicorn**: ASGI server
- **Pydantic**: Settings management

## 📚 API Documentation

- **GraphiQL Interface**: http://localhost:8000/graphql
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔧 Configuration

Edit `.env` file to configure:

```env
# Application
DEBUG=True
HOST=0.0.0.0
PORT=8000

# Database
DATABASE_PATH=data/indian_banks.db

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# API Key (optional)
API_KEY_ENABLED=False
API_KEY=your-secret-key
```

## 📊 Understanding the Architecture

### Core Layer (Plumbing)
- **config.py**: Loads environment variables, database paths, settings
- **database.py**: Manages SQLite connections, provides session context
- **logger.py**: Configures logging with file rotation

### Models Layer (Database)
- **sql_models.py**: Placeholder for SQLAlchemy ORM models (future migration)
- Currently using raw SQLite with `sqlite3` module

### Schemas Layer (Shape)
- **gql_types.py**: Strawberry GraphQL types that define API structure
- `BankType`, `BranchType`, `BranchConnection`, etc.

### Repo Layer (Data Access)
- **repository.py**: Database query functions
- `BankRepository`: CRUD for banks
- `BranchRepository`: CRUD for branches with filters

### Services Layer (Business Logic)
- **branch_service.py**: Business logic, data transformation
- Converts database rows to GraphQL types
- Handles pagination cursors

### Routes Layer (Doorway)
- **views.py**: GraphQL query definitions and resolvers
- Defines what queries are available and how they work

## 📝 Logs

Logs are saved to `logs/app.log` with automatic rotation:
- Max file size: 10MB
- Backup files: 5
- Format includes timestamp, level, and message

## 🤝 Development

### Adding New Queries

1. **Add GraphQL type** in `app/schemas/gql_types.py`
2. **Add repository method** in `app/repo/repository.py`
3. **Add service method** in `app/services/branch_service.py`
4. **Add query resolver** in `app/routes/views.py`

### Future Enhancements

- [ ] Migrate to SQLAlchemy ORM
- [ ] Add mutations (create, update, delete)
- [ ] Add authentication with API keys
- [ ] Add caching layer
- [ ] Add rate limiting
- [ ] Add tests

## 📄 License

MIT License - Feel free to use this project as you wish!
