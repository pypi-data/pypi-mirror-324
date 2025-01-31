import asyncio
import json
import os
from datetime import datetime, timezone
from typing import Optional

import aiohttp
from dash import Dash, Input, Output, dcc, html
from flask import request, session

from .ignore_routes import (add_ignore_routes, get_ignore_callbacks,
                            get_ignore_routes)


class Tracker:
    def __init__(
        self,
        app: Dash,
        tracker_endpoint: Optional[str] = None,
        ignore_routes: Optional[list] = None,
    ):
        """Tracker class for tracking Dash app usage.

        Add this class to your Dash app to track page views and
        navigation events.

        The information is sent to a tracker endpoint (Separate
        server) or printed to console.

        The user information is obtained from the Flask session.
        It defaults to anonymous if the session is not available.
        The tracker will try to pull the `user` key from the session
        and extract the `id`, `email`, and `full_name`.

        Args:
            app (Dash): Dash app
            tracker_endpoint (Optional[str], optional): string endpoint
                for tracking, if not supplied, actions will be printed
                to console. Defaults to None.
        """
        if os.environ.get("DASH_TRACKER_INITIALIZED"):
            return
        os.environ["DASH_TRACKER_INITIALIZED"] = "1"

        self.app = app
        self.tracker_endpoint = tracker_endpoint
        self._should_print = False

        self._set_base_ignore_routes()
        self._setup_tracking()

        if ignore_routes is not None:
            add_ignore_routes(app, ignore_routes)


    async def _send_event(self, event_type: str, event_data: dict):
        """
        Send event to tracker endpoint or print to console.
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        if self._should_print:
            print(
                json.dumps(
                    {
                        "event": event_type,
                        "data": event_data,
                        "timestamp": timestamp
                    }
                )
            )
        else:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.tracker_endpoint,
                    json = {
                        "event": event_type,
                        "data": event_data,
                        "timestamp": timestamp
                    }
                ): pass


    def _set_base_ignore_routes(self):
        """Set the base ignore routes for the tracker."""
        add_ignore_routes(self.app, routes = [])


    def _extract_user_info(self):
        """
        Extract user information from the Flask session.
        It defaults to anonymous if the session is not available.
        """
        user_info = {"user_id": "anonymous", "email": "anonymous", "full_name": "anonymous"}
        if "user" in session:
            user_info["user_id"] = session["user"].get("id", "anonymous")
            user_info["email"] = session["user"].get("email", "anonymous")
            user_info["full_name"] = session["user"].get("full_name", "anonymous")
        return user_info


    def _track_page_view(self):
        """
        Track page view and navigation events.

        The tracker will send a page view event if either
            * The app recognizes a HTTP request (initial page load and API calls)
            * The app recognizes Dash callbacks (to track internal navigation)
        """
        server = self.app.server

        @server.before_request
        def before_request_page_track():

            ignore_routes = get_ignore_routes(self.app)
            ignore_callbacks = get_ignore_callbacks(self.app)

            # Track Full Page Loads & API Requests
            user_info = self._extract_user_info()
            event_data = {
                "ip": request.remote_addr,
                "user_agent": request.user_agent.string,
                "base_url": request.base_url,
                "url": request.url,
                "url_root": request.url_root,
                "referrer": request.referrer,
                "path": request.path,
                "full_path": request.full_path,
                "method": request.method,
                "user_id": user_info["user_id"],
                "email": user_info["email"],
                "full_name": user_info["full_name"],
            }

            # Fallback for Internal Navigation (if `dcc.Location` isn't used)
            if request.path == "/_dash-update-component":
                body = request.get_json()

                # Exit early if the request body is not valid
                if not body or "inputs" not in body or "output" not in body:
                    return

                if body["output"] in ignore_callbacks:
                    return

                # Check whether the callback has an input using the pathname
                # If it does, check whether the pathname matches a route to ignore.
                pathname = next(
                    (
                        inp.get("value") for inp in body["inputs"]
                        if isinstance(inp, dict)
                        and inp.get("property") == "pathname"
                    ),
                    None,
                )

                if pathname:
                    if ignore_routes.test(pathname):
                        return
                    else:
                        event_data["path"] = pathname
                        asyncio.run(self._send_event("page_view", event_data))
                        return
            else:
                # If the route is not a callback route, check whether the path
                # matches a route to ignore.
                if ignore_routes.test(request.path):
                    return

                # Otherwise, send a page view event.
                asyncio.run(self._send_event("page_view", event_data))

            # Use `dcc.Location` for Efficient Internal Navigation Tracking
            try:
                if any(isinstance(child, dcc.Location) for child in self.app.layout.children):
                    @self.app.callback(
                        Output('url', 'pathname'),
                        Input('url', 'pathname'),
                        prevent_initial_call = True
                    )
                    def track_dash_navigation(pathname):
                        if not pathname or ignore_routes.test(pathname):
                            return pathname
                        user_info = self._extract_user_info()
                        event_data = {
                            "ip": request.remote_addr,
                            "user_agent": request.user_agent.string,
                            "base_url": request.base_url,
                            "url": request.url,
                            "url_root": request.url_root,
                            "referrer": request.referrer,
                            "path": pathname,
                            "full_path": request.full_path,
                            "method": "GET", # Internal navigation is a GET request
                            "user_id": user_info["user_id"],
                            "email": user_info["email"],
                            "full_name": user_info["full_name"],
                        }
                        asyncio.run(self._send_event("page_view", event_data))
                        return pathname
            except Exception:
                pass

    def _setup_tracking(self):
        """
        Setup tracking for Dash app.
        """
        if self.tracker_endpoint is None:
            print(" * No tracker endpoint supplied, tracking will be printed to console. Use this for development only.")
            self._should_print = True
        self._track_page_view()
