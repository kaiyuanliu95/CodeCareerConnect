# Project CCC

This README outlines the steps required to set up and run the Flask web application for the Project CCC.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Setup Instructions

1. **Clone the Repository**

   Clone the project repository to your local machine using the following command:

   ```
   git clone <repository-url>
   ```

2. **Navigate to the Project Directory**

   ```
   cd documents/github/ccc
   ```

3. **Create a Virtual Environment**

   Set up a virtual environment to manage the project's dependencies separately from your global Python environment.

   ```
   python3 -m venv venv
   ```

4. **Activate the Virtual Environment**

   Activate the virtual environment to use it for installing dependencies and running the application.

   ```
   source venv/bin/activate
   ```

5. **Install Dependencies**

   Install the required Python packages specified in the `requirements.txt` file.

   ```
   pip3 install -r requirements.txt
   ```

6. **Additional Packages**

   Install additional packages like `flask_mail` and `email_validator` that are required for specific functionalities within the app.

   ```
   pip3 install flask_mail
   pip3 install email_validator
   pip3 install flask_login
   ```

7. **Database Setup**

   Initialize the database with Flask-Migrate to handle database migrations.

   ```
   flask db init
   flask db migrate -m "Initial migration."
   flask db upgrade
   ```

8. **Run the Application**

   Start the Flask development server to run the application locally.

   ```
   flask run
   ```

   The application will be available at `http://127.0.0.1:5000/`.

## Additional Information

- Ensure to configure the application settings and database connection in the `migrations/alembic.ini` and other configuration files as per your setup.
- Regularly update pip to its latest version to avoid security vulnerabilities and ensure compatibility with packages.
  ```
  pip install --upgrade pip
  ```

## Troubleshooting

- If you encounter any issues with package installations, ensure your virtual environment is activated, or check the permissions and settings in your Python environment.
