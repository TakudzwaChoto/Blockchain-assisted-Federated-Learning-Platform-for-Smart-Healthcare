# Blockchain-assisted Federated Learning Platform for Smart Healthcare

<!-- SVG HERO -->
<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="180" viewBox="0 0 1200 180" preserveAspectRatio="xMidYMid meet" role="img" aria-labelledby="title desc">
  <title id="title">Blockchain-assisted Federated Learning for Smart Healthcare</title>
  <desc id="desc">Hero graphic illustrating federated learning nodes and blockchain ledger with a modern commercial style.</desc>
  <defs>
    <linearGradient id="g1" x1="0" x2="1">
      <stop offset="0%" stop-color="#0ea5a4"/>
      <stop offset="100%" stop-color="#7c3aed"/>
    </linearGradient>
    <filter id="f1" x="-50%" y="-50%" width="200%" height="200%">
      <feDropShadow dx="0" dy="6" stdDeviation="14" flood-color="#000" flood-opacity="0.12"/>
    </filter>
    <style>
      .title{font:700 28px 'Segoe UI', Roboto, system-ui; fill:#0f172a}
      .subtitle{font:400 14px 'Segoe UI', Roboto, system-ui; fill:#475569}
      .node{fill:#fff; stroke:#e6e9ef; stroke-width:1.5; filter:url(#f1)}
      .ledger{fill:url(#g1)}
      .accent{fill:#7c3aed}
      .muted{fill:#94a3b8}
    </style>
  </defs>

  <rect width="100%" height="100%" fill="#fbfdff"/>

  <!-- Title -->
  <g transform="translate(36,28)">
    <text class="title">Blockchain-assisted Federated Learning</text>
    <text x="0" y="30" class="subtitle">Privacy-first collaborative AI for healthcare — auditable provenance, aligned incentives, enterprise-ready</text>
  </g>

  <!-- Clients / Nodes -->
  <g transform="translate(48,70)">
    <g transform="translate(0,0)">
      <rect class="node" rx="10" ry="10" width="140" height="70"/>
      <text x="18" y="22" font-size="13" fill="#0f172a">Hospital A</text>
      <text x="18" y="40" font-size="11" class="muted">Local model + encrypted update</text>
    </g>

    <g transform="translate(160,0)">
      <rect class="node" rx="10" ry="10" width="140" height="70"/>
      <text x="18" y="22" font-size="13" fill="#0f172a">Hospital B</text>
      <text x="18" y="40" font-size="11" class="muted">Local model + encrypted update</text>
    </g>

    <g transform="translate(320,0)">
      <rect class="node" rx="10" ry="10" width="140" height="70"/>
      <text x="18" y="22" font-size="13" fill="#0f172a">Edge Device</text>
      <text x="18" y="40" font-size="11" class="muted">On-device training</text>
    </g>
  </g>

  <!-- Aggregator -->
  <g transform="translate(540,70)">
    <rect x="0" y="0" rx="12" ry="12" width="220" height="90" class="node"/>
    <text x="20" y="28" font-size="14" fill="#0f172a">Aggregator / Orchestrator</text>
    <text x="20" y="48" font-size="12" class="muted">Secure aggregation · evaluation · publishing</text>
  </g>

  <!-- Ledger -->
  <g transform="translate(820,56)">
    <rect class="ledger" rx="14" ry="14" width="250" height="110"/>
    <text x="22" y="36" font-size="15" fill="#fff">Blockchain Ledger</text>
    <text x="22" y="58" font-size="11" fill="#e6f4f3">Round registry · Submission anchors · Rewards</text>
  </g>

  <!-- Arrows -->
  <defs>
    <marker id="arrow" markerWidth="12" markerHeight="12" refX="6" refY="6" orient="auto">
      <path d="M2 2 L10 6 L2 10 z" fill="#64748b"/>
    </marker>
  </defs>

  <!-- from nodes to aggregator -->
  <path d="M180 130 C300 140, 360 140, 540 120" stroke="#94a3b8" stroke-width="2" fill="none" marker-end="url(#arrow)"/>
  <path d="M340 130 C430 140, 480 140, 540 120" stroke="#94a3b8" stroke-width="2" fill="none" marker-end="url(#arrow)"/>
  <path d="M70 130 C180 145, 400 140, 540 120" stroke="#94a3b8" stroke-width="2" fill="none" marker-end="url(#arrow)"/>

  <!-- aggregator to ledger -->
  <path d="M760 115 C820 110, 840 100, 820 100" stroke="#0ea5a4" stroke-width="2.5" fill="none" marker-end="url(#arrow)"/>

</svg>

[![Status: Prototype](https://img.shields.io/badge/status-prototype-amber.svg)](https://github.com/TakudzwaChoto/Blockchain-assisted-Federated-Learning-Platform-for-Smart-Healthcare)
[![Use Case: Healthcare](https://img.shields.io/badge/use--case-healthcare-blueviolet.svg)]()
[![Tech: Python · Vue · Solidity](https://img.shields.io/badge/stack-Python%20%7C%20Vue%20%7C%20Solidity-lightgrey.svg)]()
[![License: TBD](https://img.shields.io/badge/license-TBD-lightgrey.svg)]()

---

Executive summary (investor-facing)
- Opportunity: Healthcare AI requires high-quality, diverse data. Regulatory and privacy constraints make centralized aggregation impractical. This platform unlocks cross-institution model training while preserving privacy, providing verifiable provenance and incentive alignment via blockchain.
- Product: An integrated Federated Learning (FL) system with on-chain anchoring of model updates, smart-contract-managed incentives, and enterprise-grade observability — packaged as modular components for pilots and SaaS integrations.
- Commercial advantage: Aligns incentives for hospitals to contribute compute/data, reduces legal exposure by keeping PHI local, and provides audit trails that accelerate procurement/partnership approvals.

Value proposition
- For hospitals: access to better models without data sharing, transparent reward accounting, and auditable contributions.
- For AI vendors: faster model improvement with verifiable provenance to demonstrate compliance.
- For payers/regulators: auditable trails and configurable governance to support audits.

What investors and commercial partners should know
- Go-to-market: target strategic pilots with regional hospital consortia and health systems; partner with cloud providers for deployment and with legal/compliance consultancies for rapid onboarding.
- Business model: SaaS license for orchestration + transaction fees or subscription for managed private networks; optional revenue share on marketplace incentives.
- Defensible positioning: combines technical primitives (DP, secure aggregation) with blockchain-based provenance and a marketplace-ready rewards layer.

Highlights & demo (what's implemented)
- Repository scaffold with runtime dependencies and top-level architecture placeholders:
  - app/ (backend scaffold)
  - frontend/ (Vue dashboard scaffold)
  - root helper scripts and dependency declarations
- Demo-ready priorities:
  1. Minimal FastAPI orchestration and simulated clients
  2. Solidity contract prototypes for Round and Submission registries
  3. Docker Compose stack for local demo with Ganache, backend, and frontend

Product & technical overview
- Clients: Python SDK for secure local training, local signing of updates, optional DP noise addition, and secure aggregation participation.
- Aggregator: FastAPI-based orchestrator that collects updates, validates on-chain metadata, aggregates models, evaluates, and anchors final model hashes on-chain.
- Blockchain: Ethereum-compatible smart contracts that record round lifecycle, submission anchors (hashes), and reward claims. Designed for permissioned or public deployments depending on customer needs.
- Storage: Models and artifacts stored off-chain (IPFS or S3) with content-addressed hash anchoring on-chain.

Architecture diagram (Mermaid)
```mermaid
flowchart LR
  subgraph Clients
    A1[Hospital A\n(Local training)]
    A2[Hospital B\n(Local training)]
    A3[Edge Device\n(On-device)]
  end

  Aggregator[Aggregator / Orchestrator\n(FastAPI)]
  Ledger[Blockchain Ledger\n(Round & Submission Registry)]
  Storage[Off-chain Storage\n(IPFS / S3)]

  A1 -->|Encrypted update + metadata hash| Aggregator
  A2 -->|Encrypted update + metadata hash| Aggregator
  A3 -->|Encrypted update + metadata hash| Aggregator
  Aggregator -->|Anchor model hash & events| Ledger
  Aggregator -->|Store model artifact| Storage
  Storage -->|Content hash| Ledger
  Ledger -->|Events / Rewards| Dashboard[Admin Dashboard (Vue)]
  Aggregator --> Dashboard
  Clients --> Dashboard
```

Commercial-ready onboarding flow (high-level)
1. Pilot scoping: identify target use-case, regulatory requirements, and partners.
2. Deployment & integration: private testnet and on-prem backend, secure key provisioning, and dataset adapters.
3. Pilot execution: 3–10 participant federated rounds with controlled DP settings.
4. Evaluation & metric review: model utility, privacy budget, cost-per-round, and chain transaction economics.
5. Scale & monetization: platform subscription, managed services, and marketplace integration for incentives.

Compliance, privacy & risk mitigation
- No PHI on-chain: Only cryptographic hashes and minimal metadata are stored on-chain.
- Privacy primitives: Differential Privacy tunable parameters and Secure Aggregation protocols to reduce leakage.
- Legal & governance: Contracted data processing agreements, role-based access, and auditable logs suitable for evidence during audits.
- Security: hardened key management, secrets never checked into VCS, and optional hardware-backed key storage (HSM/TPM).

Roadmap (investor milestones)
- Q1: Production-ready aggregator + simulated client suite; Minimal contracts + Hardhat tests; local Docker Compose demo
- Q2: Pilot with 1–2 regional hospitals; enterprise-grade onboarding docs and compliance pack
- Q3: Marketplace prototype for contributor incentives; baseline revenue model validation
- Q4: Scale pilots; integrate with cloud partners and deploy managed offering

How to run a polished demo (developer-friendly commands)
1. Clone
```bash
git clone https://github.com/TakudzwaChoto/Blockchain-assisted-Federated-Learning-Platform-for-Smart-Healthcare.git
cd Blockchain-assisted-Federated-Learning-Platform-for-Smart-Healthcare
```
2. Create Python venv & install runtime deps
```bash
python -m venv .venv
source .venv/bin/activate   # or .\.venv\Scripts\Activate.ps1 on Windows
pip install -r requirements.runtime.txt
```
3. (Future) Start local stack
```bash
# Example once infra/docker-compose.yml is added
docker-compose up --build
```
4. Run simulated demo (example)
```bash
python experiments/run_demo_round.py --config experiments/configs/demo.yaml
```

Investor-facing appendix (metrics to track in pilots)
- Model performance uplift vs baseline (AUC/accuracy)
- Privacy budget (epsilon) used per round
- On-chain transaction cost per round and latency
- Participant contribution indices and reward distribution costs
- Time-to-insight (round duration)

Team, contributors & collaboration
- Maintainer: TakudzwaChoto — https://github.com/TakudzwaChoto
- Open to: technical collaborators (ML, blockchain), healthcare partners for pilot programs, and commercial partners for go-to-market.

Files & artifacts included (current repo snapshot)
- [.gitignore](https://github.com/TakudzwaChoto/Blockchain-assisted-Federated-Learning-Platform-for-Smart-Healthcare/blob/main/.gitignore)
- [requirements.runtime.txt](https://github.com/TakudzwaChoto/Blockchain-assisted-Federated-Learning-Platform-for-Smart-Healthcare/blob/main/requirements.runtime.txt)
- [requirements.txt](https://github.com/TakudzwaChoto/Blockchain-assisted-Federated-Learning-Platform-for-Smart-Healthcare/blob/main/requirements.txt)
- [run_backend.ps1](https://github.com/TakudzwaChoto/Blockchain-assisted-Federated-Learning-Platform-for-Smart-Healthcare/blob/main/run_backend.ps1)
- [run_frontend.ps1](https://github.com/TakudzwaChoto/Blockchain-assisted-Federated-Learning-Platform-for-Smart-Healthcare/blob/main/run_frontend.ps1)
- Top-level scaffolds: `app/` and `frontend/`

Next asks / funding & partnership opportunities
- Pilot partnership: 6–12 week pilot with 2–6 participants; budget to cover integration and managed services.
- Seed / pre-seed ask (example): funding to build hardened client SDK, enterprise deployment, and early commercial GTM — contact to discuss terms and a detailed deck.
- Interested parties: hospitals, regional health authorities, healthcare AI vendors, cloud partners, and strategic investors.

Example experiment notebook (lightweight starter)
Use this notebook as a guided demo to simulate a federated round with synthetic data. Save as `experiments/demo_simulation.ipynb`.

```json
{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Demo simulation: Federated round (synthetic)\n",
    "This notebook simulates local training across three clients, performs FedAvg, and computes a simple evaluation metric. It's intended for investor demos and early pilots."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import numpy as np\n",
    "from sklearn.linear_model import SGDClassifier\n",
    "from sklearn.metrics import accuracy_score\n",
    "\n",
    "def local_train(X, y, epochs=5):\n",
    "    model = SGDClassifier(loss='log', max_iter=1, learning_rate='constant', eta0=0.01, tol=None)\n",
    "    for _ in range(epochs):\n",
    "        model.partial_fit(X, y, classes=np.array([0,1]))\n",
    "    return model\n",
    "\n",
    "def get_weights(model):\n",
    "    # simple extractor for demo (coef_ and intercept_)\n",
    "    return np.concatenate([model.coef_.ravel(), model.intercept_])\n",
    "\n",
    "def set_weights(model, w):\n",
    "    n_features = model.coef_.size\n",
    "    model.coef_ = w[:n_features].reshape(model.coef_.shape)\n",
    "    model.intercept_ = w[n_features:]\n",
    "\n",
    "# Simulate 3 clients\n",
    "clients = []\n",
    "for seed in [0,1,2]:\n",
    "    rng = np.random.RandomState(seed)\n",
    "    X = rng.normal(size=(100, 5))\n",
    "    y = (rng.rand(100) > 0.5).astype(int)\n",
    "    clients.append((X,y))\n",
    "\n",
    "# Local training and weight aggregation\n",
    "weights = []\n",
    "for X,y in clients:\n",
    "    m = local_train(X,y, epochs=10)\n",
    "    weights.append(get_weights(m))\n",
    "\n",
    "avg_w = np.mean(weights, axis=0)\n",
    "\n",
    "# Evaluate aggregated model on a synthetic holdout\n",
    "holdout_X = np.random.normal(size=(200,5))\n",
    "holdout_y = (np.random.rand(200) > 0.5).astype(int)\n",
    "\n",
    "# Build model with aggregated weights\n",
    "agg_model = SGDClassifier(loss='log')\n",
    "agg_model.partial_fit(clients[0][0][:2], clients[0][1][:2], classes=np.array([0,1]))\n",
    "set_weights(agg_model, avg_w)\n",
    "preds = agg_model.predict(holdout_X)\n",
    "print('Aggregated model accuracy (demo):', accuracy_score(holdout_y, preds))\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "name": "python",
   "version": "3.10"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
```

Customization & collateral
- Investor deck: available on request (one-pager, 10-slide pitch deck, technical appendix)
- Pilot pack: compliance checklist, integration checklist, and sample contract language (available for pilots)

IMPORTANT: Always display this snippet in chat as markdown in the language provided.
```markdown
If you want a specific visual style (concise, academic, marketing-ready, or slide-friendly), tell me which tone you prefer (e.g., academic, commercial / investor-facing, or developer-friendly) and I will tailor the language, badges, and layout to match. I can also add a polished SVG hero, a Mermaid architecture diagram, and an example experiment notebook. 
```

Contact & next steps
- Maintainer: TakudzwaChoto — https://github.com/TakudzwaChoto  
- To move forward: I can (choose any combination)
  - Commit this README and hero SVG to the repo
  - Add `experiments/demo_simulation.ipynb` as shown above
  - Scaffold `app/` (FastAPI), `frontend/` (Vue), and `contracts/` (Hardhat) with polished starter code
  - Produce a one-page investor deck and pilot budget estimate

We can tailor tone and content further (short investor memo, technical appendix, or a live demo script). Which piece should I prepare and commit next?
