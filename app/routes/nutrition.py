from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from ..models.nutrition import NutritionRecord, Food
from .. import db
from datetime import datetime, timedelta

bp = Blueprint('nutrition', __name__, url_prefix='/nutrition')

@bp.route('/record', methods=['POST'])
@login_required
def record_meal():
    data = request.get_json()
    
    nutrition_record = NutritionRecord(
        user_id=current_user.id,
        date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
        meal_type=data['meal_type'],
        meal_time=datetime.strptime(data['meal_time'], '%Y-%m-%d %H:%M'),
        calories=data.get('calories'),
        protein=data.get('protein'),
        carbs=data.get('carbs'),
        fats=data.get('fats'),
        fiber=data.get('fiber'),
        sugar=data.get('sugar'),
        water_intake=data.get('water_intake'),
        notes=data.get('notes')
    )
    
    db.session.add(nutrition_record)
    db.session.commit()
    
    return jsonify({'message': 'Meal record added successfully'}), 201

@bp.route('/records')
@login_required
def get_nutrition_records():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = NutritionRecord.query.filter_by(user_id=current_user.id)
    
    if start_date:
        query = query.filter(NutritionRecord.date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        query = query.filter(NutritionRecord.date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    
    records = query.order_by(NutritionRecord.date.desc(), NutritionRecord.meal_time.desc()).all()
    
    return jsonify([{
        'id': record.id,
        'date': record.date.isoformat(),
        'meal_type': record.meal_type,
        'meal_time': record.meal_time.isoformat(),
        'calories': record.calories,
        'protein': record.protein,
        'carbs': record.carbs,
        'fats': record.fats,
        'fiber': record.fiber,
        'sugar': record.sugar,
        'water_intake': record.water_intake,
        'notes': record.notes
    } for record in records])

@bp.route('/analysis')
@login_required
def get_nutrition_analysis():
    # Get records from the last 7 days
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=7)
    
    records = NutritionRecord.query.filter_by(user_id=current_user.id)\
        .filter(NutritionRecord.date >= start_date)\
        .filter(NutritionRecord.date <= end_date)\
        .all()
    
    if not records:
        return jsonify({'error': 'No nutrition records found for analysis'}), 404
    
    # Calculate daily averages
    daily_totals = {}
    for record in records:
        date_str = record.date.isoformat()
        if date_str not in daily_totals:
            daily_totals[date_str] = {
                'calories': 0,
                'protein': 0,
                'carbs': 0,
                'fats': 0,
                'fiber': 0,
                'sugar': 0,
                'water_intake': 0
            }
        
        # Add up all nutrients
        for nutrient in ['calories', 'protein', 'carbs', 'fats', 'fiber', 'sugar', 'water_intake']:
            value = getattr(record, nutrient)
            if value is not None:
                daily_totals[date_str][nutrient] += value
    
    # Calculate averages
    num_days = len(daily_totals)
    averages = {
        'calories': sum(day['calories'] for day in daily_totals.values()) / num_days,
        'protein': sum(day['protein'] for day in daily_totals.values()) / num_days,
        'carbs': sum(day['carbs'] for day in daily_totals.values()) / num_days,
        'fats': sum(day['fats'] for day in daily_totals.values()) / num_days,
        'fiber': sum(day['fiber'] for day in daily_totals.values()) / num_days,
        'sugar': sum(day['sugar'] for day in daily_totals.values()) / num_days,
        'water_intake': sum(day['water_intake'] for day in daily_totals.values()) / num_days
    }
    
    # Calculate macronutrient ratios
    total_macros = averages['protein'] + averages['carbs'] + averages['fats']
    if total_macros > 0:
        macro_ratios = {
            'protein_ratio': (averages['protein'] / total_macros) * 100,
            'carbs_ratio': (averages['carbs'] / total_macros) * 100,
            'fats_ratio': (averages['fats'] / total_macros) * 100
        }
    else:
        macro_ratios = {'protein_ratio': 0, 'carbs_ratio': 0, 'fats_ratio': 0}
    
    return jsonify({
        'daily_averages': {k: round(v, 2) for k, v in averages.items()},
        'macro_ratios': {k: round(v, 2) for k, v in macro_ratios.items()},
        'daily_totals': daily_totals,
        'total_records': len(records)
    })

@bp.route('/foods', methods=['GET'])
@login_required
def get_foods():
    # Get both system foods and user's custom foods
    foods = Food.query.filter(
        (Food.user_id == current_user.id) | (Food.user_id.is_(None))
    ).all()
    
    return jsonify([{
        'id': food.id,
        'name': food.name,
        'serving_size': food.serving_size,
        'calories': food.calories,
        'protein': food.protein,
        'carbs': food.carbs,
        'fats': food.fats,
        'fiber': food.fiber,
        'sugar': food.sugar,
        'is_custom': food.is_custom
    } for food in foods])

@bp.route('/foods', methods=['POST'])
@login_required
def add_custom_food():
    data = request.get_json()
    
    food = Food(
        name=data['name'],
        serving_size=data['serving_size'],
        calories=data['calories'],
        protein=data.get('protein'),
        carbs=data.get('carbs'),
        fats=data.get('fats'),
        fiber=data.get('fiber'),
        sugar=data.get('sugar'),
        user_id=current_user.id,
        is_custom=True
    )
    
    db.session.add(food)
    db.session.commit()
    
    return jsonify({'message': 'Custom food added successfully'}), 201 