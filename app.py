import sys
import os
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

FACTS_API_URL = "https://uselessfacts.jsph.pl/api/v2/facts/random"
ARTICLES_API_URL = ("https://content.guardianapis.com/science?"
                    "order-by=newest&show-fields=bodyText&q=science&api-key=test")

def validate_args(args):
    if len(args) != 3:
        sys.exit("Usage: python script.py receiver_email [facts|articles]")
    
    receiver_email = args[1]
    if "@" not in receiver_email or "." not in receiver_email:
        sys.exit("Please provide a valid email address.")
    
    api_keyword = args[2].lower()
    if api_keyword == "facts":
        api_url = FACTS_API_URL
    elif api_keyword == "articles":
        api_url = ARTICLES_API_URL
    else:
        sys.exit("Please provide a valid API keyword: 'facts' or 'articles'")
    
    return receiver_email, api_url

def get_response_api_1(url):
    responses = [requests.get(url).json() for _ in range(3)]
    return responses

def get_response_api_2(url):
    return requests.get(url).json()

def format_response_api_1(facts):
    return "\n".join(fact["text"] for fact in facts)

def format_response_api_2(articles_json):
    articles = ""
    for result in articles_json.get("response", {}).get("results", []):
        article_link = result.get("id", "No link provided")
        body_text = result.get("fields", {}).get("bodyText", "")
        sentences = body_text.split(". ")[:2]
        body_text_formatted = ". ".join(sentences)
        articles += f"\n{body_text_formatted}\n{article_link}\n"
    return articles

def send_email(sender_email, sender_password, receiver_email, subject, email_content):
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(email_content))
    
    mailserver = smtplib.SMTP("smtp.gmail.com", 587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.ehlo()
    mailserver.login(sender_email, sender_password)
    mailserver.sendmail(sender_email, receiver_email, msg.as_string())
    mailserver.quit()

def main():
    receiver_email, api_url = validate_args(sys.argv)
    
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    
    if not sender_email or not sender_password:
        sys.exit("SENDER_EMAIL and SENDER_PASSWORD must be set in the .env file")
    
    subject = "Random Facts or the Most Recent Articles"
    
    if api_url == FACTS_API_URL:
        facts = get_response_api_1(api_url)
        email_content = format_response_api_1(facts)
    else:
        articles_json = get_response_api_2(api_url)
        email_content = format_response_api_2(articles_json)
    
    send_email(sender_email, sender_password, receiver_email, subject, email_content)

if __name__ == "__main__":
    main()
