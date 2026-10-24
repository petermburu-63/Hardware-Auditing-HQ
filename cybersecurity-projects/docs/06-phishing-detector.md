# Project 6: Phishing URL Detector (Machine Learning)

**Side:** Defense · **Difficulty:** High · **Language:** Python

## What is this, in plain English?

**Phishing** is when an attacker sends a fake link that's designed to look like a trustworthy site (your bank, your email provider, a delivery company) to trick you into entering your password or personal info on a fake page. A **phishing URL detector** looks at a link *before* you click it and predicts whether it's legitimate or fake — similar to how your email provider's spam filter or browser's "this site may be dangerous" warning works.

## Why it matters

- Phishing is consistently one of the most common ways attackers actually break into systems — it's usually far easier to trick a person than to break through technical defenses.
- This project teaches you **applied machine learning** in a security context, which is a genuinely in-demand skill — most modern security products (spam filters, browser warnings, email security gateways) use some version of this exact approach.
- It also forces you to learn *what actually makes a URL suspicious*, which makes you personally better at spotting phishing attempts by eye.

## How it actually works

1. **Collect data**: you need examples of real phishing URLs (there are public, regularly-updated datasets like PhishTank and OpenPhish) and examples of legitimate URLs (e.g., from the Alexa/Tranco top-sites list).
2. **Extract features** — the actual signals that tend to differ between phishing and legitimate URLs:
   - Length of the URL (phishing URLs are often unusually long)
   - Presence of an IP address instead of a domain name
   - Number of subdomains or dashes in the domain (e.g., `paypal-secure-login.verify-account.com`)
   - Use of URL shorteners
   - Presence of suspicious words ("login," "verify," "secure," "update") combined with a mismatched domain
   - Whether the domain is very newly registered (phishing domains are often days old)
   - Whether the page uses HTTPS (not a guarantee of safety anymore, but still a signal)
3. **Train a classifier**: feed these features into a machine learning model — a Random Forest or Logistic Regression is plenty for this and much easier to understand than deep learning.
4. **Evaluate**: split your data into training and test sets, measure accuracy, but more importantly look at **false positives** (legit sites flagged as phishing) and **false negatives** (phishing sites that slip through) — in security, missed detections (false negatives) are usually the worse failure.
5. **Deploy**: wrap it in a simple script or browser-extension-style tool that takes a URL and returns a risk score.

## Build it yourself (core pieces)

- `scikit-learn` for the ML model — a Random Forest classifier is a great, interpretable starting point.
- `pandas` to build your feature table from raw URLs.
- Start with 5-6 simple features (length, dashes, IP-as-domain, HTTPS present, suspicious keywords) before adding anything fancier — a simple model with good features usually beats a fancy model with bad ones.
- Stretch goal: use `scikit-learn`'s feature importance output to see *which* signals actually mattered most — this is often more educational than the accuracy score itself.

## Where to practice safely

- This one's naturally safe — you're analyzing public URL lists, not attacking anything.
- Just don't actually *visit* raw phishing URLs from these datasets in a normal browser; if you want to inspect one, do it in an isolated VM with no real credentials ever entered.
