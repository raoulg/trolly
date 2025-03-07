"""
Analytics module for the trolley problem experiment.

This module provides functions for analyzing the results of the
ethical trolley problem experiment, including statistical analysis
and visualization of participant responses.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import os
import json
from datetime import datetime


def load_results_from_csv(file_path):
    """
    Load experiment results from a CSV file.
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        DataFrame containing the results
    """
    try:
        df = pd.read_csv(file_path)
        # Filter out summary rows if they exist
        df = df[~df['Dilemma ID'].isna()]
        return df
    except Exception as e:
        print(f"Error loading results: {e}")
        return None


def load_all_results(directory_path):
    """
    Load all result CSV files from a directory.
    
    Args:
        directory_path: Path to directory containing result files
        
    Returns:
        DataFrame containing combined results
    """
    all_dfs = []
    
    for filename in os.listdir(directory_path):
        if filename.endswith('.csv') and 'trolley_results' in filename:
            file_path = os.path.join(directory_path, filename)
            df = load_results_from_csv(file_path)
            if df is not None:
                all_dfs.append(df)
    
    if all_dfs:
        return pd.concat(all_dfs, ignore_index=True)
    else:
        return pd.DataFrame()


def calculate_framework_percentages(df):
    """
    Calculate the percentage of utilitarian vs deontological choices.
    
    Args:
        df: DataFrame containing experiment results
        
    Returns:
        Dictionary with framework percentages
    """
    framework_counts = df['Ethical Framework'].value_counts()
    total = framework_counts.sum()
    
    percentages = {
        'utilitarian': (framework_counts.get('utilitarian', 0) / total) * 100,
        'deontological': (framework_counts.get('deontological', 0) / total) * 100
    }
    
    return percentages


def analyze_reaction_times(df):
    """
    Analyze reaction times from experiment results.
    
    Args:
        df: DataFrame containing experiment results
        
    Returns:
        Dictionary with reaction time statistics
    """
    reaction_times = df['Reaction Time (s)'].astype(float)
    
    stats = {
        'mean': reaction_times.mean(),
        'median': reaction_times.median(),
        'std_dev': reaction_times.std(),
        'min': reaction_times.min(),
        'max': reaction_times.max()
    }
    
    # Calculate reaction time by framework
    framework_reaction_times = df.groupby('Ethical Framework')['Reaction Time (s)'].agg(['mean', 'median', 'std'])
    
    stats['by_framework'] = framework_reaction_times.to_dict()
    
    return stats


def analyze_dilemma_responses(df):
    """
    Analyze responses for each dilemma.
    
    Args:
        df: DataFrame containing experiment results
        
    Returns:
        DataFrame with dilemma response statistics
    """
    # Group by dilemma and calculate statistics
    dilemma_stats = df.groupby(['Dilemma ID', 'Dilemma Title']).agg({
        'Ethical Framework': lambda x: x.value_counts().to_dict(),
        'Reaction Time (s)': ['mean', 'std']
    }).reset_index()
    
    # Calculate framework percentages for each dilemma
    for idx, row in dilemma_stats.iterrows():
        framework_counts = row['Ethical Framework']
        total = sum(framework_counts.values())
        
        utilitarian_count = framework_counts.get('utilitarian', 0)
        deontological_count = framework_counts.get('deontological', 0)
        
        dilemma_stats.at[idx, 'Utilitarian %'] = (utilitarian_count / total) * 100
        dilemma_stats.at[idx, 'Deontological %'] = (deontological_count / total) * 100
        
        # Calculate standard deviation of ethical choices (higher means more disagreement)
        dilemma_stats.at[idx, 'Choice Std Dev'] = np.std([1] * utilitarian_count + [0] * deontological_count)
    
    return dilemma_stats


def find_correlations(df):
    """
    Find correlations between reaction time and ethical framework.
    
    Args:
        df: DataFrame containing experiment results
        
    Returns:
        Dictionary with correlation results
    """
    # Convert framework to numeric (1 for utilitarian, 0 for deontological)
    df['Framework Numeric'] = df['Ethical Framework'].apply(lambda x: 1 if x == 'utilitarian' else 0)
    
    # Calculate correlation between reaction time and framework
    correlation, p_value = stats.pointbiserialr(df['Framework Numeric'], df['Reaction Time (s)'])
    
    return {
        'correlation': correlation,
        'p_value': p_value,
        'significant': p_value < 0.05
    }


def participant_framework_analysis(df):
    """
    Analyze each participant's ethical framework tendencies.
    
    Args:
        df: DataFrame containing experiment results
        
    Returns:
        DataFrame with participant framework analysis
    """
    # Group by participant and calculate framework percentages
    participant_stats = df.groupby('Participant ID').apply(
        lambda x: pd.Series({
            'Total Dilemmas': len(x),
            'Utilitarian Choices': sum(x['Ethical Framework'] == 'utilitarian'),
            'Deontological Choices': sum(x['Ethical Framework'] == 'deontological'),
            'Avg Reaction Time': x['Reaction Time (s)'].mean()
        })
    ).reset_index()
    
    # Calculate percentages
    participant_stats['Utilitarian %'] = (participant_stats['Utilitarian Choices'] / 
                                         participant_stats['Total Dilemmas']) * 100
    participant_stats['Deontological %'] = (participant_stats['Deontological Choices'] / 
                                           participant_stats['Total Dilemmas']) * 100
    
    # Determine dominant framework
    def get_dominant_framework(row):
        if row['Utilitarian %'] > 60:
            return 'Utilitarian'
        elif row['Deontological %'] > 60:
            return 'Deontological'
        else:
            return 'Mixed'
    
    participant_stats['Dominant Framework'] = participant_stats.apply(get_dominant_framework, axis=1)
    
    return participant_stats


def generate_visualizations(df, output_dir):
    """
    Generate visualizations from experiment results.
    
    Args:
        df: DataFrame containing experiment results
        output_dir: Directory to save visualizations
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Overall framework distribution
    framework_counts = df['Ethical Framework'].value_counts()
    plt.figure(figsize=(10, 6))
    framework_counts.plot(kind='bar', color=['#6200ea', '#ff5722'])
    plt.title('Distribution of Ethical Frameworks')
    plt.ylabel('Number of Choices')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'framework_distribution.png'))
    
    # 2. Reaction time distribution
    plt.figure(figsize=(10, 6))
    df['Reaction Time (s)'].hist(bins=20, color='#03dac6')
    plt.title('Distribution of Reaction Times')
    plt.xlabel('Reaction Time (seconds)')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'reaction_time_distribution.png'))
    
    # 3. Reaction time by framework
    plt.figure(figsize=(10, 6))
    df.boxplot(column='Reaction Time (s)', by='Ethical Framework', color='black')
    plt.title('Reaction Time by Ethical Framework')
    plt.suptitle('')  # Remove default suptitle
    plt.ylabel('Reaction Time (seconds)')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'reaction_time_by_framework.png'))
    
    # 4. Dilemma response distribution
    dilemma_stats = analyze_dilemma_responses(df)
    plt.figure(figsize=(12, 8))
    
    dilemmas = dilemma_stats['Dilemma Title'].tolist()
    utilitarian_pct = dilemma_stats['Utilitarian %'].tolist()
    deontological_pct = dilemma_stats['Deontological %'].tolist()
    
    x = np.arange(len(dilemmas))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.bar(x - width/2, utilitarian_pct, width, label='Utilitarian', color='#6200ea')
    ax.bar(x + width/2, deontological_pct, width, label='Deontological', color='#ff5722')
    
    ax.set_ylabel('Percentage of Choices')
    ax.set_title('Ethical Framework Distribution by Dilemma')
    ax.set_xticks(x)
    ax.set_xticklabels([d[:20] + '...' if len(d) > 20 else d for d in dilemmas], rotation=45, ha='right')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'dilemma_framework_distribution.png'))
    
    # 5. Participant framework distribution
    participant_stats = participant_framework_analysis(df)
    framework_distribution = participant_stats['Dominant Framework'].value_counts()
    
    plt.figure(figsize=(10, 6))
    framework_distribution.plot(kind='pie', autopct='%1.1f%%', colors=['#6200ea', '#03dac6', '#ff5722'])
    plt.title('Distribution of Dominant Ethical Frameworks Among Participants')
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'participant_framework_distribution.png'))


def generate_report(df, output_file):
    """
    Generate a comprehensive analysis report.
    
    Args:
        df: DataFrame containing experiment results
        output_file: Path to save the report
    """
    # Calculate overall statistics
    total_participants = df['Participant ID'].nunique()
    total_responses = len(df)
    framework_percentages = calculate_framework_percentages(df)
    reaction_time_stats = analyze_reaction_times(df)
    dilemma_stats = analyze_dilemma_responses(df)
    correlation_results = find_correlations(df)
    participant_stats = participant_framework_analysis(df)
    
    # Identify dilemmas with highest disagreement (standard deviation)
    high_disagreement_dilemmas = dilemma_stats.sort_values('Choice Std Dev', ascending=False).head(3)
    
    # Identify dilemmas with longest reaction times
    long_rt_dilemmas = dilemma_stats.sort_values(('Reaction Time (s)', 'mean'), ascending=False).head(3)
    
    # Create report dictionary
    report = {
        "report_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "summary": {
            "total_participants": int(total_participants),
            "total_responses": int(total_responses),
            "framework_distribution": {
                "utilitarian_percentage": float(framework_percentages['utilitarian']),
                "deontological_percentage": float(framework_percentages['deontological'])
            },
            "reaction_times": {
                "mean": float(reaction_time_stats['mean']),
                "median": float(reaction_time_stats['median']),
                "std_dev": float(reaction_time_stats['std_dev'])
            }
        },
        "framework_reaction_time_correlation": {
            "correlation": float(correlation_results['correlation']),
            "p_value": float(correlation_results['p_value']),
            "significant": bool(correlation_results['significant'])
        },
        "participant_framework_distribution": {
            "utilitarian_dominant": int(sum(participant_stats['Dominant Framework'] == 'Utilitarian')),
            "deontological_dominant": int(sum(participant_stats['Dominant Framework'] == 'Deontological')),
            "mixed": int(sum(participant_stats['Dominant Framework'] == 'Mixed'))
        },
        "high_disagreement_dilemmas": high_disagreement_dilemmas[['Dilemma ID', 'Dilemma Title', 'Choice Std Dev']].to_dict('records'),
        "long_reaction_time_dilemmas": long_rt_dilemmas[['Dilemma ID', 'Dilemma Title', ('Reaction Time (s)', 'mean')]].to_dict('records')
    }
    
    # Save report as JSON
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=4)
    
    return report


def run_analysis(results_dir, output_dir):
    """
    Run a complete analysis on experiment results.
    
    Args:
        results_dir: Directory containing result CSV files
        output_dir: Directory to save analysis outputs
    
    Returns:
        Summary of analysis results
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Load all results
    df = load_all_results(results_dir)
    
    if df.empty:
        print("No results found to analyze.")
        return None
    
    # Generate visualizations
    generate_visualizations(df, os.path.join(output_dir, 'visualizations'))
    
    # Generate report
    report = generate_report(df, os.path.join(output_dir, 'analysis_report.json'))
    
    # Save processed data
    df.to_csv(os.path.join(output_dir, 'combined_results.csv'), index=False)
    
    # Print summary
    print(f"Analysis complete. Results saved to {output_dir}")
    print(f"Total participants: {report['summary']['total_participants']}")
    print(f"Total responses: {report['summary']['total_responses']}")
    print(f"Utilitarian choices: {report['summary']['framework_distribution']['utilitarian_percentage']:.2f}%")
    print(f"Deontological choices: {report['summary']['framework_distribution']['deontological_percentage']:.2f}%")
    print(f"Average reaction time: {report['summary']['reaction_times']['mean']:.2f} seconds")
    
    return report


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python analytics.py <results_directory> <output_directory>")
        sys.exit(1)
    
    results_dir = sys.argv[1]
    output_dir = sys.argv[2]
    
    run_analysis(results_dir, output_dir)
