document.addEventListener('DOMContentLoaded', function () {
    const saveEmailForm = document.getElementById('save-email-form');
    const addRecipientForm = document.getElementById('add-recipient-form');
    const responseMessage = document.getElementById('response-message');

    if (saveEmailForm) {
        saveEmailForm.addEventListener('submit', function (e) {
            e.preventDefault();

            const data = {
                event_id: document.getElementById('event_id').value,
                email_subject: document.getElementById('email_subject').value,
                email_content: document.getElementById('email_content').value,
                timestamp: document.getElementById('timestamp').value
            };

            fetch('/save_emails', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                responseMessage.textContent = data.message || 'Email queued successfully!';
            })
            .catch((error) => {
                console.error('Error:', error);
                responseMessage.textContent = 'An error occurred while queuing the email.';
            });
        });
    }

    if (addRecipientForm) {
        addRecipientForm.addEventListener('submit', function (e) {
            e.preventDefault();

            const data = {
                email_address: document.getElementById('email_address').value,
                full_name: document.getElementById('full_name').value
            };

            fetch('/email-recipients', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                responseMessage.textContent = data.message || 'Recipient added successfully!';
            })
            .catch((error) => {
                console.error('Error:', error);
                responseMessage.textContent = 'An error occurred while adding the recipient.';
            });
        });
    }
});
