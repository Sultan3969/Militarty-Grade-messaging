# TacticalLink - System Architecture

## Overview
TacticalLink is an AI-powered military-grade messaging system with end-to-end encryption, self-destructing messages, and real-time threat detection.

## Architecture Components

### 1. Frontend (React + TailwindCSS)
- **Location**: `/frontend`
- **Deployment**: Vercel
- **Components**:
  - Login/Register pages
  - Secure chat interface
  - Admin dashboard with threat visualization
  - Real-time message updates via WebSocket

### 2. Backend (Flask + Python)
- **Location**: `/backend`
- **Deployment**: Railway
- **APIs**:
  - `/auth` - JWT-based authentication
  - `/chat` - Encrypted message handling
  - `/delete` - Self-destruct mechanism
  - `/threat` - AI threat analysis
  - `/admin` - Admin dashboard data

### 3. Database (MongoDB)
- **Collections**:
  - `users` - User credentials and metadata
  - `messages` - Encrypted message storage
  - `threat_logs` - AI threat detection logs
  - `session_keys` - Temporary encryption keys

### 4. AI Threat Detection
- **Model**: Isolation Forest for anomaly detection
- **Features**: Message frequency, IP patterns, timing anomalies
- **Output**: Threat score (0-100)

### 5. Encryption Layer
- **Symmetric**: AES-256 for message encryption
- **Asymmetric**: RSA-4096 for key exchange
- **Quantum-safe**: Lattice-based encryption simulation

## Data Flow

1. **User Authentication**:
   User → Frontend → Backend → JWT Token → Database

2. **Message Sending**:
   User Input → Frontend → Backend → AES Encryption → Database

3. **Threat Detection**:
   Message Metadata → AI Model → Threat Score → Admin Dashboard

4. **Self-Destruct**:
   Timer → Background Task → Database Cleanup → Key Destruction

## Security Features

- End-to-end encryption with perfect forward secrecy
- Metadata leak detection via AI
- Self-destructing messages with secure deletion
- Real-time threat monitoring
- Adaptive encryption key rotation
- Quantum-safe encryption simulation

## Deployment Architecture

```
Frontend (Vercel) ←→ Backend (Railway) ←→ MongoDB (Railway)
                           ↓
                    AI Threat Detection
                           ↓
                    Admin Dashboard
```
