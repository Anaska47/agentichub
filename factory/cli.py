from __future__ import annotations

import argparse
import json

from factory.core import (
    batch_summary,
    build_candidates,
    load_strategy,
    pick_batch,
    portfolio_warning,
    write_batch,
)
from factory.mobile import androidize_source


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate a batch of scalable casual app concepts.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    batch_parser = subparsers.add_parser("batch", help="Generate and scaffold a batch of apps.")
    batch_parser.add_argument("--count", type=int, default=5, help="Number of apps to generate.")
    batch_parser.add_argument("--output", default="generated", help="Output directory.")
    batch_parser.add_argument("--strategy", default=None, help="Path to a JSON strategy file.")
    batch_parser.add_argument("--seed", type=int, default=7, help="Random seed.")

    list_parser = subparsers.add_parser("list", help="List candidate concepts without scaffolding.")
    list_parser.add_argument("--strategy", default=None, help="Path to a JSON strategy file.")
    list_parser.add_argument("--limit", type=int, default=10, help="Number of concepts to print.")
    list_parser.add_argument("--seed", type=int, default=7, help="Random seed.")

    android_parser = subparsers.add_parser(
        "androidize",
        help="Convert a generated app or batch into Android-ready Capacitor scaffolds.",
    )
    android_parser.add_argument("--source", required=True, help="Path to a generated app folder or batch folder.")
    android_parser.add_argument("--output", default="android_exports", help="Output directory.")
    android_parser.add_argument(
        "--package-prefix",
        default="com.agentichub",
        help="Reverse-domain prefix to use for generated Android package ids.",
    )

    return parser


def cmd_batch(args: argparse.Namespace) -> int:
    strategy = load_strategy(args.strategy)
    candidates = build_candidates(strategy)
    batch = pick_batch(candidates, count=args.count, seed=args.seed)
    output_path = write_batch(args.output, batch)
    print(batch_summary(batch))
    print(f"Output: {output_path.resolve()}")
    print(portfolio_warning())
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    strategy = load_strategy(args.strategy)
    candidates = build_candidates(strategy)
    batch = pick_batch(candidates, count=args.limit, seed=args.seed)
    payload = [item.to_dict() for item in batch]
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def cmd_androidize(args: argparse.Namespace) -> int:
    output_path = androidize_source(
        source=args.source,
        output_dir=args.output,
        package_prefix=args.package_prefix,
    )
    print(f"Android exports ready: {output_path.resolve()}")
    print("Next step: npm install, npx cap add android, then build the signed AAB in Android Studio.")
    return 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "batch":
        return cmd_batch(args)
    if args.command == "list":
        return cmd_list(args)
    if args.command == "androidize":
        return cmd_androidize(args)
    raise SystemExit(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
