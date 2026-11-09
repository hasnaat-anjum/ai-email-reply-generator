# AI Email Reply Generator

> Paste any email you received — get **3 ready-to-send replies** (Detailed, Balanced, Short) in your chosen tone, in seconds. **No API key, no internet, no cost.**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![License](https://img.shields.io/badge/License-MIT-green) ![Dependencies](https://img.shields.io/badge/Dependencies-None-brightgreen)

## 📌 What it does

Answering email eats hours every week for freelancers, sellers and small business owners. This tool reads an incoming email, works out what the sender actually needs, and drafts the reply for you:

- **Detects intent** — price quote, meeting request, complaint, order update, job enquiry, or thanks
- **Finds every question** in the email so none get missed in your reply
- **Spots urgency and dates** ("urgent", "Friday", "12/11/2026") and reflects them in the draft
- **Auto-detects the sender's name** from their sign-off for a personal greeting
- **Generates 3 lengths** — Detailed, Balanced and Short — so you pick and send

## 👥 Who it benefits

- **Freelancers** replying to client enquiries and price questions all day
- **eBay / marketplace sellers** handling order, delivery and complaint messages
- **Small business owners** who need professional emails without hiring help
- **Marketers & support staff** who need a consistent tone across replies

## ✨ Features

- 5 tones: `professional`, `friendly`, `apologetic`, `sales`, `short`
- Add a one-line `--purpose` ("Confirm Friday delivery") and it is built into the reply
- Interactive mode, file mode, or one-line `--email` mode
- `--save` option to write the replies to a file
- Zero dependencies — Python standard library only
- Unit tests included

## 🛠️ Technologies used

- Python 3.10+ (standard library only: `re`, `argparse`, `dataclasses`)
- Rule-based intent / question / urgency analysis — fast, offline, explainable

## 🚀 How to use it

```bash
# 1. Clone
git clone https://github.com/Hasnaat33/ai-email-reply-generator.git
cd ai-email-reply-generator

# 2a. Try the built-in example
python app.py --file examples/sample_emails.txt --tone friendly --name "Your Name"

# 2b. Or reply to your own email text
python app.py --email "Hi, what is your price for a logo? Can we talk on Monday?" --tone sales

# 2c. Or just run it and paste an email interactively
python app.py

# 3. Run the tests
python -m unittest discover -s tests -v
```

## 📂 Project structure

```
ai-email-reply-generator/
├── app.py                    # Command-line interface
├── src/
│   └── reply_engine.py       # Analysis + reply generation engine
├── examples/
│   └── sample_emails.txt     # Sample client enquiry to try instantly
├── tests/
│   └── test_reply_engine.py  # Unit tests
├── requirements.txt          # No external packages needed
└── README.md
```

## 📸 Demo

**Input** (`examples/sample_emails.txt`): a clothing-shop owner asking for a website price, a Friday call, marked urgent.

**Output (Detailed reply, friendly tone — verified by running the sample):**

```
Hi Ahmed,

Thanks so much for reaching out!

To answer your questions ("What is your price for a business website with an online store?" "Can we schedule a call on Friday to discuss the details?"): [add your answer here].

On pricing: [insert your price / quote here]. This includes [what is included], and I am happy to walk you through the details.

A call sounds good — Friday works for me. Please let me know a time that suits you, and I will confirm right away.

I understand this is urgent, so I am treating it as a priority today.

Warm regards,
Hasnaat
```

Square-bracket placeholders mark the only spots that need your real numbers — everything else is written for you.

## 🔮 Ideas to extend it

- Connect an LLM API for fully-written answers instead of placeholders
- Add a small web UI (Flask / Streamlit)
- Save your own tone templates per client

## 📄 License

MIT — free to use, modify and share.

---
Built by [Hasnaat Anjum](https://github.com/Hasnaat33) — AI Automation | Digital Marketing | SEO | eBay Dropshipping | Frontend Developer
