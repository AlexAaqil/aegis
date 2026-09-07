# Aegis Backend

# Briefing
Hello team,


Earlier this week we shared the financial inclusion and banking whitepaper and a case study to help you understand the sector better. Those resources give you the context, gaps, and opportunities. Now it’s time to put that into practice.


Below is your problem statement for this vertical.





Finance: Face-to-Phone – Real-Time Biometric Fraud Detection

What to Build: A mobile-based fraud detection prototype that combines real-time anomaly detection with biometric user verification entirely offline. Teams will create a proof-of-concept where a phone (or small device) uses face or voice biometrics to confirm the user’s identity during sensitive financial actions, while simultaneously flagging unusual transaction patterns locally. This “Face-to-Phone” solution should serve as a mini secure banking app or device that works without internet or external data.

Must-Have Features:

    Biometric Authentication: Use on-device face recognition or voice recognition to verify the user before allowing a transaction or account access. For example, the phone’s camera might scan the user’s face and compare it to an enrolled template to approve a mobile money transfer. No biometric data should leave the device (privacy by design).

    Real-Time Fraud Checks: Implement simple offline logic or ML models to spot anomalies in activity (e.g. an unusually large transfer or a sudden SIM change event). The system should flag or halt suspicious actions in under a second. Simulated data can drive this – e.g. a dummy stream of transactions to detect outliers.

    User Alerts & Logging: If a potential fraud or impostor is detected (biometric mismatch or anomalous behaviour), the app/device must immediately alert the user or “security officer” (for demo, this could be a console message or on-screen alert). It should log the event locally for later review, with an explanation of why it was flagged (e.g. “Face mismatch – possible SIM swap fraud”).

    Fallback for Low-Tech Users: Design the workflow to be inclusive of users on basic phones. For example, if biometric sensors or smartphones aren’t available, propose an alternative like a PIN or a one-time code via SMS that the legitimate user knows (you can simulate this). Emphasize that the solution could extend to feature phones via USSD or IVR with voice ID as a second factor.

Key Constraints:

    Offline-First: The entire system must run without internet connectivity. All fraud detection logic and biometric matching should occur on the local device (e.g. using an embedded ML model or simple rules). No cloud APIs allowed – prove that security can work offline in real-time.

    Lightweight Models: Any AI models (for anomaly detection or face/voice recognition) should be small and efficient enough for a low-end Android Go smartphone or Raspberry Pi. Aim to use libraries or formats like ONNX or TensorFlow Lite for on-device inference. For voice recognition, tools like Whisper (small model) can be used, and for face recognition, a lightweight OpenCV or MobileNet-based model is acceptable – but no large GPU-required models.

    Privacy & Security: Biometric data is sensitive; the solution should store it securely on-device and ideally encrypt any logs. No personal data should be exposed externally. Explainability is important: if a transaction is blocked, the system should give a simple reason (to build user trust and satisfy regulators).

    Latency & Accuracy: Strive for sub-second detection of fraud after an action is initiated, to mimic real banking needs. Biometric matching should be accurate enough to avoid obvious false rejects/accepts during the demo (it’s okay to use a small sample or even simulate the matching logic if needed, as long as the concept is shown).

Judging Setup:

    Demo Scenario: Teams will simulate a high-risk transaction (for example, a money transfer) on their prototype. First, they’ll enroll a team member’s biometric (face/voice) as the “account owner”. During judging, another person will attempt a transaction – the system should detect either an unrecognized face or an anomalous pattern and block or flag the action. Judges might also see a successful attempt by the real user for comparison.

    What Judges Expect: A clear, live demonstration of the system working offline – for instance, by turning off Wi-Fi/data on a phone or showing network logs. Judges may try to “trick” the system (using a different face or an out-of-pattern input) to see if it catches the fraud. The best solutions will show a friendly user experience (minimal friction for the real user) and robust security for imposters. The judging will be done at the hackathon venue with your device; no external infrastructure should be needed beyond perhaps a laptop or phone. For example, a judge could be invited to attempt a login with their face, and the system should recognize the face is not the enrolled user and display an alert. The scenario should be safe and quick – no actual SIM swap needed (simply simulate that event in code if relevant). The focus is on demonstrating the concept of real-time, offline fraud prevention leveraging biometrics.

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
