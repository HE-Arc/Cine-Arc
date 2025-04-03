# 🎬 Ciné-Arc — Plateforme de réservation de séances de cinéma

**Ciné-Arc** est une application web complète permettant aux utilisateurs de **consulter les films en salle**, **réserver leurs places**, **payer en ligne** et **recevoir leurs billets** par email. L'application combine une **expérience utilisateur fluide** avec une **interface d’administration** pour gérer les films et les séances.

---

## 🚀 Fonctionnalités principales

### Pour les utilisateurs
- 🔍 Consultation des films en salle (détails récupérés via l'API [TMDB](https://www.themoviedb.org/))
- 🗓 Réservation de séances disponibles
- 🛒 Panier interactif
- 💳 Paiement en ligne avec [Stripe](https://stripe.com/)
- 📩 Réception de billets par email

### Pour les administrateurs
- 🛠 Tableau de bord pour :
  - Ajouter / supprimer des films
  - Gérer les salles et les horaires
  - Suivre les réservations

---

## 🧰 Technologies utilisées

| Côté | Stack |
|------|-------|
| Backend | **Python**, Django, Django REST Framework, Celery, Redis |
| Frontend | **Vue.js 3** + Vite, Axios, Bootstrap |
| Base de données | PostgreSQL |
| Paiement | Stripe |
| Intégration de films | TMDB API |
| Emails | SMTP / Django Email |
| Tâches périodiques | Celery + Redis |

---

## ⚙️ Installation locale (développeur)

### 1. 📦 Backend (Django)
```bash
cd api
pipenv install
pipenv shell
python manage.py migrate
python manage.py createsuperuser  # (optionnel pour admin)
```

### 2. 🚀 Lancer les services (en parallèle)
```bash
# Terminal 1 - serveur Django
python manage.py runserver

# Terminal 2 - tâches périodiques
celery -A cinearc beat --loglevel=info

# Terminal 3 - workers Celery
celery -A cinearc worker -l info --pool=solo -E

# Terminal 4 - Redis (si installé localement)
redis-server
```

### 3. 🎨 Frontend (Vue.js)
```bash
cd frontend
npm install
npm run dev
```

🔗 L'application est ensuite disponible sur : [http://localhost:5173](http://localhost:5173)

---

## 🔐 Variables d’environnement

Crée un fichier `.env` dans `api/` et `frontend/` contenant au minimum :

### Backend (`api/.env`)
```
SECRET_KEY=ton_secret_django
DEBUG=True
DB_NAME=xxx
DB_USER=xxx
DB_PASSWORD=xxx
EMAIL_HOST_USER=xxx
EMAIL_HOST_PASSWORD=xxx
```

### Frontend (`frontend/.env`)
```
VITE_API_URL=http://127.0.0.1:8000/api
```

---

## 👨‍💻 Pour les développeurs

### 📁 Arborescence simplifiée
```
cinearc/
├── api/           # Projet Django (backend)
│   ├── cinearc/   # Core Django
│   └── cinearcapp/ # App principale : utilisateurs, films, réservations
├── frontend/      # Projet Vue.js (frontend)
│   └── src/
```

### ✨ Bonnes pratiques

- 🔁 Tâches périodiques à lancer pour récupérer les films TMDB automatiquement :
```bash
python manage.py schedule_tasks
```

---

## 🤝 Contributeurs

- Annen Julien
- Berthoud Simon
- Dos Santos Ribeiro Bryan
- Teuscher Marylin

---


Ce projet a été réalisé dans le cadre du cours de développement web 2 (3255.2 DW) à l'He-Arc.
