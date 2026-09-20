const express = require('express');
const { MongoClient } = require('mongodb');
const path = require('path');

const app = express();
app.use(express.json());

// স্ট্যাটিক ফাইল বা ফ্রন্টএন্ড ফাইলের জন্য ফোল্ডার সেটআপ
app.use(express.static(__dirname));

// আপনার সঠিক MongoDB Atlas কানেকশন লিংক
const MONGO_URI = "mongodb+srv://ranaislamrs16_db_user:mdrana321@cluster0.hgumy5c.mongodb.net/?appName=Cluster0";
const client = new MongoClient(MONGO_URI);

let db;

async function startServer() {
    try {
        await client.connect();
        db = client.db(); // ডিফল্ট ডাটাবেজ কানেক্ট হবে
        console.log("Connected to MongoDB successfully!");

        const PORT = process.env.PORT || 10000;
        app.listen(PORT, () => {
            console.log(`Server is running on port ${PORT}`);
        });
    } catch (error) {
        console.error("Failed to connect to MongoDB:", error);
    }
}

startServer();

// ==================== অ্যাডমিন প্যানেল রুটসমূহ ====================

// ১. ব্রাউজারে /admin লিখলে সরাসরি অ্যাডমিন ড্যাশবোর্ড পেজ (admin.html) ওপেন হবে
app.get('/admin', (req, res) => {
    res.sendFile(path.join(__dirname, 'admin.html'));
});

// ২. পেন্ডিং উইথড্র রিকোয়েস্ট দেখার এপিআই
app.get('/api/admin/withdrawals', async (req, res) => {
    try {
        const withdrawals = await db.collection('withdrawals').find({ status: "pending" }, { projection: { _id: 0 } }).toArray();
        res.json({ success: true, withdrawals });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

// ৩. উইথড্র অ্যাপ্রুভ বা পেইড করার এপিআই
app.post('/api/admin/withdrawals/approve', async (req, res) => {
    const { user_id } = req.body;
    try {
        const result = await db.collection('withdrawals').updateOne(
            { user_id: user_id, status: "pending" },
            { $set: { status: "paid" } }
        );
        if (result.modifiedCount > 0) {
            res.json({ success: true, message: "Withdrawal marked as paid successfully!" });
        } else {
            res.status(404).json({ success: false, message: "Request not found or already processed." });
        }
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

// ৪. লাইভ ইউজার এবং র‍্যাঙ্কিং দেখার এপিআই
app.get('/api/admin/users', async (req, res) => {
    try {
        const users = await db.collection('users').find({}, { projection: { _id: 0 } }).sort({ score: -1 }).toArray();
        res.json({
            success: true,
            total_active_users: users.length,
            users: users
        });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});
