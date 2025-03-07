"""
Ethical dilemmas for the trolley problem experiment.

This module defines the ethical dilemmas used in the experiment,
with each dilemma presenting a choice between utilitarian and deontological ethics.
"""

DILEMMAS = [
    {
        "id": 1,
        "title": "Autonomous Vehicle Decision",
        "description": "An autonomous vehicle detects an unavoidable accident. It must decide between:",
        "leftChoice": {
            "title": "Swerve to minimize casualties",
            "description": "Swerve into one pedestrian to avoid hitting five others.",
            "framework": "utilitarian"
        },
        "rightChoice": {
            "title": "Maintain course",
            "description": "Continue straight ahead, following traffic rules, even though five pedestrians will be hit.",
            "framework": "deontological"
        }
    },
    {
        "id": 2,
        "title": "AI Healthcare Resource Allocation",
        "description": "An AI system must allocate a limited medical resource. It can choose between:",
        "leftChoice": {
            "title": "Maximize survival chance",
            "description": "Give the resource to a younger patient with higher recovery probability.",
            "framework": "utilitarian"
        },
        "rightChoice": {
            "title": "First come, first served",
            "description": "Give the resource to the patient who arrived first, regardless of recovery chances.",
            "framework": "deontological"
        }
    },
    {
        "id": 3,
        "title": "AI Companion Privacy",
        "description": "An AI companion detects signs of depression in its user. Should it:",
        "leftChoice": {
            "title": "Alert family members",
            "description": "Notify family members without user consent to prevent potential self-harm.",
            "framework": "utilitarian"
        },
        "rightChoice": {
            "title": "Respect privacy",
            "description": "Maintain user confidentiality and only suggest professional help to the user.",
            "framework": "deontological"
        }
    },
    {
        "id": 4,
        "title": "Automated Content Moderation",
        "description": "An AI content filter must decide on potentially harmful content that also has educational value:",
        "leftChoice": {
            "title": "Allow with warning",
            "description": "Allow the content with warnings, considering its educational benefits.",
            "framework": "utilitarian"
        },
        "rightChoice": {
            "title": "Remove content",
            "description": "Remove the content following platform guidelines against harmful material.",
            "framework": "deontological"
        }
    },
    {
        "id": 5,
        "title": "Predictive Policing",
        "description": "An AI system predicts high crime likelihood in certain areas. Police resources should be:",
        "leftChoice": {
            "title": "Data-driven allocation",
            "description": "Concentrate resources in predicted high-crime areas to maximize crime prevention.",
            "framework": "utilitarian"
        },
        "rightChoice": {
            "title": "Equal distribution",
            "description": "Distribute resources equally across all areas to avoid potential discrimination.",
            "framework": "deontological"
        }
    },
    {
        "id": 6,
        "title": "AI Job Automation",
        "description": "A company is implementing AI that will automate jobs. Should they:",
        "leftChoice": {
            "title": "Rapid implementation",
            "description": "Implement AI quickly to maximize efficiency, even though many employees will lose jobs.",
            "framework": "utilitarian"
        },
        "rightChoice": {
            "title": "Gradual transition",
            "description": "Implement slowly with retraining programs, despite delayed economic benefits.",
            "framework": "deontological"
        }
    },
    {
        "id": 7,
        "title": "Facial Recognition in Public Spaces",
        "description": "A city is considering facial recognition technology in public areas. Should they:",
        "leftChoice": {
            "title": "Deploy widely",
            "description": "Implement broadly to maximize crime prevention and public safety.",
            "framework": "utilitarian"
        },
        "rightChoice": {
            "title": "Limit deployment",
            "description": "Restrict use to protect privacy rights, even if it means less effective crime prevention.",
            "framework": "deontological"
        }
    },
    {
        "id": 8,
        "title": "AI-Generated Art Copyright",
        "description": "An AI creates art by learning from human artists. Should the AI-generated art be:",
        "leftChoice": {
            "title": "Freely available",
            "description": "Made freely available to maximize creative output and cultural benefit.",
            "framework": "utilitarian"
        },
        "rightChoice": {
            "title": "Restricted use",
            "description": "Limited in use out of respect for the original artists' work and rights.",
            "framework": "deontological"
        }
    },
    {
        "id": 9,
        "title": "Algorithmic Sentencing",
        "description": "A court is using AI to recommend criminal sentences. Should the algorithm:",
        "leftChoice": {
            "title": "Focus on rehabilitation",
            "description": "Prioritize rehabilitation potential and societal reintegration in its recommendations.",
            "framework": "utilitarian"
        },
        "rightChoice": {
            "title": "Focus on consistency",
            "description": "Prioritize consistent punishment based on the crime committed, regardless of rehabilitation potential.",
            "framework": "deontological"
        }
    },
    {
        "id": 10,
        "title": "AI Research Ethics",
        "description": "Scientists are developing advanced AI that could have dual-use applications. Should they:",
        "leftChoice": {
            "title": "Pursue research openly",
            "description": "Continue research and publish findings openly to maximize scientific progress.",
            "framework": "utilitarian"
        },
        "rightChoice": {
            "title": "Restrict research",
            "description": "Limit research or publication due to potential misuse, even if it slows scientific progress.",
            "framework": "deontological"
        }
    }
]

def get_all_dilemmas():
    """Return all dilemmas."""
    return DILEMMAS

def get_dilemma_by_id(dilemma_id):
    """Return a specific dilemma by ID."""
    for dilemma in DILEMMAS:
        if dilemma["id"] == dilemma_id:
            return dilemma
    return None
