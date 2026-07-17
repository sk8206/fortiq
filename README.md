# Fortiq

Fortiq is an enterprise-grade Post-Quantum Cryptography (PQC) migration platform that helps organizations transition their cryptographic infrastructure from classical algorithms to quantum-resistant standards. The platform combines machine learning-based risk classification with NIST-approved post-quantum algorithms.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Local Development](#local-development)
  - [Docker Deployment](#docker-deployment)
- [Project Structure](#project-structure)
- [API Reference](#api-reference)
- [Configuration](#configuration)
- [Production Deployment](#production-deployment)
  - [Vercel (Frontend)](#vercel-frontend)
  - [Backend Services](#backend-services)
- [Contributing](#contributing)
- [License](#license)

## Overview

With the advent of quantum computing, current cryptographic algorithms (RSA, ECC) face potential vulnerabilities. Fortiq provides a systematic approach to:

1. **Discover** cryptographic endpoints across your infrastructure
2. **Classify** risk levels using quantum machine learning (VQC)
3. **Migrate** to NIST-approved post-quantum algorithms
4. **Audit** the entire transition with comprehensive logging

## Features

### Risk Classification Engine
- Variational Quantum Classifier (VQC) for intelligent risk assessment
- Classical SVM baseline for model comparison
- Multi-factor risk scoring based on:
  - Algorithm strength and key length
  - Data sensitivity classification
  - Exposure surface (internet-facing, internal, air-gapped)
  - Traffic volume and certificate expiry

### Post-Quantum Cryptography Support
- **ML-KEM-768** (FIPS 203) - Key Encapsulation Mechanism
- **ML-DSA-65** (FIPS 204) - Digital Signature Algorithm
- NIST Security Level 3 compliance
- Hybrid migration support for gradual rollout

### Enterprise Features
- Role-based access control with JWT authentication
- Comprehensive audit logging
- Real-time migration progress tracking
- RESTful API with OpenAPI documentation
- Async task processing with Celery

## Architecture

```
                                 +------------------+
                                 |   React Frontend |
                                 |   (Vite + TS)    |
                                 +--------+---------+
                                          |
                                          v
+------------------+            +------------------+            +------------------+
|   PostgreSQL     |<---------->|   FastAPI        |<---------->|   Redis          |
|   (Primary DB)   |            |   Backend        |            |   (Cache/Queue)  |
+------------------+            +--------+---------+            +------------------+
                                         |
                                         v
                               +------------------+
                               |   Celery Worker  |
                               |   (Async Tasks)  |
                               +------------------+
                                         |
                    +--------------------+--------------------+
                    |                    |                    |
                    v                    v                    v
            +-------------+      +-------------+      +-------------+
            | VQC Model   |      | PQC Engine  |      | Audit Log   |
            | (PennyLane) |      | (liboqs)    |      | Service     |
            +-------------+      +-------------+      +-------------+
```

## Technology Stack

### Backend
- **Framework**: FastAPI 0.115+
- **ORM**: SQLAlchemy 2.0 (async)
- **Database**: PostgreSQL 16
- **Cache/Queue**: Redis 7
- **Task Queue**: Celery 5
- **ML Framework**: PennyLane (quantum ML)
- **PQC Library**: liboqs (via oqs-python)

### Frontend
- **Framework**: React 19 with TypeScript
- **Build Tool**: Vite 8
- **Styling**: TailwindCSS 4
- **State Management**: Zustand
- **Server State**: TanStack Query
- **Routing**: React Router 7
- **Charts**: Recharts

## Getting Started

### Prerequisites

- Node.js 20+
- Python 3.11+
- PostgreSQL 16+
- Redis 7+
- Docker and Docker Compose (optional)

### Local Development

1. **Clone the repository**

```bash
git clone https://github.com/your-org/fortiq.git
cd fortiq
```

2. **Backend Setup**

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Set environment variables (create .env file)
cat > .env << EOF
DATABASE_URL=postgresql+asyncpg://fortiq:fortiq-dev-2024@localhost:5432/fortiq
SYNC_DATABASE_URL=postgresql+psycopg2://fortiq:fortiq-dev-2024@localhost:5432/fortiq
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-here
ENVIRONMENT=development
EOF

# Run database migrations
alembic upgrade head

# Generate synthetic endpoint data
python scripts/generate_dataset.py

# Create admin user
python scripts/create_admin.py

# Train ML models (optional, takes time)
python scripts/train_models.py

# Start the backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

3. **Frontend Setup**

```bash
cd frontend

# Install dependencies
npm install

# Create environment file
cat > .env << EOF
VITE_API_URL=http://localhost:8000/api/v1
EOF

# Start development server
npm run dev
```

4. **Start Celery Worker** (separate terminal)

```bash
cd backend
source venv/bin/activate
celery -A app.celery_app worker --loglevel=info
```

5. **Access the application**

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Demo credentials: `admin` / `fortiq-demo-2024`

### Docker Deployment

For a complete containerized deployment:

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

Services will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

## Project Structure

```
fortiq/
├── backend/
│   ├── app/
│   │   ├── core/           # Core configuration and security
│   │   ├── models/         # SQLAlchemy ORM models
│   │   ├── repositories/   # Data access layer
│   │   ├── routers/        # API route handlers
│   │   ├── schemas/        # Pydantic request/response schemas
│   │   ├── services/       # Business logic layer
│   │   ├── celery_app.py   # Celery configuration
│   │   └── main.py         # FastAPI application entry
│   ├── alembic/            # Database migrations
│   ├── models/             # Trained ML model files
│   ├── scripts/            # Utility scripts
│   ├── tests/              # Test suite
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/            # API client and endpoints
│   │   ├── components/     # React components
│   │   ├── hooks/          # Custom React hooks
│   │   ├── pages/          # Page components
│   │   ├── stores/         # Zustand state stores
│   │   ├── styles/         # CSS and design tokens
│   │   └── types/          # TypeScript type definitions
│   ├── Dockerfile
│   ├── nginx.conf
│   └── package.json
├── docker-compose.yml
├── PLAN.md
└── README.md
```

## API Reference

### Authentication

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/auth/login` | POST | Authenticate user |
| `/api/v1/auth/logout` | POST | Invalidate session |
| `/api/v1/auth/refresh` | POST | Refresh access token |
| `/api/v1/auth/me` | GET | Get current user |

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/endpoints` | GET | List all endpoints (paginated) |
| `/api/v1/endpoints/{id}` | GET | Get endpoint details |
| `/api/v1/endpoints/stats/dashboard` | GET | Get dashboard statistics |

### Classification

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/classify` | POST | Trigger risk classification |
| `/api/v1/classify/jobs/{id}` | GET | Get classification job status |
| `/api/v1/classify/model-comparison` | GET | Get VQC vs SVM comparison |

### Migration

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/migrate` | POST | Trigger PQC migration |
| `/api/v1/migrate/jobs/{id}` | GET | Get migration job status |
| `/api/v1/migrate/pqc-demo` | GET | Get PQC algorithm demonstration |
| `/api/v1/migrate/audit-log` | GET | Get migration audit log |

## Configuration

### Environment Variables

#### Backend

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL async connection string | Required |
| `SYNC_DATABASE_URL` | PostgreSQL sync connection string | Required |
| `REDIS_URL` | Redis connection URL | `redis://localhost:6379/0` |
| `SECRET_KEY` | JWT signing key | Required |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token TTL | `60` |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token TTL | `7` |
| `ALLOWED_ORIGINS` | CORS allowed origins (JSON array) | `["http://localhost:5173"]` |
| `ENVIRONMENT` | Environment name | `development` |
| `LOG_LEVEL` | Logging level | `INFO` |

#### Frontend

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_URL` | Backend API base URL | `http://localhost:8000/api/v1` |

## Production Deployment

### Vercel (Frontend)

1. **Connect Repository**
   - Import the repository in Vercel dashboard
   - Set the root directory to `frontend`

2. **Configure Build Settings**
   - Framework Preset: Vite
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Install Command: `npm install`

3. **Environment Variables**

   Add the following in Vercel project settings:
   ```
   VITE_API_URL=https://your-backend-domain.com/api/v1
   ```

4. **Deploy**

   Vercel will automatically deploy on push to main branch.

### Backend Services

For production backend deployment, consider:

#### Option 1: Railway / Render / Fly.io

These platforms support Docker deployments and provide managed PostgreSQL and Redis.

```bash
# Example with Railway
railway login
railway init
railway add postgresql
railway add redis
railway up
```

#### Option 2: AWS / GCP / Azure

Deploy using container services (ECS, Cloud Run, AKS):

```bash
# Build and push Docker images
docker build -t fortiq-backend ./backend
docker build -t fortiq-frontend ./frontend

# Push to container registry
docker tag fortiq-backend your-registry/fortiq-backend:latest
docker push your-registry/fortiq-backend:latest
```

#### Production Checklist

- [ ] Use strong, randomly generated `SECRET_KEY`
- [ ] Configure proper CORS origins for your domain
- [ ] Enable HTTPS/TLS for all services
- [ ] Set up database backups
- [ ] Configure monitoring and alerting
- [ ] Use managed PostgreSQL with high availability
- [ ] Use managed Redis with persistence
- [ ] Set appropriate resource limits for containers
- [ ] Configure log aggregation

### Recommended Architecture for Production

```
                    +------------------+
                    |   Cloudflare     |
                    |   (CDN + WAF)    |
                    +--------+---------+
                             |
            +----------------+----------------+
            |                                 |
            v                                 v
    +---------------+                +---------------+
    |   Vercel      |                |   Load        |
    |   (Frontend)  |                |   Balancer    |
    +---------------+                +-------+-------+
                                             |
                                    +--------+--------+
                                    |                 |
                                    v                 v
                            +-------------+   +-------------+
                            |   Backend   |   |   Backend   |
                            |   (API)     |   |   (API)     |
                            +------+------+   +------+------+
                                   |                 |
                    +--------------+-----------------+
                    |              |                 |
                    v              v                 v
            +-------------+ +-------------+ +-------------+
            |  PostgreSQL | |    Redis    | |   Celery    |
            |  (Managed)  | |  (Managed)  | |   Workers   |
            +-------------+ +-------------+ +-------------+
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Create a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use ESLint/Prettier for TypeScript/React code
- Write tests for new features
- Update documentation as needed

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

**Fortiq** - Securing your infrastructure for the quantum future.
