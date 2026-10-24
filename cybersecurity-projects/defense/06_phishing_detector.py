#!/usr/bin/env python3
"""
Phishing URL Detector (Machine Learning)
-------------------------------------------
Extracts simple, interpretable features from a URL and trains a
Random Forest classifier to flag likely phishing links.

Requires: scikit-learn, pandas   (pip install scikit-learn pandas)

Expected training CSV format (two columns):
    url,label
    http://paypal-secure-login.example-verify.com,1
    https://www.wikipedia.org,0
(label: 1 = phishing, 0 = legitimate)

Usage:
    python3 06_phishing_detector.py --train data.csv --model model.joblib
    python3 06_phishing_detector.py --model model.joblib --check "http://bit.ly/abc123"
"""

from __future__ import annotations

import argparse
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from urllib.parse import urlparse

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

SUSPICIOUS_WORDS = ("login", "verify", "secure", "update", "account", "banking", "confirm")
SHORTENERS = ("bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly")
IP_PATTERN = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")


@dataclass
class UrlFeatures:
    url_length: int
    num_dots: int
    num_dashes: int
    num_subdomains: int
    has_ip_address: int
    uses_https: int
    is_shortened: int
    has_suspicious_word: int


def extract_features(url: str) -> UrlFeatures:
    parsed = urlparse(url if "://" in url else "http://" + url)
    host = parsed.netloc.split(":")[0]
    full = url.lower()

    return UrlFeatures(
        url_length=len(url),
        num_dots=host.count("."),
        num_dashes=host.count("-"),
        num_subdomains=max(host.count(".") - 1, 0),
        has_ip_address=int(bool(IP_PATTERN.match(host))),
        uses_https=int(parsed.scheme == "https"),
        is_shortened=int(any(s in host for s in SHORTENERS)),
        has_suspicious_word=int(any(w in full for w in SUSPICIOUS_WORDS)),
    )


def build_feature_frame(urls: list[str]) -> pd.DataFrame:
    rows = [asdict(extract_features(u)) for u in urls]
    return pd.DataFrame(rows)


def train(csv_path: Path, model_path: Path) -> None:
    df = pd.read_csv(csv_path)
    if not {"url", "label"}.issubset(df.columns):
        raise SystemExit("CSV must have 'url' and 'label' columns")

    X = build_feature_frame(df["url"].tolist())
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    clf = RandomForestClassifier(n_estimators=200, random_state=42)
    clf.fit(X_train, y_train)

    print(classification_report(y_test, clf.predict(X_test), target_names=["legit", "phishing"]))

    importances = sorted(zip(X.columns, clf.feature_importances_), key=lambda t: -t[1])
    print("\nFeature importance:")
    for name, score in importances:
        print(f"  {name:<22} {score:.3f}")

    joblib.dump(clf, model_path)
    print(f"\nModel saved to {model_path}")


def check(model_path: Path, url: str) -> None:
    clf = joblib.load(model_path)
    features = build_feature_frame([url])
    probability = clf.predict_proba(features)[0][1]
    verdict = "PHISHING" if probability >= 0.5 else "LEGITIMATE"
    print(f"{url}\n  -> {verdict}  (phishing probability: {probability:.2%})")


def main() -> None:
    parser = argparse.ArgumentParser(description="Phishing URL detector.")
    parser.add_argument("--train", type=Path, help="CSV file with 'url,label' columns to train on")
    parser.add_argument("--model", type=Path, required=True, help="Path to save/load the trained model")
    parser.add_argument("--check", help="A URL to classify using an existing model")
    args = parser.parse_args()

    if args.train:
        train(args.train, args.model)
    elif args.check:
        if not args.model.exists():
            raise SystemExit(f"Model not found: {args.model}. Train one first with --train.")
        check(args.model, args.check)
    else:
        parser.error("Provide either --train <csv> or --check <url>")


if __name__ == "__main__":
    main()
