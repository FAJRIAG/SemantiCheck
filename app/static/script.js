document.addEventListener('DOMContentLoaded', () => {
    // Inputs
    const textAInput = document.getElementById('text-a');
    const textBInput = document.getElementById('text-b');
    const textAIInput = document.getElementById('text-ai');

    // Buttons
    const btnLocal = document.getElementById('btn-local');
    const btnDetailed = document.getElementById('btn-detailed');
    const btnDetectAI = document.getElementById('btn-detect-ai');

    // Mode Toggles
    const modePlagBtn = document.getElementById('mode-plag');
    const modeAIBtn = document.getElementById('mode-ai');

    // UI Sections
    const inputPlag = document.getElementById('input-plag');
    const inputAI = document.getElementById('input-ai');
    const resultsDiv = document.getElementById('results');
    const resPlag = document.getElementById('res-plag');
    const resAI = document.getElementById('res-ai');
    const detailedContainer = document.getElementById('detailed-analysis-container');
    const analysisContent = document.getElementById('analysis-content');
    const loadingDiv = document.getElementById('loading');

    // State
    let currentMode = 'plagiarism'; // 'plagiarism' or 'ai'

    // --- Mode Switching Logic ---
    const setMode = (mode) => {
        currentMode = mode;
        resultsDiv.classList.add('hidden'); // clear results

        if (mode === 'plagiarism') {
            modePlagBtn.classList.add('active');
            modeAIBtn.classList.remove('active');
            inputPlag.classList.remove('hidden');
            inputAI.classList.add('hidden');

            // Show Plag Buttons, Hide AI Button
            btnLocal.classList.remove('hidden');
            btnDetailed.classList.remove('hidden');
            btnDetectAI.classList.add('hidden');
        } else {
            modeAIBtn.classList.add('active');
            modePlagBtn.classList.remove('active');
            inputAI.classList.remove('hidden');
            inputPlag.classList.add('hidden');

            // Hide Plag Buttons, Show AI Button
            btnLocal.classList.add('hidden');
            btnDetailed.classList.add('hidden');
            btnDetectAI.classList.remove('hidden');
        }
    };

    modePlagBtn.addEventListener('click', () => setMode('plagiarism'));
    modeAIBtn.addEventListener('click', () => setMode('ai'));

    // --- Loading State ---
    const setLoading = (isLoading) => {
        if (isLoading) {
            loadingDiv.classList.remove('hidden');
            resultsDiv.classList.add('hidden');
            // Disable all buttons
            [btnLocal, btnDetailed, btnDetectAI].forEach(b => b.disabled = true);
        } else {
            loadingDiv.classList.add('hidden');
            resultsDiv.classList.remove('hidden');
            [btnLocal, btnDetailed, btnDetectAI].forEach(b => b.disabled = false);
        }
    };

    // --- Update UI with Results ---
    const updateResults = (data, type) => {
        detailedContainer.classList.add('hidden'); // Reset detailed view

        if (type === 'plagiarism') {
            resPlag.classList.remove('hidden');
            resAI.classList.add('hidden');

            const scoreVal = document.getElementById('score-val');
            const riskVal = document.getElementById('risk-val');

            const percentage = Math.round(data.similarity_score * 100);
            scoreVal.innerText = `${percentage}%`;

            riskVal.innerText = data.risk_level;
            riskVal.className = 'value';
            if (data.risk_level === 'Low') riskVal.classList.add('risk-low');
            if (data.risk_level === 'Medium') riskVal.classList.add('risk-medium');
            if (data.risk_level === 'High') riskVal.classList.add('risk-high');

            if (data.detailed_analysis) {
                detailedContainer.classList.remove('hidden');
                analysisContent.innerHTML = marked.parse(data.detailed_analysis);
            }
        } else if (type === 'ai_detection') {
            resAI.classList.remove('hidden');
            resPlag.classList.add('hidden');

            const aiProb = document.getElementById('ai-prob');
            const aiVerdict = document.getElementById('ai-verdict');

            aiProb.innerText = `${data.ai_probability}%`;
            aiVerdict.innerText = data.verdict;

            // Color coding for AI
            aiVerdict.className = 'value';
            if (data.verdict === 'Likely Human') aiVerdict.classList.add('risk-low');
            if (data.verdict === 'Mixed') aiVerdict.classList.add('risk-medium');
            if (data.verdict === 'Likely AI') aiVerdict.classList.add('risk-high');

            if (data.reasoning) {
                detailedContainer.classList.remove('hidden');
                analysisContent.innerHTML = `<p><strong>Reasoning:</strong> ${data.reasoning}</p>`;
            }
        }
    };

    // --- API Handler ---
    const handleAnalysis = async (endpoint, payload, type) => {
        setLoading(true);
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            });

            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.detail || 'Analysis failed');
            }

            const data = await response.json();
            updateResults(data, type);

        } catch (error) {
            alert(`Error: ${error.message}`);
        } finally {
            setLoading(false);
        }
    };

    // Event Listeners
    btnLocal.addEventListener('click', () => {
        const textA = textAInput.value.trim();
        const textB = textBInput.value.trim();
        if (!textA || !textB) return alert('Please enter both texts.');
        handleAnalysis('/analyze/local', { text_a: textA, text_b: textB }, 'plagiarism');
    });

    btnDetailed.addEventListener('click', () => {
        const textA = textAInput.value.trim();
        const textB = textBInput.value.trim();
        if (!textA || !textB) return alert('Please enter both texts.');
        handleAnalysis('/analyze/detailed', { text_a: textA, text_b: textB }, 'plagiarism');
    });

    // --- File Handling Logic ---
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const fileOverlay = document.getElementById('file-overlay');
    const fileNameDisplay = document.getElementById('file-name');
    const removeFileBtn = document.getElementById('remove-file');
    const triggerUploadBtn = document.getElementById('trigger-upload');
    let selectedFile = null;

    triggerUploadBtn.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', (e) => handleFileSelect(e.target.files[0]));

    // Drag & Drop
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => dropZone.classList.add('dragover'), false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => dropZone.classList.remove('dragover'), false);
    });

    dropZone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        handleFileSelect(dt.files[0]);
    });

    function handleFileSelect(file) {
        if (!file) return;
        // Simple validation
        const validExt = ['.txt', '.docx'];
        const isDocx = file.name.endsWith('.docx');
        const isTxt = file.name.endsWith('.txt');

        if (!isDocx && !isTxt) {
            alert('Only .txt and .docx files are supported.');
            return;
        }

        selectedFile = file;
        fileNameDisplay.innerText = file.name;
        fileOverlay.classList.remove('hidden');
        textAIInput.disabled = true; // Disable text area when file is selected
    }

    removeFileBtn.addEventListener('click', () => {
        selectedFile = null;
        fileInput.value = ''; // reset input
        fileOverlay.classList.add('hidden');
        textAIInput.disabled = false;
    });


    btnDetectAI.addEventListener('click', () => {
        if (selectedFile) {
            // Handle File Upload
            const formData = new FormData();
            formData.append('file', selectedFile);

            // Use fetch directly for FormData as headers differ
            setLoading(true);
            fetch('/detect-ai/file', {
                method: 'POST',
                body: formData
                // Content-Type is auto-set for FormData
            })
                .then(async res => {
                    if (!res.ok) throw new Error((await res.json()).detail || 'Upload failed');
                    return res.json();
                })
                .then(data => updateResults(data, 'ai_detection'))
                .catch(err => alert(`Error: ${err.message}`))
                .finally(() => setLoading(false));

        } else {
            // Handle Text Input
            const text = textAIInput.value.trim();
            if (!text) return alert('Please enter text or upload a file.');
            handleAnalysis('/detect-ai', { text: text }, 'ai_detection');
        }
    });
});
