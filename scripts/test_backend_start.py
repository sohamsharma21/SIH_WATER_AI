"""
Quick test to verify backend can start without errors
"""
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

try:
    print("Testing backend imports...")
    from app.main import app
    print("✅ Backend imports successfully!")
    print("✅ All dependencies loaded correctly")
    print("\nYou can now start the backend with:")
    print("  python -m uvicorn app.main:app --reload --port 8000")
except Exception as e:
    print(f"❌ Error: {str(e)}")
    print(f"Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

