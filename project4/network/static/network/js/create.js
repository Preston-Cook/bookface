// Wait until DOM elements have loaded  
document.addEventListener("DOMContentLoaded", () => {

    // Set message block display to none
    const message = document.querySelector('#message');
    message.style.display = "none";

    // Add event listener to form
    document.querySelector('#new-post').onsubmit = () => {
        const post_body = document.querySelector('#post-body');
        
        // Check if input is empty
        if (!(post_body.value)) {
            message.style.display = 'block';

            // Prevent form submission
            return false;
        }

    }
})