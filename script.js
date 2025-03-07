// Global variables
let dilemmas = [];
let currentDilemmaIndex = 0;
let startTime = 0;
let results = [];
let participantId = '';

// DOM Elements
const welcomeScreen = document.getElementById('welcome-screen');
const dilemmaScreen = document.getElementById('dilemma-screen');
const resultsScreen = document.getElementById('results-screen');
const startBtn = document.getElementById('start-btn');
const restartBtn = document.getElementById('restart-btn');
const downloadBtn = document.getElementById('download-results');
const participantIdInput = document.getElementById('participant-id');
const progressFill = document.getElementById('progress-fill');
const dilemmaTitle = document.getElementById('dilemma-title');
const dilemmaDescription = document.getElementById('dilemma-description');
const leftChoiceTitle = document.getElementById('left-choice-title');
const leftChoiceDescription = document.getElementById('left-choice-description');
const rightChoiceTitle = document.getElementById('right-choice-title');
const rightChoiceDescription = document.getElementById('right-choice-description');
const timerDisplay = document.getElementById('timer');
const avgReactionTime = document.getElementById('avg-reaction-time');
const utilitarianBar = document.getElementById('utilitarian-bar');
const frameworkResult = document.getElementById('framework-result');
const frameworkExplanation = document.getElementById('framework-explanation');

// Event Listeners
startBtn.addEventListener('click', startExperiment);
restartBtn.addEventListener('click', resetExperiment);
downloadBtn.addEventListener('click', downloadResults);
document.addEventListener('keydown', handleKeyPress);

// Fetch dilemmas from server or use predefined ones
async function fetchDilemmas() {
    try {
        const response = await fetch('/api/dilemmas');
        if (response.ok) {
            return await response.json();
        }
    } catch (error) {
        console.error('Error fetching dilemmas:', error);
    }
    
    // Fallback to predefined dilemmas if fetch fails
    return [
        {
            id: 1,
            title: "Autonomous Vehicle Decision",
            description: "An autonomous vehicle detects an unavoidable accident. It must decide between:",
            leftChoice: {
                title: "Swerve to minimize casualties",
                description: "Swerve into one pedestrian to avoid hitting five others.",
                framework: "utilitarian"
            },
            rightChoice: {
                title: "Maintain course",
                description: "Continue straight ahead, following traffic rules, even though five pedestrians will be hit.",
                framework: "deontological"
            }
        },
        {
            id: 2,
            title: "AI Healthcare Resource Allocation",
            description: "An AI system must allocate a limited medical resource. It can choose between:",
            leftChoice: {
                title: "Maximize survival chance",
                description: "Give the resource to a younger patient with higher recovery probability.",
                framework: "utilitarian"
            },
            rightChoice: {
                title: "First come, first served",
                description: "Give the resource to the patient who arrived first, regardless of recovery chances.",
                framework: "deontological"
            }
        },
        {
            id: 3,
            title: "AI Companion Privacy",
            description: "An AI companion detects signs of depression in its user. Should it:",
            leftChoice: {
                title: "Alert family members",
                description: "Notify family members without user consent to prevent potential self-harm.",
                framework: "utilitarian"
            },
            rightChoice: {
                title: "Respect privacy",
                description: "Maintain user confidentiality and only suggest professional help to the user.",
                framework: "deontological"
            }
        },
        {
            id: 4,
            title: "Automated Content Moderation",
            description: "An AI content filter must decide on potentially harmful content that also has educational value:",
            leftChoice: {
                title: "Allow with warning",
                description: "Allow the content with warnings, considering its educational benefits.",
                framework: "utilitarian"
            },
            rightChoice: {
                title: "Remove content",
                description: "Remove the content following platform guidelines against harmful material.",
                framework: "deontological"
            }
        },
        {
            id: 5,
            title: "Predictive Policing",
            description: "An AI system predicts high crime likelihood in certain areas. Police resources should be:",
            leftChoice: {
                title: "Data-driven allocation",
                description: "Concentrate resources in predicted high-crime areas to maximize crime prevention.",
                framework: "utilitarian"
            },
            rightChoice: {
                title: "Equal distribution",
                description: "Distribute resources equally across all areas to avoid potential discrimination.",
                framework: "deontological"
            }
        },
        {
            id: 6,
            title: "AI Job Automation",
            description: "A company is implementing AI that will automate jobs. Should they:",
            leftChoice: {
                title: "Rapid implementation",
                description: "Implement AI quickly to maximize efficiency, even though many employees will lose jobs.",
                framework: "utilitarian"
            },
            rightChoice: {
                title: "Gradual transition",
                description: "Implement slowly with retraining programs, despite delayed economic benefits.",
                framework: "deontological"
            }
        },
        {
            id: 7,
            title: "Facial Recognition in Public Spaces",
            description: "A city is considering facial recognition technology in public areas. Should they:",
            leftChoice: {
                title: "Deploy widely",
                description: "Implement broadly to maximize crime prevention and public safety.",
                framework: "utilitarian"
            },
            rightChoice: {
                title: "Limit deployment",
                description: "Restrict use to protect privacy rights, even if it means less effective crime prevention.",
                framework: "deontological"
            }
        },
        {
            id: 8,
            title: "AI-Generated Art Copyright",
            description: "An AI creates art by learning from human artists. Should the AI-generated art be:",
            leftChoice: {
                title: "Freely available",
                description: "Made freely available to maximize creative output and cultural benefit.",
                framework: "utilitarian"
            },
            rightChoice: {
                title: "Restricted use",
                description: "Limited in use out of respect for the original artists' work and rights.",
                framework: "deontological"
            }
        }
    ];
}

// Randomize the order of dilemmas and which side represents which framework
function randomizeDilemmas(dilemmas) {
    // Shuffle the array
    const shuffled = [...dilemmas].sort(() => Math.random() - 0.5);
    
    // Randomize which side represents which framework
    return shuffled.map(dilemma => {
        // 50% chance to swap left and right choices
        if (Math.random() > 0.5) {
            const temp = dilemma.leftChoice;
            dilemma.leftChoice = dilemma.rightChoice;
            dilemma.rightChoice = temp;
        }
        return dilemma;
    });
}

// Start the experiment
function startExperiment() {
    participantId = participantIdInput.value.trim() || `participant_${Date.now()}`;
    
    fetchDilemmas().then(fetchedDilemmas => {
        dilemmas = randomizeDilemmas(fetchedDilemmas);
        currentDilemmaIndex = 0;
        results = [];
        
        welcomeScreen.classList.add('hidden');
        dilemmaScreen.classList.remove('hidden');
        
        showCurrentDilemma();
    });
}

// Display the current dilemma
function showCurrentDilemma() {
    const dilemma = dilemmas[currentDilemmaIndex];
    
    // Update progress bar
    const progress = ((currentDilemmaIndex) / dilemmas.length) * 100;
    progressFill.style.width = `${progress}%`;
    
    // Update dilemma content
    dilemmaTitle.textContent = dilemma.title;
    dilemmaDescription.textContent = dilemma.description;
    leftChoiceTitle.textContent = dilemma.leftChoice.title;
    leftChoiceDescription.textContent = dilemma.leftChoice.description;
    rightChoiceTitle.textContent = dilemma.rightChoice.title;
    rightChoiceDescription.textContent = dilemma.rightChoice.description;
    
    // Reset timer
    startTime = Date.now();
    updateTimer();
}

// Update the timer display
function updateTimer() {
    const elapsedTime = (Date.now() - startTime) / 1000;
    timerDisplay.textContent = `${elapsedTime.toFixed(1)}s`;
    
    if (dilemmaScreen.classList.contains('hidden')) return;
    requestAnimationFrame(updateTimer);
}

// Handle key press events
function handleKeyPress(event) {
    if (dilemmaScreen.classList.contains('hidden')) return;
    
    let choice = null;
    
    if (event.key === 'ArrowLeft') {
        choice = 'left';
    } else if (event.key === 'ArrowRight') {
        choice = 'right';
    } else {
        return; // Ignore other keys
    }
    
    const reactionTime = (Date.now() - startTime) / 1000;
    recordResult(choice, reactionTime);
    
    // Move to next dilemma or show results
    currentDilemmaIndex++;
    if (currentDilemmaIndex < dilemmas.length) {
        showCurrentDilemma();
    } else {
        showResults();
    }
}

// Record the result of a dilemma
function recordResult(choice, reactionTime) {
    const dilemma = dilemmas[currentDilemmaIndex];
    const selectedChoice = choice === 'left' ? dilemma.leftChoice : dilemma.rightChoice;
    
    results.push({
        dilemmaId: dilemma.id,
        dilemmaTitle: dilemma.title,
        choice: choice,
        framework: selectedChoice.framework,
        reactionTime: reactionTime,
        timestamp: new Date().toISOString()
    });
}

// Show the results screen
function showResults() {
    dilemmaScreen.classList.add('hidden');
    resultsScreen.classList.remove('hidden');
    
    // Calculate average reaction time
    const totalReactionTime = results.reduce((sum, result) => sum + result.reactionTime, 0);
    const averageReactionTime = totalReactionTime / results.length;
    avgReactionTime.textContent = `${averageReactionTime.toFixed(2)} seconds`;
    
    // Calculate framework tendency
    const utilitarianChoices = results.filter(result => result.framework === 'utilitarian').length;
    const utilitarianPercentage = (utilitarianChoices / results.length) * 100;
    
    utilitarianBar.style.width = `${utilitarianPercentage}%`;
    
    // Determine dominant framework
    let dominantFramework;
    if (utilitarianPercentage > 60) {
        dominantFramework = 'Utilitarian';
        frameworkResult.textContent = 'You tend toward Utilitarian ethics';
    } else if (utilitarianPercentage < 40) {
        dominantFramework = 'Deontological';
        frameworkResult.textContent = 'You tend toward Deontological ethics';
    } else {
        dominantFramework = 'Mixed';
        frameworkResult.textContent = 'You have a balanced ethical perspective';
    }
    
    // Explanation based on framework
    if (dominantFramework === 'Utilitarian') {
        frameworkExplanation.textContent = 'Your choices suggest you prioritize outcomes and the greater good, focusing on maximizing overall welfare even if it means breaking certain rules or principles.';
    } else if (dominantFramework === 'Deontological') {
        frameworkExplanation.textContent = 'Your choices suggest you prioritize principles and rules, focusing on the inherent rightness of actions rather than their consequences.';
    } else {
        frameworkExplanation.textContent = 'Your choices show a balance between considering outcomes and following principles, suggesting a nuanced ethical perspective that draws from multiple frameworks.';
    }
    
    // Send results to server
    sendResultsToServer();
}

// Send results to server
async function sendResultsToServer() {
    try {
        const response = await fetch('/api/results', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                participantId: participantId,
                results: results,
                timestamp: new Date().toISOString()
            })
        });
        
        if (!response.ok) {
            console.error('Failed to send results to server');
        }
    } catch (error) {
        console.error('Error sending results:', error);
    }
}

// Download results as CSV
function downloadResults() {
    // Calculate framework percentages
    const utilitarianChoices = results.filter(result => result.framework === 'utilitarian').length;
    const utilitarianPercentage = (utilitarianChoices / results.length) * 100;
    const deontologicalPercentage = 100 - utilitarianPercentage;
    
    // Calculate average reaction time
    const totalReactionTime = results.reduce((sum, result) => sum + result.reactionTime, 0);
    const averageReactionTime = totalReactionTime / results.length;
    
    // Create CSV header
    let csv = 'Participant ID,Dilemma ID,Dilemma Title,Choice,Ethical Framework,Reaction Time (s),Timestamp\n';
    
    // Add each result as a row
    results.forEach(result => {
        csv += `${participantId},${result.dilemmaId},"${result.dilemmaTitle}",${result.choice},${result.framework},${result.reactionTime},${result.timestamp}\n`;
    });
    
    // Add summary row
    csv += `\nSummary,,,,,\n`;
    csv += `Utilitarian Percentage,${utilitarianPercentage.toFixed(2)}%,,,\n`;
    csv += `Deontological Percentage,${deontologicalPercentage.toFixed(2)}%,,,\n`;
    csv += `Average Reaction Time,${averageReactionTime.toFixed(2)}s,,,\n`;
    
    // Create download link
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `trolley_results_${participantId}_${new Date().toISOString().split('T')[0]}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Reset the experiment
function resetExperiment() {
    resultsScreen.classList.add('hidden');
    welcomeScreen.classList.remove('hidden');
    participantIdInput.value = '';
}
