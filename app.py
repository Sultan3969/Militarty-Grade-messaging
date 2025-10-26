"""
TacticalLink Backend - AI-Powered Military-Grade Messaging System
Main Flask application with all API endpoints
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from routes.private_message import private_bp

import os
from dotenv import load_dotenv
import threading
import time

# Import our modules
from database import Database
from encryption import EncryptionManager
from ai_threat import ThreatDetector
from message_scheduler import MessageScheduler
from models import User, Message, ThreatLog


# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'tactical-link-secret-key-2024')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
app.register_blueprint(private_bp, url_prefix="/chat/private")

# Initialize extensions
jwt = JWTManager(app)
CORS(app)

# Initialize components
db = Database()
encryption_manager = EncryptionManager()
threat_detector = ThreatDetector()
message_scheduler = MessageScheduler()

# Global variables for real-time threat monitoring
threat_scores = {}
active_users = set()

@app.route('/')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'TacticalLink Backend',
        'timestamp': datetime.utcnow().isoformat()
    })

# Authentication endpoints
@app.route('/auth/register', methods=['POST'])
def register():
    """User registration endpoint"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        
        if not username or not password or not email:
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Check if user already exists
        if db.get_user_by_username(username):
            return jsonify({'error': 'Username already exists'}), 409
        
        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        
        # Generate encryption keys
        user.public_key, user.private_key = encryption_manager.generate_key_pair()
        
        # Save to database
        user_id = db.create_user(user)
        
        # Create JWT token
        access_token = create_access_token(identity=user_id)
        
        return jsonify({
            'message': 'User registered successfully',
            'access_token': access_token,
            'user_id': user_id,
            'public_key': user.public_key
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/auth/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Missing credentials'}), 400
        
        # Authenticate user
        user = db.authenticate_user(username, password)
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Update last login
        db.update_last_login(user['_id'])
        
        # Add to active users
        active_users.add(user['_id'])
        
        # Create JWT token
        access_token = create_access_token(identity=str(user['_id']))
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user_id': str(user['_id']),
            'username': user['username'],
            'public_key': user['public_key']
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Chat endpoints
@app.route('/chat/send', methods=['POST'])
@jwt_required()
def send_message():
    """Send encrypted message"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        recipient_id = data.get('recipient_id')
        message_content = data.get('message')
        self_destruct_time = data.get('self_destruct_time', 0)  # 0 = no self-destruct
        read_once = data.get('read_once', False)
        
        if not recipient_id or not message_content:
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Get recipient's public key
        recipient = db.get_user_by_id(recipient_id)
        if not recipient:
            return jsonify({'error': 'Recipient not found'}), 404
        
        # Encrypt message
        encrypted_message, session_key = encryption_manager.encrypt_message(
            message_content, recipient['public_key']
        )
        
        # Create message object
        message = Message(
            sender_id=current_user_id,
            recipient_id=recipient_id,
            content=encrypted_message,
            session_key=session_key,
            self_destruct_time=self_destruct_time,
            read_once=read_once,
            timestamp=datetime.utcnow(),
            original_content=message_content  # Store original content for sender
        )
        
        # Save message to database
        message_id = db.create_message(message)
        
        # Schedule self-destruct if specified
        if self_destruct_time > 0:
            message_scheduler.schedule_destruction(
                message_id, self_destruct_time, read_once
            )
        
        # AI Threat Detection
        threat_score = threat_detector.analyze_message_metadata(
            sender_id=current_user_id,
            recipient_id=recipient_id,
            message_length=len(message_content),
            timestamp=datetime.utcnow()
        )
        
        # Log threat if score is high
        if threat_score > 70:
            threat_log = ThreatLog(
                user_id=current_user_id,
                threat_score=threat_score,
                reason="High message frequency or suspicious pattern",
                timestamp=datetime.utcnow()
            )
            db.create_threat_log(threat_log)
        
        return jsonify({
            'message': 'Message sent successfully',
            'message_id': message_id,
            'threat_score': threat_score
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/chat/receive', methods=['GET'])
@jwt_required()
def receive_messages():
    """Receive and decrypt messages"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get user's private key
        user = db.get_user_by_id(current_user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get pending messages
        messages = db.get_pending_messages(current_user_id)
        
        decrypted_messages = []
        for msg in messages:
            try:
                # Decrypt message
                decrypted_content = encryption_manager.decrypt_message(
                    msg['content'], msg['session_key'], user['private_key']
                )
                
                decrypted_messages.append({
                    'id': str(msg['_id']),
                    'sender_id': msg['sender_id'],
                    'recipient_id': msg['recipient_id'],
                    'content': decrypted_content,
                    'timestamp': msg['timestamp'].isoformat(),
                    'read_once': msg['read_once']
                })
                
                # Mark as read
                db.mark_message_as_read(msg['_id'])
                
                # Delete immediately if read_once is True
                if msg['read_once']:
                    db.delete_message(msg['_id'])
                    encryption_manager.destroy_key(msg['session_key'])
                
            except Exception as e:
                print(f"Error decrypting message {msg['_id']}: {e}")
                continue
        
        return jsonify({
            'messages': decrypted_messages,
            'count': len(decrypted_messages)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Self-destruct endpoint
@app.route('/delete/message/<message_id>', methods=['DELETE'])
@jwt_required()
def delete_message(message_id):
    """Manually delete a message"""
    try:
        current_user_id = get_jwt_identity()
        
        # Verify ownership
        message = db.get_message_by_id(message_id)
        if not message:
            return jsonify({'error': 'Message not found'}), 404
        
        if message['sender_id'] != current_user_id and message['recipient_id'] != current_user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Delete message and destroy keys
        db.delete_message(message_id)
        encryption_manager.destroy_key(message['session_key'])
        
        return jsonify({'message': 'Message deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Threat detection endpoints
@app.route('/threat/analyze', methods=['POST'])
@jwt_required()
def analyze_threat():
    """Analyze threat level for current session"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get user's recent activity
        recent_messages = db.get_user_recent_messages(current_user_id, limit=50)
        
        # Analyze threat level
        threat_score = threat_detector.analyze_user_activity(
            user_id=current_user_id,
            messages=recent_messages
        )
        
        # Update global threat scores
        threat_scores[current_user_id] = threat_score
        
        return jsonify({
            'threat_score': threat_score,
            'risk_level': 'HIGH' if threat_score > 70 else 'MEDIUM' if threat_score > 40 else 'LOW',
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Admin endpoints
@app.route('/admin/dashboard', methods=['GET'])
@jwt_required()
def admin_dashboard():
    """Get admin dashboard data"""
    try:
        current_user_id = get_jwt_identity()
        
        # Check if user is admin (simplified - in production, use proper role-based access)
        user = db.get_user_by_id(current_user_id)
        if not user or not user.get('is_admin', False):
            return jsonify({'error': 'Admin access required'}), 403
        
        # Get dashboard data
        total_users = db.get_total_users()
        active_user_count = len(active_users)
        recent_threats = db.get_recent_threat_logs(limit=20)
        message_stats = db.get_message_statistics()
        
        return jsonify({
            'total_users': total_users,
            'active_users': active_user_count,
            'threat_scores': threat_scores,
            'recent_threats': recent_threats,
            'message_stats': message_stats,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/chat/conversation/<recipient_id>', methods=['GET'])
@jwt_required()
def get_conversation(recipient_id):
    """Get conversation messages between current user and recipient"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get user's private key
        user = db.get_user_by_id(current_user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get conversation messages (both sent and received)
        messages = db.get_conversation_messages(current_user_id, recipient_id)
        
        decrypted_messages = []
        for msg in messages:
            try:
                # Only decrypt messages sent TO current user
                if msg['recipient_id'] == current_user_id:
                    decrypted_content = encryption_manager.decrypt_message(
                        msg['content'], msg['session_key'], user['private_key']
                    )
                else:
                    # For sent messages, use original content
                    decrypted_content = msg.get('original_content', '[Message sent]')
                
                decrypted_messages.append({
                    'id': str(msg['_id']),
                    'sender_id': msg['sender_id'],
                    'recipient_id': msg['recipient_id'],
                    'content': decrypted_content,
                    'timestamp': msg['timestamp'].isoformat(),
                    'read_once': msg['read_once'],
                    'is_read': msg['is_read']
                })
                
            except Exception as e:
                print(f"Error processing message {msg['_id']}: {e}")
                continue
        
        return jsonify({
            'messages': decrypted_messages,
            'count': len(decrypted_messages)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/chat/users', methods=['GET'])
@jwt_required()
def get_chat_users():
    """Get users for chat (all authenticated users)"""
    try:
        current_user_id = get_jwt_identity()
        print(f"Getting chat users for user: {current_user_id}")
        
        # Get all active users except current user
        users = db.get_all_users()
        print(f"Total users in database: {len(users)}")
        
        chat_users = [user for user in users if user['_id'] != current_user_id]
        print(f"Chat users (excluding current): {len(chat_users)}")
        
        return jsonify({'users': chat_users}), 200
        
    except Exception as e:
        print(f"Error getting chat users: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/admin/users', methods=['GET'])
@jwt_required()
def get_all_users():
    """Get all users (admin only)"""
    try:
        current_user_id = get_jwt_identity()
        
        # Check admin access
        user = db.get_user_by_id(current_user_id)
        if not user or not user.get('is_admin', False):
            return jsonify({'error': 'Admin access required'}), 403
        
        users = db.get_all_users()
        return jsonify({'users': users}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Auth verification endpoint
@app.route('/auth/verify', methods=['GET'])
@jwt_required()
def verify_auth():
    """Verify JWT token and return user info"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get user info
        user = db.get_user_by_id(current_user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user_id': current_user_id,
            'username': user['username'],
            'is_admin': user.get('is_admin', False),
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# WebSocket endpoint for real-time updates (simplified with polling)
@app.route('/ws/status', methods=['GET'])
@jwt_required()
def websocket_status():
    """Get real-time status updates"""
    try:
        current_user_id = get_jwt_identity()
        
        return jsonify({
            'user_id': current_user_id,
            'threat_score': threat_scores.get(current_user_id, 0),
            'active_users': list(active_users),
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Background task for threat monitoring
def threat_monitoring_task():
    """Background task for continuous threat monitoring"""
    while True:
        try:
            # Analyze all active users
            for user_id in active_users.copy():
                recent_messages = db.get_user_recent_messages(user_id, limit=10)
                threat_score = threat_detector.analyze_user_activity(
                    user_id, recent_messages
                )
                threat_scores[user_id] = threat_score
                
                # Log high threat scores
                if threat_score > 80:
                    threat_log = ThreatLog(
                        user_id=user_id,
                        threat_score=threat_score,
                        reason="Automated threat detection - high risk",
                        timestamp=datetime.utcnow()
                    )
                    db.create_threat_log(threat_log)
            
            time.sleep(30)  # Check every 30 seconds
            
        except Exception as e:
            print(f"Error in threat monitoring: {e}")
            time.sleep(60)

# Start background tasks
if __name__ == '__main__':
    # Start threat monitoring in background thread
    threat_thread = threading.Thread(target=threat_monitoring_task, daemon=True)
    threat_thread.start()
    
    # Start message scheduler
    message_scheduler.start()
    
    # Run Flask app
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
