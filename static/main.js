document.addEventListener('DOMContentLoaded', () => {
    const attendanceDiv = document.getElementById('attendance');

    fetch('/data')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                attendanceDiv.innerHTML = `<p>Error: ${data.error}</p>`;
            } else {
                attendanceDiv.innerHTML = `
                    <p>Total Classes Taken: ${data.total_classes_taken}</p>
                    <p>Total Present: ${data.total_present}</p>
                    <p>Attendance Percentage: ${data.attendance_percentage}%</p>
                `;
            }
        })
        .catch(error => {
            attendanceDiv.innerHTML = `<p>Error fetching attendance data: ${error.message}</p>`;
        });
});
