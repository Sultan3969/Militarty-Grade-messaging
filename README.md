# TacticalLink - AI-Powered Military-Grade Messaging System

![TacticalLink Logo](https://img.shields.io/badge/TacticalLink-Military%20Grade-blue?style=for-the-badge&logo=shield)
![Security](https://img.shields.io/badge/Security-AES--256%20%2B%20RSA--4096-green?style=for-the-badge)
![AI](https://img.shields.io/badge/AI-Threat%20Detection-purple?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

## 🎯 Overview

TacticalLink is an advanced AI-powered messaging system designed for military-grade secure communication. It features end-to-end encryption, self-destructing messages, real-time threat detection, and adaptive security measures.

### 🔐 Key Features

- **End-to-End Encryption**: AES-256 symmetric encryption with RSA-4096 key exchange
- **Quantum-Safe Encryption**: Lattice-based encryption simulation for future-proof security
- **AI Threat Detection**: Machine learning models to detect anomalous behavior patterns
- **Self-Destructing Messages**: Automatic message deletion with configurable timers
- **Real-Time Monitoring**: Live threat assessment and security dashboard
- **Perfect Forward Secrecy**: Ephemeral keys for enhanced security
- **Adaptive Security**: Dynamic key rotation based on threat levels

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│   (React)       │◄──►│   (Flask)       │◄──►│   (MongoDB)     │
│   Vercel        │    │   Railway       │    │   Railway       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   WebSocket     │    │   AI Threat     │    │   Encryption    │
│   Real-time     │    │   Detection     │    │   Manager       │
│   Updates       │    │   (ML Models)   │    │   (AES/RSA)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Node.js 16+ and npm
- Python 3.8+
- MongoDB (local or cloud)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/tactical-link.git
   cd tactical-link
   ```

2. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

4. **Environment Configuration**
   
   Create `.env` file in the backend directory:
   ```env
   MONGODB_URL=mongodb://localhost:27017/tactical_link
   JWT_SECRET_KEY=your-super-secret-jwt-key-here
   PORT=5000
   ```

5. **Start the Application**
   
   Backend (Terminal 1):
   ```bash
   cd backend
   python app.py
   ```
   
   Frontend (Terminal 2):
   ```bash
   cd frontend
   npm start
   ```

6. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

## 📁 Project Structure

```
tactical-link/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── models.py              # Database models
│   ├── database.py            # MongoDB operations
│   ├── encryption.py          # Encryption/decryption logic
│   ├── ai_threat.py           # AI threat detection
│   ├── message_scheduler.py   # Self-destruct scheduler
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # Environment variables
├── frontend/
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── contexts/          # React contexts
│   │   ├── App.js            # Main app component
│   │   └── index.css         # TailwindCSS styles
│   ├── package.json          # Node.js dependencies
│   └── tailwind.config.js    # TailwindCSS config
├── SYSTEM_ARCHITECTURE.md    # Detailed architecture docs
└── README.md                 # This file
```

## 🔧 API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login

### Messaging
- `POST /chat/send` - Send encrypted message
- `GET /chat/receive` - Receive and decrypt messages
- `DELETE /delete/message/<id>` - Delete specific message

### Threat Detection
- `POST /threat/analyze` - Analyze threat level
- `GET /ws/status` - Real-time status updates

### Admin
- `GET /admin/dashboard` - Admin dashboard data
- `GET /admin/users` - Get all users

## 🛡️ Security Features

### Encryption
- **AES-256-GCM**: Symmetric encryption for message content
- **RSA-4096**: Asymmetric encryption for key exchange
- **Quantum-Safe**: Lattice-based encryption simulation
- **Perfect Forward Secrecy**: Ephemeral session keys

### AI Threat Detection
- **Isolation Forest**: Anomaly detection algorithm
- **Feature Analysis**: Message frequency, timing, patterns
- **Real-Time Scoring**: 0-100 threat level assessment
- **Adaptive Learning**: Model retraining with new data

### Self-Destructing Messages
- **Timer-Based**: Configurable destruction times
- **Read-Once**: Delete after first read
- **Secure Deletion**: Complete key and data destruction
- **Background Cleanup**: Automated expired message removal

## 🎨 Frontend Features

### Chat Interface
- Real-time messaging with WebSocket
- End-to-end encryption indicators
- Self-destruct timer display
- Message status tracking

### Admin Dashboard
- Real-time threat monitoring
- User activity statistics
- Message analytics
- System health indicators

### Security Indicators
- Connection status
- Threat level display
- Encryption status
- AI detection status

## 🚀 Deployment

### Vercel (Frontend)
1. Connect your GitHub repository to Vercel
2. Set build command: `npm run build`
3. Set output directory: `build`
4. Deploy

### Railway (Backend)
1. Connect your GitHub repository to Railway
2. Set environment variables in Railway dashboard
3. Deploy

### Environment Variables
```env
# Backend
MONGODB_URL=your-mongodb-connection-string
JWT_SECRET_KEY=your-jwt-secret-key
PORT=5000

# Frontend
REACT_APP_BACKEND_URL=your-backend-url
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
python -m pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📊 Monitoring

### Threat Detection Metrics
- Message frequency analysis
- IP pattern detection
- Timing anomaly detection
- Behavioral pattern analysis

### System Health
- Database connection status
- Encryption key status
- AI model performance
- Message delivery rates

## 🔒 Security Best Practices

1. **Key Management**
   - Regular key rotation
   - Secure key storage
   - Proper key destruction

2. **Authentication**
   - Strong password requirements
   - JWT token expiration
   - Session management

3. **Data Protection**
   - Encrypted data at rest
   - Encrypted data in transit
   - Secure deletion practices

4. **Monitoring**
   - Real-time threat detection
   - Anomaly logging
   - Security event tracking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review the system architecture

## 🎯 Roadmap

- [ ] Quantum-safe encryption implementation
- [ ] Advanced threat detection models
- [ ] Mobile application
- [ ] Voice message encryption
- [ ] File sharing with encryption
- [ ] Multi-factor authentication
- [ ] Blockchain-based key management

## 🏆 Acknowledgments

- Cryptography library: `cryptography`
- Machine learning: `scikit-learn`
- Frontend framework: `React`
- Styling: `TailwindCSS`
- Charts: `Recharts`

---

**⚠️ Security Notice**: This is a demonstration project. For production use, ensure proper security audits and compliance with relevant regulations.
