# Requirements:

- Python 3.13.3 installed on computer
- Pip (if not already installed with Python)

# Instructions to run server:

1. Download and extract Application.zip.
2. A virtual environment needs to be created and activated. If this has already been completed,
    skip to step 3. Ensure the requirements are fulfilled, and then:
       a. Open the command prompt and navigate to the file location. In my case, this is done
          by doing the following command:

          cd /d D:\Application

          The next line should display the location, as so:

          D:\Application>

       b. Install a virtual environment in this folder by executing the following command:

          py -m venv .venv

          Note: Depending on the system and version of python installed, “py” and “python”
          may be interchangeable.

       c. Activate the environment by executing the following command:

          .venv\Scripts\activate

          If done correctly, you should see the following:

          (.venv) D:\Application>

3. The dependencies for the application need to be installed. To do this:
    a. Navigate to web_project:

       cd web_project

    b. Execute the following command (skip if already completed):

       pip install --upgrade -r requirements.txt

       Note: this step may take some time depending on your internet and hardware.

4. While still in the web_project directory, run the server by executing the following command:

    py manage.py runserver

5. To open the server, either copy and paste the link on the line that says “Starting
    development server”, or CTRL + left click on the link. The website will open in your browser.
