import requests
from bs4 import BeautifulSoup
import re

def login_and_scrape_attendance():
    session = requests.Session()
    login_url = 

    # Request the login page to retrieve the CSRF token
    login_page = session.get(login_url)
    soup = BeautifulSoup(login_page.content, 'html.parser')
    csrf_token = soup.find('input', {'name': '_csrf'}).get('value')

    # Replace with your actual credentials
    login_data = {
        'LoginForm[username]': '',
        'LoginForm[password]': '',
        '_csrf': csrf_token
    }
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = session.post(login_url, data=login_data, headers=headers)

    if not response.ok or "Bad Request" in response.text:
        return {"error": "Login failed"}

    attendance_url = "https://mmmut.samarth.edu.in/index.php/student-attendance/attendance/index"
    attendance_response = session.get(attendance_url)

    if not attendance_response.ok:
        return {"error": "Failed to access attendance page"}

    soup = BeautifulSoup(attendance_response.text, 'html.parser')
    buttons = soup.find_all('a', class_='btn btn-primary')
    
    total_classes_taken = 0
    total_present = 0

    for button in buttons:
        link = button.get('href')
        if link:
            full_link = 'https://mmmut.samarth.edu.in' + link
            detail_response = session.get(full_link)

            if detail_response.ok:
                detail_soup = BeautifulSoup(detail_response.content, 'html.parser')
                attendance_table = detail_soup.find('table', id='w0')

                if attendance_table:
                    attendance_summary_row = attendance_table.find('th', text='Attendance Summary')
                    if attendance_summary_row:
                        attendance_summary = attendance_summary_row.find_next('td').text.strip()
                        match = re.search(r'Total Classes Taken:\s*(\d+),\s*Present Count:\s*(\d+)', attendance_summary)
                        if match:
                            total_classes_taken += int(match.group(1))
                            total_present += int(match.group(2))

    return {
        "total_classes_taken": total_classes_taken,
        "total_present": total_present,
        "attendance_percentage": round((total_present / total_classes_taken) * 100, 2) if total_classes_taken > 0 else 0
    }
