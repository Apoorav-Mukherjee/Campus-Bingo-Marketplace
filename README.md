# 🛒 Bingo — Campus Marketplace

A student-only buy-and-sell web application built with Django. Bingo lets verified college students list, discover, and purchase items from fellow students — all within a trusted campus community.

---

## 📸 Features

| Feature | Description |
|---|---|
| 🎓 Student-Only Auth | Registration restricted to verified college email domains |
| 📦 Product Listings | Create, edit, delete listings with multiple image uploads |
| 🗂️ Categories | Browse and filter by category (Books, Electronics, Clothing, etc.) |
| 🔍 Search & Filter | Search by keyword, filter by condition, sort by price or date |
| 💬 Buyer–Seller Chat | Simple messaging system between buyers and sellers |
| ✅ Mark as Sold | Sellers can toggle listing status between Available and Sold |
| 📋 My Listings | Personal dashboard with Active / Sold / All tabs |
| 🔔 Unread Badges | Live unread message count in the navbar |
| 🏠 Landing Page | Marketing page for logged-out visitors |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 5.x (Python) |
| Database | SQLite (MVP) |
| Frontend | Bootstrap 5 + Bootstrap Icons |
| Auth | Django Custom User Model |
| File Storage | Django FileField + Pillow |
| Views | Class-Based Views (CBV) |

---

## 📁 Project Structure

```
bingo_project/
├── bingo_project/               # Core Django project
│   ├── settings.py              # Project settings
│   ├── urls.py                  # Root URL configuration
│   ├── views.py                 # Custom error handlers (404, 403, 500)
│   └── context_processors.py   # Global unread message count
│
├── accounts/                    # Custom user authentication app
│   ├── models.py                # Custom User model (extends AbstractUser)
│   ├── forms.py                 # Registration, Login, Profile forms
│   ├── views.py                 # Register, Login, Logout, Profile views
│   └── urls.py                  # Auth URL routes
│
├── marketplace/                 # Core marketplace app
│   ├── models.py                # Category, Product, ProductImage models
│   ├── forms.py                 # ProductForm with multiple image upload
│   ├── views.py                 # All product CRUD views + Landing
│   └── urls.py                  # Marketplace URL routes
│
├── chat/                        # Messaging app
│   ├── models.py                # ChatRoom and Message models
│   ├── views.py                 # Inbox, ChatRoom, start_chat views
│   └── urls.py                  # Chat URL routes
│
├── templates/                   # Global templates
│   ├── base.html                # Base layout with navbar and footer
│   ├── landing.html             # Guest landing page
│   ├── 404.html                 # Custom 404 page
│   ├── 403.html                 # Custom 403 page
│   ├── accounts/                # Auth templates
│   ├── marketplace/             # Product templates
│   └── chat/                    # Chat templates
│
├── media/                       # Uploaded files (runtime)
├── static/                      # Static assets
├── db.sqlite3                   # SQLite database
├── manage.py
└── requirements.txt
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/Apoorav-Mukherjee/OLX.git
cd OLX
```

### 2. Create and activate a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure allowed email domains

Open `bingo_project/settings.py` and update:

```python
# Add your college email domains here
ALLOWED_EMAIL_DOMAINS = ['college.edu', 'university.edu']

# Set to empty list [] to allow ALL emails during development
ALLOWED_EMAIL_DOMAINS = []
```

### 5. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a superuser (for admin access)

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

---

## 🌱 Seed Initial Data

After running the server, go to `http://127.0.0.1:8000/admin/` and add categories:

| Name | Slug | Icon |
|------|------|------|
| Books | books | bi-book |
| Electronics | electronics | bi-laptop |
| Clothing | clothing | bi-bag |
| Furniture | furniture | bi-house |
| Sports | sports | bi-trophy |
| Stationery | stationery | bi-pencil |
| Others | others | bi-grid |

---

## 🗺️ URL Reference

### Accounts
| URL | View | Description |
|-----|------|-------------|
| `/accounts/register/` | RegisterView | Student registration |
| `/accounts/login/` | LoginView | Login with college email |
| `/accounts/logout/` | LogoutView | Logout |
| `/accounts/profile/` | ProfileView | View & edit profile |

### Marketplace
| URL | View | Description |
|-----|------|-------------|
| `/` | LandingView | Guest landing page |
| `/listings/` | ProductListView | Browse all listings |
| `/my-listings/` | MyListingsView | Seller dashboard |
| `/listings/new/` | ProductCreateView | Post a new listing |
| `/listings/<pk>/` | ProductDetailView | View product detail |
| `/listings/<pk>/edit/` | ProductEditView | Edit listing (seller only) |
| `/listings/<pk>/delete/` | ProductDeleteView | Delete listing (seller only) |
| `/listings/<pk>/sold/` | mark_as_sold | Toggle sold status |
| `/images/<id>/delete/` | delete_product_image | Remove a product image |

### Chat
| URL | View | Description |
|-----|------|-------------|
| `/chat/` | InboxView | All conversations |
| `/chat/start/<product_pk>/` | start_chat | Start or resume a chat |
| `/chat/room/<room_pk>/` | ChatRoomView | Read and send messages |

---

## 🔐 Authentication & Security

- **Custom User model** using `email` as the `USERNAME_FIELD`
- **College email validation** — domain checked against `ALLOWED_EMAIL_DOMAINS` in settings
- **Login required** on all create, edit, delete, chat, and profile routes
- **Seller-only protection** — edit/delete views return 404 if non-owner attempts access
- **CSRF protection** on all forms including logout
- **Nested form prevention** — image delete forms are rendered outside the product edit form to prevent accidental submissions

---

## 💬 Chat System

- One `ChatRoom` is created per **buyer + product** pair (enforced by `unique_together`)
- Sellers cannot initiate chats on their own listings
- Messages are marked as **read** when the recipient opens the chat room
- **Unread count** is injected globally via a context processor and displayed as a badge in the navbar
- Chat is **disabled** (input locked) once a product is marked as sold

---

## 🖼️ Multiple Image Upload

- Uses a custom `MultipleFileField` + `MultipleFileInput` widget
- Supports selecting multiple files at once (hold `Ctrl`/`Cmd`)
- Images stored under `media/product_images/`
- Sellers can remove individual images from the edit page
- Primary image (first uploaded) is shown as the listing thumbnail

---

## 📦 Dependencies

```
Django==5.0.6
Pillow==10.3.0
```

Install with:

```bash
pip install -r requirements.txt
```

---

## 🚧 MVP Limitations (Not Implemented)

These features are intentionally excluded from Version 1:

- ❌ Real-time chat (WebSockets)
- ❌ Payment / escrow system
- ❌ Product reviews and ratings
- ❌ Listing boost / promotion
- ❌ Push notifications
- ❌ AI-powered search
- ❌ Email verification
- ❌ Production deployment configuration

---

## 🔮 Future Roadmap (Post-MVP)

- [ ] WebSocket real-time chat with Django Channels
- [ ] Email verification on registration
- [ ] Password reset via email
- [ ] Product wishlist / saved listings
- [ ] Seller ratings and reviews
- [ ] Offer / negotiation system
- [ ] Advanced image management (reorder, crop)
- [ ] PostgreSQL for production
- [ ] Deployment to Railway / Render / AWS
- [ ] REST API + React frontend

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

Built with ❤️ as a Django MVP project.

> **Bingo** — Because finding a deal on campus should be as easy as calling it out.
