# StormPK web integration — 21 October 2026

The UniversoPristonTale web portal is deployed on the Unraid AEROCOOL host using a custom local `stormpk-integration` branch of `upt-commits/UniversoPristonTale`, located at `/mnt/user/appdata/stormpk-website/source`.

## Verified services

- Public portal: https://priston.hoststorm.com.br (HTTP 200 over HTTPS)
- Nginx Proxy Manager (Oracle): forwards to AEROCOOL `192.168.30.10:3810`
- Portal: `stormpk-portal` Docker container on AEROCOOL
- API: Windows 11 VM `StormPK`, `192.168.30.89:3811`, accessible only from AEROCOOL
- Microsoft SQL Server Express: `UPTPortal` and `UserDB`; SQL TCP remains LAN-firewalled
- Game server TCP 10007 and login server TCP 10009 reachable

The SQL API connection was repaired and tested: 12 tables in UPTPortal and 77 preexisting game accounts in UserDB. A test inserting a new game account plus a linked web account inside one SQL transaction succeeded **and was rolled back**, leaving no new account.

The registration UI now requires only username, email, and password, with a separate Turnstile check; it no longer requires CPF, address or date of birth. The dashboard query was made compatible with least-privilege UserDB permissions. Basic privacy and terms pages are deployed.

## Remaining security dependencies — no claim that login is functional

A dedicated Cloudflare Turnstile widget was created for `priston.hoststorm.com.br` (public sitekey: `0x4AAAAAAFe5ZcWP38X1YkAd`). Its secret is held in a private, chmod-0600 AEROCOOL appdata directory, not in this repository. Automatic delivery of the secret to the Windows VM was blocked by the security layer. An authorized administrator must securely install the secret into `C:\StormPK\WebsiteAPI\.env` as `CAPTCHA_SECRET_KEY` and restart `StormPK Website API` (without revealing the secret to chat or git). A real interactive Turnstile token and replay-rejection test are required before enabling public account operations.

Both `REGISTRATION_ENABLED=false` and `LOGIN_ENABLED=false` are in effect. The backend returns HTTP 503 while disabled and the frontend displays a maintenance notice. An attempted provisioning of a test account was blocked by tool security; **no test account was created by that attempt**.

The local web repository commit currently deployed is `bacee1d`; its source has not been pushed to this repository yet. Avoid claiming it is available from GitHub.

See the local `docs/STORMPK-DEPLOY.md` for operational checks. Do not open SQL directly to the internet.
