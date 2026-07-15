"""Opt-in LAN command endpoint for a companion phone app/Shortcut."""
from __future__ import annotations
from config import MOBILE_PORT, MOBILE_TOKEN


def start_mobile_bridge(handle_command):
    if not MOBILE_TOKEN:
        print("Mobile bridge disabled: set NOVA_MOBILE_TOKEN in .env to enable it.")
        return None
    try:
        from flask import Flask, jsonify, request
    except ImportError:
        print("Mobile bridge disabled: install Flask first (python -m pip install Flask).")
        return None
    app = Flask("nova-mobile")

    @app.post("/command")
    def command():
        if request.headers.get("X-Nova-Token") != MOBILE_TOKEN:
            return jsonify(error="Unauthorized"), 401
        text = (request.json or {}).get("command", "")
        if not isinstance(text, str) or not text.strip():
            return jsonify(error="A command is required"), 400
        return jsonify(reply=handle_command(text))

    from threading import Thread
    Thread(target=lambda: app.run(host="0.0.0.0", port=MOBILE_PORT, debug=False, use_reloader=False), daemon=True).start()
    print(f"Mobile bridge listening on LAN port {MOBILE_PORT}.")
    return app
