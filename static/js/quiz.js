/**
 * QuizPulse - Frontend Quiz Execution Engine
 * Manages states, countdown timers, transition animations, and postings.
 */

document.addEventListener("DOMContentLoaded", () => {
    // 1. Check if quiz config is loaded
    if (!window.QUIZ_CONFIG) {
        console.error("Quiz configuration not found. Aborting execution.");
        return;
    }

    const CONFIG = window.QUIZ_CONFIG;

    // --- DOM Elements ---
    const loaderOverlay = document.getElementById("quiz-loader");
    const errorOverlay = document.getElementById("quiz-error");
    const activeLayout = document.getElementById("quiz-active-layout");
    
    const questionBody = document.getElementById("question-body");
    const optionsContainer = document.getElementById("options-container");
    const progressFill = document.getElementById("progress-fill");
    const progressText = document.getElementById("progress-text");
    const scoreTracker = document.getElementById("score-tracker");
    
    const timerBar = document.getElementById("timer-bar");
    const timerCountdown = document.getElementById("timer-countdown");
    
    const explanationDrawer = document.getElementById("explanation-drawer");
    const explanationBody = document.getElementById("explanation-body");
    
    const btnNext = document.getElementById("btn-next");
    const nextBtnLabel = document.getElementById("next-btn-label");
    const nextBtnIconContainer = document.getElementById("next-btn-icon-container");

    // --- Quiz State Constants & Variables ---
    const SECONDS_PER_QUESTION = 15;
    const TIMER_CIRCUMFERENCE = 2 * Math.PI * 34; // 2 * pi * r (r=34) = ~213.63
    
    let questions = [];
    let currentIndex = 0;
    let score = 0;
    
    let timerInterval = null;
    let timeLeft = SECONDS_PER_QUESTION;
    
    let quizStartTime = 0;
    let questionStartTime = 0;
    let totalElapsedSeconds = 0;
    let userAnswers = {}; // Map of { question_id: selected_choice_letter }

    // --- Core Functions ---

    /**
     * Start the quiz by fetching questions from API
     */
    async function startQuiz() {
        try {
            // Build URL query params
            const queryUrl = `${CONFIG.questionsApiUrl}?category_id=${CONFIG.categoryId}&difficulty=${CONFIG.difficulty}`;
            
            const response = await fetch(queryUrl);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            questions = await response.json();
            
            if (!questions || questions.length === 0) {
                showErrorState();
                return;
            }
            
            // Initialize starts
            quizStartTime = Date.now();
            hideLoader();
            showQuizLayout();
            loadQuestion();
            
        } catch (error) {
            console.error("Failed to load questions:", error);
            showErrorState();
        }
    }

    /**
     * Display a single question onto the viewport
     */
    function loadQuestion() {
        // Reset timers & visuals
        clearInterval(timerInterval);
        timeLeft = SECONDS_PER_QUESTION;
        timerCountdown.textContent = timeLeft;
        updateTimerCircle(1); // 100% full
        
        btnNext.classList.add("hidden");
        explanationDrawer.classList.add("hidden");
        
        const q = questions[currentIndex];
        
        // Render Text
        questionBody.textContent = q.question_text;
        
        // Render Progress info
        const qNum = currentIndex + 1;
        const totalQ = questions.length;
        const progressPercentage = (qNum / totalQ) * 100;
        
        progressFill.style.width = `${progressPercentage}%`;
        progressText.textContent = `Question ${qNum} of ${totalQ}`;
        scoreTracker.textContent = `Score: ${score}`;
        
        // Clean and render options
        optionsContainer.innerHTML = "";
        
        const optionKeys = ['A', 'B', 'C', 'D'];
        optionKeys.forEach(choice => {
            const optionText = q.options[choice];
            if (optionText) {
                const btn = document.createElement("button");
                btn.className = "option-btn";
                btn.innerHTML = `
                    <span class="option-prefix">${choice}</span>
                    <span class="option-text-span">${escapeHTML(optionText)}</span>
                    <span class="choice-icon-wrapper choice-icon-container">
                        <i data-lucide="help-circle"></i>
                    </span>
                `;
                
                btn.addEventListener("click", () => handleAnswer(choice, btn));
                optionsContainer.appendChild(btn);
            }
        });
        
        lucide.createIcons();
        
        // Capture start time of this specific question
        questionStartTime = Date.now();
        
        // Fire timer countdown
        startTimer();
    }

    /**
     * Start the countdown timer for the active question
     */
    function startTimer() {
        timerInterval = setInterval(() => {
            timeLeft--;
            
            if (timeLeft >= 0) {
                timerCountdown.textContent = timeLeft;
                updateTimerCircle(timeLeft / SECONDS_PER_QUESTION);
                
                // Add emergency styling if time is low (<= 5s)
                if (timeLeft <= 5) {
                    timerCountdown.style.color = "var(--danger-light)";
                    document.getElementById("timer-bar").style.stroke = "var(--danger-light)";
                } else {
                    timerCountdown.style.color = "var(--text-primary)";
                    document.getElementById("timer-bar").style.stroke = "var(--accent-light)";
                }
            }
            
            if (timeLeft <= 0) {
                clearInterval(timerInterval);
                handleTimeout();
            }
        }, 1000);
    }

    /**
     * Updates the SVG circular progress ring based on fraction (0 to 1)
     */
    function updateTimerCircle(fraction) {
        const offset = TIMER_CIRCUMFERENCE - (fraction * TIMER_CIRCUMFERENCE);
        timerBar.style.strokeDashoffset = offset;
    }

    /**
     * User clicks on a choice button
     */
    function handleAnswer(selectedChoice, clickedButton) {
        // Stop timer
        clearInterval(timerInterval);
        
        const q = questions[currentIndex];
        const buttons = optionsContainer.getElementsByClassName("option-btn");
        
        // Lock answer choice buttons
        disableAllOptions();
        
        const isCorrect = (selectedChoice === q.correct_answer);
        userAnswers[q.id] = selectedChoice;
        
        // Visual grading triggers
        if (isCorrect) {
            score++;
            scoreTracker.textContent = `Score: ${score}`;
            clickedButton.classList.add("correct");
            
            // Update icon to checkmark
            const iconContainer = clickedButton.querySelector(".choice-icon-container");
            iconContainer.innerHTML = '<i data-lucide="check"></i>';
        } else {
            clickedButton.classList.add("incorrect");
            const iconContainer = clickedButton.querySelector(".choice-icon-container");
            iconContainer.innerHTML = '<i data-lucide="x"></i>';
            
            // Highlight the correct answer
            for (let btn of buttons) {
                const prefix = btn.querySelector(".option-prefix").textContent;
                if (prefix === q.correct_answer) {
                    btn.classList.add("correct");
                    const correctIconContainer = btn.querySelector(".choice-icon-container");
                    correctIconContainer.innerHTML = '<i data-lucide="check"></i>';
                }
            }
        }
        
        // Fade other unselected items
        for (let btn of buttons) {
            if (btn !== clickedButton && btn.querySelector(".option-prefix").textContent !== q.correct_answer) {
                btn.classList.add("faded");
            }
        }
        
        // Refresh icons inside buttons
        lucide.createIcons();
        
        // Show explanation and next actions
        showExplanation(q.explanation);
        revealNavigation();
    }

    /**
     * Triggered when timer runs out before selection
     */
    function handleTimeout() {
        const q = questions[currentIndex];
        const buttons = optionsContainer.getElementsByClassName("option-btn");
        
        disableAllOptions();
        
        // Log choice as empty (skipped)
        userAnswers[q.id] = "";
        
        // Show correct option
        for (let btn of buttons) {
            const prefix = btn.querySelector(".option-prefix").textContent;
            if (prefix === q.correct_answer) {
                btn.classList.add("correct");
                const correctIconContainer = btn.querySelector(".choice-icon-container");
                correctIconContainer.innerHTML = '<i data-lucide="check"></i>';
            } else {
                btn.classList.add("faded");
            }
        }
        
        lucide.createIcons();
        
        showExplanation(q.explanation || "Time ran out! You skipped this question.");
        revealNavigation();
    }

    /**
     * Disable all choice buttons to lock response state
     */
    function disableAllOptions() {
        const buttons = optionsContainer.getElementsByClassName("option-btn");
        for (let btn of buttons) {
            btn.disabled = true;
        }
    }

    /**
     * Slide open explanation drawer with markdown text
     */
    function showExplanation(text) {
        if (text) {
            explanationBody.textContent = text;
        } else {
            explanationBody.textContent = "No explanation provided for this question.";
        }
        explanationDrawer.classList.remove("hidden");
    }

    /**
     * Reveal "Next Question" or "Finish" buttons
     */
    function revealNavigation() {
        const isLast = (currentIndex === questions.length - 1);
        const iconName = isLast ? "award" : "arrow-right";
        nextBtnLabel.textContent = isLast ? "Finish & See Results" : "Next Question";
        nextBtnIconContainer.innerHTML = `<i data-lucide="${iconName}"></i>`;
        
        lucide.createIcons();
        btnNext.classList.remove("hidden");
    }

    // --- Navigation Click Handlers ---
    
    btnNext.addEventListener("click", () => {
        const isLast = (currentIndex === questions.length - 1);
        
        if (isLast) {
            finishQuiz();
        } else {
            currentIndex++;
            loadQuestion();
        }
    });

    /**
     * Post attempt payload to server and redirect
     */
    async function finishQuiz() {
        // Show loading spinner overlay
        showLoader("Grading and saving results...");
        
        // Calculate total seconds elapsed
        totalElapsedSeconds = Math.round((Date.now() - quizStartTime) / 1000);
        
        const payload = {
            user_name: CONFIG.userName,
            category_id: CONFIG.categoryId,
            difficulty: CONFIG.difficulty,
            time_taken: totalElapsedSeconds,
            answers: userAnswers
        };
        
        try {
            const response = await fetch(CONFIG.submitApiUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            });
            
            const result = await response.json();
            
            if (result.success && result.attempt_id) {
                // Redirect user to the result detail screen
                const finalUrl = CONFIG.redirectUrl.replace("0", result.attempt_id);
                window.location.href = finalUrl;
            } else {
                alert("Something went wrong saving your scores. Returning home.");
                window.location.href = "/";
            }
            
        } catch (error) {
            console.error("Error submitting quiz attempts:", error);
            alert("Network connection error. Failed to save score. Returning home.");
            window.location.href = "/";
        }
    }

    // --- Visual Overlay helpers ---
    
    function hideLoader() {
        loaderOverlay.classList.add("hidden");
    }

    function showLoader(message) {
        if (message) {
            loaderOverlay.querySelector("p").textContent = message;
        }
        loaderOverlay.classList.remove("hidden");
    }

    function showQuizLayout() {
        activeLayout.classList.remove("hidden");
    }

    function showErrorState() {
        hideLoader();
        activeLayout.classList.add("hidden");
        errorOverlay.classList.remove("hidden");
        lucide.createIcons();
    }

    /**
     * Quick utility to sanitize options strings to prevent injection
     */
    function escapeHTML(text) {
        const div = document.createElement('div');
        div.innerText = text;
        return div.innerHTML;
    }

    // Initialize the engine execution
    startQuiz();
});
