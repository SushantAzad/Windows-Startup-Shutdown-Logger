# System Startup and Shutdown Logger

This project provides a script to log the last 10 startup and shutdown events of a Windows system. It is especially useful for tracking system usage during times of absence, allowing users to see if and when someone accessed their system.

## Features

- Monitor System Start/Stop Events: Logs the last 10 times the system was started and stopped.
- User Details: Provides information on which user was logged - in during these events.
- Event Log Filtering: Retrieves only specific events related to system startup (Event ID 6005) and shutdown (Event ID 6006).
- Output File: Saves the event details to a system_power_events.txt file, making it easy to review system access history.

## Potential Use cases

- Security Check: Verify if someone accessed your system in your absence.
- Troubleshooting: Track unexpected shutdowns or reboots of your system.
- User Tracking: Know which user accounts were active during each event.

## Dependencies

This script requires Python and the following modules:

`win32evtlog` and `win32evtlogutil`: For reading and processing Windows Event Logs.
`os`: For file handling and path management.

## How to Use

1. Clone the Repository:

```bash
git clone https://github.com/yourusername/your_repository.git
cd your_repository
```

2. Run the Script:

```bash
Copy code
python startup_shutdown_logger.py
```

The script will:

- Check if the necessary dependencies are installed.
- Retrieve the last 10 system startup and shutdown events.
- Output the details in both the console and a file named `system_power_events.txt`.

3. View the Log File: After running the script, open `system_power_events.txt` in the same directory to see the list of startup and shutdown events.

## Example Output

### Console and file output example:

```bash
Event[1]
  Date: 2024-11-15T10:25:30Z
  Event: The system service started at
  User: JohnDoe

Event[2]
  Date: 2024-11-15T08:12:15Z
  Event: The system service was stopped
  User: JaneDoe
...
```
