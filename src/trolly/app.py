"""
Flask application for the trolley problem experiment.

This module provides a simple Flask backend for serving the experiment
and collecting participant responses.
"""

from flask import Flask, jsonify, request, send_from_directory
import os
import csv
import json
from datetime import datetime
from . import dilemmas

app = Flask(__name__, static_folder='../../')

# Ensure results directory exists
RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'results')
os.makedirs(RESULTS_DIR, exist_ok=True)

@app.route('/')
def index():
    """Serve the main experiment page."""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/styles.css')
def styles():
    """Serve the CSS file."""
    return send_from_directory(app.static_folder, 'styles.css')

@app.route('/script.js')
def script():
    """Serve the JavaScript file."""
    return send_from_directory(app.static_folder, 'script.js')

@app.route('/api/dilemmas')
def get_dilemmas():
    """Return all dilemmas as JSON."""
    return jsonify(dilemmas.get_all_dilemmas())

@app.route('/api/results', methods=['POST'])
def save_results():
    """Save experiment results."""
    data = request.json
    
    if not data or 'participantId' not in data or 'results' not in data:
        return jsonify({'error': 'Invalid data format'}), 400
    
    participant_id = data['participantId']
    results = data['results']
    timestamp = data.get('timestamp', datetime.now().isoformat())
    
    # Create CSV filename
    filename = f"trolley_results_{participant_id}_{timestamp.split('T')[0]}.csv"
    filepath = os.path.join(RESULTS_DIR, filename)
    
    # Calculate framework percentages
    utilitarian_choices = sum(1 for r in results if r['framework'] == 'utilitarian')
    total_choices = len(results)
    utilitarian_percentage = (utilitarian_choices / total_choices) * 100 if total_choices > 0 else 0
    deontological_percentage = 100 - utilitarian_percentage
    
    # Calculate average reaction time
    total_reaction_time = sum(r['reactionTime'] for r in results)
    average_reaction_time = total_reaction_time / total_choices if total_choices > 0 else 0
    
    # Write results to CSV
    with open(filepath, 'w', newline='') as csvfile:
        fieldnames = ['Participant ID', 'Dilemma ID', 'Dilemma Title', 'Choice', 
                     'Ethical Framework', 'Reaction Time (s)', 'Timestamp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for result in results:
            writer.writerow({
                'Participant ID': participant_id,
                'Dilemma ID': result['dilemmaId'],
                'Dilemma Title': result['dilemmaTitle'],
                'Choice': result['choice'],
                'Ethical Framework': result['framework'],
                'Reaction Time (s)': result['reactionTime'],
                'Timestamp': result['timestamp']
            })
        
        # Add summary rows
        writer.writerow({})
        writer.writerow({'Participant ID': 'Summary'})
        writer.writerow({
            'Participant ID': 'Utilitarian Percentage',
            'Dilemma ID': f"{utilitarian_percentage:.2f}%"
        })
        writer.writerow({
            'Participant ID': 'Deontological Percentage',
            'Dilemma ID': f"{deontological_percentage:.2f}%"
        })
        writer.writerow({
            'Participant ID': 'Average Reaction Time',
            'Dilemma ID': f"{average_reaction_time:.2f}s"
        })
    
    # Also save as JSON for easier processing
    json_filepath = os.path.join(RESULTS_DIR, f"trolley_results_{participant_id}_{timestamp.split('T')[0]}.json")
    with open(json_filepath, 'w') as jsonfile:
        json.dump({
            'participant_id': participant_id,
            'timestamp': timestamp,
            'results': results,
            'summary': {
                'utilitarian_percentage': utilitarian_percentage,
                'deontological_percentage': deontological_percentage,
                'average_reaction_time': average_reaction_time
            }
        }, jsonfile, indent=2)
    
    return jsonify({'success': True, 'filepath': filepath})

def create_app():
    """Create and configure the Flask application."""
    return app

def run_app(host='0.0.0.0', port=None, debug=False):
    """Run the Flask application."""
    # Use Heroku's PORT environment variable if available
    if port is None:
        port = int(os.environ.get('PORT', 5000))
    
    print(f"Starting trolly experiment server at http://{host}:{port}")
    app.run(host=host, port=port, debug=debug)

def cli():
    """Command line interface for running the app."""
    import sys
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, help='Port to run the server on')
    parser.add_argument('--debug', action='store_true', help='Run in debug mode')
    parser.add_argument('--view-results', action='store_true', help='View results instead of running server')
    
    args = parser.parse_args()
    
    if args.view_results:
        from .view_results import main as view_results_main
        view_results_main()
    else:
        run_app(port=args.port, debug=args.debug)

if __name__ == '__main__':
    cli()
