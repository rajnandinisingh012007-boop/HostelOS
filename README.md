# HostelOS - Setup Instructions
# ================================

## Project Structure
```
hostelos/
├── index.html              # Login page (Student / Warden / Admin)
├── dashboard-student.html  # Student dashboard
├── dashboard-warden.html   # Warden dashboard  
├── dashboard-admin.html    # Admin dashboard
├── profile-student.html    # Student's own profile (MY PROFILE)
├── students.html           # Admin/Warden: Student management list
├── rooms.html              # Room & inventory management
├── fees.html               # Fee payment (Student) / Fee management (Admin)
├── complaints.html         # Complaint system (all roles)
├── leave.html              # Leave application (Student)
├── leave-warden.html       # Leave approvals (Warden)
├── visitors.html           # Visitor log (Warden/Admin)
├── admin.html              # Reports & Export (Admin)
├── app.py                  # Python Flask backend
├── setup_database.sql      # MySQL database + 30 sample students
└── requirements.txt        # Python dependencies
```

## Step 1: Set Up MySQL Database
```bash
# Login to MySQL
mysql -u root -p

# Run setup script
SOURCE setup_database.sql;
```

## Step 2: Install Python Dependencies
```bash
pip install flask flask-cors mysql-connector-python
```

## Step 3: Configure Database
Edit `app.py` and update DB_CONFIG:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',            # your MySQL username
    'password': 'yourpassword', # your MySQL password  
    'database': 'hostelos',
}
```

## Step 4: Run the Backend
```bash
python app.py
```
Open: http://localhost:5000

## Demo Login Credentials
| Role    | ID       | Password   |
|---------|----------|------------|
| Student | STU001   | student123 |
| Warden  | WAR001   | warden123  |
| Admin   | ADMIN001 | admin123   |

## File Relationships
- index.html → redirects to dashboard-[role].html on login
- dashboard-student.html → profile-student.html, leave.html, complaints.html, fees.html
- dashboard-warden.html → leave-warden.html, complaints.html, visitors.html, students.html, rooms.html
- dashboard-admin.html → students.html, rooms.html, fees.html, complaints.html, visitors.html, admin.html
- students.html → redirects student role to profile-student.html (admin/warden see full list)

## API Endpoints
| Method | Endpoint                     | Description           |
|--------|------------------------------|-----------------------|
| POST   | /api/login                   | User login            |
| GET    | /api/students                | List all students     |
| GET    | /api/students/:id            | Get student details   |
| GET    | /api/rooms                   | List all rooms        |
| GET    | /api/fees                    | List fee records      |
| POST   | /api/fees/pay                | Process fee payment   |
| GET    | /api/complaints              | List complaints       |
| POST   | /api/complaints              | Create complaint      |
| PUT    | /api/complaints/:id/resolve  | Resolve complaint     |
| GET    | /api/leaves                  | List leave requests   |
| POST   | /api/leaves                  | Apply for leave       |
| PUT    | /api/leaves/:id/action       | Approve/reject leave  |
| GET    | /api/visitors                | List visitors         |
| POST   | /api/visitors                | Log new visitor       |
| PUT    | /api/visitors/:id/checkout   | Check out visitor     |
| GET    | /api/stats                   | Dashboard statistics  |
