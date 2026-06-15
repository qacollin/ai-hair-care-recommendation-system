import streamlit as st
import openai

# ======================
# PAGE CONFIG
# ======================
st.set_page_config(
    page_title="AI Hair Care System",
    page_icon="💇🏽‍♀️",
    layout="wide"
)

st.title("💇🏽‍♀️ AI Hair Care Recommendation System")
st.subheader("Decision Support System Prototype - v4.0")

# ======================
# API KEY
# ======================
api_key = "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"

# ======================
# USER INPUT SECTION — LONGER QUESTIONNAIRE
# ======================
st.header("Hair Assessment Survey")

col1, col2 = st.columns(2)

with col1:
    hair_type = st.selectbox(
        "What is your hair type?",
        ["Straight", "Wavy", "Curly", "Coily"]
    )
    scalp_condition = st.selectbox(
        "How would you describe your scalp?",
        ["Dry", "Oily", "Normal", "Sensitive"]
    )
    porosity = st.selectbox(
        "What is your hair porosity?",
        ["Low", "Medium", "High"]
    )
    hair_length = st.selectbox(
        "What is your current hair length?",
        ["Short (ear length or above)", "Medium (shoulder length)", "Long (past shoulder)", "Very Long (past chest)"]
    )
    wash_frequency = st.selectbox(
        "How often do you wash your hair?",
        ["Daily", "Every 2-3 days", "Once a week", "Every 2 weeks or less"]
    )

with col2:
    density = st.selectbox(
        "What is your hair density?",
        ["Fine", "Medium", "Thick"]
    )
    heat_usage = st.selectbox(
        "How often do you use heat styling tools?",
        ["Never", "Sometimes", "Often"]
    )
    chemical_treatments = st.selectbox(
        "Do you use chemical treatments (relaxer, color, etc.)?",
        ["No", "Occasionally", "Frequently"]
    )
    damage_level = st.selectbox(
        "How would you rate your current damage level?",
        ["None", "Low", "Moderate", "High"]
    )
    environment = st.selectbox(
        "What type of environment do you live in?",
        ["Humid", "Dry", "Cold", "Mixed/Moderate"]
    )

hair_goal = st.selectbox(
    "What is your main hair goal?",
    ["Hair growth", "Moisture", "Damage repair", "Frizz control", "Scalp health", "Length retention", "Strengthen hair"]
)

styling_habits = st.selectbox(
    "What is your most common styling method?",
    ["Protective styles (braids, twists, wigs)", "Heat styling (flat iron, blow dryer)", "Air dry / wash and go", "Roller sets / flexi rods", "No particular style"]
)

diet_water = st.selectbox(
    "How would you describe your water intake and diet?",
    ["Healthy diet, drink plenty of water", "Average diet, moderate water", "Poor diet, low water intake", "Prefer not to say"]
)

user_description = st.text_area(
    "Tell us more about your hair (optional):",
    placeholder="Example: My hair breaks easily at the ends and I want it longer..."
)

# ======================
# MINI BRAIN v2.0 — Original (kept exactly)
# ======================
def detect_hair_issues(scalp, heat, chemical, porosity, density):
    """Original v2.0 Mini Brain - kept exactly as written"""
    issues = []
    confidence = 70

    if scalp == "Dry":
        issues.append("Dry Scalp")
        confidence += 10
    if scalp == "Oily":
        issues.append("Oily Scalp")
        confidence += 10
    if heat == "Often":
        issues.append("Heat Damage")
        confidence += 15
    if chemical == "Frequently":
        issues.append("Chemical Damage")
        confidence += 15
    if porosity == "Low":
        issues.append("Low Porosity")
        confidence += 10
    if density == "Fine":
        issues.append("Fine Hair")
        confidence += 8

    confidence = min(confidence, 95)
    issues_str = ", ".join(issues) if issues else "No major issues detected"
    return issues_str, confidence


# ======================
# MINI BRAIN v3/v4 — Enhanced
# ======================
def run_mini_brain(scalp, heat, chemical, porosity, density, hair_type, goal, damage, environment):
    issues = []
    confidence = 70
    simple_score = 0

    if scalp == "Dry":
        issues.append("Dry Scalp")
        confidence += 10
        simple_score += 2
    elif scalp == "Oily":
        issues.append("Oily Scalp / Product Buildup Risk")
        confidence += 10
        simple_score += 1
    elif scalp == "Sensitive":
        issues.append("Scalp Sensitivity")
        confidence += 6
        simple_score += 1

    if heat == "Often":
        issues.append("Heat Damage Risk")
        confidence += 15
        simple_score += 3
    elif heat == "Sometimes":
        issues.append("Moderate Heat Exposure")
        confidence += 5
        simple_score += 1

    if chemical == "Frequently":
        issues.append("Chemical Damage")
        confidence += 15
        simple_score += 3
    elif chemical == "Occasionally":
        issues.append("Mild Chemical Processing")
        confidence += 8
        simple_score += 1

    if porosity == "Low":
        issues.append("Low Porosity — Product Buildup Prone")
        confidence += 10
        simple_score += 1
    elif porosity == "High":
        issues.append("High Porosity — Moisture Loss Risk")
        confidence += 10
        simple_score += 2

    if density == "Fine":
        issues.append("Fine Hair — Prone to Breakage")
        confidence += 8
        simple_score += 1

    if damage == "High":
        issues.append("High Damage Level (user-reported)")
        confidence += 10
        simple_score += 3
    elif damage == "Moderate":
        issues.append("Moderate Damage Level (user-reported)")
        confidence += 5
        simple_score += 2
    elif damage == "Low":
        issues.append("Low Damage Level (user-reported)")
        simple_score += 1

    if environment == "Dry":
        issues.append("Dry Climate — Increased Moisture Loss")
        simple_score += 1
    elif environment == "Humid":
        issues.append("Humid Climate — Frizz Risk")
        simple_score += 1

    if goal == "Damage repair":
        issues.append("Existing Damage (user-reported goal)")
        simple_score += 2
    elif goal == "Length retention":
        issues.append("Length Retention Goal — Breakage prevention needed")
        simple_score += 1

    # Combined flags
    if scalp == "Dry" and heat == "Often":
        issues.append("⚠️ HIGH DAMAGE RISK: Dry scalp + frequent heat")
        confidence += 5
        simple_score += 2
    if chemical == "Frequently" and porosity == "High":
        issues.append("⚠️ SEVERE DAMAGE: Chemical overprocessing + high porosity")
        confidence += 5
        simple_score += 2
    if scalp == "Oily" and chemical == "Frequently":
        issues.append("⚠️ Scalp imbalance: Oily scalp + chemical treatments")
        confidence += 3
        simple_score += 1
    if damage == "High" and heat == "Often":
        issues.append("⚠️ CRITICAL: High damage + frequent heat use")
        confidence += 5
        simple_score += 2

    confidence = min(confidence, 95)

    # Hair Profile Scores
    moisture = 80
    if scalp == "Dry": moisture -= 25
    if porosity == "High": moisture -= 20
    if heat == "Often": moisture -= 15
    if porosity == "Low": moisture -= 5
    if environment == "Dry": moisture -= 10
    moisture = max(moisture, 5)

    damage_score = 0
    if heat == "Often": damage_score += 30
    if heat == "Sometimes": damage_score += 15
    if chemical == "Frequently": damage_score += 30
    if chemical == "Occasionally": damage_score += 15
    if porosity == "High": damage_score += 10
    if damage == "High": damage_score += 20
    if damage == "Moderate": damage_score += 10
    damage_score = min(damage_score, 100)

    scalp_health = 85
    if scalp == "Dry": scalp_health -= 30
    if scalp == "Oily": scalp_health -= 20
    if scalp == "Sensitive": scalp_health -= 15
    if chemical == "Frequently": scalp_health -= 15
    scalp_health = max(scalp_health, 5)

    breakage = 0
    if density == "Fine": breakage += 30
    if porosity == "High": breakage += 25
    if chemical == "Frequently": breakage += 25
    if heat == "Often": breakage += 20
    if damage == "High": breakage += 15
    breakage = min(breakage, 100)

    hair_profile = {
        "Moisture Level": moisture,
        "Damage Level": damage_score,
        "Scalp Health": scalp_health,
        "Breakage Risk": breakage
    }

    issues_str = ", ".join(issues) if issues else "No major issues detected"
    return issues, issues_str, confidence, simple_score, hair_profile


# ======================
# HAIR PROFILE DASHBOARD
# ======================
def display_hair_profile(profile):
    st.subheader("📊 Hair Profile Score Dashboard")
    st.caption("Generated by Mini Brain rule-based analysis — before AI processing")

    col1, col2, col3, col4 = st.columns(4)
    cols = [col1, col2, col3, col4]

    icons = {
        "Moisture Level": ("🟦", "Higher = better"),
        "Damage Level":   ("🟥", "Lower = better"),
        "Scalp Health":   ("🟩", "Higher = better"),
        "Breakage Risk":  ("🟧", "Lower = better"),
    }

    for col, (label, value) in zip(cols, profile.items()):
        icon, note = icons[label]
        with col:
            st.metric(label=f"{icon} {label}", value=f"{value}/100")
            st.progress(value / 100)
            st.caption(note)


# ======================
# STRUCTURED OUTPUT — matches screenshot format exactly
# ======================
def display_structured_output(recommendation_text):
    sections = [
        ("1. Recommended Shampoo Type",        "🧴 1. Recommended Shampoo Type"),
        ("2. Recommended Conditioner Type",    "💧 2. Recommended Conditioner Type"),
        ("3. Recommended Treatment",           "✨ 3. Recommended Treatment"),
        ("4. Suggested Weekly Routine",        "🗓️ 4. Suggested Weekly Routine"),
        ("5. Explanation for Recommendations", "💡 5. Explanation for Recommendations"),
    ]

    text = recommendation_text
    extracted = {}

    for i, (key, _) in enumerate(sections):
        if key in text:
            after = text.split(key, 1)[1]
            end = len(after)
            for j, (next_key, _) in enumerate(sections):
                if j != i and next_key in after:
                    idx = after.find(next_key)
                    if idx < end:
                        end = idx
            extracted[key] = after[:end].strip()

    if not extracted:
        st.write(recommendation_text)
        return

    for key, display_title in sections:
        if key in extracted:
            with st.expander(display_title, expanded=True):
                st.write(extracted[key])


# ======================
# MAIN BUTTON
# ======================
if st.button("Get Recommendation"):

    detected_issues_simple, confidence_simple = detect_hair_issues(
        scalp_condition, heat_usage, chemical_treatments, porosity, density
    )

    issues_list, issues_str, confidence, simple_score, hair_profile = run_mini_brain(
        scalp_condition, heat_usage, chemical_treatments,
        porosity, density, hair_type, hair_goal, damage_level, environment
    )

    st.header("Your Personalized Recommendation")

    # Hair Profile Dashboard
    display_hair_profile(hair_profile)
    st.divider()

    # Hair Health Score
    st.subheader("📊 Hair Health Score")
    st.write(f"**Score: {simple_score}** — Higher = more damage/attention needed")
    if simple_score >= 8:
        st.error("🔴 High attention needed — strong recommendation confidence")
    elif simple_score >= 4:
        st.warning("🟡 Moderate condition — balanced recommendations")
    else:
        st.success("🟢 Low concern — maintenance advice")
    st.divider()

    # Detected Issues (v2 style)
    st.subheader("🧠 Detected Issues")
    st.write(detected_issues_simple)
    st.divider()

    # Detected Issues (v3 style - cards)
    st.subheader("🧠 Mini Brain — Detailed Issue Breakdown")
    st.caption("Rule-based analysis completed before AI processing")
    if issues_list:
        for issue in issues_list:
            if "⚠️" in issue:
                st.error(issue)
            else:
                st.warning(f"⚠️ {issue}")
    else:
        st.success("✅ No major issues detected")
    st.divider()

    # Build Prompt
    prompt = f"""
You are a professional licensed trichologist and hair care expert with 15+ years of experience.

User Profile:
- Hair Type: {hair_type}
- Scalp Condition: {scalp_condition}
- Porosity: {porosity}
- Density: {density}
- Hair Length: {hair_length}
- Damage Level: {damage_level}
- Main Goal: {hair_goal}
- Heat Styling: {heat_usage}
- Chemical Treatments: {chemical_treatments}
- Wash Frequency: {wash_frequency}
- Styling Habits: {styling_habits}
- Environment: {environment}
- Diet & Water Intake: {diet_water}
- Extra Info: {user_description if user_description else "None provided"}

System Detected Issues: {issues_str}
Hair Health Score: {simple_score} (higher = more damage/attention needed)
Confidence Level: {confidence}%

Provide a clear, professional, and friendly recommendation using EXACTLY these numbered sections with these exact titles:

1. Recommended Shampoo Type:
(Name the shampoo type, give it a label like "Hydrating Shampoo", then explain what ingredients to look for and why it suits this user.)

2. Recommended Conditioner Type:
(Name the conditioner type, give it a label, then explain what ingredients to look for and why it suits this user.)

3. Recommended Treatment:
(Name the treatment type, give it a label like "Protein Moisture Treatment", then explain why it helps this user's hair.)

4. Suggested Weekly Routine:
(Give a day-by-day breakdown exactly like this:
- Day 1: [steps]
- Day 2: [steps]
- Day 3: [steps]
- Day 4: [steps]
- Day 5: [steps]
- Day 6/7: [steps])

5. Explanation for Recommendations:
(Break the explanation into these sub-sections:
Hair Type: [hair type] — explain why recommendations fit
Scalp Condition: [condition] — explain why recommendations fit
Damage Level: [level] — explain why recommendations fit
Goal: [goal] — explain why recommendations fit
End with a summary sentence.)

Keep each section clearly labeled with the number and title exactly as shown above.
"""

    # OpenAI Call
    client = openai.OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    recommendation = response.choices[0].message.content

    # Display Output
    st.subheader("💡 AI Recommendation")
    display_structured_output(recommendation)
    st.divider()

    # Confidence Display (v2.0 style)
    st.progress(confidence / 100)
    st.caption(f"**System Confidence Level:** {confidence}%")

    # Confidence Level text
    st.subheader("🔍 Confidence Level")
    if simple_score >= 8:
        st.write("High attention needed → Strong recommendation confidence")
    elif simple_score >= 4:
        st.write("Moderate condition → Balanced recommendations")
    else:
        st.write("Low concern → Maintenance advice")
    st.divider()

    # Feedback
    st.subheader("Was this recommendation helpful?")
    rating = st.slider("Rate this recommendation (1 = Not helpful, 5 = Excellent)", 1, 5, 4)

    if st.button("Submit Feedback"):
        st.success("✅ Thank you for your feedback! This helps improve the system.")

# ======================
# SIDEBAR
# ======================
st.sidebar.title("System Architecture")
st.sidebar.write("""
This prototype demonstrates a **Decision Support System**.

Process:
1️⃣ User answers hair care survey
2️⃣ Streamlit collects inputs
3️⃣ Mini Brain v2.0 detects basic issues
4️⃣ Enhanced Mini Brain calculates weighted scores
5️⃣ Combined condition flags are triggered
6️⃣ Hair Profile Score Dashboard is generated
7️⃣ Hair Health Score (simple number) is calculated
8️⃣ Python builds a structured AI prompt
9️⃣ OpenAI model analyzes hair characteristics
🔟 AI generates personalized recommendations
1️⃣1️⃣ Results displayed in structured sections
1️⃣2️⃣ User rates recommendation (feedback loop)

This demonstrates how AI can support
personalized beauty and wellness decisions.
""")

st.sidebar.title("System Features")
st.sidebar.write("""
**v4.0 — All Features Combined:**
- Expanded questionnaire (13 questions)
- Hair Profile Score Dashboard
- Hair Health Score (simple number)
- Mini Brain with Confidence Score
- Enhanced Mini Brain (weighted + combined flags)
- Structured Output (5 clear sections)
- Day-by-day Weekly Routine
- Explanation broken down by hair factor
- User Feedback Loop
- Improved Prompt Engineering
""")

st.sidebar.info("This is a hybrid Decision Support System (Rules + AI)")
