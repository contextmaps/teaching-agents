"""
Scaffold-only generator. Run once during HANDOFF_01 to seed recipes/.

Produces 23 recipe JSON files under recipes/ with real metadata extracted
verbatim from SPEC.md §6 (title, number, family, tier, level, description,
recommended_platforms) and placeholder framing_paragraph + Instructions text.

Not part of the build pipeline. Re-running overwrites existing recipe JSON
files in place; if real Instructions have been authored in a later handoff,
DO NOT re-run this script — it will clobber that work.

Usage:
    python tools/generate_recipes.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from textwrap import dedent

REPO_ROOT = Path(__file__).resolve().parent.parent
RECIPES_DIR = REPO_ROOT / "recipes"

PLACEHOLDER_INSTRUCTIONS = dedent("""\
    [PLACEHOLDER — Instructions for this recipe will be authored and
    calibrated in HANDOFF_02 and beyond. The intended length for the
    final field is 200-800 words depending on the recipe complexity.
    This text exists to make the page render correctly during the
    skeleton phase.]""")

PLACEHOLDER_KNOWLEDGE_BASE = "To be specified in calibration."
PLACEHOLDER_TOOLS = "None for v1."


def framing(slug: str, title: str, description: str) -> str:
    return (
        f"This recipe defines {title}, a teaching-focused agent that fits the use case in the description above. "
        f"Use it when that description matches what you want the agent to do in your course. "
        f"The agent works best when its Instructions field is calibrated against two or three representative "
        f"prompts before you share the resulting agent with students or colleagues."
    )


# Each tuple: (number, slug, title, family_id, tier, level, description,
#              best_on, comparative_phrase, tradeoff_subline, related_recipes)
#
# All fields except framing_paragraph and fields.instructions are extracted
# verbatim from SPEC.md §6.
RECIPES = [
    # Family 1 — In-class activity engines
    (
        "1.1", "stakeholder-roleplay-partner", "The Stakeholder Roleplay Partner",
        "in_class_activity_engines", "medium", 2,
        "Plays a specific stakeholder — a CFO, customer, regulator, hotel guest, founder — for students to interview, negotiate with, or pitch to in class.",
        ["claude"], "decent on Copilot, Gemini, and ChatGPT",
        "Claude holds a single character voice across long roleplay without slipping into \"helpful assistant\" mode. The others run the recipe well for shorter exchanges; faculty running long in-class roleplays will notice the difference. A Copilot prototype is a reasonable starting point.",
        ["live-case-discussion-facilitator", "structured-debate-moderator"],
    ),
    (
        "1.2", "live-case-discussion-facilitator", "The Live Case-Discussion Facilitator",
        "in_class_activity_engines", "medium", 2,
        "Runs a structured case discussion in class — opens with framing, calls on perspectives, surfaces tensions, debriefs at the end.",
        ["copilot"], "similar performance on Gemini, ChatGPT, and Claude",
        "Multi-turn classroom orchestration works well across all four. Pick by access.",
        ["stakeholder-roleplay-partner", "structured-debate-moderator", "socratic-case-method-facilitator"],
    ),
    (
        "1.3", "structured-debate-moderator", "The Structured Debate Moderator",
        "in_class_activity_engines", "medium", 2,
        "Runs a two-sided debate in class — assigns positions, prompts each side, plays devil's advocate, synthesizes the strongest arguments.",
        ["copilot"], "similar performance on Gemini and ChatGPT, slightly stronger on Claude for contested topics",
        "All four handle the format well; Claude is a touch more reliably balanced when the debate involves politically charged or values-laden positions.",
        ["live-case-discussion-facilitator", "stakeholder-roleplay-partner", "small-group-exercise-generator"],
    ),
    (
        "1.4", "small-group-exercise-generator", "The Small-Group Exercise Generator",
        "in_class_activity_engines", "light", 2,
        "Produces a fresh small-group exercise — task, materials, time budget, debrief questions — tailored to the day's topic and class size.",
        ["copilot"], "similar performance on Gemini, ChatGPT, and Claude",
        "Fast generative task; pick by access.",
        ["think-pair-share-question-engine", "hands-on-data-activity-builder", "structured-debate-moderator"],
    ),
    (
        "1.5", "hands-on-data-activity-builder", "The Hands-On Data Activity Builder",
        "in_class_activity_engines", "medium", 3,
        "Generates a realistic, made-up dataset (CSV-shaped) plus an analysis task and discussion questions, for use in quantitative or analytics courses.",
        ["chatgpt"], "strong on Claude, decent on Copilot and Gemini",
        "ChatGPT's code interpreter validates the dataset shape and runs analyses inline, which makes the recipe more reliable. Claude can produce datasets and reason about them carefully without execution. Copilot and Gemini work for simpler datasets.",
        ["small-group-exercise-generator", "think-pair-share-question-engine", "discipline-specific-example-generator"],
    ),
    (
        "1.6", "think-pair-share-question-engine", "The Think-Pair-Share Question Engine",
        "in_class_activity_engines", "light", 2,
        "Produces a sequence of think-pair-share prompts at varying cognitive levels for a 50-minute class session, paced to fit the lecture flow.",
        ["copilot"], "similar performance on Gemini, ChatGPT, and Claude",
        "The most platform-agnostic recipe in the catalog.",
        ["small-group-exercise-generator", "discussion-question-generator", "formative-check-generator"],
    ),
    # Family 2 — Student-facing always-on agents
    (
        "2.1", "course-faq-answerer", "The Course FAQ Answerer",
        "student_facing_always_on", "light", 2,
        "Grounded on a syllabus and course documents; answers student logistics questions and refers back to the human instructor when the answer isn't in the sources.",
        ["chatgpt"], "similar performance on Gemini (custom Gem) and Claude (Projects), advanced on Copilot Studio for faculty with tenant access",
        "Custom GPTs and Gemini Gems both support file grounding and shareable links. Copilot Studio offers stronger institutional integration but requires Pamplin tenant access (most faculty would coordinate with Jim Dickhans). NotebookLM is a lightweight alternative.",
        ["reusable-course-assistant", "concept-tutor-no-answers", "adaptive-concept-practice-partner"],
    ),
    (
        "2.2", "concept-tutor-no-answers", "The Concept Tutor (No-Answers, Just Understanding)",
        "student_facing_always_on", "medium", 2,
        "Helps students build conceptual intuition — analogies, walkthroughs, \"what does this mean\" reframings — explicitly without giving away problem solutions or doing graded work.",
        ["claude"], "decent on ChatGPT, weaker on Copilot and Gemini",
        "The spoiler-protection guardrail is the entire recipe. Claude is most consistent at staying in role under student rephrasing; ChatGPT also holds well. Copilot and Gemini have been observed to give in to persistent rephrasing. Faculty deploying for graded courses should test under student pressure.",
        ["adaptive-concept-practice-partner", "reusable-course-assistant", "course-faq-answerer"],
    ),
    (
        "2.3", "adaptive-concept-practice-partner", "The Adaptive Concept-Practice Partner",
        "student_facing_always_on", "heavy", 2,
        "Asks students conceptual questions, listens to their answers, adjusts follow-ups based on what the student understood — a Socratic practice partner students use before exams.",
        ["claude"], "decent on ChatGPT, weaker on Copilot and Gemini",
        "Adaptive Socratic questioning is dialogue-quality-sensitive. Faculty wanting visual-avatar versions need a separate platform like HeyGen, outside this catalog's scope.",
        ["concept-tutor-no-answers", "reusable-course-assistant", "course-faq-answerer"],
    ),
    (
        "2.4", "reusable-course-assistant", "The Reusable Course Assistant",
        "student_facing_always_on", "heavy", 2,
        "Grounded on a faculty member's course materials — slides, readings, syllabus, past assignments — that students use throughout the semester for review and asynchronous study support.",
        ["chatgpt"], "similar performance on Claude (Projects), strong knowledge-grounding on Gemini but with sharing constraints, advanced on Copilot Studio for faculty with tenant access",
        "ChatGPT offers the most accessible deployment path for individual faculty. Gemini holds the largest grounding materials but with constrained sharing. NotebookLM is the lightweight alternative.",
        ["course-faq-answerer", "concept-tutor-no-answers", "adaptive-concept-practice-partner"],
    ),
    # Family 3 — Discussion and case-method
    (
        "3.1", "discussion-question-generator", "The Discussion Question Generator",
        "discussion_case_method", "light", 2,
        "Takes a reading and produces a tiered set of discussion questions: opening, probing, application, meta-questions about the reading itself.",
        ["copilot"], "similar performance on Gemini, ChatGPT, and Claude",
        "Among the most beginner-friendly recipes.",
        ["socratic-case-method-facilitator", "case-discussion-debrief-synthesizer", "think-pair-share-question-engine"],
    ),
    (
        "3.2", "socratic-case-method-facilitator", "The Socratic Case-Method Facilitator",
        "discussion_case_method", "medium", 2,
        "Helps faculty rehearse a case-method discussion before class — plays a skeptical student, surfaces where the discussion will go off-track.",
        ["copilot"], "similar performance on Gemini and ChatGPT, slightly stronger on Claude for sustained skeptical voice",
        "All four can play \"thoughtful student\" for a rehearsal session; Claude holds the register more consistently across long rehearsals.",
        ["discussion-question-generator", "case-discussion-debrief-synthesizer", "live-case-discussion-facilitator"],
    ),
    (
        "3.3", "case-discussion-debrief-synthesizer", "The Case-Discussion Debrief Synthesizer",
        "discussion_case_method", "medium", 2,
        "Takes notes from a case discussion that just happened and synthesizes a debrief document students can review afterward.",
        ["copilot"], "similar performance on Gemini, ChatGPT, and Claude",
        "Synthesis of messy notes into structure works well across all four.",
        ["discussion-question-generator", "socratic-case-method-facilitator", "rubric-builder"],
    ),
    # Family 4 — Course architecture and conversion
    (
        "4.1", "course-format-converter", "The Course Format Converter",
        "course_architecture", "heavy", 2,
        "Converts a course from one format to another — in-person to async online, semester to compressed, lecture-heavy to flipped — preserving learning outcomes while restructuring delivery.",
        ["gemini"], "Claude or ChatGPT (Projects) for moderate-sized · decent on Copilot",
        "Gemini's very large context window holds an entire semester's materials simultaneously. Claude and ChatGPT Projects work well for moderate courses. Copilot can do conversions on smaller courses but may lose fidelity on very large ones.",
        ["syllabus-modernizer", "module-architect", "reusable-course-assistant"],
    ),
    (
        "4.2", "syllabus-modernizer", "The Syllabus Modernizer",
        "course_architecture", "medium", 2,
        "Takes an existing syllabus and produces a revised version — clearer learning objectives, modernized tone, aligned assignments, updated policies — while preserving the faculty member's voice.",
        ["copilot"], "similar performance on Gemini and ChatGPT, slightly stronger on Claude for voice preservation",
        "Claude is a touch better at preserving distinctive voice; the others tend to standardize toward \"professional academic\" register.",
        ["module-architect", "course-format-converter", "course-ai-policy-drafter"],
    ),
    (
        "4.3", "module-architect", "The Module Architect",
        "course_architecture", "medium", 2,
        "Helps faculty design or restructure a course module from scratch — outcomes, sequence, in-class activities, assessments, materials list.",
        ["copilot"], "similar performance on Gemini, ChatGPT, and Claude",
        "Structured-output task; pick by access.",
        ["syllabus-modernizer", "course-format-converter", "rubric-builder"],
    ),
    # Family 5 — Assessment and feedback
    (
        "5.1", "rubric-builder", "The Rubric Builder",
        "assessment_feedback", "light", 2,
        "Interviews the faculty member about an assignment and produces a rubric with clear performance levels and criteria.",
        ["copilot"], "similar performance on Gemini, ChatGPT, and Claude",
        "Interview-then-produce-rubric works across all four.",
        ["formative-check-generator", "feedback-tone-matcher", "module-architect"],
    ),
    (
        "5.2", "formative-check-generator", "The Formative Check Generator",
        "assessment_feedback", "light", 2,
        "Produces a short formative-assessment instrument calibrated to a topic and student level, with explanations for why each item tests what it tests.",
        ["copilot"], "similar performance on Gemini, ChatGPT, and Claude",
        "Short-form item generation is highly platform-agnostic.",
        ["rubric-builder", "feedback-tone-matcher", "think-pair-share-question-engine"],
    ),
    (
        "5.3", "feedback-tone-matcher", "The Feedback Tone Matcher",
        "assessment_feedback", "medium", 2,
        "Helps a faculty member calibrate written feedback on student work — paste your draft and a sample of how you usually write, get suggestions that match your voice.",
        ["claude"], "decent on ChatGPT, weaker on Copilot and Gemini",
        "Voice imitation is the central value. Claude is meaningfully better at matching a faculty member's existing register; the others tend to flatten toward generic-instructor voice.",
        ["rubric-builder", "formative-check-generator", "syllabus-modernizer"],
    ),
    # Family 6 — Examples, cases, and content
    (
        "6.1", "discipline-specific-example-generator", "The Discipline-Specific Example Generator",
        "examples_cases_content", "light", 2,
        "Takes a concept and produces mini-cases or examples tuned to a specific industry, student level, or current relevance.",
        ["copilot"], "similar performance on Gemini, ChatGPT, and Claude",
        "Generative variety task; pick by access.",
        ["current-events-case-freshener", "concept-explainer-multiple-framings", "hands-on-data-activity-builder"],
    ),
    (
        "6.2", "current-events-case-freshener", "The Current-Events Case Freshener",
        "examples_cases_content", "light", 2,
        "Takes a recent news event and translates it into a mini-case or in-class discussion vehicle for a specific course.",
        ["copilot"], "similar performance on Gemini and ChatGPT, weaker on Claude for current-events freshness",
        "The first three pull recent news directly via web search; Claude handles framing well once the source is pasted but doesn't browse independently in the same way.",
        ["discipline-specific-example-generator", "concept-explainer-multiple-framings", "live-case-discussion-facilitator"],
    ),
    (
        "6.3", "concept-explainer-multiple-framings", "The Concept Explainer With Multiple Framings",
        "examples_cases_content", "medium", 3,
        "Explains a concept through the lens of multiple disciplines — for instance, \"explain risk\" with framings from Finance, Marketing, Real Estate, and Management — so faculty can pick the framing that fits or use the contrast as the teaching moment.",
        ["copilot"], "similar performance on Gemini, ChatGPT, and Claude",
        "One-shot multi-perspective generation works across all four.",
        ["discipline-specific-example-generator", "current-events-case-freshener", "module-architect"],
    ),
    # Family 7 — AI-policy
    (
        "7.1", "course-ai-policy-drafter", "The Course AI-Policy Drafter",
        "ai_policy", "medium", 2,
        "Interviews the faculty member about their course, values, and concerns; produces draft AI-use policy language for the syllabus, assignment-level guidance, and student-facing disclosure norms, calibrated to the specific course.",
        ["copilot"], "similar performance on Gemini, ChatGPT, and Claude",
        "Copilot has a slight institutional advantage: faculty drafting AI-use policy may want it to align with VT IT guidance, and Copilot's institutional embedding helps surface that alignment.",
        ["syllabus-modernizer", "module-architect", "course-faq-answerer"],
    ),
]


def build_recipe(entry) -> dict:
    (number, slug, title, family_id, tier, level, description,
     best_on, comparative_phrase, tradeoff_subline, related) = entry
    return {
        "id": slug,
        "number": number,
        "title": title,
        "family_id": family_id,
        "tier": tier,
        "level": level,
        "description": description,
        "framing_paragraph": framing(slug, title, description),
        "fields": {
            "instructions": PLACEHOLDER_INSTRUCTIONS,
            "knowledge_base": PLACEHOLDER_KNOWLEDGE_BASE,
            "tools": PLACEHOLDER_TOOLS,
            "recommended_platforms": {
                "best_on": best_on,
                "comparative_phrase": comparative_phrase,
                "tradeoff_subline": tradeoff_subline,
            },
        },
        "related_recipes": related,
    }


def filename(number: str, slug: str) -> str:
    flat = number.replace(".", "")  # "1.1" -> "11"
    family, idx = number.split(".")
    seq = (int(family) - 1) * 6 + int(idx)  # rough, not used
    # Per HANDOFF_01: 001-…json through 023-…json. Sequence by listing order.
    return f"{slug}.json"  # caller composes the prefix


def main() -> int:
    if len(RECIPES) != 23:
        print(f"ERROR: expected 23 recipes, got {len(RECIPES)}", file=sys.stderr)
        return 1

    RECIPES_DIR.mkdir(parents=True, exist_ok=True)

    expected_names = []
    for i, entry in enumerate(RECIPES, start=1):
        recipe = build_recipe(entry)
        prefix = f"{i:03d}"
        slug = recipe["id"]
        path = RECIPES_DIR / f"{prefix}-{slug}.json"
        with path.open("w", encoding="utf-8") as f:
            json.dump(recipe, f, indent=2, ensure_ascii=False)
            f.write("\n")
        expected_names.append(path.name)

    print(f"Wrote {len(expected_names)} recipe files to {RECIPES_DIR}")
    for name in expected_names:
        print(f"  {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
