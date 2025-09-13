document.addEventListener('DOMContentLoaded', function() {
    const appointmentsDiv = document.getElementById('patient-appointments');
    const doctorListDiv = document.getElementById('doctor-list');
    const contactForm = document.getElementById('contact-form');
    const contactDoctorForm = document.getElementById('contact-doctor-form');

    function fetchPatientAppointments() {
        fetch('/api/patient/appointments')
            .then(response => response.json())
            .then(data => {
                if (data.length === 0) {
                    appointmentsDiv.innerHTML = '<p>No appointments found.</p>';
                    return;
                }
                let html = '<table><thead><tr><th>Appointment ID</th><th>Doctor ID</th><th>Date</th><th>Time</th><th>Status</th><th>Notes</th></tr></thead><tbody>';
                data.forEach(appointment => {
                    html += `<tr>
                        <td>${appointment.appointment_id}</td>
                        <td>${appointment.doctor_id}</td>
                        <td>${appointment.appointment_date}</td>
                        <td>${appointment.appointment_time}</td>
                        <td>${appointment.status}</td>
                        <td>${appointment.notes || ''}</td>
                    </tr>`;
                });
                html += '</tbody></table>';
                appointmentsDiv.innerHTML = html;
            })
            .catch(error => {
                appointmentsDiv.innerHTML = '<p>Error loading appointments.</p>';
                console.error('Error fetching appointments:', error);
            });
    }

    function fetchDoctors() {
        fetch('/api/doctors')
            .then(response => response.json())
            .then(data => {
                if (data.length === 0) {
                    doctorListDiv.innerHTML = '<p>No doctors found.</p>';
                    return;
                }
                let html = '<table><thead><tr><th>Doctor ID</th><th>Name</th><th>Specialization</th><th>Action</th></tr></thead><tbody>';
                data.forEach(doctor => {
                    html += `<tr>
                        <td>${doctor.doctor_id}</td>
                        <td>${doctor.first_name} ${doctor.last_name}</td>
                        <td>${doctor.specialization}</td>
                        <td><button class="contact-btn" data-doctor-id="${doctor.doctor_id}">Contact</button></td>
                    </tr>`;
                });
                html += '</tbody></table>';
                doctorListDiv.innerHTML = html;

                // Add event listeners to contact buttons
                document.querySelectorAll('.contact-btn').forEach(btn => {
                    btn.addEventListener('click', function() {
                        const doctorId = this.getAttribute('data-doctor-id');
                        document.getElementById('selected-doctor-id').value = doctorId;
                        contactForm.style.display = 'block';
                        contactForm.scrollIntoView({ behavior: 'smooth' });
                    });
                });
            })
            .catch(error => {
                doctorListDiv.innerHTML = '<p>Error loading doctors.</p>';
                console.error('Error fetching doctors:', error);
            });
    }

    contactDoctorForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        const doctorId = formData.get('doctor_id');
        const message = formData.get('message');

        fetch('/api/contact_doctor', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                doctor_id: doctorId,
                message: message
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'busy') {
                alert(data.message);
            } else {
                alert(data.message);
                contactDoctorForm.reset();
                contactForm.style.display = 'none';
            }
        })
        .catch(error => {
            console.error('Error sending message:', error);
            alert('Error sending message. Please try again.');
        });
    });

    fetchPatientAppointments();
    fetchDoctors();
});
