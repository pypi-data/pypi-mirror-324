import subprocess
import pytest
import os


def run_installation_script(install_path):
    """Run the install.sh script with a custom installation path."""
    command = ["bash", "install.sh", install_path]
    return subprocess.run(command, text=True, capture_output=True)


def run_fob_command(fob_path, *args):
    """Helper function to execute the 'fob' command."""
    # Prepend some test-specific global arguments to args
    prepend_test_args = [
        "-d", "/tmp/fob_test_db.db",
    ]

    args = [*prepend_test_args, *args]
    command = [os.path.join(fob_path, "fob"), *args]
    return subprocess.run(command, text=True, capture_output=True)


@pytest.fixture(scope="module")
def setup_fob_binary():
    """Fixture to install fob to a temporary directory for testing."""
    test_dir = "/tmp/fob_test_installation"

    # Ensure the directory is clean
    if os.path.exists(test_dir):
        subprocess.run(["rm", "-rf", test_dir])

    os.makedirs(test_dir)

    # Run the installation script
    result = run_installation_script(test_dir)
    assert result.returncode == 0, f"Installation failed: {result.stderr}"

    # Verify the installation path
    fob_executable = os.path.join(test_dir, "fob")
    assert os.path.exists(fob_executable), "fob executable not found in the custom installation path."

    # Create the test database file
    db_path = "/tmp/fob_test_db.db"
    if os.path.exists(db_path):
        os.remove(db_path)

    yield test_dir

    # Clean up after tests and database
    subprocess.run(["rm", "-rf", test_dir])
    subprocess.run(["rm", db_path])


def run_fob_command_with_input(fob_path, input_data, *args):
    """Helper function to execute the 'fob' command with simulated input."""
    prepend_test_args = [
        "-d", "/tmp/fob_test_db.db",
    ]
    args = [*prepend_test_args, *args]
    command = [os.path.join(fob_path, "fob"), *args]

    process = subprocess.Popen(
        command,
        text=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = process.communicate(input=input_data)
    return subprocess.CompletedProcess(command, process.returncode, stdout, stderr)


def test_fob_help(setup_fob_binary):
    """Test the 'fob help' command."""
    fob_path = setup_fob_binary
    result = run_fob_command(fob_path, "help")

    assert result.returncode == 0, f"fob command 'help' failed: {result.stderr}"
    assert "Usage:" in result.stdout
    assert "Common Commands" in result.stdout


def test_fob_info(setup_fob_binary):
    """Test the 'fob info' command."""
    fob_path = setup_fob_binary
    result = run_fob_command(fob_path, "info")

    assert result.returncode == 0, f"fob command 'info' failed: {result.stderr}"
    assert "Program Information" in result.stdout
    assert "Configuration Information" in result.stdout

def get_current_year_month():
    """Get the current year and month as integers."""
    from datetime import datetime
    now = datetime.now()
    return now.year, now.month

def test_fob_new_month(setup_fob_binary):
    """Test the 'fob new_month' command with interactive input."""
    fob_path = setup_fob_binary

    year, month = get_current_year_month()

    # Simulated input for the interactive session
    new_month_user_inputs = "\n".join([
        str(year),    # year
        str(month),   # month
        "20",         # number of working days
        "5",          # number of blocks per day
        "First Area", # first area name
        "Second Area",# second area name
        "\n",         # confirm action
        "8",          # number of buffer blocks
        "46",         # number of blocks for first area
        "46",         # number of blocks for second area
        "yes"         # confirm action
    ]) + "\n"

    # Run the interactive command
    result = run_fob_command_with_input(fob_path, new_month_user_inputs, "new_month")

    assert result.returncode == 0, f"fob command 'new_month' failed: {result.stderr}"
    assert "New month successfully created!" in result.stdout


def test_fob_gm(setup_fob_binary):
    """Test the 'fob gm' command to ensure it uses the existing database."""
    fob_path = setup_fob_binary

    # interactive commands
    gm_user_inputs = "\n".join([
        "yes",
        "2",
        "2",
        "1",
    ]) + "\n"

    result = run_fob_command_with_input(fob_path, gm_user_inputs, "gm")

    assert result.returncode == 0, f"fob command 'gm' failed: {result.stderr}"
    assert "New day started." in result.stdout


def test_fob_sup(setup_fob_binary):
    """Test the 'fob sup' command, which provides a quick overview of the month and today."""
    fob_path = setup_fob_binary
    result = run_fob_command(fob_path, "sup")

    assert result.returncode == 0, f"fob command 'sup' failed: {result.stderr}"
    assert "This Month" in result.stdout


### The following 'did' and 'didnt' tests are dependent on each other, and also on the 'new_month' and 'gm' tests.
def test_fob_did(setup_fob_binary):
    """Test the 'fob did' command to check off blocks from today's checklist."""

    # Is not interactive, but requires a block ID after `fob did`
    fob_path = setup_fob_binary
    # First three (out of five) blocks today
    for block_id in range(1, 4):
        result = run_fob_command(fob_path, "did", str(block_id))

        assert result.returncode == 0, f"fob command 'did' failed for block {block_id}: {result.stderr}"
        assert f"Checklist updated." in result.stdout

    # # Last block today says "All blocks have been completed!"
    # result = run_fob_command(fob_path, "did", "5")
    # assert result.returncode == 0, f"fob command 'did' failed for block 5: {result.stderr}"
    # assert "All blocks have been completed!" in result.stdout

def test_fob_didnt(setup_fob_binary):
    """Test the 'fob didnt' command to convert a non-Buffer block to a Buffer block and mark it as complete."""

    # Is not interactive, but requires a block ID after `fob didnt`
    fob_path = setup_fob_binary
    result = run_fob_command(fob_path, "didnt", "4")

    assert result.returncode == 0, f"fob command 'didnt' failed: {result.stderr}"
    assert "Block 4 converted to Buffer block." in result.stdout

def test_fob_didnt_errors(setup_fob_binary):
    """Test that 'fob didnt' command fails when attempting to convert a already Buffer block to a Buffer block."""

    # Is not interactive, but requires a block ID after `fob didnt`
    fob_path = setup_fob_binary
    result = run_fob_command(fob_path, "didnt", "5")

    assert result.returncode == 0, f"fob command 'didnt' failed: {result.stderr}"
    assert "Error: This block is already a Buffer block." in result.stdout

def test_fob_reset(setup_fob_binary):
    """Test the 'fob reset' command to delete the database file."""
    fob_path = setup_fob_binary

    confirm = "yes\n"

    result = run_fob_command_with_input(fob_path, confirm, "reset")

    assert result.returncode == 0, f"fob command 'reset' failed: {result.stderr}"
    assert "Deleted" in result.stdout
    assert not os.path.exists("/tmp/fob_test_db.db"), "Database file was not deleted."