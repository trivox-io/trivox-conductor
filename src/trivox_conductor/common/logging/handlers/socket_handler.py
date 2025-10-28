"""
Socket handler for logging.
"""

# Justification: broad exception handling is needed to avoid logging failures
# pylint: disable=broad-exception-caught

import logging
import pickle
import queue
import random
import socket
import struct
import threading
import time
from logging.handlers import RotatingFileHandler, SocketHandler
from typing import Optional


class SocketLogger(SocketHandler):
    """
    SocketLogger extends the functionality of logging.handlers.SocketHandler.
    It sends log records over a socket connection with custom formatting and handling.
    """

    _server_available = None
    _last_check_time = 0
    _check_interval = 10

    @staticmethod
    def is_server_available(host, port):
        """
        Check if the socket server is available.
        """
        try:
            with socket.create_connection((host, port), timeout=0.1):
                return True
        except (socket.timeout, ConnectionRefusedError, OSError):
            return False

    def emit(self, record):
        current_time = time.time()

        if self._server_available is None:
            self._server_available = self.is_server_available(
                self.host, self.port
            )
            self._last_check_time = current_time

        if not self._server_available:
            return  # Skip logging if the server is unavailable

        try:
            # if record is not serializable, it will raise an exception
            # so turn it into a string
            # TODO: Santi - Improve this to handle non-serializable objects
            if not isinstance(record.msg, str):
                record.msg = str(record.msg)

            # Pickle the record
            s = pickle.dumps(record)

            # Prepend the length of the pickled data
            slen = struct.pack(">L", len(s))

            self.send(slen + s)
        except (
            pickle.PicklingError,
            TypeError,
            struct.error,
            OSError,
            socket.error,
        ):
            self.handleError(record)

    def send(self, s):
        """
        Send the s (data) to the socket. Reset server availability on errors.
        """
        try:
            super().send(s)
        except (socket.error, BrokenPipeError):
            self._server_available = None  # Reset availability flag


# Justification: many arguments are needed for configuration
# pylint: disable=too-many-arguments
class RobustSocketLogger(SocketHandler):
    """
    Non-blocking, auto-reconnecting SocketHandler with an in-memory ring buffer.
    - Enqueues records immediately (fast path)
    - Background thread handles (re)connect and flush
    - Bounded queue with drop-oldest policy
    - Optional local fallback file when queue overflows
    """

    def __init__(
        self,
        host: str,
        port: int,
        *,
        queue_maxsize: int = 2000,
        fallback_file: Optional[str] = None,
        backoff_min: float = 0.25,
        backoff_max: float = 8.0,
    ):
        # Do not connect in base __init__; we manage the socket ourselves
        super().__init__(host, port)
        # Ensure base class doesn't try to connect eagerly
        self.sock = None

        self._q: "queue.Queue[logging.LogRecord]" = queue.Queue(
            maxsize=queue_maxsize
        )
        self._stop = threading.Event()
        self._sender = threading.Thread(
            target=self._run_sender, name="LogSocketSender", daemon=True
        )

        self._backoff_min = backoff_min
        self._backoff_max = backoff_max

        self._fallback: Optional[RotatingFileHandler] = None
        if fallback_file:
            self._fallback = RotatingFileHandler(
                fallback_file,
                maxBytes=5_000_000,
                backupCount=3,
                encoding="utf-8",
                delay=True,
            )
            # simple, robust formatter; avoid fields that may be missing on foreign records
            fmt = logging.Formatter(
                "%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
            )
            self._fallback.setFormatter(fmt)

        self._sender.start()

    # ---- public logging API (fast path) ------------------------------------

    def emit(self, record: logging.LogRecord):
        """
        Enqueue and return. Never block the app's logging call.
        """
        try:
            # Wrap payload with length prefix now, keep sender simple.
            framed = self.makePickle(record)
            try:
                self._q.put_nowait((record, framed))
            except queue.Full:
                # Drop oldest (ring buffer policy)
                try:
                    self._q.get_nowait()
                except queue.Empty:
                    pass
                # Try again; if still full, fallback to file
                try:
                    self._q.put_nowait((record, framed))
                except queue.Full:
                    if self._fallback:
                        self._fallback.emit(record)
                    # else drop silently
        except Exception:
            # Never raise from logging; record to fallback if available
            if self._fallback:
                try:
                    self._fallback.emit(record)
                except Exception:
                    pass

    def close(self):
        try:
            self._stop.set()
            self._sender.join(timeout=2.0)
        finally:
            try:
                if self.sock:
                    try:
                        self.sock.shutdown(socket.SHUT_RDWR)
                    except OSError:
                        pass
                    self.sock.close()
            except Exception:
                pass
            if self._fallback:
                try:
                    self._fallback.close()
                except Exception:
                    pass
            super().close()

    # ---- background sender thread ------------------------------------------

    def _run_sender(self):
        backoff = self._backoff_min
        while not self._stop.is_set():
            try:
                if self.sock is None:
                    self._try_connect()
                    backoff = self._backoff_min  # reset on success

                # If connected, block briefly waiting for data to send
                record, framed = self._q.get(timeout=0.5)
                try:
                    self.send(
                        framed
                    )  # uses SocketHandler.send; raises on error
                except Exception:
                    # Put back to queue head if possible (best-effort)
                    self.sock = None
                    try:
                        self._q.put_nowait((record, framed))
                    except queue.Full:
                        # queue already full; fallback to file
                        if self._fallback:
                            self._fallback.emit(record)
                    # fall through to backoff
                    self._sleep_with_backoff(backoff)
                    backoff = min(backoff * 2, self._backoff_max)
            except queue.Empty:
                # No data; loop again (and reconnect if needed)
                if self.sock is None:
                    self._sleep_with_backoff(backoff)
                    backoff = min(backoff * 2, self._backoff_max)
                continue
            except Exception:
                # Any unexpected error: drop socket, backoff, continue
                self.sock = None
                self._sleep_with_backoff(backoff)
                backoff = min(backoff * 2, self._backoff_max)

    def _try_connect(self):
        # Non-blocking-ish connect with short timeout
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        try:
            s.connect((self.host, self.port))
            # Connected
            s.settimeout(None)
            self.sock = s
        except Exception:
            try:
                s.close()
            except Exception:
                pass
            self.sock = None
            raise

    def _sleep_with_backoff(self, base: float):
        # Add a tiny jitter to avoid thundering herd: [base, base+30%]
        time.sleep(base + random.random() * (base * 0.3))


# pylint: enable=too-many-arguments
# pylint: enable=broad-exception-caught
