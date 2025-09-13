document.addEventListener('DOMContentLoaded', function() {
    const appointmentsList = document.getElementById('appointments-list');
    const addAppointmentBtn = document.getElementById('add-appointment-btn');

    function fetchAppointments() {
        fetch('/api/appointments')
            .then(response => response.json())
            .then(data => {
                if (data.length === 0) {
                    appointmentsList.innerHTML = '<p>No appointments found.</p>';
                    return;
                }
                let html = '<table><thead><tr><th>ID</th><th>Patient ID</th><th>Doctor ID</th><th>Date</th><th>Time</th><th>Status</th></tr></thead><tbody>';
                data.forEach(appointment => {
                    html += `<tr>
                        <td>${appointment.appointment_id}</td>
                        <td>${appointment.patient_id}</td>
                        <td>${appointment.doctor_id}</td>
                        <td>${appointment.appointment_date}</td>
                        <td>${appointment.appointment_time}</td>
                        <td>${appointment.status}</td>
                    </tr>`;
                });
                html += '</tbody></table>';
                appointmentsList.innerHTML = html;
            })
            .catch(error => {
                appointmentsList.innerHTML = '<p>Error loading appointments.</p>';
                console.error('Error fetching appointments:', error);
            });
    }

    addAppointmentBtn.addEventListener('click', () => {
        alert('Schedule appointment functionality to be implemented.');
    });

    fetchAppointments();
});
