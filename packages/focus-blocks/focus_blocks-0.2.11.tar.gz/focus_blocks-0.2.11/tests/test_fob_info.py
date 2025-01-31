import subprocess
import pytest
import os


def run_uv_command(*args):
    """Helper function to execute the 'uv' command."""
    command = ["uv", *args]
    return subprocess.run(command, text=True, capture_output=True)


def run_fob_command(*args):
    """Helper function to execute the 'fob' command."""
    # Prepend some test-specific global arguments to args
    prepend_test_args = [
        "-d", "/tmp/fob_test_db.db",
    ]

    args = [*prepend_test_args, *args]
    command = ["fob", *args]
    return subprocess.run(command, text=True, capture_output=True)


@pytest.fixture(scope="module")
def setup_fob_binary():
    """Fixture to install focus-blocks (fob) for testing using the 'uv' package manager."""
    # Uninstall if it already exists to ensure a clean slate
    run_uv_command("tool", "uninstall", "focus-blocks")

    # Install fob using the uv package manager
    result = run_uv_command("tool", "install", "focus-blocks")
    assert result.returncode == 0, f"Installation failed: {result.stderr}"

    # Verify that the fob command is now available
    result = run_fob_command("help")
    assert result.returncode == 0, "fob CLI is not available after installation."
    assert "Usage:" in result.stdout

    # Create the test database file (if not exists)
    db_path = "/tmp/fob_test_db.db"
    if os.path.exists(db_path):
        os.remove(db_path)

    yield

    # Post-test cleanup
    run_uv_command("tool", "uninstall", "focus-blocks")
    if os.path.exists(db_path):
        os.remove(db_path)


def run_fob_command_with_input(input_data, *args):
    """Helper function to execute the 'fob' command with simulated user input."""
    prepend_test_args = [
        "-d", "/tmp/fob_test_db.db",
    ]
    args = [*prepend_test_args, *args]
    command = ["fob", *args]

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
    result = run_fob_command("help")

    assert result.returncode == 0, f"fob command 'help' failed: {result.stderr}"
    assert "Usage:" in result.stdout
    assert "Common Commands" in result.stdout


def test_fob_info(setup_fob_binary):
    """Test the 'fob info' command."""
    result = run_fob_command("info")

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
    result = run_fob_command_with_input(new_month_user_inputs, "new_month")

    assert result.returncode == 0, f"fob command 'new_month' failed: {result.stderr}"
    assert "New month successfully created!" in result.stdout


def test_fob_gm(setup_fob_binary):
    """Test the 'fob gm' command to ensure it uses the existing database."""
    # Interactive commands
    gm_user_inputs = "\n".join([
        "yes",
        "2",
        "2",
        "1",
    ]) + "\n"

    result = run_fob_command_with_input(gm_user_inputs, "gm")

    assert result.returncode == 0, f"fob command 'gm' failed: {result.stderr}"
    assert "New day started." in result.stdout


def test_fob_sup(setup_fob_binary):
    """Test the 'fob sup' command, which provides a quick overview of the month and today."""
    result = run_fob_command("sup")

    assert result.returncode == 0, f"fob command 'sup' failed: {result.stderr}"
    assert "This Month" in result.stdout


def test_fob_did(setup_fob_binary):
    """Test the 'fob did' command to check off blocks from today's checklist."""

    # Is not interactive, but requires a block ID after `fob did`
    for block_id in range(1, 4):
        result = run_fob_command("did", str(block_id))

        assert result.returncode == 0, f"fob command 'did' failed for block {block_id}: {result.stderr}"
        assert "Checklist updated." in result.stdout


def test_fob_didnt(setup_fob_binary):
    """Test the 'fob didnt' command to convert a non-Buffer block to a Buffer block and mark it as complete."""

    # Is not interactive, but requires a block ID after `fob didnt`
    result = run_fob_command("didnt", "4")

    assert result.returncode == 0, f"fob command 'didnt' failed: {result.stderr}"
    assert "Block 4 converted to Buffer block." in result.stdout


def test_fob_didnt_errors(setup_fob_binary):
    """Test that 'fob didnt' command fails when attempting to convert an already Buffer block to a Buffer block."""

    # Is not interactive, but requires a block ID after `fob didnt`
    result = run_fob_command("didnt", "5")

    assert result.returncode == 0, f"fob command 'didnt' failed: {result.stderr}"
    assert "Error: This block is already a Buffer block." in result.stdout


def test_fob_reset(setup_fob_binary):
    """Test the 'fob reset' command to delete the database file."""
    confirm = "yes\n"

    result = run_fob_command_with_input(confirm, "reset")

    assert result.returncode == 0, f"fob command 'reset' failed: {result.stderr}"
    assert "Deleted" in result.stdout
    assert not os.path.exists("/tmp/fob_test_db.db"), "Database file was not deleted."
