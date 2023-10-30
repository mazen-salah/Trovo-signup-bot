# Trovo Account Registration Bot

## Project Overview
The Trovo Account Registration Bot is a Python automation script that simplifies the process of creating new Trovo accounts. Trovo is a live streaming platform, and this script automates the account registration process by filling out the registration form, and verifying email addresses.

## Key Features
- Generates random usernames and passwords.
- Utilizes temporary email addresses for account verification.
- **Note**: The user needs to manually solve the CAPTCHA challenge.
- Logs account details in a text file for future reference.

## How It Works
1. The script navigates to the Trovo registration page using a proxy service to access the website.
2. It populates the registration form with randomly generated credentials, including a username, password, birthdate, and a temporary email address.
3. The user manually solves the CAPTCHA challenge.
4. The script verifies the email address by extracting the verification code from the temporary email.
5. The account details are saved to a text file for later use.

## Usage
- To run the script, execute the `main.py` file.
- Ensure that you have the required Python libraries (e.g., Selenium, undetected_chromedriver, Faker) installed.

## Prerequisites
- Python 3.x
- Required Python packages mentioned in `requirements.txt`.

## Installation
1. Clone this repository to your local machine.
2. Install the required Python packages using `pip install -r requirements.txt`.

## Two-Step Verification
The `verification.py` script is used for two-step verification when logging in.

## Contributing
If you would like to contribute to this project, feel free to fork the repository, make changes, and submit a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author
Mazen Tamer

## Contact
Email: mazentamer3056@gmail.com

Please use this script responsibly and in accordance with Trovo's terms of service.
