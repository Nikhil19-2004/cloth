// scripts.js

document.addEventListener('DOMContentLoaded', function () {
    const messagesContainer = document.getElementById('messages-container');
    
    if (messagesContainer) {
        // Retrieve displayed messages from local storage
        const displayedMessages = JSON.parse(localStorage.getItem('displayedMessages')) || [];

        // Loop through each message
        messagesContainer.querySelectorAll('.message').forEach(function (messageElement) {
            const messageId = messageElement.getAttribute('data-id');

            // Check if the message has been displayed before
            if (!displayedMessages.includes(messageId)) {
                // Display the message
                messageElement.style.display = 'block'; // Ensure it is displayed
                displayedMessages.push(messageId); // Add to the displayed messages list
            } else {
                // Hide the message if it has been displayed before
                messageElement.style.display = 'none';
            }
        });

        // Store the updated list of displayed messages in local storage
        localStorage.setItem('displayedMessages', JSON.stringify(displayedMessages));
    }
});
