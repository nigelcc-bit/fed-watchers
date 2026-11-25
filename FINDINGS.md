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
  claim: "Governor Waller's openness to a half-point hike and the October Fed minutes mark the peak of the Fed's tough stance on rates."
  verdict: killed
  confidence: "55%"
  numbers: ["40.9bp", "50bp", "+3.0", "+2"]
  source_file: domestic/quantitative/2026-11-peak-hawk-or-2018/RESULT.md
  run_date: 2026-11-25
  valid_until: 2026-12-08
  owner_bot: vera
  links_to: [fw-2026-11-25-peak-hawk-debate-peak-camp]
  people: ["Christopher J. Waller"]
- id: fw-2026-11-peak-hawk-or-2018-h2-behind-curve
  study: domestic/quantitative/2026-11-peak-hawk-or-2018
  type: quant
  region: US
  topic: fed-policy
  claim: "The Fed's policy rate is too low compared with what standard policy rules say it should be."
  verdict: inconclusive
  confidence: "55%"
  numbers: ["3.18 / 4.20 / 7.38", "420bp", "3.88%", "90%"]
  source_file: domestic/quantitative/2026-11-peak-hawk-or-2018/RESULT.md
  run_date: 2026-11-25
  valid_until: 2026-12-09
  owner_bot: vera
  links_to: [fw-2026-11-25-peak-hawk-debate-not-tight-enough-camp, fw-2026-11-25-peak-hawk-debate-credit-camp]
  people: []
- id: fw-2026-11-peak-hawk-or-2018-h3-2018-analogy
  study: domestic/quantitative/2026-11-peak-hawk-or-2018
  type: quant
  region: US
  topic: equities
  claim: "When the Fed raises rates while stocks are down 10% or more, a quick bottom and a rebound usually follow, as in December 2018."
  verdict: killed
  confidence: "60%"
  numbers: ["13 events", "5/13", "0.40", "0.45", "4 of 5", "1 of 8"]
  source_file: domestic/quantitative/2026-11-peak-hawk-or-2018/RESULT.md
  run_date: 2026-11-25
  valid_until: null
  owner_bot: vera
  links_to: [fw-2026-11-25-peak-hawk-debate-2018-camp]
  people: []
- id: fw-2026-11-peak-hawk-or-2018-h4-credit-confirms
  study: domestic/quantitative/2026-11-peak-hawk-or-2018
  type: quant
  region: US
  topic: credit
  claim: "Higher rates are cooling the economy through falling asset prices, and credit markets confirm the stock market's weakness."
  verdict: weak
  confidence: "50%"
  numbers: ["+139bp", "+13bp", "+0.02", "-12bp", "+0.8%", "-7.7%"]
  source_file: domestic/quantitative/2026-11-peak-hawk-or-2018/RESULT.md
  run_date: 2026-11-25
  valid_until: 2026-12-09
  owner_bot: vera
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
  claim: "One camp argued that hiking into falling stocks rhymes with December 2018, when a sharp low and strong rebound followed once the Fed turned."
  verdict: killed
  confidence: null
  numbers: ["5/13", "45%", "4/5", "1/8"]
  source_file: domestic/qualitative/2026-11-25-peak-hawk-debate.md
  run_date: 2026-11-25
  valid_until: null
  owner_bot: vera
  links_to: [fw-2026-11-peak-hawk-or-2018-h3-2018-analogy]
  people: []
- id: fw-2026-11-25-peak-hawk-debate-credit-camp
  study: domestic/qualitative/2026-11-25-peak-hawk-debate.md
  type: qual
  region: US
  topic: credit
  claim: "One camp argued that credit markets are the real signal and the Fed should keep working through asset prices rather than rescue stocks early."
  verdict: weak
  confidence: null
  numbers: ["+139bp", "5th percentile since 2000"]
  source_file: domestic/qualitative/2026-11-25-peak-hawk-debate.md
  run_date: 2026-11-25
  valid_until: 2026-12-09
  owner_bot: vera
  links_to: [fw-2026-11-peak-hawk-or-2018-h4-credit-confirms, fw-2026-11-peak-hawk-or-2018-h2-behind-curve]
  people: []
- id: fw-2026-11-25-peak-hawk-debate-peak-camp
  study: domestic/qualitative/2026-11-25-peak-hawk-debate.md
  type: qual
  region: US
  topic: fed-policy
  claim: "One camp argued that the October minutes and recent Fed speeches mark the peak of the Fed's tough stance on rates."
  verdict: killed
  confidence: null
  numbers: ["41bp", "50bp", "+2"]
  source_file: domestic/qualitative/2026-11-25-peak-hawk-debate.md
  run_date: 2026-11-25
  valid_until: 2026-12-08
  owner_bot: vera
  links_to: [fw-2026-11-peak-hawk-or-2018-h1-peak-hawk]
  people: []
- id: fw-2026-11-25-peak-hawk-debate-not-tight-enough-camp
  study: domestic/qualitative/2026-11-25-peak-hawk-debate.md
  type: qual
  region: US
  topic: fed-policy
  claim: "One camp argued that the bigger risk is the Fed still not being tight enough to bring inflation down."
  verdict: inconclusive
  confidence: null
  numbers: ["3.18 / 4.20 / 7.38", "90%", "~4.5%", "3.88%"]
  source_file: domestic/qualitative/2026-11-25-peak-hawk-debate.md
  run_date: 2026-11-25
  valid_until: 2026-12-09
  owner_bot: vera
  links_to: [fw-2026-11-peak-hawk-or-2018-h2-behind-curve]
  people: []
```
