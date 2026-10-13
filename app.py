import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Role-based Creative Chatbot", page_icon="🎭", layout="wide")

ROLES = {
    "🎥 Video Director": {
        "system": (
            "You are an experienced film director. Answer with concrete advice on "
            "shot composition, camera movement, lighting, editing rhythm, and "
            "storytelling. Suggest specific shots or scene ideas."
        ),
        "hint": "Think like a director: plan the shots, framing, and mood of a film scene.",
        "placeholder": "e.g., How can I shoot a suspenseful chase scene?",
    },
    "💃 Dance Instructor": {
        "system": (
            "You are a professional dance instructor and choreographer. Answer with "
            "practical guidance on movement, rhythm, body expression, and "
            "choreography. Describe movements step by step."
        ),
        "hint": "Think like a choreographer: express emotion through the body.",
        "placeholder": "e.g., How can I express sadness in movement?",
    },
    "👗 Fashion Stylist": {
        "system": (
            "You are a creative fashion stylist. Answer with ideas about outfits, "
            "color palettes, textures, silhouettes, and styling that fit the "
            "mood or concept described."
        ),
        "hint": "Think like a stylist: let clothing and color tell the story.",
        "placeholder": "e.g., What outfit conveys quiet confidence?",
    },
    "🎭 Acting Coach": {
        "system": (
            "You are an acting coach. Answer with practical techniques for emotion, "
            "voice, gesture, character building, and scene work. Offer short "
            "exercises the actor can try."
        ),
        "hint": "Think like a coach: build a believable character and emotion.",
        "placeholder": "e.g., How do I play a character hiding grief?",
    },
    "🎨 Art Curator": {
        "system": (
            "You are an art curator. Answer with insights on themes, visual "
            "language, art history, and exhibition concepts. Connect ideas to "
            "relevant artists or movements."
        ),
        "hint": "Think like a curator: connect ideas to art and context.",
        "placeholder": "e.g., How would you curate an exhibition about memory?",
    },
}

with st.sidebar:
    st.subheader("🔑 API & Role Settings")
    api_key = st.text_input("Enter your OpenAI API Key:", type="password", placeholder="sk-xxxxxxxxxxxxxxxxx")
    role_name = st.selectbox("Choose a role:", list(ROLES.keys()))
    st.info(ROLES[role_name]["hint"])
    model = st.selectbox("Model:", ["gpt-4o-mini", "gpt-4o"], index=0)
    
    st.divider()
    st.subheader(f"🛠️ {role_name.split()[1]} Custom Options")

    # --- 각 모드별 개성 있는 사이드바 툴바 옵션 ---
    if role_name == "🎥 Video Director":
        sub_option_1 = st.selectbox("Genre Focus:", ["Sci-Fi / Thriller", "Romance / Drama", "Action / Dynamic", "Artistic / Indie"])
        sub_option_2 = st.selectbox("Lighting Tone:", ["High-Key (Bright & Clean)", "Low-Key (Dark & Moody)", "Neon / Cyberpunk"])
    elif role_name == "💃 Dance Instructor":
        sub_option_1 = st.selectbox("Dance Genre:", ["Contemporary", "Hip-hop / Street", "K-pop Choreography", "Modern Expressive"])
        sub_option_2 = st.selectbox("Energy Level:", ["High & Powerful", "Fluid & Soft", "Sharp & Precise"])
    elif role_name == "👗 Fashion Stylist":
        sub_option_1 = st.selectbox("Occasion (TPO):", ["Daily Casual", "Business Formal", "Wedding Guest", "Date Night", "Creative Interview"])
        sub_option_2 = st.selectbox("Style Mood:", ["Minimal & Clean", "Bold & Trendy", "Vintage & Classic", "Comfortable & Cozy"])
    elif role_name == "🎭 Acting Coach":
        sub_option_1 = st.selectbox("Method Focus:", ["Stanislavski (Inner Emotion)", "Meisner (Reaction & Impulse)", "Physical Theatre"])
        sub_option_2 = st.selectbox("Scene Intensity:", ["Subtle & Quiet", "Intense & Emotional", "Comedic & Witty"])
    elif role_name == "🎨 Art Curator":
        sub_option_1 = st.selectbox("Art Movement:", ["Contemporary Art", "Impressionism", "Minimalism / Conceptual", "Surrealism"])
        sub_option_2 = st.selectbox("Exhibition Vibe:", ["Contemplative & Quiet", "Vibrant & Provocative", "Historical & Archive"])

    creativity_level = st.slider(
        "AI Creativity (Temperature):", 
        min_value=0.1, max_value=1.5, value=0.8, step=0.1
    )

st.title("🎭 Role-based Creative Chatbot")
st.write("Select a creative role and customize your project parameters!")

question = st.text_area(
    "💬 Enter your question or idea:",
    placeholder=ROLES[role_name]["placeholder"],
)

if st.button("Generate Response"):
    if not api_key:
        st.warning("Please enter your OpenAI API key in the sidebar.")
    elif not question.strip():
        st.warning("Please enter a question or idea.")
    else:
        try:
            client = OpenAI(api_key=api_key)
            
            # 선택한 옵션들을 시스템 프롬프트에 동적으로 결합
            system_prompt = ROLES[role_name]["system"]
            system_prompt += f" Tailor your expert advice reflecting these specific conditions: [Focus/Genre: {sub_option_1}], [Tone/Mood: {sub_option_2}]."

            with st.spinner("Generating creative insights..."):
                resp = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": question},
                    ],
                    temperature=creativity_level,
                )
            
            # --- 결과물 시각적 장식 (모드별 맞춤 카드 UI) ---
            st.divider()
            
            if role_name == "🎥 Video Director":
                st.markdown(f"### 🎬 Director's Scene Breakdown: `{sub_option_1}`")
                st.info(f"💡 **Applied Lighting & Mood**: {sub_option_2}")
            elif role_name == "💃 Dance Instructor":
                st.markdown(f"### 🩰 Choreography Note: `{sub_option_1}`")
                st.info(f"💡 **Execution Energy**: {sub_option_2}")
            elif role_name == "👗 Fashion Stylist":
                st.markdown(f"### 🛍️ Editorial Lookbook: `{sub_option_1}`")
                st.info(f"💡 **Selected Mood**: {sub_option_2}")
            elif role_name == "🎭 Acting Coach":
                st.markdown(f"### 🎭 Character & Method Lab: `{sub_option_1}`")
                st.info(f"💡 **Scene Intensity**: {sub_option_2}")
            elif role_name == "🎨 Art Curator":
                st.markdown(f"### 🖼️ Curatorial Vision: `{sub_option_1}`")
                st.info(f"💡 **Exhibition Vibe**: {sub_option_2}")

            # AI 응답 출력 영역
            st.write(resp.choices[0].message.content)
            
        except Exception as e:
            st.error(f"Error: {e}")

st.divider()
st.caption("Built for 'Art & Advanced Big Data' • Prof. Jahwan Koo (SKKU)")
