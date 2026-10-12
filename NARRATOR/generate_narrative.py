import os
import json
import re

def generate_scr_narrative_offline(findings: dict) -> dict:
    cleaned_rev = findings["cleaned_total_revenue_inr"]
    cod_rate = findings["return_rate_by_payment"]["COD"]
    risk_rate = findings["highest_risk_segment"]["return_rate_pct"]
    recon_delta = findings["duplicate_reconciliation_delta_inr"]
    peak_rev = findings["true_peak_month"]["revenue_inr"]

    narrative_text = f"""
### Situation
Mamaearth generated a cleaned total revenue of INR {cleaned_rev:,.2f} across validated sales orders.

### Complication
High order returns are significantly eroding operating margins. The Cash on Delivery (COD) payment method exhibits a return rate of {cod_rate}%. The highest-risk segment is concentrated in Tier-2 COD orders at {risk_rate}%. A duplicate-driven reconciliation delta of INR {recon_delta:,.2f} was identified and resolved.

### Resolution
Excluding bulk quantity outliers reveals March as the true peak month generating INR {peak_rev:,.2f} in clean revenue.
""".strip()

    return {
        "status": "success",
        "narrative": narrative_text,
        "tokens": None,
        "mode": "offline"
    }

def generate_scr_narrative(findings: dict) -> dict:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return generate_scr_narrative_offline(findings)

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)
        system_instruction = "You are a senior data analyst writing for Mamaearth's regional ops and finance heads."
        user_prompt = f"Write an executive SCR business narrative based on these exact verified findings:\n{json.dumps(findings, indent=2)}"

        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.0,
            max_output_tokens=500
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_prompt,
            config=config
        )

        return {
            "status": "success",
            "narrative": response.text,
            "tokens": getattr(response.usage_metadata, "total_token_count", None),
            "mode": "online"
        }
    except Exception as err:
        return generate_scr_narrative_offline(findings)

if __name__ == "__main__":
    with open("narrator/findings.json", "r") as f:
        findings = json.load(f)

    result = generate_scr_narrative(findings)
    print(result["narrative"])

    with open("narrator/sample_output.txt", "w") as f:
        f.write(result["narrative"])
