# instagram-scrape-followers

python3 -m venv instagram-scrape-followers
cd insta-scrape
source bin/activate
pip -r requirements.txt
curl -L -O https://raw.githubusercontent.com/backroot/instagram-scrape-followers/master/config.ini.sample
curl -L -O https://raw.githubusercontent.com/backroot/instagram-scrape-followers/master/scrape.py
cp config.ini.sample config.ini
# Edit config.ini
python scrape.py <target_account_name>
