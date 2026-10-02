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

# Target deadline: 12:00 PM local = 10:00:00 UTC (2026-10-02)
TARGET_UTC_EPOCH = 1790935200  # 2026-10-02 10:00:00 UTC

def get_status(target_epoch=TARGET_UTC_EPOCH):
    now_epoch = int(time.time())
    now_utc_str = datetime.datetime.fromtimestamp(now_epoch, tz=datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    target_utc_str = datetime.datetime.fromtimestamp(target_epoch, tz=datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    
    diff = target_epoch - now_epoch
    
    is_reached = diff <= 0
    diff_abs = abs(diff)
    mins = diff_abs // 60
    secs = diff_abs % 60
    
    return {
        "now_epoch": now_epoch,
        "now_utc": now_utc_str,
        "target_epoch": target_epoch,
        "target_utc": target_utc_str,
        "seconds_remaining": diff if not is_reached else 0,
        "minutes_remaining": mins if not is_reached else 0,
        "formatted_remaining": f"{mins:02d}m {secs:02d}s",
        "is_reached": is_reached
    }

def print_banner(status, task_context=""):
    print("=" * 72)
    print("  GEMINI ARTIST 2 :: STUDIO TIME SENTINEL & AUTONOMOUS DISCIPLINE")
    print("=" * 72)
    print(f"  Current Time   : {status['now_utc']}")
    print(f"  Target Deadline: {status['target_utc']} (12:00 PM Local / 10:00 UTC)")
    if not status['is_reached']:
        print(f"  Remaining Time : {status['formatted_remaining']} ({status['seconds_remaining']}s)")
        print("  STATUS         : ACTIVE WORK IN PROGRESS — DO NOT STOP SHORT")
    else:
        print(f"  Time Elapsed   : Target time reached or passed by {status['formatted_remaining']}")
        print("  STATUS         : DEADLINE SATISFIED — FULL SESSION DISCIPLINE ACHIEVED")
    if task_context:
        print(f"  Current Phase  : {task_context}")
    print("=" * 72)

def main():
    parser = argparse.ArgumentParser(description="Studio Time Sentinel")
    parser.add_argument("--check", action="store_true", help="Check current time vs deadline")
    parser.add_argument("--heartbeat", type=str, default="", help="Record active studio heartbeat")
    parser.add_argument("--assert-not-done", action="store_true", help="Exit with non-zero if target reached (or vice versa)")
    
    args = parser.parse_args()
    status = get_status()
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
