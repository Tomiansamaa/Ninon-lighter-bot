#!/usr/bin/env python3
"""
Inspect the lighter module to find all available classes and APIs
"""

import lighter

print("🔍 Inspecting lighter module...")
print()

print("📦 Available in lighter module:")
print("-" * 70)

# Get all public attributes
attrs = [attr for attr in dir(lighter) if not attr.startswith('_')]

for attr in attrs:
    try:
        obj = getattr(lighter, attr)
        obj_type = type(obj).__name__
        print(f"  • {attr:35s} : {obj_type}")
        
        # If it's a class, show some info
        if obj_type == 'type':
            # Check if it looks like an API class
            if 'Api' in attr or 'Client' in attr:
                print(f"     └─ Type: Class (looks like an API/Client)")
                # Show some methods
                methods = [m for m in dir(obj) if not m.startswith('_')]
                if len(methods) > 0 and len(methods) <= 20:
                    print(f"     └─ Methods: {', '.join(methods[:15])}")
    except Exception as e:
        print(f"  • {attr:35s} : Error - {e}")

print()

