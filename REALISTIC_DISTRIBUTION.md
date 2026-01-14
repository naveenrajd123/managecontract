# Realistic Contract Risk Distribution

## Overview

This document explains the realistic risk distribution strategy for the demo contract library.

## Distribution Strategy

Instead of a perfectly balanced 25%-25%-25%-25% split, we use a **realistic skewed distribution** that reflects actual enterprise contract portfolios:

| Risk Level | Count | Percentage | Rationale |
|------------|-------|------------|-----------|
| **LOW** | 23 | 20% | Small, routine contracts with minimal risk |
| **MEDIUM** | 35 | 30% | Standard business contracts, baseline compliance |
| **HIGH** | 46 | 40% | Most common - major vendors, significant compliance requirements |
| **CRITICAL** | 12 | 10% | Rare - only the most sensitive/high-value deals |

### Total: 116 Contracts

---

## Why This Distribution is Realistic

### 1. HIGH Risk is Most Common (40%)

**Real-world scenario:**
- Most enterprise contracts fall into this category
- Major cloud services, SaaS platforms, IT infrastructure
- Standard GDPR, PCI-DSS, SOC 2 compliance required
- Values typically $100K-$500K
- Significant but manageable risk

**Examples:**
- Microsoft 365 enterprise license
- Salesforce CRM agreement
- AWS/Azure cloud hosting
- Major consulting engagements

---

### 2. MEDIUM Risk Forms Baseline (30%)

**Real-world scenario:**
- Mid-tier vendors and service providers
- Standard data protection requirements
- Values $25K-$100K
- Routine compliance (CCPA, basic GDPR)

**Examples:**
- Marketing automation tools
- Mid-size software licenses
- Office equipment leases
- Regional service providers

---

### 3. LOW Risk is Uncommon (20%)

**Real-world scenario:**
- Small, routine purchases
- Minimal compliance requirements
- Values under $25K
- Low stakes, easy to replace

**Examples:**
- Office supplies vendor
- Small software tools
- Local service contracts
- Minor consulting agreements

---

### 4. CRITICAL is Rare (10%)

**Real-world scenario:**
- Only the highest-stakes contracts
- Healthcare (HIPAA), finance (SOX), defense (ITAR)
- Life safety, national security, or very high value ($500K+)
- Extensive regulatory requirements

**Examples:**
- Electronic health records system (HIPAA+PHI)
- Medical device software (FDA regulations)
- Financial trading platform (SOX compliance)
- Defense contractor (ITAR/export controls)
- Critical infrastructure (NERC CIP)

---

## Financial Thresholds by Risk Level

### LOW Risk ($5K-$25K)
- **SLA Penalties:** $100-$499 per breach
- **Termination Fee:** 3-9% of remaining value
- **Liability Cap:** 2-3x contract value
- **Insurance:** $1M general, $500K professional
- **Compliance:** General business regulations only

### MEDIUM Risk ($25K-$100K)
- **SLA Penalties:** $500-$2K per breach
- **Termination Fee:** 10-20% of remaining value
- **Liability Cap:** 3-4x contract value
- **Insurance:** $3M general, $2M professional
- **Compliance:** GDPR, CCPA, basic data protection

### HIGH Risk ($100K-$500K)
- **SLA Penalties:** $2K-$10K per breach
- **Termination Fee:** 20-30% of remaining value
- **Liability Cap:** 4-5x contract value
- **Insurance:** $5M general, $3M professional
- **Compliance:** GDPR, PCI-DSS, SOC 2, ISO 27001
- **Requirements:** Quarterly audits, DPO, 72-hour breach notification

### CRITICAL Risk ($500K-$2M)
- **SLA Penalties:** $10K-$50K per breach
- **Termination Fee:** 35-50% of remaining value
- **Liability Cap:** 5-8x contract value
- **Insurance:** $10M general, $5M professional
- **Compliance:** HIPAA+PHI, FDA, SOX, ITAR, NERC CIP, FedRAMP
- **Requirements:** 24/7 monitoring, monthly pentests, 24-hour breach notification
- **Penalties:** Up to $1.5M (HIPAA), €20M (GDPR), criminal charges

---

## Real Legal Consequences Demonstrated

### CRITICAL Contracts Include:

**HIPAA Violations:**
- Up to $1.5M per year per violation type
- Protected Health Information (PHI) handling
- 24-hour breach notification
- Business Associate Agreements (BAA)

**GDPR Violations:**
- Up to 4% of global annual revenue
- Or €20 million, whichever is greater
- Data Protection Officer (DPO) required
- Right to be forgotten compliance

**FDA Violations:**
- Product recalls
- Criminal penalties
- Regulatory audits
- ISO 13485 compliance

**SOX Violations:**
- Criminal penalties for executives
- Financial reporting obligations
- Independent auditor requirements
- Whistleblower protections

**Export Control Violations (ITAR/EAR):**
- Up to $1M per violation
- Criminal charges
- National security implications
- Government contract debarment

---

## AI Risk Assessment Logic

The AI uses a **conservative, balanced approach**:

### Step 1: Determine Base Risk (Financial)
- Contract value
- SLA penalties
- Termination fees
- Liability caps

### Step 2: Check for MAJOR Escalators (Max +2 levels)

**Major Escalators (+1 level each):**
- HIPAA + actual PHI handling (not just mention)
- FDA medical device regulations
- SOX financial reporting obligations
- ITAR/EAR export controls
- Critical infrastructure (life safety, national security)
- Large-scale sensitive data (>100K records)

**Minor Factors (DO NOT escalate):**
- Generic GDPR/CCPA compliance language
- Standard personal data (names, emails)
- Routine confidentiality clauses
- Normal IP protection
- Standard business liability

### Step 3: Calculate Final Risk (with Restraint)
- Start with financial base
- Add +1 for each MAJOR escalator (max 2)
- Minor factors ignored unless combined with high financial risk
- CRITICAL should be rare (~10%)

---

## Testing the AI

### Example 1: Should Stay LOW
```
Contract: $15,000 software license
Terms: Generic GDPR clause, standard confidentiality
Major escalators: 0
Expected: LOW ✓
```

### Example 2: Should Be MEDIUM
```
Contract: $50,000 cloud service
Terms: GDPR, CCPA, standard data protection
Major escalators: 0
Expected: MEDIUM ✓
```

### Example 3: Should Be HIGH
```
Contract: $200,000 enterprise SaaS
Terms: GDPR, PCI-DSS Level 1, SOC 2 Type II audits
Major escalators: 1 (PCI-DSS at scale)
Expected: HIGH ✓
```

### Example 4: Should Be CRITICAL
```
Contract: $750,000 healthcare platform
Terms: HIPAA+PHI, FDA Class II medical device
Major escalators: 2 (HIPAA+PHI handling, FDA regulations)
Expected: CRITICAL ✓
```

---

## Benefits of Realistic Distribution

### 1. **Authentic Demo**
- Reflects real enterprise environments
- Shows AI making nuanced decisions
- Demonstrates system's practical value

### 2. **AI Integrity**
- Justified classifications
- Not random or overly aggressive
- Based on real financial and legal consequences

### 3. **Better User Experience**
- Dashboard looks realistic (not artificially balanced)
- High-risk contracts get appropriate attention
- Critical alerts are meaningful (not 85% false alarms)

### 4. **Scalable Testing**
- Easy to add more contracts
- Distribution naturally maintains
- AI logic is consistent

---

## Status: Deployed ✓

- **AI Logic:** Updated with conservative risk assessment (deployed to Render)
- **Demo Contracts:** 116 contracts with realistic distribution (committed to Git)
- **Catalog Files:** Updated CSV, Markdown, JSON, HTML, TXT formats
- **Distribution:** 20% LOW, 30% MEDIUM, 40% HIGH, 10% CRITICAL

---

**Last Updated:** January 14, 2026
**Version:** 2.0 - Realistic Distribution
