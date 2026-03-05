
"""
AI Assistant Routes for ApnaGrocery
Handles chat requests and provides AI-powered insights
"""
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from services.ai_service import ai_assistant

ai = Blueprint("ai", __name__)


@ai.route("/ai-assistant")
@login_required
def assistant():
    """Main AI Assistant page with chat interface"""
    # Get auto-insights for the dashboard section
    insights = ai_assistant.get_auto_insights()
    return render_template("ai_assistant.html", insights=insights)


@ai.route("/ai/chat", methods=["POST"])
@login_required
def chat():
    """Handle AI chat requests"""
    data = request.get_json()
    user_query = data.get("message", "").strip()
    
    if not user_query:
        return jsonify({"error": "Please enter a message"}), 400
    
    # Get context about the current user
    user_context = {
        "username": current_user.username,
        "role": current_user.role
    }
    
    # Process the query
    response = ai_assistant.process_query(user_query, user_context)
    
    return jsonify({
        "response": response,
        "timestamp": "Just now"
    })


@ai.route("/ai/insights", methods=["GET"])
@login_required
def insights():
    """Get automatic business insights"""
    analysis = ai_assistant.analyze_business()
    return jsonify(analysis)


@ai.route("/ai/analyze", methods=["GET"])
@login_required
def analyze():
    """Get detailed business analysis"""
    analysis = ai_assistant.analyze_business()
    return jsonify({
        "success": True,
        "analysis": analysis
    })


@ai.route("/ai/alerts", methods=["GET"])
@login_required
def alerts():
    """Get current alerts"""
    alerts = ai_assistant.get_low_stock_alerts()
    return jsonify({"alerts": alerts})


@ai.route("/ai/inventory", methods=["GET"])
@login_required
def inventory():
    """Get inventory summary"""
    inventory = ai_assistant.get_inventory_summary()
    return jsonify(inventory)


@ai.route("/ai/sales", methods=["GET"])
@login_required
def sales():
    """Get sales summary"""
    sales = ai_assistant.get_sales_summary()
    return jsonify(sales)

