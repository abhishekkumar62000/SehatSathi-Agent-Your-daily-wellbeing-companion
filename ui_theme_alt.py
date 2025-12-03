import streamlit as st

def inject_theme_alt():
    st.markdown(
        """
        <style>
        :root {
          --bg: #0a0a0f;
          --card: rgba(20, 20, 30, 0.6);
          --fg: #e6e6fa;
          --muted: #a3a3c7;
          --cyan: #00e5ff;
          --magenta: #ff33cc;
          --violet: #8a2be2;
          --lime: #32cd32;
        }

        @keyframes pulseBorder {
          0% { box-shadow: 0 0 0px rgba(0,229,255,0.2), 0 0 0px rgba(255,51,204,0.2); }
          50% { box-shadow: 0 0 16px rgba(0,229,255,0.35), 0 0 16px rgba(255,51,204,0.35); }
          100% { box-shadow: 0 0 0px rgba(0,229,255,0.2), 0 0 0px rgba(255,51,204,0.2); }
        }

        @keyframes scanlines {
          0% { background-position: 0 0; }
          100% { background-position: 0 100%; }
        }

        .stApp {
          background: radial-gradient(1000px 600px at 20% 0%, rgba(138,43,226,0.12), transparent),
                      radial-gradient(800px 400px at 80% 30%, rgba(0,229,255,0.12), transparent),
                      linear-gradient(#0a0a0f, #0a0a0f);
          color: var(--fg);
        }
        .stMarkdown, .stText, .stCaption, .stSubheader, .stHeader { color: var(--fg) !important; }

        /* Neon buttons */
        .stButton>button {
          background: linear-gradient(135deg, var(--cyan), var(--magenta));
          color: #0a0a0f;
          border: 1px solid rgba(255,255,255,0.08);
          border-radius: 14px;
          padding: 0.6rem 1rem;
          font-weight: 700;
          letter-spacing: 0.2px;
          animation: pulseBorder 3s infinite;
          transition: transform 0.08s ease-in-out, filter 0.15s ease;
        }
        .stButton>button:hover { transform: translateY(-1px); filter: brightness(1.08); }
        .stButton>button:active { transform: translateY(0px) scale(0.98); }

        /* Downloads */
        .stDownloadButton>button {
          background: linear-gradient(135deg, var(--violet), var(--lime));
          color: #0a0a0f; font-weight: 800; border-radius: 14px;
        }

        /* Cards and expanders */
        .stExpander { background: var(--card); backdrop-filter: blur(8px); border-radius: 14px; }
        .stExpander .streamlit-expanderHeader { color: var(--fg); }

        /* Inputs */
        .stSelectbox, .stSlider, .stTextInput, textarea, .stMultiselect {
          border-radius: 14px !important;
        }
        [role="slider"]{ box-shadow: 0 0 0 0 rgba(0,229,255,0.0); transition: box-shadow .2s ease; }
        [role="slider"]:hover{ box-shadow: 0 0 0 6px rgba(0,229,255,0.15); }

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
          gap: 0.5rem; background: rgba(35,35,55,0.45); padding: 0.4rem; border-radius: 14px;
        }
        .stTabs [data-baseweb="tab"] { color: var(--fg); }

        /* Fancy Section Title */
        .subheader-fancy-alt {
          margin: 0.75rem 0 0.5rem; font-size: clamp(1.1rem, 2.6vw, 1.6rem);
          font-weight: 900; letter-spacing: .2px; position: relative; display: inline-flex; gap: .5rem; align-items: center;
          background: linear-gradient(135deg, var(--cyan), var(--magenta)); -webkit-background-clip:text; background-clip:text; color: transparent;
        }
        .subheader-fancy-alt::after{
          content:""; position:absolute; left:0; right:0; bottom:-6px; height:3px;
          background: linear-gradient(90deg, var(--cyan), var(--magenta), var(--violet)); border-radius:3px; opacity:.8;
          animation: pulseBorder 3s infinite;
        }
        .subheader-emoji-alt { filter: drop-shadow(0 2px 10px rgba(0,229,255,.35)); }

        /* Divider */
        .divider-alt{ height:1px; width:100%; margin:1rem 0; border-radius:999px;
          background: linear-gradient(90deg, transparent, rgba(0,229,255,.6), rgba(255,51,204,.6), transparent); }

        /* Hero */
        .hero-alt {
          margin-top: 0.5rem;
          padding: 1rem 1.2rem;
          border-radius: 18px;
          background: linear-gradient(135deg, rgba(0,229,255,0.15), rgba(255,51,204,0.15));
          border: 1px solid rgba(255,255,255,0.1);
          position: relative;
        }
        .hero-alt::after {
          content: "";
          position: absolute; inset: 0; border-radius: 18px;
          background-image: linear-gradient(rgba(255,255,255,0.04) 1px, transparent 1px);
          background-size: 100% 6px; opacity: 0.25; pointer-events: none;
          animation: scanlines 12s linear infinite;
        }
        .hero-alt h1 {
          font-size: clamp(1.6rem, 3vw, 2.2rem);
          background: linear-gradient(135deg, var(--fg), var(--muted));
          -webkit-background-clip: text; background-clip: text; color: transparent; margin: 0;
        }
        .hero-alt p { color: var(--muted); margin: 0.35rem 0 0; }
        .badge-alt {
          display:inline-block; background: linear-gradient(135deg, var(--violet), var(--cyan));
          color:#08111f; padding:4px 10px; border-radius:999px; font-weight:700; font-size:0.8rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    def render_hero_alt():
    st.markdown(
        """
        <div class="hero-alt">
          <span class="badge-alt">Neon Pulse</span>
          <h1>🧑‍⚕️SehatSathi: Your daily wellbeing companion</h1>
          <p>Fast guidance, vibrant focus — your wellbeing, illuminated.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    def section_title_alt(title: str, emoji: str | None = None):
      icon = f"<span class='subheader-emoji-alt'>{emoji}</span>" if emoji else ""
      st.markdown(f"<div class='subheader-fancy-alt'>{icon}<span>{title}</span></div>", unsafe_allow_html=True)

    def render_divider_alt(label: str | None = None):
      st.markdown("<div class='divider-alt'></div>", unsafe_allow_html=True)
