from flask import Blueprint, jsonify, request
from pymongo import MongoClient
import os

# Render বা লোকাল এনভায়রনমেন্ট থেকে ডাটাবেজ কানেকশন নেওয়া
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client.get_database() # আপনার ডিফল্ট ডাটাবেজ কানেক্ট হবে

admin_bp = Blueprint('admin_bp', __name__)

# ১. পেন্ডিং উইথড্র রিকোয়েস্ট দেখার রাউট
@admin_bp.route('/api/admin/withdrawals', methods=['GET'])
def get_pending_withdrawals():
    try:
        # ডাটাবেজ থেকে যেসব উইথড্র 'pending' অবস্থায় আছে তা খোঁজা
        withdrawals = list(db.withdrawals.find({"status": "pending"}, {"_id": 0}))
        return jsonify({"success": True, "withdrawals": withdrawals}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ২. উইথড্র অ্যাপ্রুভ বা পেইড করার রাউট
@admin_bp.route('/api/admin/withdrawals/approve', methods=['POST'])
def approve_withdrawal():
    data = request.json
    user_id = data.get("user_id")
    
    try:
        # ডাটাবেজে স্ট্যাটাস আপডেট করে 'approved' বা 'paid' করা
        result = db.withdrawals.update_one(
            {"user_id": user_id, "status": "pending"},
            {"$set": {"status": "paid"}}
        )
        if result.modified_count > 0:
            return jsonify({"success": True, "message": "Withdrawal marked as paid successfully!"}), 200
        else:
            return jsonify({"success": False, "message": "Request not found or already processed."}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ৩. লাইভ ইউজার এবং র‍্যাঙ্কিং দেখার রাউট
@admin_bp.route('/api/admin/users', methods=['GET'])
def get_live_users():
    try:
        # ইউজারদের লিস্ট এবং তাদের পয়েন্ট বা র‍্যাং অনুযায়ী সাজানো (সর্বোচ্চ পয়েন্ট উপরে থাকবে)
        users = list(db.users.find({}, {"_id": 0}).sort("score", -1))
        total_active_users = len(users)
        
        return jsonify({
            "success": True,
            "total_active_users": total_active_users,
            "users": users
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
