from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from threading import Timer

from encryption import EncryptionManager
from ai_threat import ThreatDetector
from database import Database
from message_scheduler import MessageScheduler
from models import Message, ThreatLog

private_bp = Blueprint("private_bp", __name__)

# use your existing components
db = Database()
encryption_manager = EncryptionManager()
threat_detector = ThreatDetector()
message_scheduler = MessageScheduler()


@private_bp.route("/send", methods=["POST"])
@jwt_required()
def send_private_message():
    """
    Send an encrypted private message to one target within a group.
    Default self-destruct: 60 seconds.
    """
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()

        group_id = data.get("group_id")
        target_id = data.get("target_user_id")
        message_content = data.get("message")
        self_destruct_time = data.get("self_destruct_time", 60)
        read_once = data.get("read_once", True)

        if not target_id or not message_content:
            return jsonify({"error": "Missing required fields"}), 400

        # get recipient
        recipient = db.get_user_by_id(target_id)
        if not recipient:
            return jsonify({"error": "Target user not found"}), 404

        # encrypt content
        encrypted_message, session_key = encryption_manager.encrypt_message(
            message_content, recipient["public_key"]
        )

        # create message object
        message = Message(
            sender_id=current_user_id,
            recipient_id=target_id,
            group_id=group_id,
            content=encrypted_message,
            session_key=session_key,
            self_destruct_time=self_destruct_time,
            read_once=read_once,
            timestamp=datetime.utcnow(),
            original_content=message_content
        )

        message_id = db.create_message(message)

        # schedule self-destruct (always)
        message_scheduler.schedule_destruction(
            message_id, self_destruct_time, read_once
        )

        # AI threat analysis
        threat_score = threat_detector.analyze_message_metadata(
            sender_id=current_user_id,
            recipient_id=target_id,
            message_length=len(message_content),
            timestamp=datetime.utcnow()
        )

        if threat_score > 70:
            log = ThreatLog(
                user_id=current_user_id,
                threat_score=threat_score,
                reason="Private message flagged by AI",
                timestamp=datetime.utcnow()
            )
            db.create_threat_log(log)

        return jsonify({
            "success": True,
            "message_id": message_id,
            "target_id": target_id,
            "self_destruct_time": self_destruct_time,
            "threat_score": threat_score
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
