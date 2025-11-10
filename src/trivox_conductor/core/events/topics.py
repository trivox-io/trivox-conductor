"""
Event topics used in the Trivox Conductor system.
These constants define the various event topics that components can
subscribe to or publish events under.

:cvar CAPTURE_STARTED: Event topic for when capture starts.
:cvar CAPTURE_STOPPED: Event topic for when capture stops.
:cvar CAPTURE_ERROR: Event topic for capture errors.
:cvar REPLAY_RENDER_DETECTED: Event topic for when a replay render is detected.
:cvar MUX_STARTED: Event topic for when muxing starts.
:cvar MUX_PROGRESS: Event topic for muxing progress updates.
:cvar MUX_DONE: Event topic for when muxing is done.
:cvar MUX_FAILED: Event topic for when muxing fails.
:cvar COLOR_DONE: Event topic for when color grading is done.
:cvar COLOR_FAILED: Event topic for when color grading fails.
:cvar UPLOAD_PROGRESS: Event topic for upload progress updates.
:cvar UPLOAD_DONE: Event topic for when upload is done.
:cvar UPLOAD_FAILED: Event topic for when upload fails.
:cvar NOTIFY_SENT: Event topic for when a notification is sent.
:cvar NOTIFY_FAILED: Event topic for when a notification fails.
:cvar AI_OPTIONS_READY: Event topic for when AI options are ready.
:cvar MANIFEST_UPDATED: Event topic for when the manifest is updated.
:cvar USER_NOTIFICATION: Event topic for user notifications.
"""

from __future__ import annotations

CAPTURE_STARTED = "capture.started"
CAPTURE_STOPPED = "capture.stopped"
CAPTURE_ERROR = "capture.error"

REPLAY_RENDER_DETECTED = "replay.render.detected"

MUX_STARTED = "mux.started"
MUX_PROGRESS = "mux.progress"
MUX_DONE = "mux.done"
MUX_FAILED = "mux.failed"

COLOR_DONE = "color.done"
COLOR_FAILED = "color.failed"

UPLOAD_PROGRESS = "upload.progress"
UPLOAD_DONE = "upload.done"
UPLOAD_FAILED = "upload.failed"

NOTIFY_SENT = "notify.sent"
NOTIFY_FAILED = "notify.failed"

AI_OPTIONS_READY = "ai.options.ready"
MANIFEST_UPDATED = "manifest.updated"

USER_NOTIFICATION = "user.notification"
