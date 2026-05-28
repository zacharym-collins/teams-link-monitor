## aghes-teams-monitor

A modular, lightweight internal Python package designed to transition local automation scripts into resilient, monitored system workflows.
Optimized for strict corporate Windows environments, this library enables automated scripts (such as SAP GUI automations) to instantly push
context-rich error alerts and local desktop state captures directly to Microsoft Teams via modern Workflows incoming webhooks.

### Features
- **Zero-Latency Altering**: Replaces slow, file-polling pull mechanisms with immediate asynchronus push alerts.
- **Modern Adaptive Cards**: Leverages Microsoft's strict schema version 1.4 JSON format natively supported by the Microsoft Teams Workflows App.
- **Context-Rich Diagnostics**: Isolates exceptions, execution timestamps, and automatically handles local file-system tracking documentation.
- **Visual Proof Validation**: Integrates seamlessly with display-capture libraries to isolate transient graphical GUI issues (e.g., hidden SAP popups or window freezes).
- **Extensible & Plug-and-Play**: Built as an object-oriented utility designed to easily bind to modern loggers like `loguru` or standard Python `logging`.

### Project Architecture
```plaintext
aghes-teams-monitor/
│
├── .env
├── .gitignore
├── pyproject.toml
├── README.md
│
├── app/
│    ├── __init__.py
│    ├── notifier.py
│    ├── payload.py
│    └── screenshot.py
│
└── tests/
    ├── conftest.py
    ├── test_payload.py
```

### Prerequisites: Microsoft Teams Setup
Before integrating this package, you must generate a target Webhook URL using the modern Workflows engine in Teams.  
1. Open **Microsoft Teams** and navigate to the **Teams** tab.
2. Select the Channel where you want your script alerts to be routed.
3. Click the **three dots (...)** next to the channel name and select **Manage Channel**.
4. Go to **Apps** (or **Connectors** depending on your Teams version) and search for **Workflows**.
5. Select the template named **"Post to a channel when an incoming webhook request is received"**.
6. Give your workflow a descriptive name (e.g. `Automation Monitor`) and complete the wizard.
7. Teams will generate a unique, highly secure URL that looks like:  
`https://yourcompany.webhook.office.com/webhookb2/...`
8. **Copy this URL**. You will need to place it in your project's configuration.

### Building and Installing the Package
To use this package inside your project, you will need to build it and distribute as a compiled Python Wheel (`.whl`) file.

#### 1. Generating the Wheel File (Package Maintainer)  
From the root of the `aghes-teams-monitor` source directory, run standard Python build tools to compile the project binary:
```bash
# Ensure you have the build frontend installed
pip install build

# Build the dist packages
python -m build
```

This creates a `dist/` directory containing a file named something like `aghes_teams_monitor-0.1.0-py3-none-any.whl`. This file is completely portable.

#### 2. Installing in an External Project (End User)  
To use this monitoring utility inside a seperate python automation script, navigate to that external project's folder, activate its virtual environment, and point `pip` directly to the shared wheel file:
```bash
# Navigate to your separate production script directory
cd C:/Users/MyUserName/Documents/programming/production/my-project

# Install the tracking utility directly from the built wheel binary
pip install "C:/path/to/aghes-teams-monitor/dist/aghes_teams_monitor-0.1.0-py3-none-any.whl"
```

#### 3. Configure External Environment Variables  
Inside the root working directory of your **external** project, create or append to your `.env` file so the monitoring package can locate your credentials at runtime.
```plaintext
# Microsoft Teams Workflows Webhook generated in the prerequisites step
TEAMS_WEBHOOK_URL="https://your-company.webhook.office.com/webhookb2/..."

# Absolute path directory to dump visual screenshot logs (e.g., Synced OneDrive)
MONITOR_OUTPUT_DIR="C:/Users/MyUsername/OneDrive - AGCO/My_Automation_Logs"
```

### Step-by-Step Usage Guide

#### Recipe 1: Standard Catch-All
Perfect for routines you use once a day. If any unhandled exception drops, the panic loop steps in, captures the desktop, alerts you, and terminates with a clean tracking code.
```python
import sys
from aghes_teams_monitor import TeamsNotifier, capture_desktop_state

# Initializing notifier automatically fetches variables from your local .env file
notifier = TeamsNotifier()

def main_execution_logic():
    print("Initializing SAP connection...")
    # Real SAP automation step here
    raise ConnectionError("SAP session timed out while waiting for window 'VBA_Popup'.")

if __name__ == "__main__":
    SCRIPT_NAME = "SAP_Daily_Order_Puller"

    try:
        main_execution_logic()
        print("Script completed successfully.")
        
    except Exception as e:
        print(f"Critical error caught! Commencing failure notification flow...")
        
        # 1. Capture the exact screen layout before terminating
        screenshot_name, screenshot_path = capture_desktop_state(SCRIPT_NAME)
        
        # 2. Fire the optimized payload to Teams
        notifier.send_error(
            script_name=SCRIPT_NAME, 
            error_message=str(e), 
            screenshot_path=screenshot_path
        )
        
        # Exit with error status for Task Scheduler logging tracking
        sys.exit(1)
```

#### Recipe 2: Resilient Self-Healing Loop
For continuous console tracking applications, wrap the block internally so an individual transaction drop alerts you but does not permanently crash the persistent daemon process.
```python
import time
from aghes_teams_monitor import TeamsNotifier, capture_desktop_state

notifier = TeamsNotifier()
SCRIPT_NAME = "SAP_Continuous_Order_Listener"

print(f"Starting {SCRIPT_NAME} 24/7 monitoring daemon...")

while True:
    try:
        # Long-polling function tracking SAP transactional changes
        # monitor_sap_inbound_queue()
        time.sleep(10)
        
    except Exception as e:
        # 1. Take snapshot and notify without breaking the eternal runtime loop
        _, file_path = capture_desktop_state(SCRIPT_NAME)
        notifier.send_error(SCRIPT_NAME, str(e), screenshot_path=file_path)
        
        # 2. Cool-down throttling period to prevent flooding Teams chat
        print("Error logged to Teams. Cooling down for 5 minutes before retrying...")
        time.sleep(300)
```

#### Recipe 3: Integrating Elegantly with `loguru`
If your primary automation code relies on `loguru`, you can inject this package directly as a dedicated custom **Sink**, stripping tracking infrastructure code entirely out of your functional business logic.

```python
from loguru import logger
from aghes_teams_monitor import TeamsNotifier, capture_desktop_state

notifier = TeamsNotifier()

def teams_alert_sink(message):
    record = message.record
    # Only trap elevated execution failures
    if record["level"].name in ["ERROR", "CRITICAL"]:
        script_ctx = record["extra"].get("script_name", "SAP_Generic_Task")
        
        # Pull visual proof and dispatch
        _, pic_path = capture_desktop_state(script_ctx)
        notifier.send_error(script_ctx, record["message"], screenshot_path=pic_path)

# Register sink with Loguru processor
logger.add(teams_alert_sink, level="ERROR")

# Bind context tracking names
logger = logger.bind(script_name="SAP_Parts_Dispo_Automation")

# Execution block remains incredibly clean
try:
    logger.info("Accessing SAP transaction CS02...")
    raise ValueError("Material field manipulation selector invalid or changed.")
except Exception as err:
    logger.critical(f"Execution tracking failed: {err}")
```

### Configuration & Versatility Customizations
The `TeamsNotifier` object gives you explicit validation parameters. If you have scripts that don't need screenshots (like backend string parsers), you simply omit the path argument:

```python
# Versatile usage: No screenshot tracking details appended to the Adaptive Card payload
notifier.send_error(
    script_name="Data_Ingestion_Script",
    error_message="FileNotFoundError: Missing master tracking CSV."
)
```

### Security & Compliance Note
This software functions purely as a text-payload client parsing interface and local desktop capture tool. It does not communicate outside the corporate Office 365 environment, nor does it require administrative privelages to install or run via Windows Task Scheduler. All visual captures remain inside localized storage paths defined strictly by your environment setup.
