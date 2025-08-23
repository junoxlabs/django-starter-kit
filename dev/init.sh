#!/bin/bash

# Check if dependencies are already installed
if [ ! -d "/app/.venv" ] || [ ! -d "/app/frontend/node_modules" ]; then
    echo "Installing dependencies..."
    make install
else
    echo "Dependencies already installed, skipping installation"
fi

# Start supervisord with uv
exec uv run supervisord -c /etc/supervisor/supervisord.conf