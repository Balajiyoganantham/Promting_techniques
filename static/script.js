// Method descriptions
const methodDescriptions = {
    'zero_shot': 'Direct instruction without examples - clean and straightforward approach',
    'one_shot': 'Uses a single example to guide the format and style of the summary',
    'few_shot': 'Provides multiple examples to establish clear patterns and expectations',
    'chain_of_thoughts': 'Breaks down the analysis into logical steps for systematic reasoning',
    'tree_of_thoughts': 'Explores multiple reasoning paths simultaneously for comprehensive analysis',
    'role_based': 'AI acts as a senior research analyst with 20+ years of experience',
    'react': 'Combines reasoning and acting iteratively for thorough analysis',
    'directional_stimulus': 'Provides specific guidance to direct the AI toward desired output',
    'step_back': 'Takes a higher-level perspective before diving into detailed analysis'
};

// DOM elements
const form = document.getElementById('summarizerForm');
const methodSelect = document.getElementById('promptingMethod');
const methodDescription = document.getElementById('methodDescription');
const methodDescriptionText = document.getElementById('methodDescriptionText');
const articleText = document.getElementById('articleText');
const wordCount = document.getElementById('wordCount');
const validationMessage = document.getElementById('validationMessage');
const submitBtn = document.getElementById('submitBtn');
const btnText = document.getElementById('btnText');
const resultsSection = document.getElementById('resultsSection');
const errorMessage = document.getElementById('errorMessage');
const errorText = document.getElementById('errorText');

// Method selection handler
methodSelect.addEventListener('change', function() {
    const selectedMethod = this.value;
    if (selectedMethod && methodDescriptions[selectedMethod]) {
        methodDescriptionText.textContent = methodDescriptions[selectedMethod];
        methodDescription.style.display = 'block';
    } else {
        methodDescription.style.display = 'none';
    }
});

// Word counting and validation
articleText.addEventListener('input', function() {
    const text = this.value.trim();
    const words = text ? text.split(/\s+/).filter(word => word.length > 0) : [];
    const count = words.length;
    
    wordCount.textContent = `${count} words`;
    
    if (count === 0) {
        wordCount.className = 'word-count';
        validationMessage.textContent = 'Enter your article to begin';
        validationMessage.className = 'validation-message';
    } else if (count < 500) {
        wordCount.className = 'word-count invalid';
        validationMessage.textContent = `Need ${500 - count} more words (minimum 500)`;
        validationMessage.className = 'validation-message';
    } else if (count > 1000) {
        wordCount.className = 'word-count invalid';
        validationMessage.textContent = `${count - 1000} words over limit (maximum 1000)`;
        validationMessage.className = 'validation-message';
    } else {
        wordCount.className = 'word-count valid';
        validationMessage.textContent = 'Article length is valid ✓';
        validationMessage.className = 'validation-message';
    }
});

// Form submission
form.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = new FormData(form);
    const data = {
        article: formData.get('article').trim(),
        prompting_method: formData.get('prompting_method')
    };

    // Validate form
    if (!data.article || !data.prompting_method) {
        showError('Please fill in all required fields');
        return;
    }

    // Show loading state
    setLoading(true);
    hideError();
    hideResults();

    try {
        const response = await fetch('/api/summarize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok && result.success) {
            showResults(result.data);
        } else {
            showError(result.error || 'Failed to generate summary');
        }
    } catch (error) {
        showError('Network error: ' + error.message);
    } finally {
        setLoading(false);
    }
});

// Helper functions
function setLoading(loading) {
    if (loading) {
        submitBtn.disabled = true;
        btnText.innerHTML = '<span class="loading-spinner"></span>Generating Summary...';
    } else {
        submitBtn.disabled = false;
        btnText.textContent = 'Generate Summary';
    }
}

function showResults(data) {
    document.getElementById('methodUsed').textContent = `Method: ${methodDescriptions[data.prompting_method] || data.prompting_method}`;
    document.getElementById('summaryWordCount').textContent = `Summary: ${data.word_count} words`;
    document.getElementById('processingTime').textContent = `Model: ${data.model_used}`;
    document.getElementById('summaryContent').textContent = data.summary;
    
    resultsSection.classList.add('show');
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

function showError(message) {
    errorText.textContent = message;
    errorMessage.style.display = 'block';
    errorMessage.scrollIntoView({ behavior: 'smooth' });
}

function hideError() {
    errorMessage.style.display = 'none';
}

function hideResults() {
    resultsSection.classList.remove('show');
}

// Initialize

document.addEventListener('DOMContentLoaded', function() {
    // Check API health
    fetch('/health')
        .then(response => response.json())
        .then(data => {
            console.log('API Health:', data);
        })
        .catch(error => {
            console.error('API Health Check Failed:', error);
        });
}); 