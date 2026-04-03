# LearnHub — Digital Learning Platform

A mobile-first digital learning platform built with **Django** and **Wagtail CMS**, selling programming and COBOL courses with integrated Stripe payments. Containerized with Docker for reproducible development environments.

> University project — will serve as the foundation for a bachelor thesis on automated testing and CI/CD.

---

## Features

- **Content Management** — All pages, courses, pricing tiers, and FAQ items are managed through Wagtail's admin interface. No code changes needed to update content.
- **Stripe Checkout** — Real payment integration using Stripe's hosted checkout (test mode). Supports recurring subscriptions for pricing tiers.
- **Mobile-First Design** — Responsive layout with breakpoints at 540px, 640px, 768px, and 900px. Off-canvas navigation with hamburger menu on mobile.
- **Dark Mode** — Full dark/light theme toggle with CSS custom properties, localStorage persistence, and system preference detection.
- **Dynamic Pricing** — Pricing tiers managed via Wagtail admin with drag-and-drop reordering. Each tier connects to a Stripe product via Price ID.
- **Contact Form** — Built with Wagtail's AbstractEmailForm. Fields are configurable from admin. Submissions stored in the database.
- **FAQ Accordion** — Expandable FAQ items managed as inline panels in the CMS.
- **Dockerized** — Single command setup with Docker Compose. Bind mounts for live code editing.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11, Django, Wagtail CMS |
| Database | SQLite |
| Payments | Stripe Checkout (redirect flow) |
| Frontend | HTML5, CSS3 (custom properties), vanilla JavaScript |
| Typography | Fraunces (headings) + DM Sans (body) via Google Fonts |
| Containerization | Docker, Docker Compose |
| Version Control | Git, GitHub |

---

## Pages

| Page | Description |
|------|-------------|
| Home | Hero section, course catalog previews by category |
| Pricing | 3 dynamic tiers (Free / Learner / Professional) with Stripe checkout |
| Course Catalog (×2) | Programming & QA courses, COBOL courses |
| Course Detail (×4) | Individual course pages with StreamField content |
| About | Platform description with team image |
| Contact | Dynamic form (Name, Email, Message) with database-stored submissions |
| FAQ | Accordion-style Q&A managed from admin |

---

## Quick Start

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- A [Stripe account](https://dashboard.stripe.com/register) (free, for test mode)

### 1. Clone the repository

```bash
git clone https://github.com/flwnxt/e-commerce.git
cd e-commerce
```

### 2. Create the environment file

Create a `.env` file in the project root:

```
STRIPE_PUBLIC_KEY=pk_test_your_key_here
STRIPE_SECRET_KEY=sk_test_your_key_here
DJANGO_SETTINGS_MODULE=mysite.settings.dev
```

### 3. Build and run

```bash
docker compose up --build
```

### 4. Access the application

- **Website:** [http://localhost:8000](http://localhost:8000)
- **Admin panel:** [http://localhost:8000/admin/](http://localhost:8000/admin/)

### Admin credentials

```
Username: admin
Password: (ask the team or create one below)
```

To create a new superuser:

```bash
docker compose exec web python manage.py createsuperuser
```

---

## Stripe Setup (Test Mode)

1. Create a free account at [stripe.com](https://dashboard.stripe.com/register)
2. Go to **Developers → API Keys** and copy the test keys into your `.env` file
3. Go to **Products → Add product**:
   - Create **Learner Plan** — €29.00/month (recurring)
   - Create **Professional Plan** — €49.00/month (recurring)
4. Copy each Price ID and paste it into the corresponding pricing tier in Wagtail admin
5. Test with card number `4242 4242 4242 4242` (any future expiry, any CVC)

---

## Project Structure

```
e-commerce/
  ├── .env                     # Stripe keys (not committed)
  ├── .gitignore
  ├── .dockerignore
  ├── Dockerfile
  ├── docker-compose.yml
  └── mysite/
      ├── manage.py
      ├── requirements.txt
      ├── db.sqlite3
      ├── mysite/
      │   ├── settings/
      │   │   ├── base.py      # Shared settings + Stripe config
      │   │   ├── dev.py       # Development overrides
      │   │   └── production.py
      │   ├── templates/
      │   │   └── base.html    # Master template with all CSS/JS
      │   └── urls.py          # URL routing (payment routes + Wagtail catch-all)
      ├── home/
      │   ├── models.py        # HomePage model
      │   └── templates/home/
      │       └── home_page.html
      └── pages/
          ├── models.py        # All page models + PricingTier
          ├── views.py         # Stripe checkout + payment views
          └── templates/pages/
              ├── pricing_page.html
              ├── payment_success.html
              ├── payment_cancel.html
              └── ...
```

---

## Key Architecture Decisions

**Wagtail over WordPress** — Wagtail is a code-first CMS built on Django. Page types are defined as Python models with typed fields, giving us structured content (StreamField) instead of HTML blobs. It fits naturally into the Django/Python ecosystem.

**SQLite over PostgreSQL** — Sufficient for a student project with low traffic. The database file is committed to Git so both team members share the same content and page structure.

**Stripe Checkout (redirect flow)** — Users are redirected to Stripe's hosted payment page. We never handle card data, which means no PCI compliance requirements. Price IDs stored in the CMS connect each tier to a Stripe product.

**Docker** — Ensures identical development environments across machines. One command (`docker compose up --build`) sets up everything. Bind mounts enable live code editing without rebuilding the container.

**Split settings** — `base.py` for shared config, `dev.py` for local development, `production.py` for deployment. Secrets are read from environment variables following the Twelve-Factor App methodology.

---

## Development

### Running without Docker

```bash
cd mysite
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Making model changes

```bash
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
```

### Adding dependencies

```bash
docker compose exec web pip install <package>
docker compose exec web pip freeze > requirements.txt
docker compose up --build       # Rebuild to bake into image
```

---

## Future Work (Bachelor Thesis)

This project will be extended with:

- **Automated testing** — Unit tests, integration tests, and end-to-end tests
- **CI/CD pipeline** — Jenkins pipeline for automated builds, tests, and deployment
- **Production deployment** — PythonAnywhere or similar hosting with production settings

---

## Authors

- **Florescu Dan Stefan**
- **Vasile Maria Alberta**

---

## Built With

- [Django](https://www.djangoproject.com/) — Web framework
- [Wagtail](https://wagtail.org/) — Content management system
- [Stripe](https://stripe.com/) — Payment processing
- [Docker](https://www.docker.com/) — Containerization
- [Google Fonts](https://fonts.google.com/) — Fraunces + DM Sans
