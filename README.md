**Django JWT Authentication Project**
This repository contains a Django project that implements JWT (JSON Web Token) authentication. It's designed to provide a straightforward example of how to secure your Django REST APIs using JWT.

**Prerequisites**
Before you begin, ensure you have met the following requirements:

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

**Setting Up the Project**
To get this project up and running on your local machine, follow these steps:

1. Clone the Repository

git clone git@github.com:waqasidrees07/django-token-authentication.git
cd django-token-authentication

2. Create and Activate a Virtual Environment

- For Unix/macOS:
python3 -m venv env
source env/bin/activate

- For Windows:
python -m venv env
.\env\Scripts\activate

3. Install Required Packages
pip install -r requirements.txt

4. Set Up Environment Variables
Copy the .env_example file to a new file named .env.
Modify the .env file to include your specific settings (e.g., Email data, DATABASE data).

5. Run Migrations
python manage.py migrate


6. Run the Development Server
python manage.py runserver
Your Django project should now be running at http://localhost:8000.

**Using the API**
To interact with the API, you can use Postman. A Postman collection has been provided to help you get started with the available endpoints.

Import Postman Collection: https://api.postman.com/collections/22964694-6347544f-5ceb-4a4e-80d1-6f60b39136fd?access_key=PMAT-01HS0J2SKDAQE25F6PK2JX4GYA

**Contributing**
Contributions to this project are welcome! To contribute, please follow these steps:

Fork the repository.
Create a new branch (git checkout -b feature/AmazingFeature).
Commit your changes (git commit -m 'Add some AmazingFeature').
Push to the branch (git push origin feature/AmazingFeature).
Open a pull request.

**Acknowledgments**
Thank you to everyone who has contributed to making this project better.
