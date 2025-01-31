# M365 User Manager

A robust Python package for automating Microsoft 365 user management operations through Microsoft Graph API, with support for both local execution and Asio RPA integration.

## Features

- **User Creation & Management**
  - Create new M365 users with comprehensive profile details
  - Copy properties, groups, and roles from template users
  - Manage group memberships and license assignments
  - Handle phone number formatting and validation

- **License Management**
  - Automatic license availability checking
  - Smart license name matching and resolution
  - Batch license assignment with detailed reporting
  - Support for all major Microsoft 365 license types

- **Security & Authentication**
  - Secure password generation and sharing
  - Integration with Password Pusher and fallback services
  - Token management for Microsoft Graph API
  - Comprehensive error handling and logging

- **Environment Flexibility**
  - Supports both local execution and Asio RPA environment
  - Environment-aware configuration loading
  - Unified logging across environments

## Installation

```bash
# Clone the repository
gh repo clone VinnyVanGogh/m365_user_manager
cd m365-user-manager

# Install dependencies
pip install -r requirements.txt
```

## Configuration

1. Create a configuration file at `environments/asio_365_config.json`:

```json
{
    "client_id": "your_client_id",
    "client_secret": "your_client_secret",
    "tenant_id": "your_tenant_id"
}
```

(Optional) Set up Discord webhook for logging:

- Configure webhook URL through the input form or environment configuration

## Usage

### Basic Usage

```python
from m365_user_manager import UserManagementOrchestrator

# Initialize and run the orchestrator
orchestrator = UserManagementOrchestrator()
orchestrator.run()
```

### Creating a New User

```python
from m365_user_manager import M365UserManager

# Initialize the manager
user_manager = M365UserManager(access_token, logger)

# Create a new user
result = user_manager.create_user(
    display_name="John Doe",
    email_address="john.doe@example.com",
    job_title="Software Engineer",
    department="Engineering",
    license_skus=["Microsoft 365 E3", "Power BI Pro"],
    groups=["Engineering Team", "All Company"]
)
```

### Copying User Properties

```python
# Create user by copying from template
result = user_manager.create_user(
    display_name="Jane Smith",
    email_address="jane.smith@example.com",
    user_to_copy="template@example.com",
    copy_licenses=True
)
```

## Input Parameters

| Parameter | Description | Required |
|-----------|-------------|----------|
| display_name | User's full name | Yes |
| email_address | User's email address | Yes |
| password | Initial password (generated if not provided) | No |
| job_title | User's job title | No |
| department | User's department | No |
| office_location | Office location | No |
| city | City | No |
| state | State/Province | No |
| business_phone | Business phone number | No |
| mobile_phone | Mobile phone number | No |
| groups | List or comma-separated string of groups | No |
| license_skus | List or comma-separated string of licenses | No |
| user_to_copy | Template user's email to copy from | No |
| copy_licenses | Whether to copy licenses from template user | No |

## Error Handling

The package includes comprehensive error handling with custom exceptions:

- `GraphAPIError`: Microsoft Graph API operation failures
- `TokenManagerError`: Authentication and token-related issues
- `PasswordManagerError`: Password management operation failures
- `InsufficientPermissionsError`: Permission-related failures

## Logging

The package uses a unified logging system supporting:

- Local file logging
- Discord webhook integration
- ASIO logging integration

Configure logging through the `logging_config` function in `config/default_config.py`.

## Dependencies

- Microsoft Graph API
- Password Pusher API (for secure password sharing)
- Discord Webhook (optional, for logging)
- Asio RPA Framework (optional)

## License

[MIT License](LICENSE)

## Contributing

Please read the [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.
