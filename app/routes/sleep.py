from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from ..models.sleep import SleepRecord
from .. import db
from datetime import datetime, timedelta

bp = Blueprint('sleep', __name__, url_prefix='/sleep')

@bp.route('/record', methods=['POST'])
@login_required
def record_sleep():
    data = request.get_json()
    
    sleep_record = SleepRecord(
        user_id=current_user.id,
        date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
        sleep_time=datetime.strptime(data['sleep_time'], '%Y-%m-%d %H:%M'),
        wake_time=datetime.strptime(data['wake_time'], '%Y-%m-%d %H:%M'),
        quality=data.get('quality'),
        interruptions=data.get('interruptions', 0),
        deep_sleep_duration=data.get('deep_sleep_duration'),
        rem_sleep_duration=data.get('rem_sleep_duration'),
        notes=data.get('notes')
    )
    
    db.session.add(sleep_record)
    db.session.commit()
    
    return jsonify({'message': 'Sleep record added successfully'}), 201

@bp.route('/records')
@login_required
def get_sleep_records():
    # Get date range from query parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = SleepRecord.query.filter_by(user_id=current_user.id)
    
    if start_date:
        query = query.filter(SleepRecord.date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        query = query.filter(SleepRecord.date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    
    records = query.order_by(SleepRecord.date.desc()).all()
    
    return jsonify([{
        'id': record.id,
        'date': record.date.isoformat(),
        'sleep_time': record.sleep_time.isoformat(),
        'wake_time': record.wake_time.isoformat(),
        'duration': record.duration,
        'quality': record.quality,
        'interruptions': record.interruptions,
        'deep_sleep_duration': record.deep_sleep_duration,
        'rem_sleep_duration': record.rem_sleep_duration,
        'notes': record.notes
    } for record in records])

@bp.route('/analysis')
@login_required
def get_sleep_analysis():
    # Get records from the last 30 days
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=30)
    
    records = SleepRecord.query.filter_by(user_id=current_user.id)\
        .filter(SleepRecord.date >= start_date)\
        .filter(SleepRecord.date <= end_date)\
        .all()
    
    if not records:
        return jsonify({'error': 'No sleep records found for analysis'}), 404
    
    # Calculate average metrics
    total_duration = sum(record.duration for record in records)
    avg_duration = total_duration / len(records)
    
    avg_quality = sum(record.quality for record in records if record.quality) / \
                 len([r for r in records if r.quality])
    
    avg_interruptions = sum(record.interruptions for record in records) / len(records)
    
    # Find patterns
    weekday_durations = {}
    for record in records:
        weekday = record.date.strftime('%A')
        if weekday not in weekday_durations:
            weekday_durations[weekday] = []
        weekday_durations[weekday].append(record.duration)
    
    weekday_averages = {
        day: sum(durations) / len(durations)
        for day, durations in weekday_durations.items()
    }
    
    return jsonify({
        'average_duration': round(avg_duration, 2),
        'average_quality': round(avg_quality, 2),
        'average_interruptions': round(avg_interruptions, 2),
        'weekday_patterns': weekday_averages,
        'total_records': len(records)
    })

@bp.route('/record/<int:record_id>', methods=['PUT'])
@login_required
def update_sleep_record(record_id):
    record = SleepRecord.query.get_or_404(record_id)
    
    # Ensure user owns this record
    if record.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    # Update fields
    if 'sleep_time' in data:
        record.sleep_time = datetime.strptime(data['sleep_time'], '%Y-%m-%d %H:%M')
    if 'wake_time' in data:
        record.wake_time = datetime.strptime(data['wake_time'], '%Y-%m-%d %H:%M')
    if 'quality' in data:
        record.quality = data['quality']
    if 'interruptions' in data:
        record.interruptions = data['interruptions']
    if 'deep_sleep_duration' in data:
        record.deep_sleep_duration = data['deep_sleep_duration']
    if 'rem_sleep_duration' in data:
        record.rem_sleep_duration = data['rem_sleep_duration']
    if 'notes' in data:
        record.notes = data['notes']
    
    db.session.commit()
    return jsonify({'message': 'Sleep record updated successfully'})

@bp.route('/record/<int:record_id>', methods=['DELETE'])
@login_required
def delete_sleep_record(record_id):
    record = SleepRecord.query.get_or_404(record_id)
    
    # Ensure user owns this record
    if record.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': 'Sleep record deleted successfully'}) 