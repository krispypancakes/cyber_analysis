# Cyber Analysis
This is an example application to analyse cybersecurity data.
Question I want to answer / angles I want to explore are:
* Frequency of attack on a specific company
* What are the most common attacks? ... over different time spans
* Which kind of attachs have the most impact
* Are attacks getting more/less complex / severe / impactful

This is visualized in a streamlit dashboard. The dashboard provides initial visualizations, but is capable of 
being adjusted.

## prerequisits
install ollama `curl -fsSL https://ollama.com/install.sh | sh` 

and run / download model `ollama run mistral-nemo`... we can also run a smaller one depending on your machine.

Create a virtual environment
`python3 -m venv .venv`

Install dependencies
`pip install --upgrade pip`
`pip install -r requirements.txt`

## run
`streamlit run main.py`
