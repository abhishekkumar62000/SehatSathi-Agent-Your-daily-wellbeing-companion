import streamlit as st

def inject_theme():
    st.markdown(
        """
        <style>
        :root {
          --bg0: #0b1020;
          --bg1: #0f172a;
          --fg: #e5e7eb;
          --muted: #94a3b8;
          --primary: #22c55e;
          --primary-2: #10b981;
          --accent: #8b5cf6;
          --accent-2: #06b6d4;
          --danger: #ef4444;
          --warning: #f59e0b;
        }

        @keyframes gradientShift {
          0% { background-position: 0% 50%; }
          50% { background-position: 100% 50%; }
          100% { background-position: 0% 50%; }
        }

        @keyframes glowPulse {
          0% { box-shadow: 0 0 0px rgba(34,197,94,0.2); }
          50% { box-shadow: 0 0 18px rgba(34,197,94,0.35); }
          100% { box-shadow: 0 0 0px rgba(34,197,94,0.2); }
        }

        @keyframes titleGlow {
          0% { text-shadow: 0 0 0px rgba(139,92,246,0.0); }
          50% { text-shadow: 0 4px 16px rgba(139,92,246,0.35); }
          100% { text-shadow: 0 0 0px rgba(139,92,246,0.0); }
        }

        @keyframes underlineSweep {
          0% { background-position: 0% 50%; }
          50% { background-position: 100% 50%; }
          100% { background-position: 0% 50%; }
        }

        .stApp {
          background: linear-gradient(120deg, var(--bg0), var(--bg1), #0a1325);
          background-size: 200% 200%;
          animation: gradientShift 18s ease infinite;
          color: var(--fg);
        }
        .stMarkdown, .stText, .stCaption, .stSubheader, .stHeader {
          color: var(--fg) !important;
        }
        .stButton>button {
          background: linear-gradient(135deg, var(--primary), var(--primary-2));
          color: #0b1020;
          border: none;
          border-radius: 12px;
          padding: 0.6rem 1rem;
          font-weight: 600;
          transition: transform 0.08s ease-in-out, filter 0.15s ease;
          animation: glowPulse 3s ease-in-out infinite;
        }
        .stButton>button:hover { transform: translateY(-1px); filter: brightness(1.08); }
        .stButton>button:active { transform: translateY(0px) scale(0.98); }

        /* Download buttons */
        .stDownloadButton>button {
          background: linear-gradient(135deg, var(--accent), var(--accent-2));
          color: #0b1020;
          border-radius: 12px; font-weight: 700;
        }

        .stExpander { background: rgba(17,24,39,0.6); border-radius: 12px; }
        .stExpander .streamlit-expanderHeader { color: var(--fg); }

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
          gap: 0.4rem;
          background: rgba(17,24,39,0.4);
          padding: 0.35rem;
          border-radius: 12px;
        }
        .stTabs [data-baseweb="tab"] {
          color: var(--fg);
        }

        /* Inputs */
        .stSelectbox, .stSlider, .stTextInput, textarea, .stMultiselect {
          border-radius: 12px !important;
        }

        /* Slider glow */
        [role="slider"] {
          box-shadow: 0 0 0 0 rgba(34,197,94,0.0);
          transition: box-shadow .2s ease;
        }
        [role="slider"]:hover {
          box-shadow: 0 0 0 6px rgba(34,197,94,0.15);
        }

        /* Accent badges */
        .badge {
          display: inline-block;
          background: linear-gradient(135deg, var(--accent), var(--accent-2));
          color: #08111f;
          padding: 4px 10px;
          border-radius: 999px;
          font-weight: 700;
          font-size: 0.8rem;
        }

        /* Fancy section headers */
        .subheader-fancy {
          margin: 0.75rem 0 0.5rem;
          font-size: clamp(1.1rem, 2.6vw, 1.6rem);
          font-weight: 800;
          letter-spacing: .2px;
          background: linear-gradient(135deg, var(--fg), var(--muted));
          -webkit-background-clip: text; background-clip: text; color: transparent;
          position: relative; display: inline-flex; align-items: center; gap: .5rem;
        }
        .subheader-fancy::after {
          content: ""; position: absolute; left: 0; right: 0; bottom: -6px; height: 3px;
          background: linear-gradient(90deg, var(--accent), var(--accent-2), var(--primary));
          background-size: 200% 200%; animation: underlineSweep 6s linear infinite;
          border-radius: 3px; opacity: .7;
        }
        .subheader-emoji { filter: drop-shadow(0 2px 8px rgba(16,185,129,.25)); }

        /* Gradient divider */
        .divider {
          height: 1px; width: 100%; margin: 1rem 0; border-radius: 999px;
          background: linear-gradient(90deg, transparent, rgba(6,182,212,.5), rgba(139,92,246,.6), transparent);
        }

        /* Agent team grid */
        .agent-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:12px; margin:.5rem 0 0; }
        .agent-card {
          background: linear-gradient(180deg, rgba(17,24,39,0.55), rgba(17,24,39,0.35));
          border: 1px solid rgba(148,163,184,0.22);
          border-radius: 14px; padding: 12px; position: relative; overflow:hidden;
          transition: transform .12s ease, border-color .2s ease;
        }
        .agent-card:hover { transform: translateY(-2px); border-color: rgba(139,92,246,0.5); }
        .agent-emoji { font-size: 1.2rem; filter: drop-shadow(0 2px 6px rgba(139,92,246,.35)); }
        .agent-title { font-weight: 800; letter-spacing:.2px; }
        .agent-sub { color: var(--muted); font-size: .92rem; }

        /* Hero */
        .hero {
          margin-top: 0.5rem;
          padding: 1rem 1.2rem;
          border-radius: 16px;
          background: radial-gradient(1000px 500px at 10% 10%, rgba(139,92,246,0.15), transparent),
                      radial-gradient(800px 400px at 90% 0%, rgba(6,182,212,0.15), transparent);
          border: 1px solid rgba(148,163,184,0.2);
        }
        .hero h1 {
          font-size: clamp(1.6rem, 3vw, 2.2rem);
          background: linear-gradient(135deg, var(--fg), var(--muted));
          -webkit-background-clip: text; background-clip: text; color: transparent;
          margin: 0;
          animation: titleGlow 4s ease-in-out infinite;
        }
        .hero p { color: var(--muted); margin: 0.35rem 0 0; }
        </style>
        """,
        unsafe_allow_html=True,
    )

def render_hero():
    st.markdown(
        """
        <div class="hero">
          <h1>🧑‍⚕️SehatSathi: Your daily wellbeing companion</h1>
          <p>Personalized support, practical steps, and gentle progress — all in one place.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

def success_confetti():
    try:
        st.balloons()
    except Exception:
        pass

def section_title(title: str, emoji: str | None = None):
  icon = f"<span class='subheader-emoji'>{emoji}</span>" if emoji else ""
  st.markdown(f"<div class='subheader-fancy'>{icon}<span>{title}</span></div>", unsafe_allow_html=True)

def render_divider(label: str | None = None):
  if label:
    st.markdown(f"<div class='divider'></div>", unsafe_allow_html=True)
  else:
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
