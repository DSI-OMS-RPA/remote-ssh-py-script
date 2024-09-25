import os
import time
import asyncssh
import asyncio
import logging
from typing import Tuple, Optional

# Configure the logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Connect to a remote SSH server using password-based authentication.
async def connect_ssh(hostname: str, port: int, username: str, password: str, keepalive_interval: int = 30) -> asyncssh.SSHClient:
    """
    Establishes an SSH connection to a remote server using password authentication.

    Args:
        hostname (str): The hostname or IP address of the server.
        port (int): The SSH port to connect to.
        username (str): The username for the SSH connection.
        password (str): The password for the SSH connection.
        keepalive_interval (int): Interval in seconds to send keepalive messages. Default is 30.

    Returns:
        asyncssh.SSHClient: The connected SSH client.

    Raises:
        ValueError: If there is an error connecting to the SSH server.
    """
    logger.info(f"Connecting to SSH server at {hostname}:{port}")
    try:
        # Connect to the SSH server with keepalive_interval
        ssh_client = await asyncssh.connect(
            hostname,
            port=port,
            username=username,
            password=password,
            known_hosts=None,
            keepalive_interval=keepalive_interval
        )
        logger.info("Successfully connected to the SSH server.")
        return ssh_client
    except asyncssh.Error as e:
        logger.error(f"SSH connection error: {e}")
        raise ValueError(f"SSH connection error: {e}") from e

async def disconnect_ssh(ssh_client: asyncssh.SSHClient) -> None:
    """
    Closes an active SSH client connection and ensures all resources are properly released.

    Args:
        ssh_client (asyncssh.SSHClient): An active SSH client connection.
    """
    if ssh_client is not None:
        ssh_client.close()
        await ssh_client.wait_closed()
        logger.info("SSH connection closed successfully.")

# Upload a local file to a remote server using SFTP.
async def upload_file(ssh_client: asyncssh.SSHClientConnection, local_file_path: str, remote_folder: str, new_filename: str) -> bool:
    """
    Uploads a file to a remote server over SFTP.

    Args:
        ssh_client (asyncssh.SSHClientConnection): An active SSH client connection.
        local_file_path (str): The path to the local file to upload.
        remote_folder (str): The remote folder path where the file will be uploaded.
        new_filename (str): The desired filename for the file on the remote server.

    Returns:
        bool: True if the upload was successful, False otherwise.

    Raises:
        FileNotFoundError: If the local file is not found.
        ValueError: If an error occurs during the SFTP operation.
    """
    try:
        async with ssh_client.start_sftp_client() as sftp_client:
            remote_path = f"{remote_folder}/{new_filename}"
            await sftp_client.put(local_file_path, remote_path)
            logger.info(f"File uploaded to {remote_path}")
            return True
    except FileNotFoundError:
        logger.error(f"Local file not found: {local_file_path}")
        return False
    except asyncssh.SFTPError as sftp_error:
        logger.error(f"SFTP error during file upload: {sftp_error}")
        return False

# Download a file from a remote server using SFTP.
async def download_file(ssh_client: asyncssh.SSHClientConnection, remote_file_path: str, local_folder: str, new_filename: str) -> bool:
    """
    Downloads a file from a remote server over SFTP.

    Args:
        ssh_client (asyncssh.SSHClientConnection): An active SSH client connection.
        remote_file_path (str): The path to the remote file to download.
        local_folder (str): The path to the local folder where the file will be saved.
        new_filename (str): The desired filename for the downloaded file on the local machine.

    Returns:
        bool: True if the file was downloaded successfully, False otherwise.

    Raises:
        FileNotFoundError: If the remote file does not exist.
        ValueError: If an SFTP error occurs during the download process.
    """
    try:
        async with ssh_client.start_sftp_client() as sftp_client:
            local_path = os.path.join(local_folder, new_filename)
            await sftp_client.get(remote_file_path, local_path)
            logger.info(f"File downloaded to {local_path}")
            return os.path.exists(local_path)
    except FileNotFoundError as e:
        logger.error(f"Remote file not found: {remote_file_path}")
        raise FileNotFoundError(f"Remote file not found: {remote_file_path}") from e
    except asyncssh.SFTPError as sftp_error:
        logger.error(f"SFTP error during file download: {sftp_error}")
        raise ValueError(f"SFTP error during file download: {sftp_error}") from sftp_error

# Check if a file exists in a remote folder.
async def check_remote_file(ssh_client: asyncssh.SSHClientConnection, remote_file_path: str) -> bool:
    """
    Checks if a file exists in a remote folder over SFTP.

    Args:
        ssh_client (asyncssh.SSHClientConnection): An active SSH client connection.
        remote_file_path (str): The path to the remote file to check.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    try:
        async with ssh_client.start_sftp_client() as sftp_client:
            return bool(await sftp_client.exists(remote_file_path))
    except asyncssh.SFTPError as sftp_error:
        logger.error(f"SFTP error during file existence check: {sftp_error}")
        return False
