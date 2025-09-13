document.addEventListener('DOMContentLoaded', function() {
    const doctorsList = document.getElementById('doctors-list');
    const addDoctorBtn = document.getElementById('add-doctor-btn');

    function fetchDoctors() {
        fetch('/api/doctors')
            .then(response => response.json())
            .then(data => {
                if (data.length === 0) {
                    doctorsList.innerHTML = '<p>No doctors found.</p>';
                    return;
                }
                let html = '<table><thead><tr><th>ID</th><th>Name</th><th>Specialization</th><th>Phone</th><th>Email</th><th>Available</th></tr></thead><tbody>';
                data.forEach(doctor => {
                    html += `<tr>
                        <td>${doctor.doctor_id}</td>
                        <td>${doctor.first_name} ${doctor.last_name}</td>
                        <td>${doctor.specialization}</td>
                        <td>${doctor.phone || ''}</td>
                        <td>${doctor.email || ''}</td>
                        <td>${doctor.is_available ? 'Yes' : 'No'}</td>
                    </tr>`;
                });
                html += '</tbody></table>';
                doctorsList.innerHTML = html;
            })
            .catch(error => {
                doctorsList.innerHTML = '<p>Error loading doctors.</p>';
                console.error('Error fetching doctors:', error);
            });
    }

    addDoctorBtn.addEventListener('click', () => {
        alert('Add doctor functionality to be implemented.');
    });

    fetchDoctors();
});
