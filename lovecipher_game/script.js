console.log("LoveCipher script loaded!");

// --- Facebook SDK Stubs ---
function initializeFacebookSDK() {
    console.log("FB SDK: Attempting to initialize...");
    if (typeof FBInstant !== 'undefined') {
        console.log("FB SDK: FBInstant found. Initializing SDK...");
        FBInstant.initializeAsync()
            .then(() => {
                console.log("FB SDK: Successfully initialized.");
                // SDK is ready, now get player info, signal loading, etc.
                getFacebookPlayerInfo();
                signalGameReadyToFacebook();
            })
            .catch((error) => {
                console.error("FB SDK: Initialization failed:", error);
            });
    } else {
        console.warn("FB SDK: FBInstant not found. Running in standalone mode. Facebook features will be simulated.");
        // Simulate a successful initialization for testing flow
        getFacebookPlayerInfo(); // Call these directly if SDK not present
        signalGameReadyToFacebook();
    }
}

function getFacebookPlayerInfo() {
    console.log("FB SDK: Attempting to get player info...");
    if (typeof FBInstant !== 'undefined' && FBInstant.player) {
        const playerName = FBInstant.player.getName();
        const playerId = FBInstant.player.getID();
        console.log(`FB SDK: Player Name: ${playerName}, Player ID: ${playerId}`);
        // You could update UI elements here with player name if desired
    } else {
        console.log("FB SDK: (Simulated) Player Name: TestUser, Player ID: 12345");
    }
}

function signalGameReadyToFacebook() {
    console.log("FB SDK: Signaling game ready to Facebook...");
    if (typeof FBInstant !== 'undefined') {
        FBInstant.startGameAsync()
            .then(() => {
                console.log("FB SDK: Game started successfully with Facebook platform.");
            })
            .catch((error) => {
                console.error("FB SDK: startGameAsync failed:", error);
            });
    } else {
        console.log("FB SDK: (Simulated) Game ready signal sent.");
    }
}

function saveFacebookGameState(gameState) {
    console.log("FB SDK: Attempting to save game state...", gameState);
    if (typeof FBInstant !== 'undefined' && FBInstant.player) {
        FBInstant.player.setDataAsync(gameState)
            .then(() => {
                console.log("FB SDK: Game state saved successfully.");
            })
            .catch((error) => {
                console.error("FB SDK: Failed to save game state:", error);
            });
    } else {
        console.log("FB SDK: (Simulated) Game state saved.", gameState);
    }
}

function loadFacebookGameState() {
    console.log("FB SDK: Attempting to load game state...");
    return new Promise((resolve, reject) => {
        if (typeof FBInstant !== 'undefined' && FBInstant.player) {
            FBInstant.player.getDataAsync(['currentStage', 'relationshipScore', 'collectedClues', 'playerPathClues'])
                .then(data => {
                    console.log("FB SDK: Game state loaded successfully.", data);
                    resolve(data);
                })
                .catch(error => {
                    console.error("FB SDK: Failed to load game state:", error);
                    reject(error);
                });
        } else {
            console.log("FB SDK: (Simulated) No game state found or SDK not available.");
            resolve(null); // Resolve with null if no data or SDK not present
        }
    });
}
// --- End Facebook SDK Stubs ---

document.addEventListener('DOMContentLoaded', () => {
    initializeFacebookSDK(); // Initialize FB SDK first

    const playerInput = document.getElementById('player-input');
    const sendButton = document.getElementById('send-button');
    const chatDisplay = document.getElementById('chat-display');
    const dialogueChoicesArea = document.getElementById('dialogue-choices-area');
    const cluesList = document.getElementById('clues-list');
    const statusText = document.getElementById('status-text');

    // --- Game State & Data ---
    const conversations = {
        intro: [
            { sender: 'npc', text: "Hello there... stranger. Found my little message in a bottle, did you?" },
            { sender: 'npc', text: "I'm a bit surprised anyone did. It's been a while." },
            { sender: 'npc', text: "So, tell me, what are you seeking?" } // Player responds via text input
        ],
        post_intro_reply: [ // After player's first text reply
            { sender: 'npc', text: "Interesting. Seeking, are we? Well, perhaps you can solve something for me first." },
            { sender: 'npc', text: "I have cities, but no houses. I have mountains, but no trees. I have water, but no fish. What am I?", puzzle: 'map_riddle', answer: 'a map' }
        ],
        riddle_correct: [
            { sender: 'npc', text: "Impressive! 'A map' it is. You're sharper than you look." },
            { sender: 'npc', text: "Maybe you are interesting after all. Tell me..." },
            {
                sender: 'npc',
                text: "Are you the type to rush into things, or do you prefer to observe from the shadows?",
                choices: [
                    { text: "I jump in head first!", nextStage: 'choice_rush' },
                    { text: "I like to watch and learn.", nextStage: 'choice_observe' },
                    { text: "A bit of both, really.", nextStage: 'choice_both' }
                ]
            }
        ],
        riddle_incorrect: [
            { sender: 'npc', text: "Hmm, not quite. Think harder." } // Stays on riddle
        ],
        choice_rush: [
            { sender: 'npc', text: "A thrill-seeker, eh? I can appreciate that. Sometimes." },
            { sender: 'npc', text: "We'll see how that pans out for you." } // Leads to next phase
        ],
        choice_observe: [
            { sender: 'npc', text: "The cautious type. Wise, perhaps. Or perhaps too timid." },
            { sender: 'npc', text: "Observation can only get you so far." } // Leads to next phase
        ],
        choice_both: [
            { sender: 'npc', text: "Balanced, or just indecisive? Time will tell." },
            { sender: 'npc', text: "Let's move on, but remember this number: 7." , clue: "Number: 7"}, // Clue 1
            { sender: 'npc', text: "And this word: 'whisper'." , clue: "Word: whisper"}, // Clue 2
            { sender: 'npc', text: "They might be useful if you're observant.", nextStage: 'puzzle_gate_intro' }
        ],
        choice_rush: [
            { sender: 'npc', text: "A thrill-seeker, eh? I can appreciate that. Sometimes." },
            { sender: 'npc', text: "You like speed? Then maybe you'll appreciate the swiftness of a 'comet'." , clue: "Speed: comet"}, // Clue 1
            { sender: 'npc', text: "And also, keep the number '3' in mind." , clue: "Number: 3"}, // Clue 2
            { sender: 'npc', text: "We'll see how that pans out for you.", nextStage: 'puzzle_gate_intro' }
        ],
        choice_observe: [
            { sender: 'npc', text: "The cautious type. Wise, perhaps. Or perhaps too timid." },
            { sender: 'npc', text: "You watch for details? Then note the color 'indigo'." , clue: "Color: indigo"}, // Clue 1
            { sender: 'npc', text: "And the number '5'." , clue: "Number: 5"}, // Clue 2
            { sender: 'npc', text: "Observation can only get you so far.", nextStage: 'puzzle_gate_intro' }
        ],
        puzzle_gate_intro: [
            { sender: 'npc', text: "Alright, enough chit-chat for a moment." },
            { sender: 'npc', text: "I have a little gate here. It needs two specific things you might have picked up from our conversation to open." },
            { sender: 'npc', text: "Tell me the first one, then the second. What's the first part of the code?", puzzle: 'gate_puzzle_part1', expects: 'clue1_value' }
            // expects 'clue1_value' will be dynamically determined based on path taken
        ],
        puzzle_gate_part2: [
            { sender: 'npc', text: "Okay, and the second part?", puzzle: 'gate_puzzle_part2', expects: 'clue2_value' }
        ],
        puzzle_gate_correct: [
            { sender: 'npc', text: "Click. The gate swings open. Well done." },
            { sender: 'npc', text: "You're proving to be quite capable." }
        ],
        puzzle_gate_incorrect: [
            { sender: 'npc', text: "That doesn't seem right. The gate remains shut." }
            // This will loop back to the current puzzle part
        ]
    };

    let currentStage = 'intro';
    let currentMessages = [...conversations.intro];
    let messageIndex = 0;
    let expectingPuzzleAnswer = null; // e.g. { id: 'gate_puzzle_part1', expects: 'clue1_value' }
    let relationshipScore = 0;
    let collectedClues = []; // Stores objects like { text: "Number: 7" }
    let playerPathClues = []; // Stores the actual clue values player should have based on path, e.g. ['comet', '3']
    let tempPlayerInputForPuzzle = null; // To store the first part of a two-part puzzle answer

    // --- UI Functions ---
    function setInputMode(mode) { // 'text' or 'choice'
        if (mode === 'choice') {
            playerInput.disabled = true;
            sendButton.disabled = true;
            playerInput.placeholder = "Choose an option above";
            dialogueChoicesArea.classList.remove('hidden');
        } else { // 'text'
            playerInput.disabled = false;
            sendButton.disabled = false;
            playerInput.placeholder = "Type your message...";
            dialogueChoicesArea.classList.add('hidden');
            dialogueChoicesArea.innerHTML = ''; // Clear old choices
        }
    }

    // --- Message & Choice Display Functions ---

    function addMessageToChat(sender, message) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');
        messageElement.classList.add(sender === 'player' ? 'player-message' : 'npc-message');
        messageElement.textContent = message;
        chatDisplay.appendChild(messageElement);
        chatDisplay.scrollTop = chatDisplay.scrollHeight; // Auto-scroll to bottom
    }

    function updateCluesDisplay() {
        cluesList.innerHTML = ''; // Clear existing clues
        collectedClues.forEach(clue => {
            const listItem = document.createElement('li');
            listItem.textContent = clue.text; // Display the full clue text e.g. "Number: 7"
            cluesList.appendChild(listItem);
        });
    }

    function displayChoices(choices) {
        dialogueChoicesArea.innerHTML = ''; // Clear previous choices
        setInputMode('choice');

        choices.forEach(choice => {
            const button = document.createElement('button');
            button.classList.add('choice-button');
            button.textContent = choice.text;
            button.addEventListener('click', () => handleChoiceSelection(choice));
            dialogueChoicesArea.appendChild(button);
        });
    }

    function displayNextMessage() {
        if (messageIndex < currentMessages.length) {
            const messageData = currentMessages[messageIndex];

            if (messageData.sender === 'npc') {
                setTimeout(() => {
                    addMessageToChat(messageData.sender, messageData.text);

                    if (messageData.clue) {
                        const newClue = { text: messageData.clue };
                        if (!collectedClues.some(c => c.text === newClue.text)) {
                            collectedClues.push(newClue);
                            updateCluesDisplay();
                            const clueValue = messageData.clue.split(": ")[1].toLowerCase();
                            if (playerPathClues.length < 2) {
                                playerPathClues.push(clueValue);
                            }
                        }
                    }

                    messageIndex++;

                    if (messageData.choices) {
                        displayChoices(messageData.choices);
                    } else if (messageData.puzzle) {
                        expectingPuzzleAnswer = { id: messageData.puzzle, expects: messageData.expects };
                        setInputMode('text');
                    } else if (messageData.nextStage && messageIndex >= currentMessages.length) {
                        currentStage = messageData.nextStage;
                        currentMessages = [...(conversations[currentStage] || [])];
                        messageIndex = 0;
                        displayNextMessage(); // Auto-progress
                    } else if (messageIndex < currentMessages.length && currentMessages[messageIndex].sender === 'npc') {
                        displayNextMessage();
                    } else { // NPC turn ends
                        if(!messageData.choices && !messageData.puzzle) { // and no choices/puzzle pending from this message
                           setInputMode('text'); // enable text input for player
                        }
                    }
                }, 700);
            }
        } else { // End of currentMessages
            if (expectingPuzzleAnswer) {
                // Current messages finished, but still expecting a puzzle answer (e.g., after incorrect feedback)
                // Re-prompt for the current puzzle.
                let puzzleStageKey = null;
                for (const stageKey in conversations) {
                    if (conversations[stageKey].some(m => m.puzzle === expectingPuzzleAnswer.id)) {
                        puzzleStageKey = stageKey;
                        break;
                    }
                }
                if (puzzleStageKey) {
                    currentStage = puzzleStageKey; // This might be redundant if stage didn't change
                    currentMessages = [...conversations[currentStage]];
                    messageIndex = 0;
                    // Find the specific message that poses the puzzle to start from there.
                    const puzzleMessageIndex = currentMessages.findIndex(m => m.puzzle === expectingPuzzleAnswer.id);
                    if (puzzleMessageIndex !== -1) {
                        messageIndex = puzzleMessageIndex;
                    }
                    setTimeout(() => displayNextMessage(), 300); // Display the puzzle prompt again
                } else {
                     // Fallback: couldn't find puzzle stage, enable text input
                    console.error("Could not find stage for puzzle:", expectingPuzzleAnswer.id);
                    setInputMode('text');
                }
            } else if (dialogueChoicesArea.classList.contains('hidden')) {
                 // No puzzle pending, no choices displayed, so enable text input.
                 setInputMode('text');
            }
        }
    }

    // --- Player Action Handlers ---

    function handleChoiceSelection(choice) {
        addMessageToChat('player', choice.text);
        currentStage = choice.nextStage;
        // Reset playerPathClues when a choice is made that leads to new clues
        if (currentStage === 'choice_rush' || currentStage === 'choice_observe' || currentStage === 'choice_both') {
            playerPathClues = [];
            // Clues will be added by displayNextMessage as it processes the new stage's messages
        }
        currentMessages = [...(conversations[currentStage] || [])];
        messageIndex = 0;

        // Example: Update relationshipScore based on choice
        if (choice.scoreEffect) { // This property isn't used yet, but good for future
            relationshipScore += choice.scoreEffect;
        }
        if (currentStage === 'choice_rush') {
            relationshipScore += 5;
            // playerPathClues are now ['comet', '3'] via displayNextMessage
        } else if (currentStage === 'choice_observe') {
            relationshipScore += 5;
            // playerPathClues are now ['indigo', '5']
        } else if (currentStage === 'choice_both') {
            relationshipScore += 2;
            // playerPathClues are now ['7', 'whisper']
        }

        statusText.textContent = `Relationship Score: ${relationshipScore}`;

        setInputMode('text');
        dialogueChoicesArea.innerHTML = '';
        displayNextMessage();
        saveFacebookGameState(getCurrentGameState()); // Save after choice
    }

    function processPlayerTextInput(text) {
        const cleanedText = text.toLowerCase().trim();

        if (expectingPuzzleAnswer) {
            let puzzleSolvedForThisTurn = false;

            if (expectingPuzzleAnswer.id === 'map_riddle') {
                const riddleDefinition = conversations.post_intro_reply.find(m => m.puzzle === expectingPuzzleAnswer.id);
                if (riddleDefinition && cleanedText === riddleDefinition.answer) {
                    currentStage = 'riddle_correct';
                    relationshipScore += 10;
                    statusText.textContent = `She's impressed! Score: ${relationshipScore}`;
                    expectingPuzzleAnswer = null; // Puzzle fully solved
                    puzzleSolvedForThisTurn = true;
                } else {
                    currentMessages = [...conversations.riddle_incorrect];
                    statusText.textContent = `Not quite... Score: ${relationshipScore}`;
                    // expectingPuzzleAnswer for map_riddle remains, displayNextMessage will re-prompt
                }
            } else if (expectingPuzzleAnswer.id === 'gate_puzzle_part1') {
                if (playerPathClues.length > 0 && cleanedText === playerPathClues[0]) {
                    tempPlayerInputForPuzzle = cleanedText;
                    currentStage = 'puzzle_gate_part2'; // Moves to ask for the second part
                    // expectingPuzzleAnswer will be updated by displayNextMessage when it processes puzzle_gate_part2
                    puzzleSolvedForThisTurn = true; // Part 1 is correct
                } else {
                    currentMessages = [...conversations.puzzle_gate_incorrect];
                    // expectingPuzzleAnswer for gate_puzzle_part1 remains, displayNextMessage will re-prompt
                }
            } else if (expectingPuzzleAnswer.id === 'gate_puzzle_part2') {
                if (playerPathClues.length > 1 && tempPlayerInputForPuzzle && cleanedText === playerPathClues[1]) {
                    currentStage = 'puzzle_gate_correct';
                    relationshipScore += 15;
                    statusText.textContent = `Gate opened! Score: ${relationshipScore}`;
                    expectingPuzzleAnswer = null; // Puzzle fully solved
                    puzzleSolvedForThisTurn = true;
                    tempPlayerInputForPuzzle = null;
                } else {
                    currentMessages = [...conversations.puzzle_gate_incorrect];
                    tempPlayerInputForPuzzle = null;
                    // Add the restart message if not already there to loop back.
                    if (!conversations.puzzle_gate_incorrect.find(m => m.nextStage === 'puzzle_gate_intro')) {
                        conversations.puzzle_gate_incorrect.push({ sender: 'npc', text: "Let's try that gate sequence again from the start.", nextStage: 'puzzle_gate_intro'});
                    }
                    // expectingPuzzleAnswer remains for gate_puzzle_part2, but the nextStage in the incorrect message
                    // will effectively reset it by going to puzzle_gate_intro.
                }
            }

            // If puzzle was solved (or part 1 of gate puzzle was correct), load the new stage's messages.
            // Otherwise, currentMessages is already set to the "incorrect" feedback.
            if (puzzleSolvedForThisTurn) {
                 currentMessages = [...(conversations[currentStage] || [])];
                 if (expectingPuzzleAnswer === null) { // Puzzle was fully solved
                    saveFacebookGameState(getCurrentGameState()); // Save after solving a puzzle
                 }
            }

            messageIndex = 0;
            displayNextMessage();

        } else {
            // General conversation progression
            if (currentStage === 'intro') {
                currentStage = 'post_intro_reply';
                currentMessages = [...(conversations[currentStage] || [])];
                messageIndex = 0;
                displayNextMessage();
            }
        }
    }

    function handlePlayerSend() {
        const messageText = playerInput.value.trim();
        if (messageText && !playerInput.disabled) {
            addMessageToChat('player', messageText);
            playerInput.value = '';
            processPlayerTextInput(messageText);
        }
    }

    // --- Event Listeners ---
    if (sendButton) {
        sendButton.addEventListener('click', handlePlayerSend);
    }

    if (playerInput) {
        playerInput.addEventListener('keypress', (event) => {
            if (event.key === 'Enter' && !playerInput.disabled) {
                handlePlayerSend();
            }
        });
    }

    // --- Game Initialization ---
    async function startGame() { // Made async to await potential FB load
        console.log("Game initialized.");

        // Attempt to load game state from Facebook
        const loadedData = await loadFacebookGameState();
        if (loadedData) {
            console.log("Applying loaded game state:", loadedData);
            // Carefully apply loaded data, ensuring types and existence
            if (loadedData.currentStage) currentStage = loadedData.currentStage;
            if (typeof loadedData.relationshipScore === 'number') relationshipScore = loadedData.relationshipScore;
            if (Array.isArray(loadedData.collectedClues)) collectedClues = [...loadedData.collectedClues];
            if (Array.isArray(loadedData.playerPathClues)) playerPathClues = [...loadedData.playerPathClues];

            // Need to re-find currentMessages and messageIndex based on loadedStage
            currentMessages = [...(conversations[currentStage] || [])];
            messageIndex = 0; // Start from beginning of loaded stage, or find exact message if saved

            updateCluesDisplay(); // Update UI with loaded clues
            // Potentially, if a puzzle was partially completed, restore that state too.
            // For now, restarting the stage is simpler.
        }

        statusText.textContent = `Relationship Score: ${relationshipScore}`;
        setInputMode('text');

        // If we loaded a stage that ends in choices or a puzzle, displayNextMessage will handle it.
        // If it's an NPC message, it will display.
        // If it's the very start (intro) or a point where player should type, it will wait.
        displayNextMessage();

        // Example of saving state (e.g., if game auto-saves on start after loading)
        // saveFacebookGameState(getCurrentGameState());
    }

    function getCurrentGameState() {
        return {
            currentStage: currentStage,
            relationshipScore: relationshipScore,
            collectedClues: collectedClues,
            playerPathClues: playerPathClues,
            // Potentially add expectingPuzzleAnswer if you want to save mid-puzzle state
        };
    }

    startGame();
});
