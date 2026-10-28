"""Simple CLI for local Falvorn AI instance."""
import argparse
import json
import os
import sys
import httpx
from .sdk import FalvornClient


def main():
    parser = argparse.ArgumentParser(prog="falvornctl", description="Manage your independent Falvorn AI")
    parser.add_argument("--url", default=os.getenv("FALVORN_BASE_URL", "http://127.0.0.1:8000"), help="Platform API URL")
    parser.add_argument("--key", default=os.getenv("FALVORN_API_KEY", ""), help="API key")
    subs = parser.add_subparsers(dest="command", required=True)
    a = subs.add_parser("fetch"); a.add_argument("page"); a.add_argument("--js", action="store_true")
    a = subs.add_parser("search"); a.add_argument("query")
    a = subs.add_parser("agent"); a.add_argument("page"); a.add_argument("goal")
    a = subs.add_parser("run"); a.add_argument("id")
    a = subs.add_parser("monitor"); a.add_argument("page")
    opts = parser.parse_args()
    try:
        with FalvornClient(opts.url, opts.key) as client:
            if opts.command == "fetch": result = client.fetch(opts.page, opts.js)
            elif opts.command == "search": result = client.search(opts.query)
            elif opts.command == "agent": result = client.start_agent(opts.page, opts.goal)
            elif opts.command == "run": result = client.get_run(opts.id)
            else: result = client.monitor(opts.page)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except httpx.HTTPError as exc:
        sys.exit(f"Request failed: {exc}")

if __name__ == "__main__":
    main()
