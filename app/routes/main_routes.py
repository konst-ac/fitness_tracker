from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

main_routes = Blueprint('main_routes', __name__)

@main_routes.route('/')
def index():
    return render_template('index.html')

@main_routes.route('/sleep', methods=['GET', 'POST'])
@login_required
def sleep():
    if request.method == 'POST':
        # Handle sleep log submission
        date = request.form.get('date')
        sleep_time = request.form.get('sleep_time')
        wake_time = request.form.get('wake_time')
        quality = request.form.get('quality')
        notes = request.form.get('notes')
        
        # TODO: Save sleep data to database
        flash('Sleep data logged successfully!', 'success')
        return redirect(url_for('main_routes.sleep'))
    
    return render_template('sleep.html')

@main_routes.route('/nutrition', methods=['GET', 'POST'])
@login_required
def nutrition():
    if request.method == 'POST':
        # Handle meal log submission
        date = request.form.get('date')
        meal_type = request.form.get('meal_type')
        food_name = request.form.get('food_name')
        calories = request.form.get('calories')
        serving_size = request.form.get('serving_size')
        protein = request.form.get('protein')
        carbs = request.form.get('carbs')
        fat = request.form.get('fat')
        notes = request.form.get('notes')
        
        # TODO: Save nutrition data to database
        flash('Meal logged successfully!', 'success')
        return redirect(url_for('main_routes.nutrition'))
    
    return render_template('nutrition.html')

@main_routes.route('/workout', methods=['GET', 'POST'])
@login_required
def workout():
    if request.method == 'POST':
        # Handle workout log submission
        date = request.form.get('date')
        workout_type = request.form.get('workout_type')
        exercise_name = request.form.get('exercise_name')
        sets = request.form.get('sets')
        reps = request.form.get('reps')
        weight = request.form.get('weight')
        duration = request.form.get('duration')
        intensity = request.form.get('intensity')
        notes = request.form.get('notes')
        
        # TODO: Save workout data to database
        flash('Workout logged successfully!', 'success')
        return redirect(url_for('main_routes.workout'))
    
    return render_template('workout.html') 