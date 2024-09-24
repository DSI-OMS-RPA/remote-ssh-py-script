
# SSH Utility Script

This project provides an asynchronous utility script to connect to a remote SSH server, perform file uploads/downloads using SFTP, and execute commands over SSH. The configuration details such as SSH credentials are loaded from a `.env` file.

## Features

- Connect to a remote SSH server using `asyncssh`.
- Upload and download files via SFTP.
- Execute shell commands on the remote server.
- Check if a file exists on the remote server.
- Find a file in a remote directory by prefix.

## Requirements

- Python 3.7+
- The following Python packages:
  - `asyncssh`
  - `python-dotenv`

You can install the required packages using:

```bash
pip install -r requirements.txt
```

### Sample `requirements.txt`
```text
asyncssh
python-dotenv
```

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ssh-utility-script.git
   cd ssh-utility-script
   ```

2. Create a `.env` file with your SSH connection details:

   ```bash
   touch .env
   ```

   Add the following to your `.env` file:

   ```
   SSH_HOSTNAME=example.com
   SSH_PORT=22
   SSH_USERNAME=myuser
   SSH_PASSWORD=mypassword
   REMOTE_DIR=/remote/path/
   LOCAL_DIR=/local/path/
   REMOTE_FILE_PREFIX=ABC_
   ```

3. Update the local and remote directories as well as the SSH credentials.

## Usage

1. Ensure all dependencies are installed:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the script:

   ```bash
   python main.py
   ```

### Functionality Overview

- **SSH Connection**: Connect to a remote SSH server using credentials from the `.env` file.
- **Upload File**: Upload a file from your local machine to the remote server.
- **Execute Command**: Execute a shell command on the remote server and retrieve the output.
- **Check Remote File**: Verify if a file exists on the remote server.
- **Find File by Prefix**: Search for a file in the remote directory by matching a prefix.
- **Download File**: Download a file from the remote server to your local machine.

### Example

Here’s an example of running the main script:

```bash
python main.py
```

The script will:
- Connect to the SSH server specified in your `.env` file.
- Upload a local file.
- Execute a command on the remote server.
- Check if a file exists on the remote server.
- Find a file with a specific prefix in the remote directory.
- Download a file from the remote server.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

If you’d like to contribute, please fork the repository and submit a pull request.

## Troubleshooting

- **SSH Connection Issues**: Ensure your SSH credentials are correct and your machine has network access to the SSH server.
- **File Not Found Errors**: Double-check that the file paths in both local and remote machines are correct.
