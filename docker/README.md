# SkillSwap Docker Demo Setup

This directory contains Docker configuration for easy presentation and demo deployment of the SkillSwap platform.

## Quick Start for Presentations

### One-Command Demo Setup
```bash
# Build and start the demo with populated data
docker-compose up --build
```

This single command will:
- Build the Docker image with all dependencies
- Set up the database with migrations
- Create admin user (admin/admin123)
- Populate 25 demo users with complete profiles and skills
- Start the development server on http://localhost:8000

### Demo Credentials
- **Admin Panel**: http://localhost:8000/admin/
  - Username: `admin`
  - Password: `admin123`
- **Demo Users**: Various populated users with realistic profiles and skills

## Manual Docker Commands

### Build the Image
```bash
docker build -t skillswap-demo .
```

### Run Container
```bash
docker run -p 8000:8000 -v $(pwd)/media:/app/media skillswap-demo
```

### Clean Restart
```bash
# Stop and remove containers
docker-compose down

# Rebuild and restart with fresh data
docker-compose up --build
```

## Demo Features Included

### Pre-populated Data
- 25 diverse user profiles with realistic information
- Skills across all categories (Technology, Languages, Music, etc.)
- Complete location data (various cities and countries)
- Profile pictures and bio information
- Realistic skill offers and requests
- Sample ratings and reviews

### Demo User Types
- **Sarah Martinez** - Web developer offering Django lessons, seeking Italian
- **Marco Rossi** - Italian teacher offering language lessons, seeking tech skills
- **Emma Johnson** - Designer offering UI/UX lessons, seeking photography
- **And 22 more diverse profiles...**

## Presentation Workflow

### Before Your Presentation
1. **Start the Demo**: `docker-compose up --build`
2. **Wait for Setup**: Watch for "Demo setup complete!" message
3. **Verify Access**: Visit http://localhost:8000
4. **Test Key Flows**: Login, browse skills, filter users

### During Presentation
- **Clean Environment**: Fresh data every time you restart
- **Predictable Demo**: Same users and skills for consistent demo flow
- **No Dependencies**: Works on any machine with Docker
- **Quick Reset**: `docker-compose restart` for fresh demo state

### After Presentation
```bash
# Stop the demo
docker-compose down

# Clean up (optional)
docker system prune
```

## Troubleshooting

### Port Already in Use
```bash
# Use different port
docker-compose up --build -p 8001:8000
```

### Permission Issues
```bash
# Make entrypoint script executable
chmod +x docker-entrypoint.sh
```

### Fresh Database
```bash
# Remove existing database and restart
rm db.sqlite3
docker-compose up --build
```

## Development vs Demo

This Docker setup is optimized for presentations and demos. For development work, continue using your local virtual environment setup with the convenience scripts (`./dev-server.sh`, `./manage.sh`).

## Technical Details

### Docker Image Features
- **Python 3.11**: Latest stable Python version
- **Slim Base**: Optimized for smaller image size
- **System Dependencies**: Includes image processing libraries for Pillow
- **Static Files**: Pre-collected for faster startup
- **Auto-Setup**: Automatic database setup and data population

### Security Notes
- Demo credentials are intentionally simple for presentation purposes
- Not suitable for production deployment without security enhancements
- Database and media files are persisted via Docker volumes
