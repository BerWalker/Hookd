# controllers/health_controller.py
from flask import Blueprint, jsonify
from extensions import db
from sqlalchemy import text

health_bp = Blueprint('health', __name__)

@health_bp.route("/health")
def health_check():
    try:
        db.session.execute(text("SELECT 1"))
        db.session.commit()
        return jsonify({
            "status": "healthy", 
            "database": "connected",
            "service": "Hook'd"
        }), 200
    except Exception as exc:
        return jsonify({
            "status": "unhealthy", 
            "error": str(exc), 
            "database": "disconnected",
            "service": "Hook'd"
        }), 503

@health_bp.route("/health/detailed")
def detailed_health_check():
    health_status = {
        "service": "Hook'd",
        "version": "1.0.0",
        "checks": {}
    }
    
    try:
        db.session.execute(text("SELECT 1"))
        db.session.commit()
        health_status["checks"]["database"] = {
            "status": "healthy",
            "message": "Database connection successful"
        }
    except Exception as exc:
        health_status["checks"]["database"] = {
            "status": "unhealthy",
            "message": str(exc)
        }
    
    all_healthy = all(check["status"] == "healthy" for check in health_status["checks"].values())
    health_status["overall_status"] = "healthy" if all_healthy else "unhealthy"
    
    return jsonify(health_status), 200 if all_healthy else 503 