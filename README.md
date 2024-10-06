# Memorable Insta Bot

## Description
This is a very interesting project, as it is a bot that follows the followers of an Instagram account. Given some target accounts, the bot follows the followers of these accounts, with a criteria that can be configured. Since Instagram has certain restrictions, the bot randomly goes through the instagram feed and also looks at it with criteria, ignoring content that does not meet the criteria. The criteria are evaluated by AI, to have a personalized feed and follow suitable accounts.

![](insta_bot.png)

## Core Features
- **Image Description:** Generates detailed descriptions for images using generative AI.
- **User Engagement Prediction:** Predicts whether a user would be interested in an image based on its description.
- **Local and URL Image Support:** Supports both local image files and images from URLs.
- **Configurable Settings:** Allows customization of various settings through a configuration file.
- **Debug Mode:** Includes a debug mode for easier troubleshooting and development.

## Technologies Used
- **Python:** The primary programming language used for its simplicity and extensive libraries.
- **Pillow:** A Python Imaging Library (PIL) fork that adds image processing capabilities.
- **Requests:** A simple HTTP library for making requests to web services.
- **Google Generative AI:** Utilized for generating image descriptions.
- **Selenium**: A powerful tool for automating web browsers, commonly used for web scraping and automated testing.

## How to use
- You need to have python installed
- Run ``` pip install -r requirements.txt ```
- Then setup the ```TARGET_PAGES.txt``` with the instagram pages names you what the bot choose to look for people to follow
- Setup the .env with the ```GEMINI_API_KEY```


![Python](https://img.shields.io/badge/python-%233776AB.svg?style=for-the-badge&logo=python&logoColor=white)
![Pillow](https://img.shields.io/badge/pillow-%2300C7B7.svg?style=for-the-badge&logo=python&logoColor=white)
![Requests](https://img.shields.io/badge/requests-%23003B57.svg?style=for-the-badge&logo=python&logoColor=white)
![Google Generative AI](https://img.shields.io/badge/google%20generative%20ai-%231FA2F1.svg?style=for-the-badge&logo=google&logoColor=white)
![Google Cloud](https://img.shields.io/badge/GoogleCloud-%234285F4.svg?style=for-the-badge&logo=google-cloud&logoColor=white)
![Selenium](https://img.shields.io/badge/-selenium-%43B02A?style=for-the-badge&logo=selenium&logoColor=white)