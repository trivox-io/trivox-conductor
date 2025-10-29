"""
OBS Capture Plugin (trivox_conductor.plugins.capture_obs)
========================================================

This package provides a Capture *adapter* that talks to OBS Studio via
the `obsws-python` client (WebSocket protocol v5). It implements the
:class:`~trivox_conductor.core.contracts.capture.CaptureAdapter`
contract so the Conductor can:

- Discover scenes and profiles
- Select a scene/profile
- Start/stop recording
- Probe recording status

Registration & Discovery
------------------------
The plugin is discovered by the registry loader via a sibling
``plugin.yaml`` file:

    name: capture_obs
    role: capture
    module: adapter
    class: OBSAdapter
    version: "0.1.0"
    requires_api: ">=1.0,<2.0"
    capabilities:
      - scenes:list
      - profiles:list

Configuration
-------------
Connection settings are passed through the service → adapter pipeline:

- ``host`` (str, default: "127.0.0.1")
- ``port`` (int, default: 4455)
- ``password`` (str, default: "")
- ``request_timeout_sec`` (float, default: 3.0)

The adapter also accepts a transient ``session_id`` (str) used when
emitting events.

Events
------
The adapter publishes bus events during lifecycle:

- :data:`trivox_conductor.core.events.topics.CAPTURE_STARTED`
- :data:`trivox_conductor.core.events.topics.CAPTURE_STOPPED`
- :data:`trivox_conductor.core.events.topics.CAPTURE_ERROR`

Dependencies
------------
- obsws-python >= 1.8,<2.0

The adapter is defensive against minor response-shape differences across
OBS builds and SDK versions.

Exports
-------
- :class:`OBSAdapter`
"""

from .adapter import OBSAdapter

__all__ = ["OBSAdapter"]
