import time
import smtplib
import ssl
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from daftlistings import *
from config import *
from bot_secrets import EMAIL_ADDRESS, EMAIL_PASSWORD, RECIPIENT_EMAIL

class Mail:

	def __init__(self):
		self.port = SMTP_SERVER_PORT
		self.smtp_server_domain_name = SMTP_SERVER
		self.sender_mail = EMAIL_ADDRESS
		self.password = EMAIL_PASSWORD

	def send(self, sender_name, address, subject, content):
		ssl_context = ssl.create_default_context()
		service = smtplib.SMTP_SSL(self.smtp_server_domain_name, self.port, context=ssl_context)
		service.login(self.sender_mail, self.password)

		html = "<html><body><p>$(content)</p></body></html>"
		html = html.replace("$(content)", content.replace('\n', "<br>"))

		mime = MIMEMultipart()
		mime['Subject'] = subject
		mime['From'] = formataddr((sender_name, self.sender_mail))
		mime['To'] = address
		mime.attach(MIMEText(html, 'html'))

		service.sendmail(self.sender_mail, address, mime.as_string())

		service.quit()

def setup_daft_search():
    daft = Daft()
    daft.set_location(Location.DUBLIN, Distance.KM10)
    daft.set_search_type(SearchType.SHARING)
    daft.set_property_type(PropertyType.APARTMENT)
    daft.set_suitability(SuitableFor.MALE)
    daft.set_max_price(1400)
    return daft

def print_listing_details(listing, available_from, available_for):
    print_and_log("-" * 40)  # print a divider
    print_and_log(f"{'ID':<10}: {listing.id}")
    print_and_log(f"{'Title':<10}: {listing.title}")
    print_and_log(f"{'Sections':<10}: {', '.join(listing.sections)}")
    print_and_log(f"{'Price':<10}: {listing.price}")
    print_and_log(f"{'Link':<10}: {listing.daft_link}")
    print_and_log(f"{'Available From':<15}: {available_from}")
    print_and_log(f"{'Available For':<15}: {available_for}")
    print_and_log("-" * 40)  # print a divider

def print_and_log(s):
    print(s)
    with open(LOG_FILE, 'a') as f:
        f.write(s + "\n")

def get_available(soup, x):
    available_x_element = soup.find(lambda tag: tag.name=='li' and tag.span != None and tag.span.text == 'Available ' + x)
    if available_x_element is None:
        return NOT_FOUND
    return available_x_element.text.split(":")[1].strip()

def send_email(mail_service, listing, available_from, available_for):  
    email_body = f"""Title: {listing.title}
    Sections: {', '.join(listing.sections)}
    Price: {listing.price}
    Link: {listing.daft_link}
    Available From: {available_from}
    Available For: {available_for}
    """

    mail_service.send(
         "Daft.ie Python Bot", 
         RECIPIENT_EMAIL, 
         f"New listing found: {listing.title}\n",
         email_body)

def main():
    seen_ids = set()
    mail_service = Mail()

    while True:
        try:
            with open(ALREADY_SEEN_FILE, 'a') as f:
                pass
            with open(ALREADY_SEEN_FILE, 'r') as f:
                seen_ids = set(int(line.strip()) for line in f)
            print("{} Seen IDs: {}".format(len(seen_ids), seen_ids))

            daft = setup_daft_search()
            listings = daft.search()

            s = Service(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=s)
            driver.minimize_window()

            for listing in listings:
                if int(listing.id) in seen_ids:
                    print_and_log("Skipping ID " + str(listing.id))
                    continue
                
                driver.get(listing.daft_link)
                complete_page = driver.page_source
                
                
                soup = BeautifulSoup(complete_page, 'html.parser')
                available_from = get_available(soup, "From")
                available_for = get_available(soup, "For")
            
                print_listing_details(listing, available_from, available_for)

                if available_from not in EXCLUDE_AVAILABLE_FROM and available_for not in EXCLUDE_AVAILABLE_FOR:
                    print_and_log("Does not match any exclude criteria. Sending email!")
                    send_email(mail_service, listing, available_from, available_for)
                    print_and_log("Email sent successfully!")
                else:
                    print_and_log("Not interesting, not sending email.")
                     
                seen_ids.add(listing.id)
                with open(ALREADY_SEEN_FILE, 'a') as f:
                    f.write(f"{listing.id}\n")
                
            driver.quit()
            print_and_log("Finished analyzing list!")
            print_and_log("Waiting for 15 minutes before checking again...")    
            print_and_log("*" * 40)  # print a divider
        except Exception as e:
            print_and_log(f"An error occurred: {e}")

        # wait for 15 min
        time.sleep(900)

if __name__ == "__main__":
    main()
