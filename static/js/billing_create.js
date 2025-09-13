document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('create-bill-form');

    form.addEventListener('submit', function(e) {
        e.preventDefault();

        // Get form data
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        // Validate required fields
        if (!data.patient_id) {
            alert('Please select a patient.');
            return;
        }

        if (!data.total_amount || parseFloat(data.total_amount) <= 0) {
            alert('Please enter a valid total amount.');
            return;
        }

        // Submit the form
        fetch('/billing/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (response.ok) {
                alert('Bill created successfully!');
                window.location.href = '/billing';
            } else {
                return response.json().then(err => {
                    throw new Error(err.error || 'Failed to create bill');
                });
            }
        })
        .catch(error => {
            console.error('Error creating bill:', error);
            alert('Error creating bill: ' + error.message);
        });
    });

    // Auto-populate due date if not set
    const dueDateInput = document.getElementById('due_date');
    if (!dueDateInput.value) {
        const today = new Date();
        today.setDate(today.getDate() + 30); // Default to 30 days from now
        dueDateInput.value = today.toISOString().split('T')[0];
    }
});
