document.addEventListener('DOMContentLoaded', function() {
    const patientsList = document.getElementById('patients-list');
    const addPatientBtn = document.getElementById('add-patient-btn');

    function fetchPatients() {
        fetch('/api/patients')
            .then(response => response.json())
            .then(data => {
                if (data.length === 0) {
                    patientsList.innerHTML = '<p>No patients found.</p>';
                    return;
                }
                let html = '<table><thead><tr><th>ID</th><th>Name</th><th>Gender</th><th>DOB</th><th>Phone</th><th>Email</th></tr></thead><tbody>';
                data.forEach(patient => {
                    html += `<tr>
                        <td>${patient.patient_id}</td>
                        <td>${patient.first_name} ${patient.last_name}</td>
                        <td>${patient.gender}</td>
                        <td>${patient.date_of_birth}</td>
                        <td>${patient.phone || ''}</td>
                        <td>${patient.email || ''}</td>
                    </tr>`;
                });
                html += '</tbody></table>';
                patientsList.innerHTML = html;
            })
            .catch(error => {
                patientsList.innerHTML = '<p>Error loading patients.</p>';
                console.error('Error fetching patients:', error);
            });
    }

    addPatientBtn.addEventListener('click', () => {
        alert('Add patient functionality to be implemented.');
    });

    fetchPatients();
});
