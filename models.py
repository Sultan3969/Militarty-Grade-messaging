"""
TacticalLink Database Models
Defines data structures for users, messages, and threat logs
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import bcrypt

class User:
    """User model for authentication and encryption"""
    
    def __init__(self, username: str, email: str, is_admin: bool = False):
        self.username = username
        self.email = email
        self.is_admin = is_admin
        self.created_at = datetime.utcnow()
        self.last_login = None
        self.public_key = None
        self.private_key = None
        self.password_hash = None
        self.is_active = True
        
    def set_password(self, password: str):
        """Hash and store password"""
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    def check_password(self, password: str) -> bool:
        """Verify password"""
        if not self.password_hash:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for database storage"""
        return {
            'username': self.username,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': self.created_at,
            'last_login': self.last_login,
            'public_key': self.public_key,
            'private_key': self.private_key,
            'password_hash': self.password_hash,
            'is_active': self.is_active
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """Create User instance from dictionary"""
        user = cls(data['username'], data['email'], data.get('is_admin', False))
        user.created_at = data.get('created_at', datetime.utcnow())
        user.last_login = data.get('last_login')
        user.public_key = data.get('public_key')
        user.private_key = data.get('private_key')
        user.password_hash = data.get('password_hash')
        user.is_active = data.get('is_active', True)
        return user

class Message:
    """Message model for encrypted communication"""
    
    def __init__(self, sender_id: str, recipient_id: str, content: str, 
                 session_key: str, self_destruct_time: int = 0, 
                 read_once: bool = False, timestamp: Optional[datetime] = None,
                 original_content: str = None):
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.content = content  # Encrypted content
        self.original_content = original_content  # Original content for sender
        self.session_key = session_key  # Encrypted session key
        self.self_destruct_time = self_destruct_time  # Seconds until self-destruct
        self.read_once = read_once  # Delete after first read
        self.timestamp = timestamp or datetime.utcnow()
        self.is_read = False
        self.is_deleted = False
        self.destruct_at = None
        
        # Calculate destruction time if specified
        if self_destruct_time > 0:
            self.destruct_at = self.timestamp + timedelta(seconds=self_destruct_time)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for database storage"""
        return {
            'sender_id': self.sender_id,
            'recipient_id': self.recipient_id,
            'content': self.content,
            'original_content': self.original_content,
            'session_key': self.session_key,
            'self_destruct_time': self.self_destruct_time,
            'read_once': self.read_once,
            'timestamp': self.timestamp,
            'is_read': self.is_read,
            'is_deleted': self.is_deleted,
            'destruct_at': self.destruct_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        """Create Message instance from dictionary"""
        message = cls(
            data['sender_id'],
            data['recipient_id'],
            data['content'],
            data['session_key'],
            data.get('self_destruct_time', 0),
            data.get('read_once', False),
            data.get('timestamp', datetime.utcnow()),
            data.get('original_content')
        )
        message.is_read = data.get('is_read', False)
        message.is_deleted = data.get('is_deleted', False)
        message.destruct_at = data.get('destruct_at')
        return message

class ThreatLog:
    """Threat detection log model"""
    
    def __init__(self, user_id: str, threat_score: float, reason: str, 
                 timestamp: Optional[datetime] = None, metadata: Optional[Dict] = None):
        self.user_id = user_id
        self.threat_score = threat_score
        self.reason = reason
        self.timestamp = timestamp or datetime.utcnow()
        self.metadata = metadata or {}
        self.is_resolved = False
        self.resolved_at = None
        self.resolved_by = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for database storage"""
        return {
            'user_id': self.user_id,
            'threat_score': self.threat_score,
            'reason': self.reason,
            'timestamp': self.timestamp,
            'metadata': self.metadata,
            'is_resolved': self.is_resolved,
            'resolved_at': self.resolved_at,
            'resolved_by': self.resolved_by
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ThreatLog':
        """Create ThreatLog instance from dictionary"""
        threat_log = cls(
            data['user_id'],
            data['threat_score'],
            data['reason'],
            data.get('timestamp', datetime.utcnow()),
            data.get('metadata', {})
        )
        threat_log.is_resolved = data.get('is_resolved', False)
        threat_log.resolved_at = data.get('resolved_at')
        threat_log.resolved_by = data.get('resolved_by')
        return threat_log

class SessionKey:
    """Session key model for temporary encryption keys"""
    
    def __init__(self, key_id: str, encrypted_key: str, 
                 created_at: Optional[datetime] = None, expires_at: Optional[datetime] = None):
        self.key_id = key_id
        self.encrypted_key = encrypted_key
        self.created_at = created_at or datetime.utcnow()
        self.expires_at = expires_at
        self.is_destroyed = False
        self.destroyed_at = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for database storage"""
        return {
            'key_id': self.key_id,
            'encrypted_key': self.encrypted_key,
            'created_at': self.created_at,
            'expires_at': self.expires_at,
            'is_destroyed': self.is_destroyed,
            'destroyed_at': self.destroyed_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SessionKey':
        """Create SessionKey instance from dictionary"""
        session_key = cls(
            data['key_id'],
            data['encrypted_key'],
            data.get('created_at', datetime.utcnow()),
            data.get('expires_at')
        )
        session_key.is_destroyed = data.get('is_destroyed', False)
        session_key.destroyed_at = data.get('destroyed_at')
        return session_key

# Database Schema Documentation
"""
MongoDB Collections Schema:

1. users
   - _id: ObjectId
   - username: String (unique)
   - email: String (unique)
   - password_hash: String
   - public_key: String (RSA public key)
   - private_key: String (encrypted RSA private key)
   - is_admin: Boolean
   - is_active: Boolean
   - created_at: DateTime
   - last_login: DateTime

2. messages
   - _id: ObjectId
   - sender_id: ObjectId (reference to users._id)
   - recipient_id: ObjectId (reference to users._id)
   - content: String (AES-256 encrypted)
   - session_key: String (RSA encrypted AES key)
   - self_destruct_time: Integer (seconds)
   - read_once: Boolean
   - timestamp: DateTime
   - is_read: Boolean
   - is_deleted: Boolean
   - destruct_at: DateTime

3. threat_logs
   - _id: ObjectId
   - user_id: ObjectId (reference to users._id)
   - threat_score: Float (0-100)
   - reason: String
   - timestamp: DateTime
   - metadata: Object
   - is_resolved: Boolean
   - resolved_at: DateTime
   - resolved_by: ObjectId (reference to users._id)

4. session_keys
   - _id: ObjectId
   - key_id: String (unique)
   - encrypted_key: String
   - created_at: DateTime
   - expires_at: DateTime
   - is_destroyed: Boolean
   - destroyed_at: DateTime

5. system_logs
   - _id: ObjectId
   - event_type: String
   - user_id: ObjectId (optional)
   - message: String
   - timestamp: DateTime
   - metadata: Object

Indexes:
- users.username: unique
- users.email: unique
- messages.sender_id: index
- messages.recipient_id: index
- messages.timestamp: index
- threat_logs.user_id: index
- threat_logs.timestamp: index
- session_keys.key_id: unique
"""
