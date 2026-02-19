# Cadburys Secret Santa Restock Monitor

__**How It Works**__
- You can enter any links in array ``URLS_TO_CHECK``
- You enter your discord webhook(s) in the array ``WEBHOOKS``
- If it's your first time using python or any of the imported librarys, run ``pip install requests logging urllib``
- On a server or any host, locate the directory you've saved this in and type in ``python main.py``

__**Features**__
- No pings will come through if requests fail or redirect to _starfreebies_ or _latestfreestuff_ domains
- Threaded requests to ensure fast times
- No proxies or extra handling (TLS, cURL modifications, cookie/header rotations etc.) required as this is just expanding URLs
- Multi-Discord webhook posts if you wanted to offer the monitor services to other servers
- Spam prevention with a 300s cooldown (5 minutes) on the same link. This is due to 5 minute cart holds on the Cadbury's site 

__**Why I've Open Sourced This**__
- Simply put: I've found a more efficient method to scrape restocks directly from an endpoint on the Secret Santa site, so I thought i'd open source this code for anyone who wants to run this next year

