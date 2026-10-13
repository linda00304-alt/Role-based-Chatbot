import streamlit as st
from anthropic import Anthropic

st.set_page_config(page_title="Role-based Creative Chatbot (Claude)", page_icon="🎭", layout="wide")

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
    st.subheader("🔑 Anthropic API & Role Settings")
    api_key = st.text_input("Enter your Anthropic API Key:", type="password", placeholder="sk-ant-xxxxxxxxxxxxxxxxx")
    role_name = st.selectbox("Choose a role:", list(ROLES.keys()))
    st.info(ROLES[role_name]["hint"])
    
    # Claude 모델 선택 (claude-3-5-sonnet 또는 claude-3-opus 등)
    model = st.selectbox("Model:", ["claude-3-5-sonnet-20241022", "claude-3-haiku-20240307"], index=0)
    
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
        min_value=0.1, max_value=1.0, value=0.7, step=0.1
    )

st.title("🎭 Role-based Creative Chatbot (Claude)")
st.write("Select a creative role and customize your project parameters!")

question = st.text_area(
    "💬 Enter your question or idea:",
    placeholder=ROLES[role_name]["placeholder"],
)

if st.button("Generate Response"):
    if not api_key:
        st.warning("Please enter your Anthropic API key in the sidebar.")
    elif not question.strip():
        st.warning("Please enter a question or idea.")
    else:
        try:
            # Claude 클라이언트 초기화
            client = Anthropic(api_key=api_key)
            
            # 선택한 옵션들을 시스템 프롬프트에 동적으로 결합
            system_prompt = ROLES[role_name]["system"]
            system_prompt += f" Tailor your expert advice reflecting these specific conditions: [Focus/Genre: {sub_option_1}], [Tone/Mood: {sub_option_2}]."

            with st.spinner("Generating creative insights with Claude..."):
                # Claude API 호출 방식 적용
                message = client.messages.create(
                    model=model,
                    max_tokens=1024,
                    system=system_prompt,
                    messages=[
                        {"role": "user", "content": question}
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

            # Claude 응답 출력 영역 (content[0].text 형태로 받아옴)
            st.write(message.content[0].text)
            
        except Exception as e:
            st.error(f"Error: {e}")

st.divider()
st.caption("Built for 'Art & Advanced Big Data' • Prof. Jahwan Koo (SKKU)")
