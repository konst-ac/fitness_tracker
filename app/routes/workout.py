from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from ..models.workout import WorkoutRecord, Exercise, WorkoutPlan
from ..models.wellness import WellnessRecord
from .. import db
from datetime import datetime, timedelta

bp = Blueprint('workout', __name__, url_prefix='/workout')

@bp.route('/record', methods=['POST'])
@login_required
def record_workout():
    data = request.get_json()
    
    workout_record = WorkoutRecord(
        user_id=current_user.id,
        date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
        workout_type=data['workout_type'],
        duration=data['duration'],
        intensity=data['intensity'],
        calories_burned=data.get('calories_burned'),
        energy_level=data.get('energy_level'),
        muscle_soreness=data.get('muscle_soreness'),
        perceived_exertion=data.get('perceived_exertion'),
        satisfaction=data.get('satisfaction'),
        notes=data.get('notes')
    )
    
    db.session.add(workout_record)
    db.session.commit()
    
    return jsonify({'message': 'Workout record added successfully'}), 201

@bp.route('/records')
@login_required
def get_workout_records():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = WorkoutRecord.query.filter_by(user_id=current_user.id)
    
    if start_date:
        query = query.filter(WorkoutRecord.date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        query = query.filter(WorkoutRecord.date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    
    records = query.order_by(WorkoutRecord.date.desc()).all()
    
    return jsonify([{
        'id': record.id,
        'date': record.date.isoformat(),
        'workout_type': record.workout_type,
        'duration': record.duration,
        'intensity': record.intensity,
        'calories_burned': record.calories_burned,
        'energy_level': record.energy_level,
        'muscle_soreness': record.muscle_soreness,
        'perceived_exertion': record.perceived_exertion,
        'satisfaction': record.satisfaction,
        'notes': record.notes
    } for record in records])

@bp.route('/exercises')
@login_required
def get_exercises():
    # Get both system exercises and user's custom exercises
    exercises = Exercise.query.filter(
        (Exercise.user_id == current_user.id) | (Exercise.user_id.is_(None))
    ).all()
    
    return jsonify([{
        'id': exercise.id,
        'name': exercise.name,
        'category': exercise.category,
        'equipment_needed': exercise.equipment_needed,
        'difficulty_level': exercise.difficulty_level,
        'description': exercise.description,
        'instructions': exercise.instructions,
        'is_custom': exercise.is_custom
    } for exercise in exercises])

@bp.route('/exercises', methods=['POST'])
@login_required
def add_custom_exercise():
    data = request.get_json()
    
    exercise = Exercise(
        name=data['name'],
        category=data['category'],
        equipment_needed=data.get('equipment_needed'),
        difficulty_level=data['difficulty_level'],
        description=data.get('description'),
        instructions=data.get('instructions'),
        user_id=current_user.id,
        is_custom=True
    )
    
    db.session.add(exercise)
    db.session.commit()
    
    return jsonify({'message': 'Custom exercise added successfully'}), 201

@bp.route('/plans')
@login_required
def get_workout_plans():
    plans = WorkoutPlan.query.filter_by(user_id=current_user.id).all()
    
    return jsonify([{
        'id': plan.id,
        'name': plan.name,
        'description': plan.description,
        'duration_weeks': plan.duration_weeks,
        'difficulty_level': plan.difficulty_level,
        'goal': plan.goal
    } for plan in plans])

@bp.route('/plans', methods=['POST'])
@login_required
def create_workout_plan():
    data = request.get_json()
    
    plan = WorkoutPlan(
        user_id=current_user.id,
        name=data['name'],
        description=data.get('description'),
        duration_weeks=data['duration_weeks'],
        difficulty_level=data['difficulty_level'],
        goal=data['goal']
    )
    
    db.session.add(plan)
    db.session.commit()
    
    return jsonify({'message': 'Workout plan created successfully'}), 201

@bp.route('/recommend')
@login_required
def get_workout_recommendation():
    # Get today's wellness record
    today = datetime.now().date()
    wellness = WellnessRecord.query.filter_by(
        user_id=current_user.id,
        date=today
    ).first()
    
    if not wellness:
        return jsonify({
            'message': 'Please complete today\'s wellness check for personalized recommendations',
            'recommendation': {
                'type': 'moderate',
                'intensity': 'medium',
                'duration': 30
            }
        })
    
    # Calculate recommendation based on wellness metrics
    score = wellness.overall_wellness_score
    
    if score >= 4:
        recommendation = {
            'type': 'strength or high-intensity',
            'intensity': 'high',
            'duration': 45,
            'message': 'You\'re feeling great! This is an excellent day for a challenging workout.'
        }
    elif score >= 3:
        recommendation = {
            'type': 'moderate cardio or strength',
            'intensity': 'medium',
            'duration': 30,
            'message': 'You\'re doing well. A moderate workout would be beneficial today.'
        }
    elif score >= 2:
        recommendation = {
            'type': 'light cardio or mobility',
            'intensity': 'low',
            'duration': 20,
            'message': 'Consider a lighter workout today to maintain activity while allowing recovery.'
        }
    else:
        recommendation = {
            'type': 'recovery',
            'intensity': 'very low',
            'duration': 15,
            'message': 'Focus on rest and recovery today. Light stretching or walking recommended.'
        }
    
    return jsonify({
        'wellness_score': score,
        'recommendation': recommendation
    }) 