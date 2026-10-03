"""
Studio Time Sentinel & Autonomous Working Rhythm Guardian
Author: Gemini Artist 2
Session: 005

Ensures the studio adheres to its temporal commitments without stopping short.
Audits elapsed time, target completion time, stratum balance, and active session work.
"""

import time
import sys
import os
import argparse
import datetime

# Target deadline for Session 008 (Extended Work): 17:30 local = 15:30:00 UTC (2026-10-03)
DEFAULT_TARGET_UTC_EPOCH = 1791041400  # 2026-10-03 15:30:00 UTC

def get_status(target_epoch=None):
    if target_epoch is None:
        target_epoch = DEFAULT_TARGET_UTC_EPOCH
    now_epoch = int(time.time())
    now_utc = datetime.datetime.fromtimestamp(now_epoch, tz=datetime.timezone.utc)
    target_utc = datetime.datetime.fromtimestamp(target_epoch, tz=datetime.timezone.utc)
    
    # Local time is UTC + 2
    local_tz = datetime.timezone(datetime.timedelta(hours=2))
    now_local = now_utc.astimezone(local_tz)
    target_local = target_utc.astimezone(local_tz)
    
    diff = target_epoch - now_epoch
    is_reached = diff <= 0
    diff_abs = abs(diff)
    mins = diff_abs // 60
    secs = diff_abs % 60
    
    return {
        "now_epoch": now_epoch,
        "now_utc": now_utc.strftime('%Y-%m-%d %H:%M:%S UTC'),
        "now_local": now_local.strftime('%H:%M:%S (Local)'),
        "target_epoch": target_epoch,
        "target_utc": target_utc.strftime('%Y-%m-%d %H:%M:%S UTC'),
        "target_local": target_local.strftime('%H:%M:%S (Local)'),
        "seconds_remaining": diff if not is_reached else 0,
        "minutes_remaining": mins if not is_reached else 0,
        "formatted_remaining": f"{mins:02d}m {secs:02d}s",
        "is_reached": is_reached
    }

def print_banner(status, task_context=""):
    print("=" * 76)
    print("  STUDIO AGON :: STUDIO TIME SENTINEL & AUTONOMOUS DISCIPLINE")
    print("=" * 76)
    print(f"  Current Time   : {status['now_local']} / {status['now_utc']}")
    print(f"  Target Deadline: {status['target_local']} / {status['target_utc']}")
    if not status['is_reached']:
        print(f"  Remaining Time : {status['formatted_remaining']} ({status['seconds_remaining']}s)")
        print("  STATUS         : ACTIVE WORK IN PROGRESS — SUSTAIN PRACTICE DEEPLY")
    else:
        print(f"  Time Elapsed   : Target time reached or passed by {status['formatted_remaining']}")
        print("  STATUS         : DEADLINE SATISFIED — FULL TEMPORAL DISCIPLINE ACHIEVED")
    if task_context:
        print(f"  Current Phase  : {task_context}")
    print("=" * 76)

def main():
    parser = argparse.ArgumentParser(description="Studio Time Sentinel")
    parser.add_argument("--check", action="store_true", help="Check current time vs deadline")
    parser.add_argument("--target-epoch", type=int, default=DEFAULT_TARGET_UTC_EPOCH, help="Target UTC epoch")
    parser.add_argument("--heartbeat", type=str, default="", help="Record active studio heartbeat")
    parser.add_argument("--assert-not-done", action="store_true", help="Exit with non-zero if target not reached")
    
    args = parser.parse_args()
    status = get_status(args.target_epoch)
    print_banner(status, args.heartbeat)
    
    if args.assert_not_done:
        if status['is_reached']:
            print("[SENTINEL NOTICE] Target time satisfied.")
            sys.exit(0)
        else:
            print(f"[SENTINEL ALERT] Work still required: {status['formatted_remaining']} remaining.")
            sys.exit(1)

if __name__ == "__main__":
    main()
