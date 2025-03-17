# Personal Fitness Tracker

A comprehensive fitness tracking application that helps users monitor their sleep, nutrition, and workouts while adapting to their daily wellness state.

## Features

- **Sleep Tracking**
  - Sleep duration and quality monitoring
  - Sleep pattern analysis
  - Smart wake-up recommendations

- **Nutrition Tracking**
  - Daily meal logging
  - Nutrient intake analysis
  - Personalized nutrition recommendations
  - Water intake tracking

- **Workout Planning**
  - Dynamic workout adjustments based on wellness state
  - Progress tracking
  - Exercise library
  - Custom workout creation

## Getting Started

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up the environment variables:
   ```bash
   cp .env.example .env
   ```
4. Initialize the database:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```
5. Run the application:
   ```bash
   flask run
   ```

## Project Structure

```
fitness_tracker/
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── routes/
│   ├── services/
│   └── static/
├── tests/
├── .env.example
├── requirements.txt
└── README.md
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 