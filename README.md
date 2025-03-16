## Description
This application fetches random facts or the most recent science articles from public APIs and sends the content to a specified email address.

## Setup Instructions

### 1. Clone the Repository
bash  
git clone <REPOSITORY_URL>  
cd <REPOSITORY_DIRECTORY>  

2. (Optional) Create a Virtual Environment  
It's recommended to use a virtual environment:

bash  
Copy  
python -m venv venv  
# On Windows:  
venv\Scripts\activate  
# On macOS/Linux:  
source venv/bin/activate  

3. Install Dependencies  
Install the required packages using pip:

bash  
Copy  
pip install -r requirements.txt  

If you don't have a requirements.txt, create one with the following content:

nginx  
Copy  
requests  
python-dotenv  

4. Configure Environment Variables  
Create a .env file in the project root directory and add your sender email and Google app password:

env  
Copy  
SENDER_EMAIL=your_email@example.com  
SENDER_PASSWORD=your_google_app_password  

Note: To obtain your Google app password, enable 2-Step Verification on your Google account and generate an app password. See Google's App Password Help for detailed instructions.

How to Run the App  
Run the application by providing the receiver email and a keyword to select the API:

bash  
Copy  
python script.py receiver_email [facts|articles]  

Replace receiver_email with the recipient's email address.  
Use facts to fetch random facts or articles to fetch recent science articles.

Example  
bash  
Copy  
python script.py recipient@example.com facts  

License  
This project is licensed under the MIT License.

Copy
