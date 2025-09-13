document.addEventListener('DOMContentLoaded', function() {
    const reportsContent = document.getElementById('reports-content');
    const generateReportBtn = document.getElementById('generate-report-btn');

    function generateReport() {
        reportsContent.innerHTML = '<p>Generating report...</p>';

        Promise.all([
            fetch('/api/patients').then(res => res.json()),
            fetch('/api/doctors').then(res => res.json()),
            fetch('/api/appointments').then(res => res.json()),
            fetch('/api/billing').then(res => res.json())
        ])
        .then(([patients, doctors, appointments, billing]) => {
            const report = {
                totalPatients: patients.length,
                totalDoctors: doctors.length,
                totalAppointments: appointments.length,
                totalBilling: billing.length,
                pendingBills: billing.filter(b => b.payment_status === 'pending').length
            };

            reportsContent.innerHTML = `
                <h3>Hospital Statistics Report</h3>
                <ul>
                    <li>Total Patients: ${report.totalPatients}</li>
                    <li>Total Doctors: ${report.totalDoctors}</li>
                    <li>Total Appointments: ${report.totalAppointments}</li>
                    <li>Total Bills: ${report.totalBilling}</li>
                    <li>Pending Bills: ${report.pendingBills}</li>
                </ul>
            `;
        })
        .catch(error => {
            reportsContent.innerHTML = '<p>Error generating report.</p>';
            console.error('Error generating report:', error);
        });
    }

    generateReportBtn.addEventListener('click', generateReport);

    // Generate initial report
    generateReport();
});
