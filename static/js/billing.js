document.addEventListener('DOMContentLoaded', function() {
    const billingList = document.getElementById('billing-list');
    const addBillBtn = document.getElementById('add-bill-btn');

    function fetchBilling() {
        fetch('/api/billing')
            .then(response => {
                if (!response.ok) {
                    return response.json().then(err => { throw err; });
                }
                return response.json();
            })
            .then(data => {
                if (data.error) {
                    billingList.innerHTML = `<p>${data.error}</p>`;
                    return;
                }
                if (data.length === 0) {
                    billingList.innerHTML = '<p>No billing records found.</p>';
                    return;
                }
                let html = '<table><thead><tr><th>Bill ID</th><th>Patient ID</th><th>Appointment ID</th><th>Total Amount</th><th>Paid Amount</th><th>Status</th><th>Description</th><th>Created At</th></tr></thead><tbody>';
                data.forEach(bill => {
                    html += `<tr>
                        <td>${bill.bill_id}</td>
                        <td>${bill.patient_id}</td>
                        <td>${bill.appointment_id || ''}</td>
                        <td>${bill.total_amount ? bill.total_amount.toFixed(2) : '0.00'}</td>
                        <td>${bill.paid_amount ? bill.paid_amount.toFixed(2) : '0.00'}</td>
                        <td>${bill.payment_status || 'N/A'}</td>
                        <td>${bill.description}</td>
                        <td>${bill.created_at}</td>
                    </tr>`;
                });
                html += '</tbody></table>';
                billingList.innerHTML = html;
            })
            .catch(error => {
                console.error('Error fetching billing:', error);
                billingList.innerHTML = `<p>${error.error || 'Unable to load billing records. Please check your connection and try again.'}</p>`;
            });
    }

    addBillBtn.addEventListener('click', () => {
        // Show a modal or redirect to a bill creation form
        window.location.href = '/billing/create'; // Example: redirect to bill creation page
    });

    fetchBilling();
});
