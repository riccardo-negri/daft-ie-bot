# Daft.ie scraper bot
Automatically scrape advertisements and send emails for the matching ads.

Compared to [daftlistings](https://github.com/AnthonyBloomer/daftlistings), this bot allows you to additionally exclude listings based on the "available from" and "available for" dates. Moreover, it sends the matching listings via email.

## Requirements
All the requirements are listed in the `requirements.txt` file. You can install them by running:
```bash
pip install -r requirements.txt
```

## Setup
To run the bot you need to set the following variables in the `config.py` file:
- `SMTP_SERVER`: The SMTP server to send the emails from.
- `SMTP_PORT`: The port of the SMTP server.
- `LOG_FILE`: The file to log the bot's output to.
- `ALREADY_SEEN_FILE`: The file to store the already seen listings.
- `EXCLUDE_AVAILABLE_FROM`: The "available from" dates to exclude.
- `EXCLUDE_AVAILABLE_FOR`: The "available for" dates to exclude.

Additionally, you need create the `bot_secrets.py` file. Inside this file you need
to set the following secrets:
- `EMAIL_ADDRESS`: The email address to send the emails from.
- `EMAIL_PASSWORD`: The password of the email address.
- `RECIPIENT_EMAIL`: The email address to send the emails to.

Finally, you can personalize the search by setting the search criteria in the `setup_daft_search()` function in the `x.py` file.
More information on the search criteria available can be found at [daftlistings](https://github.com/AnthonyBloomer/daftlistings).

## Usage
To run the bot, simply run the `x.py` file:
```bash
python3 x.py
```

## Log Example
```
----------------------------------------
ID        : 5871803
Title     : Apartment 39, Virginia Hall, Belgard Square, Belga, Tallaght, Dublin 24
Sections  : Property, Sharing, Apartment
Price     : €750 per month
Link      : http://www.daft.ie/share/apartment-39-virginia-hall-belgard-square-belga-tallaght-dublin-24/5871803
Available From : Immediately
Available For  : 1 Year +
----------------------------------------
Not interesting, not sending email.
----------------------------------------
ID        : 5882296
Title     : the crescent, carrickmines manor, Carrickmines, Dublin 18
Sections  : Property, Sharing, Apartment
Price     : €1,100 per month
Link      : http://www.daft.ie/share/the-crescent-carrickmines-manor-carrickmines-co-dublin/5882296
Available From : Nov 1st, 2024
Available For  : 3 Months
----------------------------------------
Does not match any exclude criteria. Sending email!
Email sent successfully!
----------------------------------------
```
The email sent will contain the same information as the log.

## Credits
Based on [daftlistings](https://github.com/AnthonyBloomer/daftlistings).