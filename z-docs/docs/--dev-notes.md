# The problem
Millions of people in Africa rely on mobile money but don’t have formal bank accounts.
Without a credit history, they cannot access loans to grow businesses or handle emergencies.
At the same time, fraud in mobile money is on the rise, reducing trust in digital finance.

## Our Solution
We’re building an AI-powered app that does two things:
1. AI Credit Scoring: analyzes mobile money transaction patterns (sending, receiving, saving habits) to create a trust score, even without a bank account.
2. Fraud Detection: monitors for unusual or risky activities in real-time and alerts users to prevent financial losses.

## The Impact
1. Financial Inclusion: Unlocks access to loans for unbanked communities.
2. Safety & Trust: Makes digital finance more secure for everyone.
3. Scalability: Can expand beyond Kenya to other mobile money markets.

## Why This Matters
This project doesn’t just solve one problem—it solves two of Africa’s biggest financial challenges: lack of access and lack of safety.

# Development
Phase 1 (Now): Fraud detection for mobile money (stop scams, protect users, build trust).
Phase 2 (Future): Use transaction data to create AI credit scoring once trust is established.

# Problem Statement
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

    What Judges Expect: A clear, live demonstration of the system working offline – for instance, by turning off Wi-Fi/data on a phone or showing network logs. Judges may try to “trick” the system (using a different face or an out-of-pattern input) to see if it catches the fraud. The best solutions will show a friendly user experience (minimal friction for the real user) and robust security for imposters. The judging will be done at the hackathon venue with your device; no external infrastructure should be needed beyond perhaps a laptop or phone. For example, a judge could be invited to attempt a login with their face, and the system should recognize the face is not the enrolled user and display an alert. The scenario should be safe and quick – no actual SIM swap needed (simply simulate that event in code if relevant). The focus is on demonstrating the concept of real-time, offline fraud prevention 
