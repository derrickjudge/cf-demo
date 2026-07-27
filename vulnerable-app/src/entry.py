"""Intentionally vulnerable demo Worker — WAF/rate-limit bait, not a real app.

Every route below is deliberately insecure; do not reuse this file as a
template for real code. Seed data lives in ../schema.sql.
"""

import hmac
import logging
from urllib.parse import ParseResult, parse_qs, urlparse

from branding import render_customers_page, render_dashboard_page, render_login_page
from workers import Response, WorkerEntrypoint

logger = logging.getLogger(__name__)

# The one real demo account. Its password is never committed to the repo --
# it's checked against the DEMO_LOGIN_PASSWORD Worker secret, set locally via
# `wrangler secret put DEMO_LOGIN_PASSWORD`. Every other credential
# (including the seed users in schema.sql, whose password_hash values are
# fabricated and unusable for real auth) falls through to the unconditional
# 401 that already backs the rate-limit demo.
DEMO_USERNAME = "djudge"


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        url = urlparse(request.url)
        params = parse_qs(url.query)

        if url.path == "/":
            return self._redirect_to_login(url)
        if url.path == "/login":
            return self._login_page()
        if url.path == "/dashboard":
            return self._dashboard_page()
        if url.path == "/customers":
            return self._customers_page()
        if url.path == "/search":
            return await self._search(params)
        if url.path == "/greet":
            return self._greet(params)
        if url.path == "/api/login" and request.method == "POST":
            return await self._login(request)
        return Response("not found", status=404)

    def _redirect_to_login(self, url: ParseResult) -> Response:
        """Redirect the bare root path to the Value Corp login page."""
        return Response.redirect(f"{url.scheme}://{url.netloc}/login")

    def _login_page(self) -> Response:
        """Serve the Value Corp branded login page."""
        return Response(
            render_login_page(), headers={"content-type": "text/html; charset=utf-8"}
        )

    def _dashboard_page(self) -> Response:
        """Serve the Value Corp branded post-login dashboard (decorative, no real auth)."""
        return Response(
            render_dashboard_page(),
            headers={"content-type": "text/html; charset=utf-8"},
        )

    def _customers_page(self) -> Response:
        """Serve the Value Corp customer search page (calls GET /search)."""
        return Response(
            render_customers_page(),
            headers={"content-type": "text/html; charset=utf-8"},
        )

    async def _login(self, request) -> Response:
        """Check submitted credentials against the single real demo account.

        All other requests -- malformed bodies, wrong username, wrong
        password, or the DEMO_LOGIN_PASSWORD secret not yet being set --
        fall through to the same unconditional 401 this endpoint has always
        returned, so the rate-limit demo is unaffected.
        """
        try:
            body = await request.json()
        except (ValueError, OSError) as exc:
            logger.error("login request body was not valid JSON: %s", exc)
            return Response("unauthorized", status=401)

        username = body.get("username", "")
        password = body.get("password", "")
        expected_password = getattr(self.env, "DEMO_LOGIN_PASSWORD", None)

        if (
            expected_password
            and username == DEMO_USERNAME
            and hmac.compare_digest(password.encode(), expected_password.encode())
        ):
            return Response.json({"ok": True})

        return Response("unauthorized", status=401)

    async def _search(self, params):
        # Deliberately vulnerable: raw string interpolation, no .bind() —
        # this is the SQLi bait for the WAF demo.
        q = params.get("q", [""])[0]
        sql = (
            "SELECT id, username, email, password_hash FROM users "
            f"WHERE username LIKE '%{q}%'"
        )
        result = await self.env.DB.prepare(sql).all()
        return Response.json(result.results)

    def _greet(self, params):
        # Deliberately vulnerable: unescaped reflection — XSS bait.
        name = params.get("name", [""])[0]
        return Response(
            f"<h1>Hello, {name}!</h1>",
            headers={"content-type": "text/html"},
        )
