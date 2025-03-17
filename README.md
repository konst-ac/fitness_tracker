# Fitness Tracker Application

A comprehensive fitness tracking application built with Flask that helps users monitor their health and wellness journey.

## Features

- **User Management**
  - Registration and authentication
  - Profile management
  - Secure password handling

- **Sleep Tracking**
  - Record sleep duration and quality
  - Track sleep patterns
  - View sleep analytics

- **Nutrition Tracking**
  - Log meals and nutritional intake
  - Custom food database
  - Nutritional analysis and recommendations

- **Workout Tracking**
  - Log exercises and workouts
  - Create and follow workout plans
  - Track progress over time

- **Wellness Monitoring**
  - Track overall wellness metrics
  - Integrate sleep, nutrition, and workout data
  - Personalized recommendations

## Technical Stack

- **Backend**: Flask (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Flask-Login
- **API**: RESTful with CORS support
- **Database Migrations**: Flask-Migrate

## Project Structure

```
fitness_tracker/
├── app/
│   ├── models/
│   │   ├── user.py
│   │   ├── sleep.py
│   │   ├── nutrition.py
│   │   └── workout.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── sleep.py
│   │   ├── nutrition.py
│   │   └── workout.py
│   └── __init__.py
├── migrations/
├── instance/
├── tests/
├── .env
├── .flaskenv
├── app.py
├── requirements.txt
└── README.md
```

## Setup

1. Create and activate a virtual environment:
```bash
conda create -n fitness_env python=3.11
conda activate fitness_env
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
export FLASK_APP=app.py
export FLASK_DEBUG=1
```

4. Initialize and migrate the database:
```bash
flask db init
flask db migrate
flask db upgrade
```

5. Run the application:
```bash
flask run
```

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout
- `GET /auth/profile` - Get user profile
- `PUT /auth/profile` - Update user profile

### Sleep Tracking
- `POST /sleep/record` - Record sleep data
- `GET /sleep/records` - Get sleep records
- `GET /sleep/analysis` - Get sleep analysis
- `PUT /sleep/record/<id>` - Update sleep record
- `DELETE /sleep/record/<id>` - Delete sleep record

### Nutrition Tracking
- `POST /nutrition/record` - Log meal/nutrition data
- `GET /nutrition/records` - Get nutrition records
- `GET /nutrition/analysis` - Get nutrition analysis
- `POST /nutrition/food` - Add custom food
- `GET /nutrition/foods` - Get custom foods list

### Workout Tracking
- `POST /workout/record` - Log workout
- `GET /workout/records` - Get workout records
- `POST /workout/plan` - Create workout plan
- `GET /workout/plans` - Get workout plans
- `GET /workout/exercises` - Get exercise list

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - feel free to use this project for your own purposes. 