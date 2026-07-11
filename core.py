"""
WebCore App – Opens main.html in a Native Window using Tkinter
Uses tkinterweb or tkinter with a webview for native display.
"""

import os
import sys
import threading
import time
from pathlib import Path

# ---------- configuration ----------
APP_DIR = Path(__file__).parent.absolute()
MAIN_HTML = APP_DIR / "main.html"

# ---------- check if main.html exists ----------
if not MAIN_HTML.exists():
    print(f"❌ Error: main.html not found at {MAIN_HTML}")
    print("   Please place your main.html file in the same directory as this script.")
    sys.exit(1)

print(f"✅ Found main.html at {MAIN_HTML}")

# ---------- Try using tkinterweb for native window ----------
def try_tkinterweb():
    """Attempt to use tkinterweb for a native window."""
    try:
        import tkinter as tk
        from tkinterweb import HtmlFrame
        print("✅ tkinterweb found - using native window")
        
        root = tk.Tk()
        root.title("WebCore App")
        root.geometry("1200x800")
        
        # Create HTML frame
        frame = HtmlFrame(root, horizontal_scrollbar="auto")
        frame.load_file(str(MAIN_HTML))
        frame.pack(fill="both", expand=True)
        
        root.mainloop()
        return True
    except ImportError:
        print("⚠️ tkinterweb not available. Install with: pip install tkinterweb")
        return False
    except Exception as e:
        print(f"❌ tkinterweb error: {e}")
        return False

# ---------- Try using PyWebView (with the CORRECT approach) ----------
def try_pywebview():
    """Attempt to use PyWebView with the correct API."""
    try:
        import webview
        print("✅ PyWebView found - using native window")
        
        # The key fix: create window AND start it properly
        window = webview.create_window(
            title="WebCore App",
            url=str(MAIN_HTML.absolute()),
            width=1200,
            height=800,
            resizable=True,
            min_size=(800, 600)
        )
        
        # Start the window - CORRECT: pass the window object
        webview.start(window, debug=False)
        return True
    except ImportError:
        print("⚠️ PyWebView not available")
        return False
    except Exception as e:
        print(f"❌ PyWebView error: {e}")
        return False

# ---------- Try using webbrowser (simplest fallback) ----------
def open_in_browser():
    """Open in default browser."""
    import webbrowser
    print("🔄 Opening in browser...")
    file_url = MAIN_HTML.absolute().as_uri()
    webbrowser.open(file_url)
    print("✅ Browser opened with main.html")
    print("   The browser window will stay open independently.")

# ---------- Main ----------
def main():
    print("🎯 WebCore App Launcher")
    print("=" * 50)
    
    # Try PyWebView first (with the fix)
    print("🔄 Attempting to open with PyWebView...")
    if try_pywebview():
        return
    
    # Try tkinterweb if PyWebView fails
    print("🔄 Attempting to open with tkinterweb...")
    if try_tkinterweb():
        return
    
    # Fallback: open in browser
    print("🔄 Using browser fallback...")
    open_in_browser()

if __name__ == "__main__":
    main()
