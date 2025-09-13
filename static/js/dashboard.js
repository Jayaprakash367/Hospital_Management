document.addEventListener('DOMContentLoaded', function() {
    const statsDiv = document.getElementById('stats');

    function fetchStats() {
        Promise.all([
            fetch('/api/patients').then(res => res.json()),
            fetch('/api/doctors').then(res => res.json()),
            fetch('/api/appointments').then(res => res.json())
        ])
        .then(([patients, doctors, appointments]) => {
            const today = new Date().toISOString().split('T')[0];
            const todayAppointments = appointments.filter(app => app.appointment_date === today);

            statsDiv.innerHTML = `
                <div class="stat-card">
                    <h3>Total Patients</h3>
                    <p>${patients.length}</p>
                </div>
                <div class="stat-card">
                    <h3>Total Doctors</h3>
                    <p>${doctors.length}</p>
                </div>
                <div class="stat-card">
                    <h3>Today's Appointments</h3>
                    <p>${todayAppointments.length}</p>
                </div>
            `;
        })
        .catch(error => {
            statsDiv.innerHTML = '<p>Error loading statistics.</p>';
            console.error('Error fetching stats:', error);
        });
    }

    fetchStats();
});
