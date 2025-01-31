# Dash Tracker

Dash Tracker is a lightweight tracking library for Dash applications. It logs user interactions, page views, and navigation events, sending the data to a specified tracking endpoint or printing it to the console for development purposes.

## Features

* Tracks full-page loads and internal navigation events.
* Captures user information from Flask sessions (ID, email, full name).
* Supports ignoring specific routes and callbacks.
* Sends tracking data via HTTP requests or logs to the console.
* Seamless integration with Dash and Flask.

## Usage

Simply instantiate Tracker with your Dash app:

```python
from dash import Dash
from dash_tracker import Tracker

app = Dash(__name__)
tracker = Tracker(app, tracker_endpoint="https://your-tracker-endpoint.com")
```

If no tracking endpoint is provided, events are logged to the console.

The information captured by the tracker will look like this:

```json
{
    "event": "page_view",
    "data":
    {
        "ip": "127.0.0.1",
        "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "base_url": "http://127.0.0.1:8050/",
        "url": "http://127.0.0.1:8050/",
        "url_root": "http://127.0.0.1:8050/",
        "referrer": null,
        "path": "/",
        "full_path": "/?",
        "method": "GET",
        "user_id": "anonymous",
        "email": "anonymous",
        "full_name": "anonymous"
    },
    "timestamp": "2025-01-30T20:29:28.543062+00:00"
}
```
