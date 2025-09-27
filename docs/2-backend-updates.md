# Aegis Backend

# Transaction & Fraud Detection Foundations
## What is a Transaction in Our System?
A transaction is any movement of value in or out of a user’s mobile wallet, account, or digital platform.
Since we’re targeting mobile money first (like M-Pesa, Airtel Money, MTN MoMo, etc.), every transaction comes into our backend via webhooks (API notifications from providers).

Think of it as:
Who sent money? (sender)
Who received money? (receiver)
How much and in what currency? (amount + currency)
When did it happen? (timestamp)
What’s the provider’s unique ID for it? (transaction reference)
What’s the complete raw data? (to keep for audits, disputes, and AI training)

Types of Transactions We Support
Customer → Customer (peer-to-peer)
Customer → Merchant (buying goods, paying bills)
Bank → Wallet / Wallet → Bank (deposits, withdrawals)
System Adjustments (reversals, failed payments, chargebacks)

Why it matters:
We normalize all these into one Transaction model so we can analyze patterns consistently, no matter the provider.



## What Makes a Transaction “Flagged”?
Fraud detection means automatically marking suspicious activity.

There are two layers:
A. Rules-based Fraud Detection (short term: hackathon-ready)
High-Value Transfers: If amount > X threshold (e.g., 100,000 KES), flag.
Velocity Checks: If the same user sends too many transactions in a short time (e.g., >5 in 10 minutes).
Known Fraud Accounts: If sender/receiver matches a blacklist.
Geographic/Channel Anomaly: If someone usually transacts locally but suddenly from another region.
Structuring (Smurfing): Multiple small payments (e.g., 20 x 999 KES) within an hour to bypass detection.

These rules are simple but very effective to stop common scams.

B. AI/ML Fraud Detection (long term: scalable, Phase 2)
Behavioral Anomaly Detection: Compare a transaction against a user’s past history.
Example: If a user typically spends 200–500 KES weekly, but suddenly sends 20,000 KES, it’s suspicious.
Network Analysis: Detect fraud rings by mapping relationships between senders/receivers.
Supervised Models: Train classifiers (logistic regression, random forests, deep learning) using historical fraud data.

This allows us to move beyond fixed thresholds and adapt to new fraud patterns.

## Why Store Raw + Normalized Data?
Normalized Fields → Sender, receiver, amount, timestamp, etc. (for rules, API queries, dashboards).
Raw Payload → The complete data provider gave us (needed for compliance, disputes, retraining AI).

This makes our system future-proof:

We can re-run old data on new AI models.
We can handle audits or customer complaints without losing details.

## Flow of Events (How Fraud Detection Works in Practice)
Mobile Money Provider → Aegis
Provider sends a JSON payload to our webhook (e.g., M-Pesa STK push response).

Store Transaction
Save normalized + raw data into DB.

Fraud Check Engine
Run rule-based checks instantly.

If matched, create a Fraud Alert record.
Notify / Act

Alert shown on dashboard (for admins).
Optionally, notify user or auto-freeze suspicious accounts.

AI Enhancement (Future)
Feed stored transactions into ML models for smarter scoring.

## Example (Real-World Scenarios)
Case 1: Simple Fraud
John normally sends 200 KES → 500 KES daily.
Suddenly, he sends 50,000 KES to a new number.

Rule triggered: “High-value anomaly.” → Flagged.

Case 2: Structuring
Mary sends 15 transactions of 999 KES within 10 minutes.
Rule triggered: “Suspicious velocity/structuring.” → Flagged.

Case 3: Blacklist
Receiver number is in blacklist of known fraudsters.
Rule triggered: “Blacklisted account.” → Flagged immediately.

## Why This Matters (for the meeting pitch)
We’ve mapped out how transactions flow from providers into our system.
We’ve defined clear rules for detecting fraud (Phase 1 MVP).
We’ve prepared the backend structure to handle AI integration later without breaking things.
This shows we’re not just coding blindly — we’re designing for financial inclusion + security in a scalable way.
