import streamlit as st
import pandas as pd

# --- Load Data ---
st.set_page_config(layout="wide")

# Cleaner font adjustments (no thicker sliders, no heavy visual breaks)
st.markdown("""
    <style>
    h4 { font-size: 1.3rem; font-weight: 600; margin-bottom: 0.5rem; }
    h5 { font-size: 1.1rem; font-weight: 500; margin-top: 1rem; margin-bottom: 1rem; }
    </style>
""", unsafe_allow_html=True)

try:
    df = pd.read_excel("Defining the business.xlsx", sheet_name=0)

    business_opps = df.iloc[:, 0].dropna().tolist()
    differentiators = df.columns[1:].tolist()

    st.title("Business Opportunity Fit Assessment")

    st.markdown("<h4>Fit Scores</h4>", unsafe_allow_html=True)
    scores = {}

    for opp in business_opps:
        scores[opp] = 0

    for idx, opp in enumerate(business_opps):
        if idx < len(df):
            for diff in differentiators:
                scores[opp] += df.loc[idx, diff]

    fit_df = pd.DataFrame(list(scores.items()), columns=["Business Opportunity", "Total Score"])

    score_placeholder = st.empty()

    def display_scores():
        sorted_df = fit_df.sort_values("Total Score", ascending=False)
        with score_placeholder.container():
            for idx, row in sorted_df.iterrows():
                st.metric(label=row["Business Opportunity"], value=int(row["Total Score"]))

    display_scores()

    st.markdown("<h4>Rate each opportunity against our differentiators (1 = Poor Fit, 5 = Strong Fit)</h4>", unsafe_allow_html=True)

    for opp in business_opps:
        st.markdown(f"<h5>{opp}</h5>", unsafe_allow_html=True)
        cols = st.columns(len(differentiators))
        opp_scores = []
        for idx, diff in enumerate(differentiators):
            with cols[idx]:
                score = st.slider(f"{diff}", 1, 5, int(df.loc[df[df.columns[0]] == opp, diff].values[0]), key=f"{opp}-{diff}", step=1)
                opp_scores.append(score)
        scores[opp] = sum(opp_scores)
        fit_df.loc[fit_df["Business Opportunity"] == opp, "Total Score"] = scores[opp]
        display_scores()

    st.markdown("<h4>Ease of Entry vs Profitability</h4>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Easier to Enter")
        st.markdown("""
        **More Profitable**
        - Social Media Advertising
        - Influencer Marketing
        - Patient Ambassador Programs

        **Less Profitable**
        - Patient Marketing (DTC)
        - Peer-to-Peer Marketing
        """)

    with col2:
        st.subheader("Harder to Enter")
        st.markdown("""
        **More Profitable**
        - SaaS AI Platform
        - Patient Supplier Model
        - Market Research (Patient Insights)

        **Less Profitable**
        - Clinical Trial Recruitment
        - Market Access Advocacy
        """)

    st.markdown("<h4>Profitability Potential by Segment</h4>", unsafe_allow_html=True)

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
            "Very High",
            "High",
            "High",
            "Medium-High",
            "Medium-High",
            "Medium-High",
            "Medium",
            "Medium",
            "Low-Moderate",
            "Low",
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
    st.dataframe(profitability_df, use_container_width=True)

    st.markdown("<h4>Segment Ease of Entry and Challenges</h4>", unsafe_allow_html=True)

    challenges_data = {
        "Segment": [
            "Patient Marketing (DTC)",
            "Social Media Advertising",
            "Influencer Marketing",
            "Patient Ambassador Programs",
            "Peer-to-Peer Marketing",
            "Market Research (Patient Insights)",
            "Patient Supplier (Performance-Based)",
            "Clinical Trial Recruitment",
            "Market Access Advocacy",
            "SaaS AI Platform",
        ],
        "Ease of Entry": [
            "Easy to Moderate",
            "Easy",
            "Easy",
            "Moderate",
            "Moderate",
            "Moderate",
            "Moderate",
            "Harder",
            "Harder",
            "Hardest",
        ],
        "Why": [
            "Huge spend, constant demand, pharma already outsources marketing, digital patient targeting is hot, and agencies are always looking for partners/tools to differentiate.",
            "Pharma knows they need better social media engagement but many agencies are weak at patient targeting; offering AI targeting and patient-first creative will be welcomed.",
            "Fast-growing area, pharma is just starting to use patient and physician influencers, very few companies are specialized here. Low competition compared to other segments.",
            "Pharma is expanding ambassador programs, but few vendors are truly specialized. If you combine tech (matching, tracking) and human support, you have a unique offer.",
            "Growing interest in community-based patient engagement; pharma values organic reach. Less structured RFPs mean easier to innovate.",
            "Pharma always needs patient insights, and the move toward patient-centered research is strong. If you can recruit fast and analyze smartly (AI), you have an edge.",
            "Sponsors LOVE pay-per-patient models. Huge upside if you can deliver patients — big pharma trials and support programs desperately need new sources.",
            "Big need, growing budgets, AI is attractive — but pharma CROs are conservative and trial recruitment is highly regulated and competitive.",
            "Pharma cares about patient voices in market access, but these budgets are smaller and advocacy groups already have pharma relationships.",
            "Massive long-term opportunity, recurring revenue potential, and huge scalability if successful. But hard to land first few customers because pharma is slow to buy pure SaaS without proof."
        ],
        "Challenges": [
            "Need relationships with brand teams or agencies. Compliance and medical/legal approval can slow campaign launch times.",
            "Pharma is cautious about public posts (regulatory fears), so approvals can slow down execution.",
            "Heavy compliance burden: training influencers to follow FDA rules, and close oversight required.",
            "Requires recruiting/training ambassadors; pharma will expect strong compliance and reporting.",
            "Hard to measure direct ROI at first; pharma buyers need education about how to fund/measure it.",
            "Competitive space (many research firms exist); pharma likes trusted partners so it can take time to win first contracts.",
            "Risky: if you can't find enough patients affordably, you lose money.",
            "Sponsors often have preferred vendors (e.g., CROs), slow contracting cycles, strict patient privacy/data rules.",
            "Need deep expertise in policy/advocacy, and trust with patient groups, which takes time to build.",
            "High cost to build, long sales cycles, pilots required, pharma prefers known brands for critical software tools."
        ]
    }

    challenges_df = pd.DataFrame(challenges_data)
    st.dataframe(challenges_df, use_container_width=True)

except FileNotFoundError:
    st.error("Excel file 'Defining the business.xlsx' not found. Please make sure it's uploaded with the app.")
