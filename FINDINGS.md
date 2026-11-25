# Findings: fed-watchers
Last updated: 2026-11-25

## domestic/quantitative/2026-11-peak-hawk-or-2018
Status: complete | Run: 2026-11-25 | Source: domestic/quantitative/2026-11-peak-hawk-or-2018/RESULT.md
```yaml
- id: fw-2026-11-peak-hawk-or-2018-h1-peak-hawk
  study: domestic/quantitative/2026-11-peak-hawk-or-2018
  type: quant
  region: US
  topic: fed-policy
  hypothesis: "Governor Waller's openness to a half-point hike and the October Fed minutes mark the peak of the Fed's tough stance on rates."
  verdict: killed
  finding: "Not the peak: markets still expect less tightening than Waller floated, and the October minutes sounded tougher than September's, though one scoring method disagreed."
  key_stats:
    - "about 41bp of the 50bp Waller floated is priced by January"
    - "Waller's stance score rose 3.0 points from his earlier speeches"
    - "October minutes scored 2 points tougher than September's"
  confidence: "55%"
  numbers: ["41bp", "50bp", "40.9bp", "+3.0", "+2"]
  source_file: domestic/quantitative/2026-11-peak-hawk-or-2018/RESULT.md
  run_date: 2026-11-25
  valid_until: 2026-12-08
  owner: fx-115
  links_to: [fw-2026-11-25-peak-hawk-debate-peak-camp]
  people: ["Christopher J. Waller"]
- id: fw-2026-11-peak-hawk-or-2018-h2-behind-curve
  study: domestic/quantitative/2026-11-peak-hawk-or-2018
  type: quant
  region: US
  topic: fed-policy
  hypothesis: "The Fed's policy rate is below what standard policy rules say it should be, so the Fed is behind the curve."
  verdict: inconclusive
  finding: "Can't tell: standard policy rules disagree too widely to judge, though most of them point to a rate higher than today's."
  key_stats:
    - "policy rate of 3.88%"
    - "rule estimates range from 3.18 to 7.38 percent"
    - "90% of rule versions point higher than today's rate"
  confidence: "55%"
  numbers: ["3.88%", "3.18 / 4.20 / 7.38", "420bp", "90%"]
  source_file: domestic/quantitative/2026-11-peak-hawk-or-2018/RESULT.md
  run_date: 2026-11-25
  valid_until: 2026-12-09
  owner: fx-115
  links_to: [fw-2026-11-25-peak-hawk-debate-not-tight-enough-camp, fw-2026-11-25-peak-hawk-debate-credit-camp]
  people: []
- id: fw-2026-11-peak-hawk-or-2018-h3-2018-analogy
  study: domestic/quantitative/2026-11-peak-hawk-or-2018
  type: quant
  region: US
  topic: equities
  hypothesis: "When the Fed raises rates while stocks are down 10% or more, a quick bottom and a rebound usually follow, as in December 2018."
  verdict: killed
  finding: "Not as a rule: a quick bottom and rebound followed only 5 of 13 such hikes, no better than usual; rebounds mostly came when the Fed reversed course."
  key_stats:
    - "quick bottom and rebound in 5 of 13 past cases"
    - "rebound in 4 of 5 cases when the Fed reversed"
    - "rebound in 1 of 8 cases when it did not"
  confidence: "60%"
  numbers: ["13 events", "5/13", "4 of 5", "1 of 8", "0.40", "0.45", "10%", "2018"]
  source_file: domestic/quantitative/2026-11-peak-hawk-or-2018/RESULT.md
  run_date: 2026-11-25
  valid_until: null
  owner: fx-115
  links_to: [fw-2026-11-25-peak-hawk-debate-2018-camp]
  people: []
- id: fw-2026-11-peak-hawk-or-2018-h4-credit-confirms
  study: domestic/quantitative/2026-11-peak-hawk-or-2018
  type: quant
  region: US
  topic: credit
  hypothesis: "Higher rates are cooling the economy through falling asset prices, and credit markets confirm the stock market's weakness."
  verdict: weak
  finding: "Only partly: stress shows up in the riskiest company bonds and AI stocks, but broad borrowing conditions remain loose and the average stock has barely fallen."
  key_stats:
    - "riskiest junk bonds widened 139bp versus safer junk bonds"
    - "typical corporate bond spread up only 13bp"
    - "equal-weight S&P up 0.8% while the main index fell 7.7%"
  confidence: "50%"
  numbers: ["+139bp", "+13bp", "+0.8%", "-7.7%", "+0.02", "-12bp"]
  source_file: domestic/quantitative/2026-11-peak-hawk-or-2018/RESULT.md
  run_date: 2026-11-25
  valid_until: 2026-12-09
  owner: fx-115
  links_to: [fw-2026-11-25-peak-hawk-debate-credit-camp]
  people: []
```

## domestic/qualitative/2026-11-25-peak-hawk-debate.md
Status: complete | Run: 2026-11-25 | Source: domestic/qualitative/2026-11-25-peak-hawk-debate.md
```yaml
- id: fw-2026-11-25-peak-hawk-debate-2018-camp
  study: domestic/qualitative/2026-11-25-peak-hawk-debate.md
  type: qual
  region: US
  topic: equities
  hypothesis: "Hiking into falling stocks rhymes with December 2018, when a sharp low and strong rebound followed once the Fed turned."
  verdict: killed
  finding: "The pattern does not hold in general: rebounds after such hikes came mainly when the Fed later reversed, and nothing yet signals one."
  key_stats:
    - "quick bottom and rebound in 5 of 13 past cases"
    - "rebound in 4 of 5 cases with a Fed reversal versus 1 of 8 without"
  confidence: null
  numbers: ["5/13", "45%", "4/5", "1/8"]
  source_file: domestic/qualitative/2026-11-25-peak-hawk-debate.md
  run_date: 2026-11-25
  valid_until: null
  owner: fx-115
  links_to: [fw-2026-11-peak-hawk-or-2018-h3-2018-analogy]
  people: []
- id: fw-2026-11-25-peak-hawk-debate-credit-camp
  study: domestic/qualitative/2026-11-25-peak-hawk-debate.md
  type: qual
  region: US
  topic: credit
  hypothesis: "Credit markets, not stocks, show whether tighter policy is working, and they show financial conditions are still loose."
  verdict: weak
  finding: "Partly backed: credit shows stress only in the riskiest bonds, while overall borrowing conditions stay loose, which fits this camp's view that policy is not yet biting."
  key_stats:
    - "riskiest junk bonds widened 139bp versus safer junk bonds"
    - "typical corporate bond spreads near their 5th percentile since 2000"
  confidence: null
  numbers: ["+139bp", "5th percentile since 2000"]
  source_file: domestic/qualitative/2026-11-25-peak-hawk-debate.md
  run_date: 2026-11-25
  valid_until: 2026-12-09
  owner: fx-115
  links_to: [fw-2026-11-peak-hawk-or-2018-h4-credit-confirms, fw-2026-11-peak-hawk-or-2018-h2-behind-curve]
  people: []
- id: fw-2026-11-25-peak-hawk-debate-peak-camp
  study: domestic/qualitative/2026-11-25-peak-hawk-debate.md
  type: qual
  region: US
  topic: fed-policy
  hypothesis: "The October minutes and recent Fed speeches mark the peak of the Fed's tough stance on rates."
  verdict: killed
  finding: "Not the peak: markets still expect less tightening than officials floated, and the minutes grew tougher rather than softer."
  key_stats:
    - "about 41bp of a possible 50bp priced by January"
    - "October minutes scored 2 points tougher than September's"
  confidence: null
  numbers: ["41bp", "50bp", "+2"]
  source_file: domestic/qualitative/2026-11-25-peak-hawk-debate.md
  run_date: 2026-11-25
  valid_until: 2026-12-08
  owner: fx-115
  links_to: [fw-2026-11-peak-hawk-or-2018-h1-peak-hawk]
  people: []
- id: fw-2026-11-25-peak-hawk-debate-not-tight-enough-camp
  study: domestic/qualitative/2026-11-25-peak-hawk-debate.md
  type: qual
  region: US
  topic: fed-policy
  hypothesis: "The Fed is still not tight enough to bring inflation down."
  verdict: inconclusive
  finding: "Unproven: standard policy rules disagree too widely to settle it, though most point to a higher rate and markets expect rates to rise."
  key_stats:
    - "90% of rule versions point above today's 3.88% rate"
    - "markets expect about 4.5% in a year"
  confidence: null
  numbers: ["3.18 / 4.20 / 7.38", "90%", "~4.5%", "3.88%"]
  source_file: domestic/qualitative/2026-11-25-peak-hawk-debate.md
  run_date: 2026-11-25
  valid_until: 2026-12-09
  owner: fx-115
  links_to: [fw-2026-11-peak-hawk-or-2018-h2-behind-curve]
  people: []
```
