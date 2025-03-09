# Ethical Trolley Problem Experiment

An interactive research tool for exploring ethical dilemmas related to emerging technologies. This experiment presents participants with a series of ethical dilemmas and measures their responses and reaction times to analyze their ethical framework tendencies.

## Features

- Interactive ethical dilemmas focused on technology ethics
- Measurement of reaction times for decision-making analysis
- Classification of responses according to ethical frameworks (Utilitarian vs. Deontological)
- Data collection and analysis tools for research purposes
- Visualization of results and ethical tendencies

## Installation

### Using uv (Recommended)
[uv docs](https://docs.astral.sh/uv/)

```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync
```

### Using pip
If you also prefer the longest line at the supermarket:

```bash
# Create a virtual environment
python -m venv .venv
source .venv/bin/activate
pip install .
```

## Running the Experiment

1. Start the Flask server:

```bash
python -m src.trolly.app
```

2. Open a web browser and navigate to:

```
http://localhost:8080
```

3. Enter a participant ID and follow the on-screen instructions to complete the experiment.

## Viewing Results

After collecting data from participants, you can analyze the results using the built-in analytics tools:

```bash
# View results interactively
python -m src.trolly.app view-results

# Or run the full analysis
mkdir -p results analysis_output
python -m src.trolly.analytics results analysis_output
```

This will generate:
- Visualizations in the `analysis_output/visualizations` directory
- A comprehensive analysis report in `analysis_output/analysis_report.json`
- A combined CSV file with all results in `analysis_output/combined_results.csv`

You can also view individual participant results in the `results` directory.

## Privacy and Informed Consent

### For Researchers

Before conducting this experiment:

1. Ensure you have proper ethical approval from your institution's IRB or ethics committee.
2. Prepare an informed consent form that clearly explains:
   - The purpose of the study
   - What data will be collected
   - How the data will be used and stored
   - That participation is voluntary and can be withdrawn at any time
   - Contact information for questions or concerns

3. Modify the welcome screen in `index.html` to include consent information or add a separate consent screen.

### For Participants

As a participant in this study:

- Your responses to ethical dilemmas and reaction times will be recorded
- The data collected is used to analyze ethical framework tendencies
- No personally identifiable information is collected beyond the participant ID you provide
- You can download your own results at the end of the experiment
- You can withdraw from the experiment at any time by closing the browser

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
