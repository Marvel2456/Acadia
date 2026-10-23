# Acadia — Artisan Bakery, Celebration Cakes & Food Ordering Website

A modern, responsive web application for **Acadia**, an artisan bakery and bistro based in Lagos, Nigeria. Specializing in freshly baked treats, savory cooked meals, creative custom celebration cakes, and thoughtful surprise gift packages.

---

## 🎨 Brand Identity & Logo Variations

The visual identity is built around the Acadia brand ethos: *"A Little Sweetness. A Lot of Love."*

### 1. Logo Variations
All 4 client-supplied logo assets are preserved in SVG format in `static/images/logos/`:
- **`acadia-script-character.svg`**: Primary brand header logo featuring the custom Acadia script wordmark and playful baker mascot with chef hat and rolling pin.
- **`acadia-badge.svg`**: Ornate circular badge with monogram initial 'A', botanical flourishes, and year marking.
- **`acadia-badge-lavender.svg`**: Soft lavender badge variant used on light/cream backgrounds.
- **`acadia-wordmark-orange.svg`**: Warm orange script wordmark used for promotional banners and dark backdrops.

### 2. Brand Color Palette (Tailwind Design Tokens)
- **Soft Lime**: `#E0E77A` (`bg-acadia-lime`, `text-acadia-lime`)
- **Lavender**: `#E8A9EF` (`bg-acadia-lavender`, `text-acadia-lavender`)
- **Warm Orange**: `#FFBD55` (`bg-acadia-orange`, `text-acadia-orange`)
- **Cream White**: `#FFFBEF` (`bg-acadia-cream`)
- **Deep Charcoal**: `#171717` (`text-acadia-charcoal`, `bg-acadia-charcoal`)
- **Soft Background**: `#FFFCF7` (`bg-acadia-bg`)

---

## 🚀 Tech Stack

- **Backend**: Python 3.12, Django 6.1
- **Interactivity**: HTMX 1.9.12 (real-time add to cart, live quantity adjustments, search filtering)
- **Frontend & Styling**: Tailwind CSS, Google Fonts (*Playfair Display* & *Plus Jakarta Sans*), Vanilla CSS
- **Database**: SQLite (local development), PostgreSQL ready
- **Media & Assets**: Pillow for image handling, responsive lazy-loaded food photography

---

## 📂 Project Architecture

```
Acadia/
├── catalog/                # Product catalogue, categories, variations & occasions
│   ├── models.py           # Category, Occasion, Product, ProductVariation
│   ├── views.py            # Product list, category filter, product details
│   └── tests.py            # Automated catalog tests
├── orders/                 # Shopping cart, checkout & fulfillment
│   ├── cart.py             # Server-side session cart with database verification
│   ├── models.py           # Order, OrderItem with status tracking
│   ├── views.py            # HTMX cart drawer, add/update/remove, checkout
│   └── tests.py            # Automated order & cart tests
├── enquiries/              # Custom cake builder & surprise packages
│   ├── models.py           # CustomCakeEnquiry, SurprisePackage, SurprisePackageEnquiry
│   ├── forms.py            # Lead-time validation (min 2 days notice) & reference upload
│   ├── views.py            # Custom cake multi-step enquiry, surprise package builder
│   └── tests.py            # Automated enquiry & validation tests
├── cms/                    # Staff dashboard, homepage content, testimonials, site settings
│   ├── models.py           # SiteSettings, HeroSection, PromotionalBanner, Testimonial, Newsletter
│   ├── views.py            # Public home/about/contact, Staff CMS dashboard, sitemap, robots.txt
│   └── forms.py            # Staff forms for products, categories, orders, settings
├── templates/              # Reusable Django templates & HTMX partials
│   ├── base.html           # Central layout, SEO/Open Graph tags, navigation & cart drawer
│   ├── catalog/            # Product catalogue & detail views
│   ├── orders/             # Cart page, drawer, and checkout
│   ├── enquiries/          # Custom cake form & surprise package showcase
│   └── cms/                # Homepage, About, Contact, Staff CMS portal
├── static/                 # CSS, SVGs, brand logos, and photography
└── media/                  # User & staff uploaded product and package images
```

---

## ⚡ Quick Start

### 1. Environment Setup
```bash
# Clone the repository
git clone https://github.com/Marvel2456/Acadia.git
cd Acadia

# Create and activate virtual environment
python3 -m venv env
source env/bin/activate

# Install dependencies
pip install django pillow python-dotenv requests
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

### 3. Database Migrations & Initial Seeding
```bash
# Run database migrations
python manage.py migrate

# Seed database with initial products, categories, packages, and settings
python manage.py seed_acadia
```

### 4. Staff / Admin Credentials
The initial seed command configures a default superuser:
- **Username**: `admin`
- **Password**: `acadia2026`
- **CMS Portal URL**: `http://127.0.0.1:8000/cms/`
- **Django Standard Admin**: `http://127.0.0.1:8000/admin/`

### 5. Run Development Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser.

---

## 🌟 Key Features

### 1. Conversion-Focused Homepage
- Striking hero section with Acadia headline *"A Little Sweetness. A Lot of Love."*
- Dynamic category pills linking directly to filtered product collections.
- Bestsellers showcase in Nigerian Naira (`₦`) with instant HTMX add-to-cart buttons.
- Custom Cake showcase and Surprise Packages featurettes.
- Verified customer testimonials (conditionally rendered only when authentic reviews exist).
- Working newsletter subscription endpoint with server-side validation.

### 2. Product Catalogue (`/shop/`)
- Real-time HTMX category filtering and search without full-page reloads.
- Product variations (e.g. Size, Flavor, Serving options) with dynamic price calculation.
- Lead-time indicators (e.g. "Order 4 hours in advance", "2 days notice required").

### 3. Shopping Cart & Checkout (`/cart/`, `/checkout/`)
- Server-side session cart that recalculates all totals securely against the database.
- Interactive slide-out cart drawer on every page via HTMX.
- Guest checkout with delivery or self-pickup options, customer notes, and payment method selection.
- Unique order reference numbers (e.g. `ACD-XXXXXX`) and order confirmation receipts.

### 4. Bespoke Custom Cake Enquiries (`/custom-cakes/`)
- Multi-field enquiry form: servings/tiers, flavor combinations, occasion, budget tier, and reference image upload.
- Automated server-side lead-time verification (enforces minimum 48-hour advance notice).
- Staff review workflow in the CMS dashboard to assign quotes and manage status.

### 5. Surprise Packages (`/surprise-packages/`)
- Curated celebration hampers with itemized contents list and occasion tags.
- Dedicated booking workflow for recipient details, personalized gift note, and preferred date.

### 6. Staff CMS Dashboard (`/cms/`)
- Real-time business metrics: total products, active orders, pending custom cake requests, and revenue summary.
- Order management: update fulfillment statuses (`Pending`, `Paid`, `Preparing`, `Out for Delivery`, `Completed`).
- Product & Category management: upload images, toggle availability, edit prices in ₦.
- Business settings: configure contact phone numbers, WhatsApp, business hours, and delivery fees.

### 7. Search Engine Optimization & Social Sharing
- Open Graph and Twitter Card tags configured on all pages.
- Dynamically generated `sitemap.xml` listing all active products, categories, and packages.
- Crawl-optimized `robots.txt`.

---

## 🧪 Running Automated Tests

Run the complete test suite:
```bash
python manage.py test
```
All 15 test cases across catalog, orders, enquiries, CMS, and SEO endpoints run with zero errors.

---

## 💳 Payment Gateway (Paystack) Configuration

The application is architected for Paystack integration:
1. Set `PAYSTACK_PUBLIC_KEY` and `PAYSTACK_SECRET_KEY` in your `.env` file.
2. Orders support online card payment, bank transfer, and USSD.
3. For local testing without active API keys, manual bank transfer with staff verification is enabled by default.

---

## 📱 Responsive Design Verification
The website is tested and optimized across all major breakpoints:
- **Mobile**: 320px, 375px, 390px, 430px (slide-out menu, touch-friendly inputs, sticky bottom cart)
- **Tablet**: 768px, 1024px (adaptive 2-to-3 column grids)
- **Desktop & Widescreen**: 1280px, 1440px+ (generous whitespace, editorial imagery layout)
