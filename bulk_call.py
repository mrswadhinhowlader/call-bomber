#!/usr/bin/env python3
import os
import time
import subprocess
import threading
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NetHunterBulkCaller:
    def __init__(self):
        self.package_name = "com.android.dialer"  # Default dialer
    
    def test_dialer(self):
        """Test if dialer works"""
        try:
            subprocess.run(["am", "start", "-a", "android.intent.action.DIAL"], 
                         timeout=5, check=True)
            logger.info("✅ Dialer accessible")
            return True
        except:
            logger.error("❌ Dialer not working")
            return False
    
    def clear_dialpad(self):
        """Clear dialpad"""
        subprocess.run(["input", "keyevent", "123"], timeout=2)  # Delete all
        time.sleep(0.5)
    
    def dial_number(self, number):
        """Dial number directly"""
        self.clear_dialpad()
        subprocess.run(["input", "text", number], timeout=2)
        time.sleep(0.5)
        subprocess.run(["input", "keyevent", "66"], timeout=2)  # CALL button
        logger.info(f"📞 Calling {number}")
    
    def open_call_screen(self):
        """Open dialer app"""
        subprocess.run([
            "am", "start", 
            "-n", f"{self.package_name}/.DialtactsActivity",
            "-a", "android.intent.action.DIAL"
        ], timeout=3)
        time.sleep(2)
    
    def hangup(self):
        """Auto hangup"""
        time.sleep(25)  # 25 sec ring + connect
        subprocess.run(["input", "keyevent", "6"], timeout=2)  # End call
        subprocess.run(["input", "keyevent", "3"], timeout=2)  # Home (optional)
        logger.info("📞 Hangup OK")
    
    def single_call(self, number):
        """One complete call cycle"""
        self.open_call_screen()
        self.dial_number(number)
        
        # Start hangup in background
        hangup_thread = threading.Thread(target=self.hangup)
        hangup_thread.daemon = True
        hangup_thread.start()
        
        time.sleep(35)  # Wait for full cycle
    
    def bulk_attack(self, number, total_calls=50, delay=3):
        """Main bulk call function"""
        logger.info(f"🚀 NetHunter Bulk Attack START")
        logger.info(f"📱 Target: {number}")
        logger.info(f"🔥 Total: {total_calls} calls")
        
        if not self.test_dialer():
            logger.error("❌ Dialer test failed!")
            return
        
        try:
            for i in range(total_calls):
                self.single_call(number)
                progress = f"📊 [{i+1}/{total_calls}]"
                logger.info(progress)
                time.sleep(delay)  # Gap between calls
            
            logger.info("✅ MISSION COMPLETE! 🎉")
            
        except KeyboardInterrupt:
            logger.info("⏹️ Attack stopped by user (Ctrl+C)")

def main():
    print("=" * 50)
    print("🔥  NetHunter Bulk Caller v2.0 🔥")
    print("💯 100% FREE - No API needed!")
    print("=" * 50)
    
    number = input("📱 Target (+8801XXXXXXXXX): ").strip()
    
    if len(number) != 13 or not number.startswith('+880'):
        print("❌ Invalid! Example: +8801712345678")
        return
    
    try:
        total = int(input("🔢 Total calls [50]: ") or "50")
        delay = float(input("⏱️ Delay between calls [3s]: ") or "3")
    except:
        total, delay = 50, 3
    
    caller = NetHunterBulkCaller()
    caller.bulk_attack(number, total, delay)

if __name__ == "__main__":
    main()
