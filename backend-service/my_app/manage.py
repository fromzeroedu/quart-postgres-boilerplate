"""
The entry point to our Python Quart application.
"""

import asyncio
from my_app.application import create_app

app = asyncio.run(create_app())
