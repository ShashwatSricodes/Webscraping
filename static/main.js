document.addEventListener('DOMContentLoaded', () => {
    const attendanceDiv = document.getElementById('attendance');
    const ctx = document.getElementById('attendanceChart').getContext('2d');

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

                new Chart(ctx, {
                    type: 'pie',
                    data: {
                        labels: ['Present', 'Absent'],
                        datasets: [{
                            data: [data.total_present, data.total_classes_taken - data.total_present],
                            backgroundColor: ['#9a82db', '#3e3e3e'],
                            hoverOffset: 4,
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: {
                                display: true,
                                position: 'bottom',
                                labels: {
                                    color: '#ffffff'
                                }
                            }
                        },
                        animation: {
                            animateScale: true,
                            animateRotate: true
                        }
                    }
                });
            }
        })
        .catch(error => {
            attendanceDiv.innerHTML = `<p>Error fetching attendance data: ${error.message}</p>`;
        });
});
