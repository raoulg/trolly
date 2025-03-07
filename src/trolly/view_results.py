"""
Utility script to view and explore experiment results.

This script provides a simple command-line interface to view
the results of the ethical trolley problem experiment.
"""

import os
import json
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt
from .analytics import load_results_from_csv, analyze_dilemma_responses, participant_framework_analysis

def list_results(results_dir):
    """List all result files in the directory."""
    results = []
    for filename in os.listdir(results_dir):
        if filename.endswith('.csv') and 'trolley_results' in filename:
            # Extract participant ID from filename
            parts = filename.replace('trolley_results_', '').split('_')
            participant_id = parts[0]
            date = '_'.join(parts[1:]).replace('.csv', '')
            results.append((participant_id, date, filename))
    
    if not results:
        print("No results found in directory:", results_dir)
        return
    
    print("\nAvailable Results:")
    print(tabulate(results, headers=["Participant ID", "Date", "Filename"]))

def view_participant_summary(results_dir, participant_id=None, filename=None):
    """View summary for a specific participant."""
    if filename:
        file_path = os.path.join(results_dir, filename)
    elif participant_id:
        # Find the most recent file for this participant
        matching_files = [f for f in os.listdir(results_dir) 
                         if f.endswith('.csv') and f'trolley_results_{participant_id}' in f]
        if not matching_files:
            print(f"No results found for participant: {participant_id}")
            return
        file_path = os.path.join(results_dir, sorted(matching_files)[-1])  # Get the most recent
    else:
        print("Please provide either participant_id or filename")
        return
    
    # Load the data
    df = load_results_from_csv(file_path)
    if df is None or df.empty:
        print(f"Could not load data from: {file_path}")
        return
    
    # Calculate basic statistics
    total_dilemmas = len(df)
    utilitarian_choices = sum(df['Ethical Framework'] == 'utilitarian')
    deontological_choices = sum(df['Ethical Framework'] == 'deontological')
    avg_reaction_time = df['Reaction Time (s)'].mean()
    
    # Print summary
    print("\nParticipant Summary:")
    print(f"Participant ID: {df['Participant ID'].iloc[0]}")
    print(f"Total dilemmas answered: {total_dilemmas}")
    print(f"Utilitarian choices: {utilitarian_choices} ({utilitarian_choices/total_dilemmas*100:.1f}%)")
    print(f"Deontological choices: {deontological_choices} ({deontological_choices/total_dilemmas*100:.1f}%)")
    print(f"Average reaction time: {avg_reaction_time:.2f} seconds")
    
    # Determine dominant framework
    if utilitarian_choices/total_dilemmas > 0.6:
        framework = "Utilitarian"
    elif deontological_choices/total_dilemmas > 0.6:
        framework = "Deontological"
    else:
        framework = "Mixed"
    
    print(f"Dominant ethical framework: {framework}")
    
    # Show detailed responses
    print("\nDetailed Responses:")
    response_data = []
    for _, row in df.iterrows():
        response_data.append([
            row['Dilemma ID'],
            row['Dilemma Title'],
            row['Ethical Framework'].capitalize(),
            f"{row['Reaction Time (s)']:.2f}s"
        ])
    
    print(tabulate(response_data, headers=["ID", "Dilemma", "Framework", "Reaction Time"]))
    
    # Plot the results
    plt.figure(figsize=(10, 6))
    frameworks = ['Utilitarian', 'Deontological']
    counts = [utilitarian_choices, deontological_choices]
    plt.bar(frameworks, counts, color=['#6200ea', '#ff5722'])
    plt.title(f'Ethical Framework Distribution - Participant {df["Participant ID"].iloc[0]}')
    plt.ylabel('Number of Choices')
    plt.tight_layout()
    
    # Save the plot
    output_dir = os.path.join(results_dir, 'visualizations')
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, f'participant_{df["Participant ID"].iloc[0]}_distribution.png'))
    print(f"\nVisualization saved to: {output_dir}/participant_{df['Participant ID'].iloc[0]}_distribution.png")
    
    # Ask if user wants to open the visualization
    try:
        response = input("\nWould you like to view the visualization? (y/n): ")
        if response.lower() == 'y':
            plt.show()
    except Exception:
        pass

def view_all_participants_summary(results_dir):
    """View summary of all participants."""
    # Load all results
    all_dfs = []
    for filename in os.listdir(results_dir):
        if filename.endswith('.csv') and 'trolley_results' in filename:
            file_path = os.path.join(results_dir, filename)
            df = load_results_from_csv(file_path)
            if df is not None and not df.empty:
                all_dfs.append(df)
    
    if not all_dfs:
        print("No results found to analyze.")
        return
    
    combined_df = pd.concat(all_dfs, ignore_index=True)
    
    # Get participant statistics
    participant_stats = participant_framework_analysis(combined_df)
    
    # Print summary
    print("\nAll Participants Summary:")
    print(f"Total participants: {len(participant_stats)}")
    print(f"Total responses: {len(combined_df)}")
    
    # Framework distribution
    utilitarian_dominant = sum(participant_stats['Dominant Framework'] == 'Utilitarian')
    deontological_dominant = sum(participant_stats['Dominant Framework'] == 'Deontological')
    mixed_dominant = sum(participant_stats['Dominant Framework'] == 'Mixed')
    
    print(f"Participants with Utilitarian tendency: {utilitarian_dominant} ({utilitarian_dominant/len(participant_stats)*100:.1f}%)")
    print(f"Participants with Deontological tendency: {deontological_dominant} ({deontological_dominant/len(participant_stats)*100:.1f}%)")
    print(f"Participants with Mixed tendency: {mixed_dominant} ({mixed_dominant/len(participant_stats)*100:.1f}%)")
    
    # Average reaction time
    avg_rt = combined_df['Reaction Time (s)'].mean()
    print(f"Average reaction time across all participants: {avg_rt:.2f} seconds")
    
    # Participant details
    print("\nParticipant Details:")
    participant_data = []
    for _, row in participant_stats.iterrows():
        participant_data.append([
            row['Participant ID'],
            row['Total Dilemmas'],
            f"{row['Utilitarian %']:.1f}%",
            f"{row['Deontological %']:.1f}%",
            f"{row['Avg Reaction Time']:.2f}s",
            row['Dominant Framework']
        ])
    
    print(tabulate(participant_data, headers=["ID", "Dilemmas", "Utilitarian", "Deontological", "Avg RT", "Framework"]))
    
    # Plot the results
    plt.figure(figsize=(10, 6))
    frameworks = ['Utilitarian', 'Deontological', 'Mixed']
    counts = [utilitarian_dominant, deontological_dominant, mixed_dominant]
    plt.bar(frameworks, counts, color=['#6200ea', '#ff5722', '#03dac6'])
    plt.title('Dominant Ethical Framework Distribution Among Participants')
    plt.ylabel('Number of Participants')
    plt.tight_layout()
    
    # Save the plot
    output_dir = os.path.join(results_dir, 'visualizations')
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, 'all_participants_framework_distribution.png'))
    print(f"\nVisualization saved to: {output_dir}/all_participants_framework_distribution.png")
    
    # Ask if user wants to open the visualization
    try:
        response = input("\nWould you like to view the visualization? (y/n): ")
        if response.lower() == 'y':
            plt.show()
    except Exception:
        pass

def main():
    """Main function to run the script."""
    results_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'results')
    
    if not os.path.exists(results_dir) or not os.listdir(results_dir):
        print(f"No results found in {results_dir}. Please run the experiment first.")
        return
    
    while True:
        print("\n===== Ethical Trolley Problem Results Viewer =====")
        print("1. List all results")
        print("2. View summary for a specific participant")
        print("3. View summary for all participants")
        print("4. Run full analysis (generates visualizations and report)")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == '1':
            list_results(results_dir)
        
        elif choice == '2':
            list_results(results_dir)
            participant_input = input("\nEnter participant ID or filename: ")
            if 'trolley_results' in participant_input and participant_input.endswith('.csv'):
                view_participant_summary(results_dir, filename=participant_input)
            else:
                view_participant_summary(results_dir, participant_id=participant_input)
        
        elif choice == '3':
            view_all_participants_summary(results_dir)
        
        elif choice == '4':
            from .analytics import run_analysis
            output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'analysis_output')
            print(f"\nRunning full analysis. Results will be saved to {output_dir}")
            run_analysis(results_dir, output_dir)
            print(f"\nAnalysis complete. Open {output_dir}/visualizations to view the generated visualizations.")
        
        elif choice == '5':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
