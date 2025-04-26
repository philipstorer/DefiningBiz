
import streamlit as st
import pandas as pd

# --- Load Data ---
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    # Read the first sheet
    df = pd.read_excel(uploaded_file, sheet_name=0)

    # Business Opportunities and Differentiators
    business_opps = df.iloc[:, 0].dropna().tolist()
    differentiators = df.columns[1:].tolist()

    st.title("\U0001F4C8 Business Opportunity Fit Assessment")

    st.markdown("### ✨ Rate each opportunity against our differentiators (1 = Poor Fit, 5 = Strong Fit)")

    scores = {}

    for opp in business_opps:
        st.markdown(f"#### {opp}")
        cols = st.columns(len(differentiators))
        opp_scores = []
        for idx, diff in enumerate(differentiators):
            with cols[idx]:
                score = st.slider(f"{diff}", 1, 5, 3, key=f"{opp}-{diff}")
                opp_scores.append(score)
        scores[opp] = sum(opp_scores)

    st.markdown("---")
    st.header("\U0001F4CA Fit Scores")
    fit_df = pd.DataFrame(list(scores.items()), columns=["Business Opportunity", "Total Score"])

    for idx, row in fit_df.sort_values("Total Score", ascending=False).iterrows():
        st.metric(label=row["Business Opportunity"], value=int(row["Total Score"]))

    st.markdown("---")
    st.header("\U0001F5FA️ Ease of Entry vs Profitability")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Easier to Enter")
        st.markdown("""
        **More Profitable**
        - 🔥 Social Media Advertising
        - 🔥 Influencer Marketing
        - 🔥 Patient Ambassador Programs

        **Less Profitable**
        - 👍 Patient Marketing (DTC)
        - 👍 Peer-to-Peer Marketing
        """)

    with col2:
        st.subheader("Harder to Enter")
        st.markdown("""
        **More Profitable**
        - 🚀 SaaS AI Platform
        - 🚀 Patient Supplier Model
        - 🚀 Market Research (Patient Insights)

        **Less Profitable**
        - ⚠️ Clinical Trial Recruitment
        - ⚠️ Market Access Advocacy
        """)

    st.markdown("---")
    st.header("\U0001F4B0 Profitability Potential by Segment")

    profitability_data = {
        "Segment": [
            "SaaS AI Platform",
            "Patient Supplier (Performance-Based)",
            "Market Research (Patient Insights)",
            "Patient Ambassador Programs",
            "Social Media Advertising",
            "Influencer Marketing",
            "Patient Marketing (DTC)",
            "Peer-to-Peer Marketing",
            "Clinical Trial Recruitment",
            "Market Access Advocacy",
        ],
        "Profitability Potential": [
            "★★★★★ Very High",
            "★★★★☆ High",
            "★★★★☆ High",
            "★★★★☆ Medium-High",
            "★★★★☆ Medium-High",
            "★★★★☆ Medium-High",
            "★★★☆☆ Medium",
            "★★★☆☆ Medium",
            "★★☆☆☆ Low-Moderate",
            "★★☆☆☆ Low",
        ],
        "Why": [
            "Recurring revenue, high margins (software scales without proportional headcount), very sticky once integrated into pharma/CRO workflow.",
            "You get paid per success. If your AI finds patients efficiently, margin is enormous. Sponsors pay a lot per patient.",
            "Pharma pays a premium for insights. If you automate recruiting and analysis with AI, you make high margin per project and build reusable IP.",
            "Pharma pays well for these programs. If you run multiple programs off a centralized platform, costs stay low and profits grow.",
            "Social ad management fees are good (10–20% of spend). If you use AI to automate targeting and content optimization, margin improves.",
            "Influencer campaigns are lower overhead (no paid media costs to manage). You charge a fee to manage influencers and campaigns.",
            "Huge budgets, but competitive agency landscape. Pharma often negotiates hard on fees. Can be profitable but requires scaling multiple accounts.",
            "If you build a patient community platform, can be profitable with sponsorships and insights sales — but early stage and slower to monetize.",
            "Can be profitable, but delivery risk is high. Recruitment is expensive (patient incentives, call centers, etc.), so margin is tight unless AI really boosts efficiency.",
            "Strategic work, but budgets are smaller. Harder to scale without adding people. Hard to automate with tech. Typically modest fees compared to marketing."
        ]
    }

    profitability_df = pd.DataFrame(profitability_data)
    st.dataframe(profitability_df)

else:
    st.info("Please upload an Excel file to begin.")
