# Group Members

# Project CCC

This README outlines the steps to set up and run the Flask web application for Project CCC.

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


6. **Database Setup and Migration**:

   Delete existing SQLite database file if the database is not empty.

   ```
   rm app.db

   ```
   Initialize the Database and generate migration.

   ```
   flask db init
   flask db migrate -m "Initial migration."
   flask db upgrade
   ```

7. **Run the Application**

   Start the Flask development server to run the application locally.

   ```
   flask run
   ```

   The application will be available at `http://127.0.0.1:5000/`.


## Troubleshooting

- If you encounter any issues with package installations, ensure your virtual environment is activated, or check the permissions and settings in your Python environment.
