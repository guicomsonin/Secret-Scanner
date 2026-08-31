import argparse
import sys

from .reporter import render_json, render_text
from .scanner import Scanner


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="secretscanner",
        description="Fast, lightweight secret scanner for developers.",
    )
    parser.add_argument(
        "target",
        help="File or directory to scan.",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        metavar="DIR",
        help="Additional directory name to exclude (can be used multiple times).",
    )
    parser.add_argument(
        "--exclude-ext",
        action="append",
        default=[],
        metavar=".EXT",
        help="Additional file extension to exclude (can be used multiple times).",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format.",
    )
    parser.add_argument(
        "--ci",
        action="store_true",
        help="Exit with code 1 if any secret is found (for CI pipelines).",
    )
    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    scanner = Scanner(
        target=args.target,
        exclude_dirs=set(args.exclude),
        exclude_extensions=set(args.exclude_ext),
    )
    findings = scanner.scan()

    if args.format == "json":
        output = render_json(findings, args.target)
    else:
        output = render_text(findings, args.target)

    print(output)

    if args.ci and findings:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
