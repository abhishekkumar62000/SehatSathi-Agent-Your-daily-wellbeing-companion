<img width="551" height="602" alt="logo" src="https://github.com/user-attachments/assets/35841e90-077f-47ea-ba6c-20fcfdd3513d" />
<img width="1920" height="1080" alt="App page" src="https://github.com/user-attachments/assets/1714ed95-e337-485f-806a-419a69fc0544" />


### App Demo:--

https://github.com/user-attachments/assets/f80877da-fb9b-4ded-af7f-e0e28dc52570


# 🧑‍⚕️ SehatSathi: Your Daily Wellbeing Companion

Live App: [https://sehatsathi-agent-your-daily-wellbeing-companion.streamlit.app/](https://sehatsathi-agent-your-daily-wellbeing-companion.streamlit.app/)

SehatSathi is an AI-powered daily mental wellbeing companion that blends structured assessment, instant guidance, long-term planning, and smart habit support — all wrapped in a colorful, animated Streamlit interface. The app helps users reflect, regulate, plan, and prepare for professional support when needed.

---

## Purpose

SehatSathi provides a personalized, AI-guided mental wellbeing assistant that performs three core roles:

1. Assess your emotional and mental health with screeners and dynamic triage.
2. Guide you immediately with coping tools and micro-interventions.
3. Support your longer-term care with plans, pathway builders, nudges, and handoff summaries.

The UI is colorful, theme-driven, and animation-enhanced to make wellbeing activities feel warm and engaging.

---

## Architecture Overview

• **UI Layer**

* Built in `ai_mental_wellbeing_agent.py`
* Themed styling powered by `ui_theme.py` and `ui_theme_alt.py`
* Animated dark UI, neon accents, gradient headers, micro-interactions
* Live sidebar accent color pickers override CSS variables in real-time

• **LLM Intelligence**

* Primary: AG2/AutoGen Swarm (Assessment → Action → Follow-up)
* Fallback: OpenAI Python client replicating the same 3-section generation
* Seamless switching based on availability

• **Config & State**

* Sidebar: API key input, model selector, theme toggle, accent colors
* Internal: `st.session_state` handles screenings, playlists, mood logs, and plan data

---

## Core Features

### 1. Agent Team Grid

Interactive 3-card system that acts as the main navigation for wellbeing actions:

* **Assess Me** → Opens PHQ/GAD and mood inputs
* **Guide Me Now** → Coping Toolkit spotlight
* **Build My Path** → Personalized care pathway generation

### 2. Triage Assistant

Risk-aware triage assistant with:

* PHQ-9 & GAD-7 score interpretation
* Stress/sleep indicators
* Detection of crisis keywords
* Sensitivity slider (low/medium/high)
* Inline quick actions for grounding, breathing, or outreach
* Pre-written outreach script for contacting support

### 3. Screening Tools

* **PHQ-9** with total score + severity classification
* **GAD-7** with total score + severity classification
* Integrated into triage and plan generation

### 4. Coping Toolkit

Instant micro-interventions for relief:

* Live **box breathing timer**
* **5-4-3-2-1 grounding exercise** with user notes
* **Journaling prompts** for reflection and regulation

### 5. Session Playlists

Users can build and run personalized stacks of interventions:

* Add multiple tools to a playlist
* Run sessions with timers
* Capture relief ratings (before/after)
* Chart analytics for each tool
* Favorite tools for quick access

### 6. Resource Finder

Simple directory with filters for:

* City
* Affordability
* Therapist language
* Remote/in-person
  Includes customizable outreach message for contacting professionals.

### 7. Progress Tracking

* Weekly check-ins
* Mood/stress/sleep logs
* Visual charts
* Smart Insights & Nudges based on correlations

### 8. Personalized Care Pathways

AI-generated multi-day plan including:

* Daily steps
* Duration-based guidance
* Focus areas
* Custom notes
* Downloadable markdown

### 9. Habit Coach

* Micro-habits
* Streak mosaic visualization
* Trigger-based habit suggestions

### 10. Therapist Handoff

De-identified summary with:

* PHQ-9 and GAD-7 totals
* Mood notes
* Key symptoms
* Recent actions
* Downloadable markdown handoff

### 11. Downloads

Users can download:

* Final Plan
* Care Pathway
* Safety Card

---

## UI / UX Design

### Themes

• Default dark theme
• “Neon Pulse” — animated neon headers, dividers, button pulses
• Real-time accent color overrides in sidebar

### Branding

• Sidebar logo: `logo.png`
• Developer credit section with `developer.jpg` / `developer.png`
• Gradient headers and animated components

### Interactions

• Micro-animations on buttons, sliders, and section transitions
• Smooth panel expansions for generated content
• Playlists and breathing tools animate during use

---

## How the App Works (User Flow)

1. **Enter details:**

   * Mood, stress, sleep quality, support system, recent changes, symptoms

2. **Run screeners (optional):**

   * PHQ-9
   * GAD-7

3. **Use Agent Actions:**

   * *Assess Me* → Screeners + triage
   * *Guide Me Now* → Coping tools
   * *Build My Path* → Care pathways

4. **Generate Plan:**

   * AG2/AutoGen orchestrates 3-step LLM flow
   * Assessment → Action → Follow-up
   * Fallback LLM replicates same sections
   * User views in expanders and downloads markdown

5. **Track Progress:**

   * Weekly check-ins
   * Mood charts
   * Smart nudges

6. **Build Playlists & Habits:**

   * Add interventions
   * Measure relief
   * Build habits and streaks

7. **Professional Handoff (if needed):**

   * Export a safe, anonymized summary

---

## LLM Flow (Detailed)

### AG2/AutoGen Path

Three agents operate with handoff:

1. **Assessment Agent:**

   * Reviews symptoms, PHQ/GAD, notes, stress/sleep

2. **Action Agent:**

   * Provides grounding, coping, and immediate next steps

3. **Follow-up Agent:**

   * Suggests monitoring, habits, and when to seek help

### OpenAI Fallback

If swarm is unavailable:

* A single LLM produces the three sections
* App splits text using predefined header markers

### Model Selection

Sidebar allows users to choose:

* GPT-4.x models
* GPT-3.5 or custom keys
* Any compatible OpenAI-style model

---

## Summary

SehatSathi functions as a complete, daily mental wellbeing system integrating:

* Intelligent risk-sensitive assessment
* Immediate grounding/relief tools
* Structured care planning
* Smart habit formation
* Personalized pathways
* Progress charts
* Crisis-aware triage
* Professional handoff preparation

With animated themes, neon UI, modular Streamlit components, and dual-path LLM architecture, it provides an accessible, warm, and intelligent wellbeing companion.

---

---

# ✅ **1) LangGraph-Style Agent Workflow Tree**

```
                         ┌──────────────────────┐
                         │   START / USER INPUT │
                         └──────────┬───────────┘
                                    │
                                    ▼
                     ┌───────────────────────────────┐
                     │ Collect Mood + Stress + Sleep │
                     │ + Support + Symptoms + Notes  │
                     └──────────┬────────────────────┘
                                │
                     ┌──────────▼──────────┐
                     │ Optional Screeners  │
                     │   PHQ-9 / GAD-7     │
                     └──────────┬──────────┘
                                │
                                ▼
                    ┌──────────────────────────┐
                    │ TRIAGE ASSISTANT LOGIC   │
                    │ • Risk scoring           │
                    │ • Crisis keyword check   │
                    │ • Sensitivity slider     │
                    └──────────┬──────────────┘
                               │
                               ▼
           ┌──────────────────────────────────────────┐
           │            AGENT TEAM ENTRY              │
           │ (Triggered by user choice below)         │
           └─────────────────┬────────────────────────┘
                             │
         ┌───────────────────┼───────────────────────┐
         ▼                   ▼                       ▼
┌────────────────┐   ┌────────────────┐    ┌─────────────────────┐
│ Assess Me      │   │ Guide Me Now   │    │ Build My Path       │
│ (Screen/Plan)  │   │ (Coping Tools) │    │ (Care Pathways)     │
└───────┬────────┘   └──────┬─────────┘    └────────┬────────────┘
        │                    │                       │
        ▼                    ▼                       ▼
┌────────────────┐   ┌────────────────────┐   ┌────────────────────────┐
│ Trigger LLM    │   │ Open Toolkit UI    │   │ Trigger Plan Builder   │
│ Agent Chain    │   │ (Breathing, 54321) │   │ (Goals + Notes)        │
└───────┬────────┘   └────────┬───────────┘   └────────┬──────────────┘
        │                     │                       │
        ▼                     ▼                       ▼
        ┌───────────────────────────────────────────────────────────────┐
        │        AG2 / AUTOGEN MULTI-AGENT SEQUENCE                     │
        └───────────────────────────────────────────────────────────────┘
                     │                     │                     │
                     ▼                     ▼                     ▼
    ┌────────────────────────┐   ┌────────────────────────┐   ┌───────────────────────────┐
    │ ASSESSMENT AGENT       │ → │ ACTION AGENT           │ → │ FOLLOW-UP AGENT            │
    │ - Evaluate condition   │   │ - Coping steps         │   │ - Monitoring plan          │
    │ - Read PHQ/GAD scores  │   │ - Immediate guidance   │   │ - Habits & nudges          │
    └────────────────────────┘   └────────────────────────┘   └───────────────────────────┘
                     │                     │                     │
                     └─────────────────────┴─────────────────────┘
                                       ▼
                           ┌─────────────────────┐
                           │ Structured Output   │
                           │ • Assessment        │
                           │ • Action Steps      │
                           │ • Follow-Up Plan    │
                           └─────────┬───────────┘
                                     │
                                     ▼
                     ┌─────────────────────────────────┐
                     │  UI Expanders + Download Files  │
                     │  (Plan, Care Path, Safety Card) │
                     └─────────────────┬───────────────┘
                                       │
                                       ▼
                     ┌───────────────────────────────────┐
                     │ PROGRESS TRACKING + PLAYLISTS     │
                     │ • Weekly check-ins                │
                     │ • Relief analytics                │
                     │ • Insights & Smart Nudges         │
                     └──────────────────┬────────────────┘
                                        │
                                        ▼
                           ┌────────────────────────────┐
                           │ Optional Therapist Handoff │
                           │ (PHQ/GAD + summary MD)     │
                           └──────────────┬─────────────┘
                                          │
                                          ▼
                                 ┌────────────────┐
                                 │      END/LOOP  │
                                 │ (User revisits)│
                                 └────────────────┘
```

---

# ✅ **2) Full App Interaction Tree (UI → Logic → Agents → Output)**

```
USER OPENS APP
│
├── Sidebar
│     ├── API Key
│     ├── Model
│     ├── Theme (Default / Neon Pulse)
│     └── Accent Color Picker
│
├── Agent Team Grid
│     ├── Assess Me → PHQ/GAD → Triage → Agents
│     ├── Guide Me Now → Coping Toolkit
│     └── Build My Path → Care Path Generator
│
├── User Inputs Page
│     ├── Mood
│     ├── Stress
│     ├── Sleep
│     ├── Support
│     ├── Symptoms
│     └── Journaling Notes
│
├── Screeners
│     ├── PHQ-9 → score → severity
│     └── GAD-7 → score → severity
│
├── Triage System
│     ├── Risk Flags
│     ├── Crisis Keywords
│     ├── Sensitivity Slider
│     └── Quick Actions (grounding, crisis, outreach)
│
├── LLM ROUTE
│     ├── If AG2 available → Multi-Agent
│     │        ├── Assessment Agent
│     │        ├── Action Agent
│     │        └── Follow-up Agent
│     └── Else → OpenAI fallback
│
├── Output
│     ├── Assessment Section
│     ├── Action Plan
│     └── Follow-Up Strategy
│
├── Downloads
│     ├── Full Plan
│     ├── Care Pathway
│     └── Safety Card
│
├── Coping Toolkit
│     ├── Box Breathing Timer
│     ├── 5-4-3-2-1 grounding
│     ├── Journal prompts
│     └── Instant calming actions
│
├── Session Playlists
│     ├── Add tools
│     ├── Run session
│     ├── Relief rating
│     └── Analytics chart
│
├── Progress Tracking
│     ├── Weekly check-ins
│     ├── Trends chart
│     └── Smart Nudges
│
└── Therapist Handoff
      ├── De-identified summary
      ├── PHQ-9/GAD-7 totals
      └── Download briefing
```

## 👨‍💻 Developer Information  
**Created by:** **Abhishek Kumar**  
**📧 Email:** [abhiydv23096@gmail.com](mailto:abhiydv23096@gmail.com)  
**🔗 LinkedIn:** [Abhishek Kumar](https://www.linkedin.com/in/abhishek-kumar-70a69829a/)  
**🐙 GitHub Profile:** [@abhishekkumar62000](https://github.com/abhishekkumar62000)

![developer](https://github.com/user-attachments/assets/6283838c-8640-4f22-87d4-6d4bfcbbb093)

<p align="center">
  <img src="https://github.com/user-attachments/assets/6283838c-8640-4f22-87d4-6d4bfcbbb093" width="120">
</p>





---




