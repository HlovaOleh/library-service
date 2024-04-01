# library-service

This app was created for managing library data, with information on books, borrowings and payments regarding them.

# Implemented:
    - CRUD for Books, Borrowings and Users
    - Stripe Payment system
    - Telegram notifications
    - Scheduled tasks
    - Project documentation

# .env

Before running the project either in Docker or locally, you need to create .env file in the project`s root directory.
You can fill it with this data or create it from .env.sample with your own:

- STRIPE_SECRET_KEY=STRIPE_SECRET_KEY
- STRIPE_PUBLISHABLE_KEY=STRIPE_PUBLISHABLE_KEY
- POSTGRES_HOST=db
- POSTGRES_DB=library
- POSTGRES_USER=postgres
- POSTGRES_PASSWORD=postgres
- RABBIT_URL=amqp://guest:guest@rabbitmq3:5672/
- DOMAIN=http://localhost:8080
- TELEGRAM_BOT_TOKEN=TELEGRAM_BOT_TOKEN
- CHAT_URL=CHAT_URL

You can get stripe keys here: https://stripe.com/
Chat URL is for your telegram chat`s url, and you can get Telegram Bot Token here: https://t.me/BotFather

# Lauching project locally

To launch the application, follow next steps:

1. Fork the repository

2. Clone it:
`git clone <here goes the HTTPS link you could copy on github repositiry page>`

3. Create a new branch:
`git checkout -b <new branch name>`

4. Create virtual environment:
`python -m venv venv`

5. Activate venv:
`source venv/Scripts/activate`

6. Install requirements:
`pip install -r requirements.txt`

7. Run migrations:
`python manage.py migrate`

8. Load the data from fixture:
`python manage.py loaddata books_fixture.json`

9. Run server:
`python manage.py runserver`

To run the tests:

`python manage.py test book/tests`

`python manage.py test customer/tests`

`python manage.py test payment/tests`

# Running with docker

After installing Docker run:
- docker-compose build
- docker-compose up 
