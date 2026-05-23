from flask import Flask, render_template, request, redirect
from flask_mail import Mail, Message
from datetime import datetime

app = Flask(__name__)

# ===================================================
# 🛠️ GMAIL BACKEND MAIL SETUP
# ===================================================
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'Vickydaksh17@gmail.com'

# ⚠️ APNA GOOGLE WALA 16-DIGIT PASSWORD YAHAN BINA SPACES KE PASTE KARO
app.config['MAIL_PASSWORD'] = 'vuvkwhyekzlzchqf' 

mail = Mail(app)

# ===================================================
# 📊 LIVE TRACKING DATA SYSTEM (Global Memory)
# ===================================================
user_info = {
    "name": "Duggu Sharma"
}

visitor_stats = {
    "total_count": 0,
    "history": []
}

# ===================================================
# 🌐 MAIN HOME PAGE ROUTE (With Live Visitor Tracker)
# ===================================================
@app.route('/')
def index():
    # 1. Visitor count ko ek badhao
    visitor_stats["total_count"] += 1
    
    # 2. Visitor ki unique network details nikalna
    visitor_ip = request.remote_addr 
    user_agent = request.headers.get('User-Agent') 
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 3. Data record generate karna
    visitor_data = {
        "ip": visitor_ip,
        "time": current_time,
        "browser": user_agent[:50] + "..." if user_agent else "Unknown"
    }
    visitor_stats["history"].append(visitor_data)
    
    # 4. Command prompt / terminal par live alert print karna
    print(f"\n📢 [NEW VISITOR ALERT] 🕒 Time: {current_time} | 🌐 IP: {visitor_ip}")
    print(f"🖥️ Browser: {visitor_data['browser']}\n")
    
    # 5. Front-end ko total counts ke sath render karna
    return render_template('index.html', user=user_info, total_visitors=visitor_stats["total_count"])

# ===================================================
# 📩 DUGGU KA LIVE FORM ROUTE (Ab bilkul sahi jagah par hai)
# ===================================================
@app.route('/send_message', methods=['POST'])
def send_message():
    if request.method == 'POST':
        # Form se data nikal rahe hain
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        user_msg = request.form.get('message')

        # Email ka dappa taiyar ho raha hai
        msg = Message(
            subject=f"🔥 New Portfolio Message from {name}!",
            sender=app.config['MAIL_USERNAME'],
            recipients=['Vickydaksh17@gmail.com'] # Isi par mail aayegi
        )
        
        msg.body = f"""
        Hey Duggu, aapke portfolio par ek naya message aaya hai!

        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        👤 Name  : {name}
        📧 Email : {email}
        📞 Phone : {phone}
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        💬 Message:
        {user_msg}

        — Automated Portfolio System
        """

        try:
            mail.send(msg)
            print("🚀 Chakachak! Email chali gayi!")
        except Exception as e:
            print(f"❌ Koi gadbad hui: {e}")

        # Message bhejkar page wapas normal reload ho jayega ek pop-up ke saath
        return redirect('/?success=true')

# ===================================================
# 🚀 SERVER START ENGINE (Sabse Aakhiri Mein)
# ===================================================
if __name__ == '__main__':
    app.run(debug=True)