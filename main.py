import os
import asyncio
from dotenv import load_dotenv
import logging
from remote_ssh import connect_ssh, disconnect_ssh, upload_file, download_file, execute_command, check_remote_file, find_file

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Retrieve SSH configuration from environment variables
SSH_HOSTNAME = os.getenv('SSH_HOSTNAME')
SSH_PORT = int(os.getenv('SSH_PORT', 22))  # Default to 22 if not specified
SSH_USERNAME = os.getenv('SSH_USERNAME')
SSH_PASSWORD = os.getenv('SSH_PASSWORD')
REMOTE_DIR = os.getenv('REMOTE_DIR')
LOCAL_DIR = os.getenv('LOCAL_DIR')
REMOTE_FILE_PREFIX = os.getenv('REMOTE_FILE_PREFIX', 'MEPS_')

# Main function to execute SSH tasks
async def main():

    try:

        # Establish an SSH connection
        ssh_client = await connect_ssh(SSH_HOSTNAME, SSH_PORT, SSH_USERNAME, SSH_PASSWORD)

        # Example 1: Upload a file to the remote server
        local_file_path = os.path.join(LOCAL_DIR, 'example.txt')
        if os.path.exists(local_file_path):
            upload_status = await upload_file(ssh_client, local_file_path, REMOTE_DIR, 'uploaded_example.txt')
            logger.info(f"File upload status: {upload_status}")
        else:
            logger.warning(f"Local file does not exist: {local_file_path}")

        # Example 2: Execute a command on the remote server
        command = 'ls -l /home'
        stdout, exit_status, execution_time = await execute_command(ssh_client, command)
        logger.info(f"Command output: {stdout}")
        logger.info(f"Exit status: {exit_status}")
        logger.info(f"Execution time: {execution_time} seconds")

        # Example 3: Check if a file exists on the remote server
        remote_file_path = os.path.join(REMOTE_DIR, 'uploaded_example.txt')
        file_exists = await check_remote_file(ssh_client, remote_file_path)
        logger.info(f"Remote file exists: {file_exists}")

        # Example 4: Find a file in the remote directory that starts with a given prefix
        found_file = await find_file(ssh_client, REMOTE_DIR, REMOTE_FILE_PREFIX)
        if found_file:
            logger.info(f"File found with prefix {REMOTE_FILE_PREFIX}: {found_file}")
        else:
            logger.info(f"No files found with prefix {REMOTE_FILE_PREFIX}")

        # Example 5: Download a file from the remote server
        if found_file:
            download_status = await download_file(ssh_client, os.path.join(REMOTE_DIR, found_file), LOCAL_DIR, 'downloaded_example.txt')
            logger.info(f"File download status: {download_status}")

    finally:
        # Close the SSH connection
        await disconnect_ssh(ssh_client)

# Run the main function
if __name__ == '__main__':
    asyncio.run(main())
