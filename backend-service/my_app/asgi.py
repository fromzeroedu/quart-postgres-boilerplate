"""
ASGI file for Hypercorn
"""

import os
import sys
import asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from my_app.application import create_app

app = asyncio.run(create_app())

if __name__ == "__main__":
    app.run()
