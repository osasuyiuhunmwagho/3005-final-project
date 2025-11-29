# Environment Configuration

This folder contains environment variable templates for the fitness center management application.

## Setup Instructions

1. Copy the `template.env` file to the project root as `.env`:
   ```bash
   cp env/template.env .env
   ```

2. Edit the `.env` file with your actual PostgreSQL database credentials:
   - Update `DATABASE_HOST` (usually `localhost` if using pgAdmin locally)
   - Update `DATABASE_PORT` (default PostgreSQL port is `5432`)
   - Update `DATABASE_NAME` (create a database in pgAdmin called `fitness_center_db` or your preferred name)
   - Update `DATABASE_USER` (default is usually `postgres`)
   - Update `DATABASE_PASSWORD` (your PostgreSQL password)

3. Generate a secure `SECRET_KEY` for your application:
   ```python
   import secrets
   print(secrets.token_urlsafe(32))
   ```

## Individual PostgreSQL Setup in pgAdmin

For **personal/individual development**:

1. Open pgAdmin
2. Connect to your local PostgreSQL server
3. Create a new database (e.g., `fitness_center_db`)
4. Note down your connection details (host, port, database name, username, password)
5. Use these details in your `.env` file

## Group Collaboration Setup (Shared Database)

For **team collaboration** where all members work on the same database:

### Option A: Shared Local Server (Same Network)

1. **Team Lead Setup:**
   - One team member (or everyone on the same network) sets up PostgreSQL server
   - Configure PostgreSQL to accept remote connections (edit `postgresql.conf` and `pg_hba.conf`)
   - Create a shared database: `fitness_center_db_group`
   - Create a shared user: `group_user` with appropriate permissions
   - Share the connection details with team members

2. **All Team Members:**
   - Open pgAdmin
   - Add a new server connection with the shared database details
   - Use the shared database connection details in your `.env` file
   - Coordinate with team to avoid conflicts when running migrations or making schema changes



1. **Team Lead:**
   ```bash
   # Create a shared Docker PostgreSQL container
   docker run --name fitness-center-db -e POSTGRES_PASSWORD=shared_password -e POSTGRES_DB=fitness_center_db_group -p 5432:5432 -d postgres
   ```

2. **All Team Members:**
   - Connect to the Docker container's exposed port
   - Use `localhost:5432` in `.env` if running locally
   - Use Docker container host IP if accessing remotely

### Group Coordination Best Practices

- **Coordinate schema changes**: Use version control for database migrations
- **Use separate test data**: Each developer should have their own test data or use specific prefixes
- **Communicate before major changes**: Alert team before running migrations or altering schema
- **Document connection details**: Keep connection info in a shared document (password-protected) or password manager
- **Use transactions**: When testing, wrap operations in transactions you can rollback
- **Backup regularly**: Before major changes, export the database schema and data

## Switching Between Individual and Group Database

In your `.env` file, you can comment/uncomment the database configuration sections:
- Uncomment **OPTION 1** for individual local development
- Uncomment **OPTION 2** for shared group database

Make sure only ONE option is active at a time.

## Security Note

The `.env` file is already in `.gitignore` and will not be committed to version control.
Never commit sensitive credentials like passwords or secret keys.

**For Group Work:**
- Share credentials securely (password manager, encrypted chat)
- Rotate passwords periodically if using a shared database
- Use read-only accounts for team members who only need to query data

