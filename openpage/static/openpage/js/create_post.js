document.addEventListener('DOMContentLoaded', function () {
    const createPostForm = document.getElementById('create-post-form');
    const submitButton = document.getElementById('submit-post-button');
    const loadingIndicator = document.getElementById('loading-indicator');
    const promptTextarea = document.getElementById('id_prompt'); // Default Django ID for prompt field
    const promptErrorSpan = document.getElementById('prompt-error');

    if (createPostForm && submitButton && loadingIndicator && promptTextarea && promptErrorSpan) {
        createPostForm.addEventListener('submit', function(event) {
            // Client-side validation for prompt emptiness
            if (promptTextarea.value.trim() === '') {
                promptErrorSpan.textContent = 'The prompt cannot be empty.';
                promptErrorSpan.style.display = 'block';
                promptTextarea.focus(); // Focus on the field with error
                event.preventDefault(); // Prevent form submission
                return; // Stop further processing
            } else {
                promptErrorSpan.textContent = ''; // Clear any previous error
                promptErrorSpan.style.display = 'none';
            }

            // If validation passes, show loading indicator and disable button
            loadingIndicator.style.display = 'block';
            submitButton.disabled = true;
            submitButton.textContent = 'Creating...'; // Optional: change button text

            // The form will submit naturally. If the server responds with an error
            // and re-renders the page, the button will be enabled again because
            // it's a fresh page load.
        });
    } else {
        console.warn('One or more elements for create post form interactivity not found. JS features might not work.');
        if (!promptTextarea) console.warn('Prompt textarea (id_prompt) not found.');
        if (!promptErrorSpan) console.warn('Prompt error span (prompt-error) not found.');
    }

    // Character counter logic
    const captionTextarea = document.getElementById('id_caption'); // Default Django ID for caption field
    const promptCharCountSpan = document.getElementById('prompt-char-count');
    const captionCharCountSpan = document.getElementById('caption-char-count');

    function updateCharCount(textarea, charCountSpan) {
        if (textarea && charCountSpan) {
            charCountSpan.textContent = textarea.value.length + ' characters';
        }
    }

    if (promptTextarea && promptCharCountSpan) {
        // Initial count
        updateCharCount(promptTextarea, promptCharCountSpan);
        // Update on input
        promptTextarea.addEventListener('input', function() {
            updateCharCount(promptTextarea, promptCharCountSpan);
        });
    } else {
        if (!promptTextarea) console.warn('Prompt textarea (id_prompt) not found for char counter.');
        if (!promptCharCountSpan) console.warn('Prompt char count span (prompt-char-count) not found.');
    }

    if (captionTextarea && captionCharCountSpan) {
        // Initial count
        updateCharCount(captionTextarea, captionCharCountSpan);
        // Update on input
        captionTextarea.addEventListener('input', function() {
            updateCharCount(captionTextarea, captionCharCountSpan);
        });
    } else {
        if (!captionTextarea) console.warn('Caption textarea (id_caption) not found for char counter.');
        if (!captionCharCountSpan) console.warn('Caption char count span (caption-char-count) not found.');
    }
});
