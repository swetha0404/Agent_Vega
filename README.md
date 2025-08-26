# PingFederate Ops Agent

A CLI tool for managing PingFederate license operations with intelligent intent routing using CrewAI.

## Features

- **License Management**: Monitor and update PingFederate licenses across multiple instances
- **Daily Monitoring**: Automated daily license status checks with expiry warnings
- **Natural Language Interface**: Use CrewAI for intent-based CLI interactions
- **MongoDB Caching**: Fast license status retrieval from cached data
- **Simulated Environment**: Complete FastAPI-based PingFederate API simulator for testing

## Quick Start
### Simulator logs: FastAPI access logs when running simulator

## GitHub Repository Setup

### Preparing for GitHub Upload

Before uploading to GitHub, ensure you have:

1. **Clean up sensitive data**:
   ```bash
   # Remove any .env files with real API keys
   # Ensure .env is in .gitignore
   echo ".env" >> .gitignore
   echo "*.env" >> .gitignore
   echo "__pycache__/" >> .gitignore
   echo "*.pyc" >> .gitignore
   echo ".pytest_cache/" >> .gitignore
   echo "venv/" >> .gitignore
   echo "build/" >> .gitignore
   echo "dist/" >> .gitignore
   echo "*.egg-info/" >> .gitignore
   ```

2. **Create example environment file**:
   ```bash
   # Create .env.example with template values
   echo "# Copy this file to .env and update with your values" > .env.example
   echo "USE_FILE_STORAGE=true" >> .env.example
   echo "OPENAI_API_KEY=sk-your-openai-api-key-here" >> .env.example
   echo "SIM_BASE_URL=http://localhost:8080" >> .env.example
   ```

3. **Test the complete setup**:
   ```bash
   # Run full test suite
   make test
   # Or manually:
   pytest -v
   ```

### Repository Structure for GitHub

```
your-repo/
├── README.md              # This comprehensive guide
├── LICENSE                # MIT License
├── .gitignore            # Exclude sensitive files
├── .env.example          # Template for environment variables
├── pyproject.toml        # Python project configuration
├── requirements.txt      # Alternative dependency list (optional)
├── Makefile             # Development shortcuts
├── pf_agent/            # Main source code
├── samples/             # Sample license files
├── References/          # Documentation
└── tests/               # Test files
```

### Creating requirements.txt (Optional)

Some users prefer requirements.txt:

```bash
# Generate requirements.txt from pyproject.toml
pip freeze > requirements.txt
```

### Installation Instructions for GitHub Users

Add this section to your GitHub README:

```markdown
## Installation from GitHub

1. **Clone and setup**:
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   python -m venv venv
   venv\Scripts\activate  # Windows
   pip install -e .
   ```

2. **Configure environment**:
   ```bash
   copy .env.example .env
   # Edit .env with your OpenAI API key
   ```

3. **Run**:
   ```bash
   pf-agent simulate up
   ```
```### Prerequisites

- **Python 3.11 or higher**
- **Git** (for cloning the repository)
- **MongoDB** (optional - can use file storage instead)

### Installation for Personal Use

#### 1. Clone the Repository

```bash
git clone <repository-url>
cd "Agentic Workflow"
```

#### 2. Set Up Python Environment

**Windows (PowerShell/Command Prompt):**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -e .
```

**macOS/Linux:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -e .
```

#### 3. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Option 1: Use file storage (no MongoDB required - recommended for personal use)
USE_FILE_STORAGE=true

# Option 2: Use MongoDB (if you have MongoDB installed)
# MONGO_URI=mongodb://localhost:27017
# DB_NAME=pf_agent

# OpenAI API Key (required for CrewAI natural language features)
# Get your key from: https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-your-actual-openai-api-key-here

# Simulator configuration (default values)
SIM_BASE_URL=http://localhost:8080
```

#### 4. Alternative Setup Using Make (Windows)

If you have `make` installed:

```bash
# Automated setup
make dev

# Activate the created environment
venv\Scripts\activate
```

#### 5. Verify Installation

```bash
# Check if pf-agent is installed correctly
pf-agent --help
```

### Run Simulator

```bash
# Start the PingFederate API simulator
pf-agent simulate up
```

The simulator will run on http://localhost:8080 with endpoints:
- `/pf1/license`, `/pf2/license`, etc. (GET/PUT)
- `/pf*/license/agreement` (GET/PUT)

## Running the Project

### Step 1: Start the Simulator

The project includes a FastAPI-based PingFederate simulator for testing. Start it first:

```bash
# Activate your virtual environment if not already active
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Start the simulator
pf-agent simulate up
```

The simulator will start on http://localhost:8080 and simulate multiple PingFederate instances.

### Step 2: Basic Operations

Once the simulator is running, you can perform various operations:

```bash
# Check all license statuses
pf-agent run "check license"

# Get specific instance license
pf-agent license get --instance pf1

# Apply a sample license
pf-agent license apply --instance pf-dev-1 --file ./samples/pf_new.lic

# Manual refresh from APIs
pf-agent refresh
```

### Step 3: License Update Operations

The project includes comprehensive license updating capabilities:

#### Basic License Updates

```bash
# Apply a new license to a specific instance
pf-agent license apply --instance pf1 --file ./samples/pf_new.lic

# Apply license with full path
pf-agent license apply --instance pf-prod-1 --file "C:\path\to\your\license.lic"

# Apply license using natural language
pf-agent run "apply new license to pf-dev-1"
```

#### License Update Scenarios

```bash
# Renew an expiring license
pf-agent license apply --instance pf2 --file ./samples/pf_extended.lic

# Update from evaluation to enterprise license
pf-agent license apply --instance pf1 --file ./samples/pf_enterprise.lic

# Emergency license replacement (for expired licenses)
pf-agent license apply --instance pf3 --file ./samples/pf_emergency.lic
```

#### Bulk License Updates

```bash
# Update multiple instances (using different licenses)
pf-agent license apply --instance pf-prod-1 --file ./samples/pf_new.lic
pf-agent license apply --instance pf-prod-2 --file ./samples/pf_new.lic
pf-agent license apply --instance pf-dev-1 --file ./samples/pf_dev_license.lic

# Check status after updates
pf-agent run "check all license status"
```

#### What Happens During License Update

1. **File Validation**: Checks if the license file exists and is readable
2. **License Encoding**: Converts license file to base64 for API transmission
3. **API Application**: Sends the license to the PingFederate instance via REST API
4. **Verification**: Re-fetches license data to confirm the update was successful
5. **Database Update**: Updates the local cache (MongoDB or file storage) with new license info
6. **Audit Trail**: Creates an audit record of the license update operation
7. **Notifications**: Shows status and sends simulated Slack notifications
8. **Status Check**: Displays the new expiry date and license status

### Step 4: Test Different Scenarios

The project includes sample license files for testing:

```bash
# Test with an expired license
pf-agent license apply --instance pf1 --file ./samples/pf_expired.lic

# Test with an expiring soon license
pf-agent license apply --instance pf2 --file ./samples/pf_expiring_soon.lic

# Test with a new license
pf-agent license apply --instance pf3 --file ./samples/pf_new.lic
```

### Step 4: Monitor License Status

```bash
# Check overall status
pf-agent run "show me all license details"

# Check which licenses are expiring
pf-agent run "check which licenses are expiring soon"
```

### Running Tests

```bash
# Run all tests to verify everything works
pytest

# Run specific test files
pytest test_simulator.py
pytest test_endpoints.py
```

### Basic Usage

```bash
# Check all license statuses (from cache)
pf-agent run "check license"

# Get specific instance license
pf-agent license get --instance pf-prod-1

# Apply new license
pf-agent license apply --instance pf-dev-1 --file ./samples/pf_new.lic

# Manual refresh from APIs
pf-agent refresh
```

### Natural Language Commands

```bash
# These all work with CrewAI intent routing:
pf-agent run "show me all license details"
pf-agent run "check which licenses are expiring soon"
pf-agent run "apply new license to pf-prod-1"

# Skip NL processing with explicit commands:
pf-agent license get --no-nl
```

## License Update Management

### Overview

The PingFederate Ops Agent provides comprehensive license update capabilities, allowing you to:
- Apply new licenses to PingFederate instances
- Renew expiring licenses before they expire
- Replace expired licenses immediately
- Track all license changes with full audit trails
- Receive notifications about license status changes

### License Update Commands

#### Direct License Application

```bash
# Basic license update
pf-agent license apply --instance <instance-id> --file <license-file>

# Examples:
pf-agent license apply --instance pf-prod-1 --file ./samples/pf_new.lic
pf-agent license apply --instance pf-dev-2 --file "/path/to/license.lic"
```

#### Natural Language License Updates

```bash
# AI-powered license updates using CrewAI
pf-agent run "apply new license to pf-prod-1"
pf-agent run "update license for pf-dev-2"
pf-agent run "renew the license on pf-staging"
```

### License File Formats Supported

The simulator and API client support multiple license file formats:

#### Format 1: Simple Key-Value Format
```
LICENSE_TYPE=PingFederate
ISSUED_TO=Acme Corporation
PRODUCT=PingFederate  
VERSION=11.3
EXPIRY=2026-01-15
FEATURES=SSO,SAML
```

#### Format 2: PingFederate Native Format
```
ID=00759625
WSTrustSTS=true
OAuth=true
Product=PingFederate
Version=12.2
ExpirationDate=2026-01-15
Organization=Acme Corporation
```

#### Format 3: Extended Format (Recommended)
```
ID=00759625
Product=PingFederate
Version=12.2
Tier=Enterprise
IssueDate=2025-08-25
ExpirationDate=2026-01-15
Organization=Acme Corporation
Signature=1A89744AFC2B1325352E72461C3D6742F697A123
```

### License Update Workflow

1. **Pre-Update Validation**
   ```bash
   # Check current license status before updating
   pf-agent license get --instance pf-prod-1
   ```

2. **Apply New License**
   ```bash
   # Apply the new license
   pf-agent license apply --instance pf-prod-1 --file ./new-license.lic
   ```

3. **Verify Update**
   ```bash
   # Confirm the update was successful
   pf-agent license get --instance pf-prod-1
   
   # Or check all instances
   pf-agent run "show me all license details"
   ```

4. **Monitor Status**
   ```bash
   # Refresh data and check for any issues
   pf-agent refresh
   ```

### Advanced License Update Scenarios

#### Emergency License Replacement

For expired licenses that need immediate replacement:

```bash
# 1. Check which licenses are expired
pf-agent run "show expired licenses"

# 2. Apply emergency licenses
pf-agent license apply --instance pf-prod-1 --file ./emergency-license.lic
pf-agent license apply --instance pf-prod-2 --file ./emergency-license.lic

# 3. Verify all instances are now valid
pf-agent refresh
```

#### License Renewal Process

For licenses expiring soon:

```bash
# 1. Check which licenses are expiring
pf-agent run "check which licenses are expiring soon"

# 2. Apply renewed licenses before expiry
pf-agent license apply --instance pf-staging --file ./renewed-license.lic

# 3. Schedule production updates during maintenance window
# (Use the same command during your maintenance window)
pf-agent license apply --instance pf-prod-1 --file ./renewed-license.lic
```

#### Development to Production License Migration

```bash
# 1. Test with development license first
pf-agent license apply --instance pf-dev-1 --file ./enterprise-license.lic

# 2. Verify functionality
pf-agent license get --instance pf-dev-1

# 3. Apply to staging
pf-agent license apply --instance pf-staging --file ./enterprise-license.lic

# 4. Apply to production (during maintenance)
pf-agent license apply --instance pf-prod-1 --file ./enterprise-license.lic
```

### License Update Best Practices

1. **Test First**: Always test license updates in development/staging environments
2. **Backup**: Keep copies of current working licenses before applying new ones
3. **Schedule**: Plan license updates during maintenance windows for production
4. **Monitor**: Use the daily monitoring to track expiry dates proactively
5. **Document**: Keep records of license update schedules and renewal dates
6. **Verify**: Always check license status after applying updates
7. **Audit**: Review audit logs to track all license changes

## Configuration

### Environment Variables

- `MONGO_URI`: MongoDB connection string (default: mongodb://localhost:27017)
- `DB_NAME`: Database name (default: pf_agent)
- `SIM_BASE_URL`: Simulator base URL (default: http://localhost:8080)
- `SLACK_WEBHOOK`: Slack webhook for notifications (simulated in MVP)

### Inventory Configuration

Edit `inventory.yaml` to configure your PingFederate instances:

```yaml
instances:
  - id: pf-prod-1
    name: PF Admin Node 1
    env: prod
    base_url: http://localhost:8080/pf1
  # ... more instances
```

## Daily Monitoring

### APScheduler (Recommended)

The scheduler runs automatically when you start any pf-agent command:

```bash
# Scheduler starts automatically and runs daily at 07:00
pf-agent refresh  # Also triggers immediate refresh
```

### System Cron (Alternative)

Add to your crontab:

```bash
# Daily license refresh at 7 AM
0 7 * * * /path/to/venv/bin/pf-agent refresh >> /var/log/pf-agent.log 2>&1
```

## Development

### Quick Commands Using Make

If you have `make` installed, you can use these shortcuts:

```bash
# Setup development environment
make dev

# Run simulator
make simulate

# Run tests
make test

# Manual refresh
make refresh

# Example license application
make apply

# Clean build artifacts
make clean
```

### Manual Commands (Without Make)

```bash
# Start simulator manually
python -m pf_agent.simulators.pingfed_mock

# Or using the CLI
pf-agent simulate up

# Run tests manually
python -m pytest

# Check specific components
python test_simulator.py
python test_endpoints.py
```

### Development Setup

For contributing to the project:

```bash
# Install development dependencies
pip install -e .[dev]

# Run linting tools
make lint
# Or manually:
black pf_agent/
isort pf_agent/
mypy pf_agent/
```

### Make Commands

```bash
# Setup development environment
make dev

# Run simulator
make simulate

# Run tests
make test

# Manual refresh
make refresh

# Example license application
make apply
```

### Testing

```bash
# Run all tests
pytest

# Run specific test categories
pytest tests/test_simulator.py
pytest tests/test_services.py
pytest tests/test_cli.py
```

## Project Structure & Components

### What This Project Does

This is a **PingFederate License Management System** that:
- **Monitors** license expiration dates across multiple PingFederate instances
- **Provides** a CLI interface for license operations
- **Uses AI** (CrewAI) for natural language command processing
- **Includes** a complete PingFederate API simulator for testing
- **Stores** license data in MongoDB or local files

### Directory Structure

```
pf_agent/                   # Main package
├── cli.py                 # Command-line interface (main entry point)
├── config.py              # Configuration management
├── inventory.yaml         # List of PingFederate instances to monitor
├── agents/                # AI agents for natural language processing
│   ├── crew.py           # CrewAI agent definitions
│   └── intents.py        # Intent recognition for user commands
├── tools/                 # Core utilities and integrations
│   ├── db.py             # Database operations (MongoDB/file storage)
│   ├── pf_client.py      # PingFederate API client
│   ├── repos.py          # Data repositories
│   ├── scheduler.py      # Background job scheduling
│   └── notifier.py       # Notification system
├── domain/                # Business logic
│   ├── models.py         # Data models (License, Instance, etc.)
│   ├── services.py       # Business services
│   └── mapping.py        # Data transformation utilities
├── simulators/            # Testing infrastructure
│   ├── pingfed_mock.py   # FastAPI simulator mimicking PingFederate API
│   └── seed_data.py      # Sample test data
└── tests/                 # Test suite

samples/                    # Sample license files for testing
├── pf_expired.lic         # Expired license
├── pf_expiring_soon.lic   # License expiring within 30 days
├── pf_new.lic             # Valid license with long expiry
└── ...

References/                 # Documentation and examples
├── swagger.PingFed.json   # PingFederate API specification
└── License_Summary.ipynb  # Jupyter notebook with analysis examples
```

### Key Components Explained

1. **CLI Interface (`cli.py`)**: Main entry point - handles all `pf-agent` commands
2. **Simulator (`simulators/pingfed_mock.py`)**: Fake PingFederate API for testing
3. **AI Agents (`agents/`)**: Process natural language commands like "check licenses"
4. **License Repository (`tools/repos.py`)**: Handles storing/retrieving license data
5. **Scheduler (`tools/scheduler.py`)**: Runs daily license checks automatically

## Architecture

### Database Schema

**licenses collection:**
```json
{
  "instance_id": "pf-prod-1",
  "instance_name": "PF Admin Node 1", 
  "env": "prod",
  "license_key_id": "LIC-ABC123",
  "issued_to": "Acme Corp",
  "product": "PingFederate",
  "expiry_date": "2025-12-31",
  "days_to_expiry": 120,
  "status": "OK",
  "last_synced_at": "2025-08-23T10:00:00Z",
  "source": "pf-api"
}
```

**audits collection:**
```json
{
  "timestamp": "2025-08-23T10:00:00Z",
  "actor": "system",
  "action": "refresh",
  "instance_id": "pf-prod-1",
  "details": {"status": "OK", "days_to_expiry": 120}
}
```

## Status Thresholds

- **OK**: More than 30 days until expiry
- **WARNING**: 30 days or less until expiry  
- **EXPIRED**: Past expiry date

## Example Workflows

### Daily Monitoring Workflow

1. APScheduler triggers daily at 07:00
2. Reads `inventory.yaml` for all instances
3. Calls simulator `/license` endpoint for each instance
4. Updates MongoDB with current license status
5. Sends Slack notifications for WARNING/EXPIRED licenses

### License Application Workflow

1. User runs: `pf-agent license apply --instance pf-prod-1 --file new.lic`
2. Validates license file exists and is readable
3. Reads license file and base64 encodes content
4. Calls simulator `PUT /license` with encoded data
5. Simulator parses `EXPIRY=YYYY-MM-DD` or `ExpirationDate=YYYY-MM-DD` from license content
6. Re-fetches license data to confirm update was successful
7. Updates MongoDB/file storage with new license information
8. Creates audit record with update details and timestamp
9. Shows success message with new expiry date and status
10. Sends notification (simulated Slack message) about license update

### License Update Scenarios

#### Proactive License Renewal
```bash
# Monitor for licenses expiring in 30 days
pf-agent run "check which licenses are expiring soon"

# Apply renewed license before expiry
pf-agent license apply --instance pf-prod-1 --file ./renewed-license.lic

# Verify update
pf-agent license get --instance pf-prod-1
```

#### Emergency License Replacement
```bash
# Check for expired licenses
pf-agent run "show expired licenses"

# Apply emergency license immediately
pf-agent license apply --instance pf-prod-1 --file ./emergency-license.lic

# Refresh all data and verify
pf-agent refresh
```

#### Bulk License Updates
```bash
# Update multiple instances (can be scripted)
for instance in pf-prod-1 pf-prod-2 pf-staging; do
  pf-agent license apply --instance $instance --file ./new-enterprise.lic
done

# Verify all updates
pf-agent run "show me all license details"
```

## Simulator Details

The FastAPI simulator provides realistic PingFederate API responses:

- **GET /pf*/license**: Returns current license information
- **PUT /pf*/license**: Accepts base64-encoded license files
- **GET/PUT /pf*/license/agreement**: License agreement endpoints

License files should contain authentic PingFederate format with `ExpirationDate=YYYY-MM-DD` for simulator parsing.

Example license format:
```
ID=00759625
WSTrustSTS=true
OAuth=true
SaasProvisioning=true
Product=PingFederate
Version=12.2
EnforcementType=3
Tier=Enterprise
IssueDate=2025-08-25
ExpirationDate=2026-01-15
GracePeriod=1
DeploymentMethod=Traditional
Organization=Acme Corporation
SignCode=EE1F
Signature=1A89744AFC2B1325352E72461C3D6742F697A123GBB0201678634525363636363868363863863
```

## Troubleshooting

### Personal Device Setup Issues

#### Python/Virtual Environment Issues

**Problem**: `python` command not found
```bash
# Windows: Try python3 or py
py -m venv venv
# Or
python3 -m venv venv

# macOS/Linux: Ensure Python 3.11+ is installed
python3 --version
```

**Problem**: Virtual environment activation fails
```bash
# Windows (if PowerShell execution policy is restricted)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Alternative activation methods
# Windows Command Prompt:
venv\Scripts\activate.bat

# Windows PowerShell:
venv\Scripts\Activate.ps1

# Git Bash on Windows:
source venv/Scripts/activate
```

**Problem**: Package installation fails
```bash
# Update pip first
python -m pip install --upgrade pip

# Install with verbose output to see errors
pip install -e . -v
```

#### Port/Network Issues

**Problem**: Port 8080 already in use
```bash
# Windows: Find what's using the port
netstat -ano | findstr :8080

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F

# Or change the port in your .env file
SIM_BASE_URL=http://localhost:8081
```

**Problem**: Simulator won't start
```bash
# Check if port is available
netstat -an | findstr :8080

# Try a different port
pf-agent simulate up --port 8081
```

#### Database/Storage Issues

**Problem**: MongoDB connection errors (if using MongoDB)
```bash
# Switch to file storage instead (add to .env)
USE_FILE_STORAGE=true

# Or install MongoDB locally
# Windows: Download from https://www.mongodb.com/try/download/community
# macOS: brew install mongodb-community
# Linux: Follow MongoDB installation guide for your distribution
```

**Problem**: File permission errors
```bash
# Windows: Run as administrator if needed
# Or check file permissions on the project directory

# macOS/Linux: Fix permissions
chmod -R 755 ./samples/
chmod -R 755 ./data/
```

#### OpenAI API Issues

**Problem**: CrewAI commands fail
```bash
# Ensure you have a valid OpenAI API key in .env
OPENAI_API_KEY=sk-your-actual-key-here

# Test without natural language processing
pf-agent license get --no-nl
```

#### License Update Issues

**Problem**: License file not found
```bash
# Check file path and permissions
ls -la ./path/to/license.lic

# Use absolute path if needed
pf-agent license apply --instance pf1 --file "C:\full\path\to\license.lic"

# Check file exists
if (Test-Path "./samples/pf_new.lic") { "File exists" } else { "File missing" }
```

**Problem**: License application fails
```bash
# Check if simulator is running
pf-agent simulate up

# Verify instance ID exists in inventory.yaml
type pf_agent\inventory.yaml

# Test API connectivity
curl http://localhost:8080/pf1/license
```

**Problem**: License shows as expired after update
```bash
# Check license file expiry date format
findstr /i "expiry\|expirationdate" ./license-file.lic

# Verify the date is in the future and format is YYYY-MM-DD
# Common formats supported:
# EXPIRY=2026-01-15
# ExpirationDate=2026-01-15
```

**Problem**: License update succeeds but status is still WARNING/EXPIRED
```bash
# Force refresh from API after license update
pf-agent refresh

# Check if the simulator parsed the expiry date correctly
pf-agent license get --instance pf1

# If using file with no expiry date, simulator defaults to 1 year from now
```

**Problem**: Permission denied when reading license file
```bash
# Windows: Check file permissions
icacls ./license-file.lic

# Ensure the file is readable
attrib ./license-file.lic

# Run as administrator if needed
```

### Common Issues

1. **MongoDB Connection**: Ensure MongoDB is running and accessible
2. **Simulator Not Starting**: Check port 8080 is available
3. **License File Format**: Ensure license files contain `EXPIRY=YYYY-MM-DD`
4. **Permission Issues**: Ensure proper file permissions for license files

### Logs

- APScheduler logs: Check console output when running pf-agent commands
- Audit trail: All operations logged to MongoDB audits collection
- Simulator logs: FastAPI access logs when running simulator
