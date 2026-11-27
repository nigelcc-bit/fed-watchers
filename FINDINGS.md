# Findings: fed-watchers
Last updated: 2026-11-27

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

## quick-lookups/2026-11-27-token-pricing
Status: complete | Run: 2026-11-27 | Source: quick-lookups/2026-11-27-token-pricing/RESULT.md
```yaml
- id: fw-2026-11-27-token-pricing-crack
  study: quick-lookups/2026-11-27-token-pricing
  type: quant
  region: US
  topic: ai-pricing
  hypothesis: "Falling AI token prices are a crack in the AI revenue thesis: spending is not keeping up as prices fall."
  verdict: killed
  finding: "Not yet: business spending on AI tokens kept rising even as prices fell, but the cushion is thinning and the result depends on how new models are counted."
  key_stats:
    - "token prices down 43% over the latest 13 weeks"
    - "token spend up 20% over the same 13 weeks"
  confidence: "45%"
  numbers: ["-43%", "+20%", "+108%", "1.33", "13 weeks"]
  source_file: quick-lookups/2026-11-27-token-pricing/RESULT.md
  run_date: 2026-11-27
  valid_until: 2026-12-15
  owner: fx-115
  links_to: [fw-2026-11-27-token-pricing-anthropic-elasticity, fw-2026-11-27-token-pricing-mix]
  people: []
- id: fw-2026-11-27-token-pricing-anthropic-elasticity
  study: quick-lookups/2026-11-27-token-pricing
  type: quant
  region: US
  topic: ai-pricing
  hypothesis: "Spending on Anthropic's models still rises faster than its token prices fall."
  verdict: weak
  finding: "Only just: Anthropic's spend grew 5.9% over 13 weeks while its prices fell, and the margin has shrunk every week for two months."
  key_stats:
    - "Anthropic token spend up 5.9% over 13 weeks"
    - "Anthropic price-sensitivity reading of 1.10, close to the tipping point"
  confidence: null
  numbers: ["+5.9%", "1.10", "13 weeks"]
  source_file: quick-lookups/2026-11-27-token-pricing/RESULT.md
  run_date: 2026-11-27
  valid_until: 2026-12-15
  owner: fx-115
  links_to: [fw-2026-11-27-token-pricing-crack]
  people: []
- id: fw-2026-11-27-token-pricing-mix
  study: quick-lookups/2026-11-27-token-pricing
  type: quant
  region: US
  topic: ai-pricing
  hypothesis: "Average token prices fell mostly because customers switched to cheaper models, not because prices were cut."
  verdict: weak
  finding: "It depends on definitions: the same model versions did not get cheaper, but newer versions in each tier cost far less, so tier for tier prices fell 65%."
  key_stats:
    - "same-version prices up 2% since the March peak"
    - "tier-for-tier prices down 65% since the March peak"
  confidence: null
  numbers: ["+2%", "-65%", "102%", "87%"]
  source_file: quick-lookups/2026-11-27-token-pricing/RESULT.md
  run_date: 2026-11-27
  valid_until: null
  owner: fx-115
  links_to: [fw-2026-11-27-token-pricing-crack]
  people: []
- id: fw-2026-11-27-token-pricing-share-vs-price
  study: quick-lookups/2026-11-27-token-pricing
  type: quant
  region: US
  topic: ai-pricing
  hypothesis: "Anthropic's share of business AI token spend does not respond to its price relative to OpenAI."
  verdict: weak
  finding: "Not settled: Anthropic's share tends to slip when it gets relatively pricier, but with an effective sample of 5.8 data points the link is not firm."
  key_stats:
    - "effective sample of only 5.8 independent data points"
  confidence: null
  numbers: ["5.8", "-13.4pp", "0.093"]
  source_file: quick-lookups/2026-11-27-token-pricing/RESULT.md
  run_date: 2026-11-27
  valid_until: null
  owner: fx-115
  links_to: []
  people: []
- id: fw-2026-11-27-token-pricing-revenue-per-compute
  study: quick-lookups/2026-11-27-token-pricing
  type: quant
  region: US
  topic: ai-pricing
  hypothesis: "Anthropic earns less revenue per dollar of compute than it did at the start of 2026."
  verdict: killed
  finding: "Not compared with the start of 2026, but revenue per compute dollar fell 17% in the latest quarter after peaking in the spring."
  key_stats:
    - "revenue per compute dollar of 1.40 in Q1 2026, 2.08 in Q2 and 1.72 in Q3"
    - "price cuts worth $600M, about 11.1% of the latest quarter's revenue growth"
  confidence: null
  numbers: ["1.40", "2.08", "1.72", "-17%", "Q1 2026", "(Q2)", "(Q3)", "$600M", "11.1%"]
  source_file: quick-lookups/2026-11-27-token-pricing/RESULT.md
  run_date: 2026-11-27
  valid_until: null
  owner: fx-115
  links_to: [fw-2026-11-27-token-pricing-crack]
  people: []
```
