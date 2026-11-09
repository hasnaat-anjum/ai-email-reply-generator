"""
app.py — AI Email Reply Generator (command line)

Usage:
  python app.py                          # interactive mode (paste an email)
  python app.py --file examples/sample_emails.txt --tone friendly --name "Hasnaat"
  python app.py --email "Hi, what is your price?" --tone sales --save reply.txt

Options:
  --tone    professional | friendly | apologetic | sales | short
  --purpose One line you want the reply to achieve, e.g. "Confirm Friday delivery"
  --name    Your name for the sign-off
  --sender  Sender's name (auto-detected from the email if omitted)
  --save    Save the 3 replies to a text file as well as printing them
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))  # so `src` is importable anywhere
from src.reply_engine import TONES, generate_replies  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="AI Email Reply Generator — draft replies in seconds, no API key needed.")
    parser.add_argument("--email", help="The incoming email text")
    parser.add_argument("--file", help="Path to a .txt file containing the incoming email")
    parser.add_argument("--tone", default="professional", choices=list(TONES), help="Reply tone")
    parser.add_argument("--name", default="Hasnaat", help="Your name for the sign-off")
    parser.add_argument("--sender", default="", help="Sender's name (auto-detected if omitted)")
    parser.add_argument("--purpose", default="", help="What the reply must achieve, in one line")
    parser.add_argument("--save", help="Also save the replies to this file")
    args = parser.parse_args()

    email_text = args.email or ""
    if args.file:
        email_text = Path(args.file).read_text(encoding="utf-8")
    if not email_text.strip():
        print("Paste the email you received, then press Enter twice:\n")
        lines: list[str] = []
        while True:
            line = input()
            if line == "" and lines and lines[-1] == "":
                break
            lines.append(line)
        email_text = "\n".join(lines).strip()
    if not email_text:
        print("No email text given. Nothing to do.")
        return

    result = generate_replies(email_text, tone=args.tone, your_name=args.name,
                              sender_name=args.sender, purpose=args.purpose)
    a = result["analysis"]
    print("\n================ WHAT THE ENGINE FOUND ================")
    print(f"Sender:    {a.sender_name}")
    print(f"Intents:   {', '.join(a.intents) if a.intents else 'general'}")
    print(f"Urgent:    {'YES — prioritised in the reply' if a.urgent else 'no'}")
    print(f"Questions: {len(a.questions)} detected")

    output = []
    for label in ("detailed", "balanced", "short"):
        block = f"\n================ {label.upper()} REPLY ================\n{result['replies'][label]}"
        print(block)
        output.append(block)

    if args.save:
        Path(args.save).write_text("\n".join(output), encoding="utf-8")
        print(f"\nSaved to {args.save}")


if __name__ == "__main__":
    main()
