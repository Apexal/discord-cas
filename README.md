# Discord + CAS

A platform for RPI organizations to use that allows RPI users to verify their identity with CAS and connect their Discord account. It can be used to limit access to servers to only verified RPI students/faculty, or to distinguish verified RPI users on a server.

Current organizations using it or derivatives:
- ITWS
- RCOS
- NSBE

## Adding Your Organization (Recommended)

I run an instance of this on a free Heroku tier for any organizations that want to use it. All that is required is adding the bot to your server. Simply reach out to me either by [email](mailto:matraf@rpi.edu) or on Discord @Frank‽#0001.


### Self-Hosting

If you prefer to own all of the data, you can self-host the program. All it requires is a Python installation and Postgres database.

### Environment Variables
- `DISCORD_CLIENT_ID`, `DISCORD_CLIENT_SECRET`, `DISCORD_REDIRECT_URI`, `DISCORD_BOT_TOKEN` - From the Discord Developers page for your application
- `DISCORD_VERIFIED_ROLE_ID` - ID of the role to add to members when they connect their account
- `FLASK_SECRET_KEY` - Randomly generated secret key for Flask
<!-- - `REDIS_URL` - Url to Redis server -->
- `DATABASE_URL` - postgres://user:pass@localhost:5432/discord_cas
- `ADMIN_RCS_IDS` - Comma separated RCS IDs for those who have access to add, edit, and remove clients