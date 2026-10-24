# Project 6: Phishing URL Detector (Machine Learning)

**Side:** Defense · **Difficulty:** High · **Language:** Python

## What is this, in plain English?

Phishing is when an attacker sends a fake link designed to look like a trustworthy site such as your bank, your email provider, or a delivery company. A phishing URL detector looks at a link before you click it and predicts whether it is legitimate or fake. This is similar to how an email provider's spam filter or a browser warning system works.

## Why it matters

- Phishing is one of the most common ways attackers actually break into systems. It is often easier to trick a person than to break through technical defenses.
- This project teaches applied machine learning in a security context, which is a genuinely in-demand skill.
- It also forces you to learn what actually makes a URL suspicious, which helps you spot phishing attempts by eye.

## How it actually works

1. Collect data: you need examples of real phishing URLs and examples of legitimate URLs.
2. Extract features: the actual signals that tend to differ between phishing and legitimate URLs.
   - Length of the URL
   - Presence of an IP address instead of a domain name
   - Number of subdomains or dashes in the domain
   - Use of URL shorteners
   - Presence of suspicious words such as login, verify, secure, or update
   - Whether the domain is very new
   - Whether the page uses HTTPS
3. Train a classifier: feed these features into a machine learning model such as a Random Forest or Logistic Regression.
4. Evaluate: split your data into training and test sets and measure accuracy, false positives, and false negatives.
5. Deploy: wrap it in a script or browser-extension style tool that takes a URL and returns a risk score.

## Build it yourself (core pieces)

- `scikit-learn` for the ML model, with a Random Forest as a good starting point.
- `pandas` to build your feature table from raw URLs.
- Start with 5 to 6 simple features: length, dashes, IP as domain, HTTPS presence, suspicious keywords, and shortened links.
- Stretch goal: use `scikit-learn` feature importance output to see which signals mattered most.

## Where to practice safely

- This one is naturally safe. You are analyzing public URL lists rather than attacking anything.
- Do not visit raw phishing URLs in a normal browser. If you want to inspect one, do it in an isolated VM with no real credentials ever entered.
