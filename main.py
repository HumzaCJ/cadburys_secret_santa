import requests
import time
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%H:%M:%S")
log = logging.getLogger(__name__)

URLS_TO_CHECK = [
    # Links Here
]
WEBHOOKS = [
    # Discord Webhooks To Forward To
]

TARGET_SKIP = "https://secretsanta.cadbury.co.uk/missed-out"
BLOCKED_DOMAINS = ["starfreebies.co.uk", "https://www.latestfreestuff.co.uk"]
REPOST_COOLDOWN = 300

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0 (compatible; CadburysMonitor/1.0)"})

last_posted: dict[str, float] = {}
def post_to_discord(final_url: str) -> None:
    unix_timestamp = int(time.time())
    payload = {
        "embeds": [{
            "title": "New Cadburys Link",
            "url": final_url,
            "color": 16422035,
            "footer": {
                "text": "Powered By Lunar FBA - Cadburys Monitor",
                "icon_url": "https://lunarfba.com/assets/images/lunar_logo.png"
            },
            "fields": [{
                "name": "Time Live",
                "value": f"<t:{unix_timestamp}:f> | <t:{unix_timestamp}:R>"
            }]
        }]
    }

    for webhook in WEBHOOKS:
        while True:
            try:
                r = requests.post(webhook, json=payload, timeout=10)
                if r.status_code == 204:
                    log.info(f"Choccy found → {final_url}")
                    break
                elif r.status_code == 429:
                    time.sleep(2)
                else:
                    break
            except requests.exceptions.RequestException:
                time.sleep(2)

def is_blocked(url: str) -> bool:
    parsed = urlparse(url)
    return (
        url.startswith(TARGET_SKIP)
        or parsed.path.endswith("missed-out")
        or any(domain in parsed.netloc for domain in BLOCKED_DOMAINS)
    )

def check_link(url: str) -> None:
    try:
        r = session.get(url, allow_redirects=True, timeout=10)
        final_url = r.url.strip()

        if is_blocked(final_url):
            return

        now = time.time()
        if final_url in last_posted and now - last_posted[final_url] < REPOST_COOLDOWN:
            return

        post_to_discord(final_url)
        last_posted[final_url] = now

    except requests.exceptions.RequestException:
        pass

def main() -> None:
    log.info(f"Monitoring {len(URLS_TO_CHECK)} links...")
    while True:
        with ThreadPoolExecutor(max_workers=25) as executor:
            futures = [executor.submit(check_link, u) for u in URLS_TO_CHECK]
            for _ in as_completed(futures):
                pass
        time.sleep(1)

if __name__ == "__main__":
    main()
