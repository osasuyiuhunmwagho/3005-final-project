# Group Database Setup

Hey everyone! So we need to set up a shared database for the project. I put together this quick guide based on what we discussed. Let me know if anything doesn't work or if you have questions.

## Quick Checklist

- [ ] Pick how we're hosting the database (Docker seems easiest tbh)
- [ ] Someone creates the database and shares the login info
- [ ] Everyone adds it to pgAdmin
- [ ] Everyone updates their `.env` file
- [ ] Test that it works from your machine
- [ ] Don't mess with the schema without telling people first

## Option 1: Docker (Recommended)

This is probably the easiest way to do it. Whoever has Docker installed can run this:

```bash
docker run --name fitness-center-db \
  -e POSTGRES_PASSWORD=your_shared_password \
  -e POSTGRES_DB=fitness_center_db_group \
  -p 5432:5432 \
  -d postgres:latest
```

Then share these details in our group chat:
- Host: `localhost` (or whatever IP the Docker host is on)
- Port: `5432`
- Database: `fitness_center_db_group`
- User: `postgres`
- Password: `your_shared_password` (obviously use a real password lol)

Everyone else just needs to:
- Add the server in pgAdmin (see below)
- Update your `.env` file

## Option 2: Shared Local Server

If someone wants to host it on their machine instead:

1. On the host machine, you need to:
   - Edit `postgresql.conf` and set `listen_addresses = '*'`
   - Edit `pg_hba.conf` and add `host all all 0.0.0.0/0 md5`
   - Restart PostgreSQL
   - Make sure firewall allows port 5432

2. Create the database:
   ```sql
   CREATE DATABASE fitness_center_db_group;
   CREATE USER group_user WITH PASSWORD 'shared_password';
   GRANT ALL PRIVILEGES ON DATABASE fitness_center_db_group TO group_user;
   ```

3. Share your IP address and the credentials with everyone

4. Everyone connects using that IP

## Setting Up pgAdmin

1. Open pgAdmin
2. Right-click "Servers" → "Register" → "Server"
3. General Tab:
   - Name it something like `Fitness Center DB - Group`
4. Connection Tab:
   - Host: (whatever we decided above)
   - Port: `5432`
   - Maintenance database: `fitness_center_db_group` (or `postgres` if that doesn't work)
   - Username: (the shared username)
   - Password: (the shared password)
   - You can check "Save password" if you want
5. Click Save and hopefully it connects!

## .env File Setup

Everyone needs to create/update their `.env` file in the project root. It should look like this:

```env
# Group Database Configuration
DATABASE_HOST=your_shared_host
DATABASE_PORT=5432
DATABASE_NAME=fitness_center_db_group
DATABASE_USER=group_user
DATABASE_PASSWORD=shared_password
DATABASE_URL=postgresql://group_user:shared_password@your_shared_host:5432/fitness_center_db_group
```

Just replace the values with whatever we actually decided on.

## Rules for Working Together

### Schema Changes

- **Before you change anything:** Message the group chat saying what you're about to modify
- **Only one person runs migrations at a time** - otherwise we'll get conflicts
- If you can test it locally first, that's probably a good idea

### Test Data

- Try to use unique prefixes for your test stuff (like `test_member_1`, `test_member_2`)
- Or use separate schemas if you know how
- **Please clean up your test data when you're done** - don't leave a bunch of junk in there

### Don't Break Each Other's Stuff

- Use transactions when testing (you can ROLLBACK if something goes wrong)
- Don't delete other people's test data without asking
- If you're testing, maybe use IDs that are way out there (like starting at 10000 or something)

## Troubleshooting

### Can't Connect?

- Check if the firewall is blocking it
- Double-check the credentials
- Make sure the database server is actually running
- If you get "permission denied", the user might not have the right privileges

### Other Common Errors

- **"Database does not exist"**: Someone needs to create it first in pgAdmin
- **"Password authentication failed"**: Check your `.env` file, the password might be wrong
- **"Too many connections"**: Some of us might need to close our connections

## IMPORTANT: Don't Commit .env Files!

⚠️ **Seriously, don't commit your `.env` file to git!** It has passwords in it. The `.env` file should already be in `.gitignore` but double-check just in case.

## If You're Stuck

1. Check the main README.md first
2. Ask in the group chat
3. Google the error message (usually works for me)
4. Check the PostgreSQL docs if you're feeling ambitious





