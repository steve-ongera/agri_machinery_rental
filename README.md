# 🚜 AgriRent — Affordable Farm Machinery for Every Smallholder
### Mechanizing African Agriculture, One Rental at a Time

---

## 👨‍💻 Lead Developer

**Steve Ongera**
Software Developer
📞 +254 112 284 093
📧 steveongera001@gmail.com

---

## 🌍 The Problem

Over 70% of Africa's food is produced by smallholder farmers — families working 1 to 10 acres of land with hand tools, relying on seasonal rain and manual labor. When the planting window opens, it lasts only a few weeks. A farmer who cannot afford or access a tractor in time loses an entire season. A season lost can mean a family going hungry.

Tractor ownership is completely out of reach for most smallholders. Hiring through informal brokers is unreliable, overpriced, and often leads to disputes. There is no accountability, no pricing transparency, and no way to plan. Labor shortages driven by rural-urban migration have made the situation worse.

The result: low yields, high production costs, wasted land, and a generation of farmers abandoning agriculture entirely.

---

## 💡 The Solution

**AgriRent** is a digital marketplace that connects smallholder farmers with tractor owners and equipment operators across Kenya and East Africa. Farmers can browse available machinery, book it for specific dates, pay securely via mobile money, and track the operator in real time.

For equipment owners, AgriRent unlocks income from underutilized assets. A tractor sitting idle for six months a year becomes a revenue-generating business. For farmers, it means affordable, reliable access to mechanization without the capital cost of ownership.

The platform delivers:
- Verified equipment listings with real photos and specifications
- Transparent, upfront pricing with no hidden broker fees
- Secure mobile money payments (M-Pesa, Airtel Money)
- GPS tracking of equipment during jobs
- Two-way reviews building trust between farmers and operators
- SMS booking confirmations for farmers without smartphones

---

## 🎯 My Transformation Goals

As lead developer, I am not building a rental app. I am building the infrastructure layer for African agricultural mechanization.

**Goal 1 — Make Mechanization Accessible Within 50km of Every Farmer**
Right now, a farmer in a remote county cannot find a tractor even if they have the money. I am building a geo-based discovery engine so that any farmer, anywhere, can find verified equipment within their radius — and book it in under 5 minutes.

**Goal 2 — Eliminate the Middleman and Return Margin to Farmers and Operators**
Traditional equipment brokers take 20–40% cuts while adding no value. AgriRent charges a fair, transparent platform fee and routes the rest directly to operators via instant mobile money payouts. Farmers pay less. Operators earn more.

**Goal 3 — Build the Data Layer for African Agricultural Finance**
Every booking on this platform is a data point — what crops are being planted, where, when, at what scale. This data is gold for banks, insurance companies, and input suppliers who have never had reliable smallholder data. I will build anonymized data products that unlock financing for farmers who have never had a credit history.

**Goal 4 — Extend to Full Farm Input Logistics**
Machinery rental is phase one. Phase two adds seed, fertilizer, and agrochemical delivery — booked at the same time as the tractor. Phase three adds post-harvest handling: threshers, dryers, and cold storage. AgriRent becomes the full logistics operating system for smallholder farming.

**Goal 5 — Empower Equipment Owners to Build Real Businesses**
Many tractor owners are individuals or small cooperatives with no business management tools. I will build in-app earnings dashboards, maintenance scheduling, loan application tools using rental history as collateral, and operator training resources — turning asset owners into agri-entrepreneurs.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 4.x + Django REST Framework |
| Database | PostgreSQL + PostGIS (geospatial) |
| Cache | Redis |
| Task Queue | Celery + Celery Beat |
| Storage | AWS S3 |
| Maps & GPS | Google Maps API / Mapbox |
| Payments | M-Pesa Daraja API + Flutterwave |
| SMS | Africa's Talking |
| Auth | JWT (SimpleJWT) |
| Frontend | React.js + React Native |
| Deployment | Docker + AWS |

---

## 📁 Project Structure

```
agri_machinery_rental/
├── config/                  # Django project settings
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── core/                    # Main application
│   ├── models.py            # All data models
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
├── templates/
│   └── core/
├── static/
├── media/
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 🚀 Getting Started

```bash
# Clone the repository
git clone https://github.com/steveongera/agri-machinery-rental.git
cd agri_machinery_rental

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env — include M-Pesa Daraja keys, DB credentials, Google Maps key

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

---

## 🌱 Roadmap

- [x] Core models — Equipment, Bookings, Payments, Reviews
- [ ] REST API with DRF
- [ ] M-Pesa Daraja STK Push integration
- [ ] Operator GPS tracking (WebSockets)
- [ ] PostGIS-powered equipment proximity search
- [ ] Automated payout system (post-job completion)
- [ ] Farmer mobile app (React Native)
- [ ] Agricultural data analytics dashboard
- [ ] Bank/MFI integration for equipment financing

---

## 🤝 Contributing

Reach out if you are a developer, agronomist, or agri-finance professional who wants to build this vision with me.

📧 steveongera001@gmail.com
📞 +254 112 284 093

---

## 📄 License

MIT License — built for Africa's farmers.

---

*"A tractor shared is a harvest multiplied. Technology should put that tractor in reach of every farmer, not just the wealthy ones."*
*— Steve Ongera, Lead Developer*