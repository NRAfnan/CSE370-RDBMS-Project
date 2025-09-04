# Special Care Platform - Eldercare Management System

A comprehensive Django-based platform for managing eldercare services, including medication tracking, appointment scheduling, care tasks, and health monitoring.

## 🚀 Technology Stack

### Backend
- **Python 3.8+** - Core programming language
- **Django 4.2+** - Web framework
- **MySQL** - Database (with SQLite fallback for development)

### Frontend
- **HTML5** - Markup structure
- **Font Awesome 6** - Icons

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- MySQL Server 8.0 or higher
- pip (Python package manager)

### 1. Clone and Setup
```bash
git clone <repository-url>
cd Eldercare
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. MySQL Database Setup
```sql
-- Create database
CREATE DATABASE eldercare_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create user (optional)
CREATE USER 'eldercare_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON eldercare_db.* TO 'eldercare_user'@'localhost';
FLUSH PRIVILEGES;
```

### 4. Environment Configuration
Create a `.env` file in the project root:
```bash
# Copy from env_example.txt
cp env_example.txt .env
```

Edit `.env` with your actual values:
```bash
DATABASE_URL=mysql://eldercare_user:your_password@localhost:3306/eldercare_db
SECRET_KEY=your-super-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Database Migration
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Run Development Server
```bash
python manage.py runserver
```

Access the application at: http://127.0.0.1:8000

## 🌐 Web Deployment

### Option 1: Traditional VPS/Server

#### 1. Server Requirements
- Ubuntu 20.04+ / CentOS 8+ / Debian 11+
- Python 3.8+
- MySQL 8.0+
- Nginx
- Gunicorn

#### 2. Server Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv mysql-server nginx -y

# Install MySQL client
sudo apt install python3-dev default-libmysqlclient-dev build-essential -y
```

#### 3. Application Deployment
```bash
# Clone application
git clone <repository-url> /var/www/eldercare
cd /var/www/eldercare

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp env_example.txt .env
# Edit .env with production values

# Collect static files
python manage.py collectstatic

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

#### 4. Gunicorn Configuration
Create `/etc/systemd/system/eldercare.service`:
```ini
[Unit]
Description=Eldercare Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/eldercare
Environment="PATH=/var/www/eldercare/venv/bin"
ExecStart=/var/www/eldercare/venv/bin/gunicorn --workers 3 --bind unix:/var/www/eldercare/eldercare.sock special_care_platform.wsgi:application

[Install]
WantedBy=multi-user.target
```

#### 5. Nginx Configuration
Create `/etc/nginx/sites-available/eldercare`:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /var/www/eldercare;
    }

    location /media/ {
        root /var/www/eldercare;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/eldercare/eldercare.sock;
    }
}
```

#### 6. Enable and Start Services
```bash
# Enable and start Gunicorn
sudo systemctl enable eldercare
sudo systemctl start eldercare

# Enable and restart Nginx
sudo ln -s /etc/nginx/sites-available/eldercare /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

### Option 2: Cloud Platforms

#### Heroku
```bash
# Install Heroku CLI
# Create app and set environment variables
heroku create your-eldercare-app
heroku config:set DATABASE_URL=mysql://...
heroku config:set SECRET_KEY=...
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=your-app.herokuapp.com

# Deploy
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

#### DigitalOcean App Platform
- Connect your GitHub repository
- Set environment variables
- Choose Python runtime
- Deploy automatically

#### AWS Elastic Beanstalk
- Create Python environment
- Upload application
- Configure environment variables
- Deploy

## 🔧 Configuration Options

### Database Settings
- **MySQL**: Primary production database
- **SQLite**: Development fallback
- **PostgreSQL**: Alternative production option

### Environment Variables
- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (False for production)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts

## 📱 Features

- **Elder Profiles**: Comprehensive elder information management
- **Medication Management**: Scheduling, tracking, and logging
- **Care Tasks**: Task assignment and completion tracking
- **Appointments**: Health appointment scheduling
- **Vitals Monitoring**: Health metrics tracking
- **Emergency Contacts**: Quick access to emergency information
- **Incident Reporting**: Safety and incident documentation
- **User Management**: Role-based access control
- **Notifications**: Automated alerts and reminders

## 🔒 Security Features

- User authentication and authorization
- Role-based permissions
- CSRF protection
- XSS protection
- Secure password validation
- HTTPS enforcement in production

## 📊 Monitoring & Maintenance

### Logs
```bash
# Application logs
sudo journalctl -u eldercare

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Database Backup
```bash
# Create backup
mysqldump -u username -p eldercare_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore backup
mysql -u username -p eldercare_db < backup_file.sql
```

### Updates
```bash
# Pull latest code
git pull origin main

# Update dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Restart services
sudo systemctl restart eldercare
sudo systemctl restart nginx
```

## 🆘 Support

For technical support or questions:
- Check Django documentation: https://docs.djangoproject.com/
- Review Django deployment guide: https://docs.djangoproject.com/en/stable/howto/deployment/
- MySQL documentation: https://dev.mysql.com/doc/

## 📄 License

This project is licensed under the MIT License.

