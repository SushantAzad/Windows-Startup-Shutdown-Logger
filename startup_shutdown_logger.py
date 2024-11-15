import subprocess
import sys
import os
import traceback

def check_and_install_dependencies():
    required_packages = ["pywin32"]

    for package in required_packages:
        try:
            __import__(package)  
        except ImportError:
            print(f"Package '{package}' not found. Installing it now...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

check_and_install_dependencies()

try:
    import win32evtlog
    import win32evtlogutil
except ImportError:
    print("Dependencies could not be installed. Please check your network and administrator permissions.")
    sys.exit(1)

def format_custom_description(event):
    """Format the event description with custom messages for startup and shutdown events."""
    try:
        event_id = event.EventID & 0xFFFF
        if event_id == 6005:  
            return "The system service started at"
        elif event_id == 6006:
            return "The system service was stopped at"
        else:
            return "No description available"
    except Exception:
        return "No description available"

def write_events_to_file():
    server = 'localhost'
    log_type = 'System'
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ

    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'system_power_events.txt')
    
    try:
        print("Opening System event log...")
        hand = win32evtlog.OpenEventLog(server, log_type)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("Windows System Power Events Log\n")
            f.write("=" * 70 + "\n\n")
            
            event_count = 0
            while True:
                events = win32evtlog.ReadEventLog(hand, flags, 0)
                if not events:
                    break
                
                for event in events:
                    event_id = event.EventID & 0xFFFF
                    if event_id in [6005, 6006]:  
                        time_generated = event.TimeGenerated.Format() if event.TimeGenerated else "N/A"
                        custom_description = format_custom_description(event)
                        user_account = getattr(event, 'Sid', None)  
                        user_name = win32evtlogutil.FormatMessage(event, log_type) if user_account else "N/A"

                        event_info = (
                            f"Event[{event_count + 1}]\n"
                            f"  Date: {time_generated}\n"
                            f"  Event ID: {event_id}\n"
                            f"  Description: {custom_description}\n"
                            f"  User Account: {user_name}\n\n"
                        )
                        
                        f.write(event_info)
                        print(event_info)
                        
                        event_count += 1
                        if event_count >= 10:
                            break
                if event_count >= 10:
                    break

        print(f"\nEvents have been written to: {file_path}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        print(traceback.format_exc())
        
    finally:
        if 'hand' in locals() and hand:
            win32evtlog.CloseEventLog(hand)

if __name__ == "__main__":
    write_events_to_file()
