"""Intentionally vulnerable demo Worker — WAF/rate-limit bait, not a real app.

Every route below is deliberately insecure; do not reuse this file as a
template for real code. Seed data lives in ../schema.sql.
"""

from urllib.parse import parse_qs, urlparse

from workers import Response, WorkerEntrypoint


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        url = urlparse(request.url)
        params = parse_qs(url.query)

        if url.path == "/search":
            return await self._search(params)
        if url.path == "/greet":
            return self._greet(params)
        if url.path == "/api/login" and request.method == "POST":
            return Response("unauthorized", status=401)
        return Response("not found", status=404)

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
