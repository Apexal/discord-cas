# Discord + CAS

A simple Flask application that allows RPI members to link their Discord account to their RPI identity. It can be used to limit access to servers to only verified RPI students/faculty.

Current organizations using it:
- ITWS
- RCOS

## Deploy

> Want to use this for your RPI Discord server? Reach out to me Frank Matranga '22 and I can host it for free for you.

### Create Discord Bot

Create a Discord application and bot user. Add it to the desired server with administrator permissions. (More detail coming)

### Environment Variables
- `SITE_TITLE` - Custom website title
- `DISCORD_SERVER_ID` - ID of Discord server
- `DISCORD_CLIENT_ID`, `DISCORD_CLIENT_SECRET`, `DISCORD_REDIRECT_URI` - From the Discord Developers page for your application
- `DISCORD_VERIFIED_ROLE_ID` - ID of the role to add to members when they connect their account
- `FLASK_SECRET_KEY` - Randomly generated secret key for Flask
