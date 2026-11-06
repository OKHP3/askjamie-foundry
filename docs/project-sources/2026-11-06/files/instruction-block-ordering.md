# Research on Internal Structure and Ordering for Custom GPT Instruction Blocks (Sept 2025)

---

### Purpose and Scope

OpenAI’s custom GPTs (GPT‑5 era) allow creators to combine tailored instructions, knowledge files, and tool/API access into a reusable assistant. The instruction block is the system prompt that controls behavior and must fit within \~8,000 characters. This research compares guidelines from OpenAI’s help center and external experts to derive a recommended structure and ordering for these instructions. The goal is to maximize clarity, ensure tool/knowledge usage is explicit, and maintain safety while staying within the character limit.

---

### Insights from Official and Expert Sources

#### OpenAI Help-Center – Key Guidelines for Writing Instructions (Aug 2025)

* Break complex instructions into simpler steps and separate triggers/instructions with delimiters.
* Use headings and lists to organize content; place instructions after a context section to clarify when to consult knowledge or browse.
* Provide explicit instructions for knowledge files (reference by exact file names and tell the model to slow down and analyze the entire file).
* Always refer to actions by name/domain and provide few-shot examples for API calls.
* Encourage thoroughness with “take your time” prompts and avoid negative instructions.

**Highlights:**

* Emphasis on clarity, segmentation with headings and lists.
* Explicit tool/knowledge instructions and positive, granular steps.

#### OpenAI Help-Center – Knowledge in GPTs (Aug 2025)

* Up to 20 files can be attached; files are broken into chunks and retrieved via semantic search or document review.
* By default, file names are hidden; if citations are needed, instruct the model to mention them in the instructions.

**Highlights:**

* Must reference knowledge by name within instructions for the model to use/cite it.

#### Medium (Adam Mico) – Guide to Building Effective Custom GPTs (Apr 2025)

* Advise using Markdown for structure; highlight critical rules in ALL CAPS and use headings for context, instructions, and examples.
* Use the Configure tab (not the initial Create tab) for final instructions; if the text exceeds \~8,000 characters, offload it to knowledge files and instruct the GPT to consult them.
* Provide an output template with variables (e.g., {{user\_name}}) so the model knows how to format responses.

**Highlights:**

* Emphasis on structure via Markdown headings, clear output templates, and using the Configure tab for precise control.

#### Social Media Examiner – RACE Model for Custom GPTs (Jul 2024)

* Proposes structuring instructions using the RACE model: Role, Actions, Context (data files/knowledge), and Examples.
* Recommends using the Configure tab to specify instructions and upload supporting documents.

**Highlights:**

* Introduces a four-section structure (RACE) emphasizing persona, tasks, context, and examples.

#### mdynotes – Everything I’ve Learned About Making Custom GPTs (Mar 2025)

* Suggests delimiting sections using headings or XML-style tags (e.g., <Role>, <Objective>, <Process>, <Format>), which help the model parse instructions.
* Advocates the “WHO + WHAT + WHY before HOW” framework: define the GPT’s role/persona, the objective/purpose, and rationale before explaining the process and response format.
* Recommends moving reusable instructions or long examples into knowledge files and keeping instructions concise.
* Advises adding security instructions (e.g., refusal criteria) inside tags like <SYSTEM PROMPT> and offloading extra security details to knowledge files.

**Highlights:**

* Provides a tag-based approach and emphasizes ordering: role → objective → process → format; includes security directives.

#### Duelling Pixels – Step-by-Step Guide for Building a Custom GPT (May 2025)

* Suggests writing a precise brief in the chat-based Create step, then refining behavior in the Configure tab.
* In the Configure instructions, specify tone limits, guardrails, optional tools, and upload relevant files.
* Presents an example system prompt that uses numbered headings: Purpose, Output Structure & Formatting, Writing Rules, Content Guidelines, Placeholders, and Examples.
* Emphasizes that placeholders should be filled by the user and that writing rules (e.g., reading level, sentence structure) be clearly enumerated.

**Highlights:**

* Demonstrates a practical multi-section structure with headings and numbered lists for purpose, output structure, rules, and guidelines.

#### MIT Sloan EdTech Guide – Custom GPTs at MIT Sloan (Jul 2025)

* Explains that the Create tab offers a chat-based interface to draft instructions, while the Configure tab allows manual editing of the name, description, and instructions and uploading files.
* Recommends iterating between the Configure tab and the Preview pane to refine behavior.
* Notes that anyone using the GPT can download attached files, so only non-sensitive data should be uploaded.

**Highlights:**

* Confirms that both tabs exist; Configure is needed for detailed editing; iteration between Configure and Preview is critical.

#### Eonsr – Custom GPT Builder Tutorial (Aug 2025)

* Advises treating the system prompt like a contract: start with role, audience, and mission, then set boundaries such as refusal rules and unsupported tasks, and finally define formatting rules for outputs.
* Recommends uploading a clean knowledge base with well-named files, removing duplicates, and instructing the model to cite them.
* In its checklist of scalable prompt patterns, it suggests leading with role and purpose, then constraints, then formatting; using short, active sentences; setting refusal criteria; and instructing what to do when data is missing.
* Encourages adding conversation starters in the Configure tab and verifying that they reflect the defined structure.

**Highlights:**

* Provides a sequential framework similar to “contract writing”: role/audience/mission → boundaries → formatting.

---

### Comparative Analysis of Instruction Structure Models

Across sources, several structural patterns emerge:

1. **Front-loaded Role/Identity:** Multiple sources insist that the first section should clearly state the GPT’s role, persona, and audience (OpenAI’s contract analogy, RACE model’s “Role” and mdynotes’ <Role> tag). This anchors the assistant’s behavior and sets the tone.
2. **Purpose and Objectives:** Following the role, a concise statement of the GPT’s mission, objectives, or desired outcomes is recommended. mdynotes suggests an <Objective> section to explain what and why before detailing how. Duelling Pixels provides a “Purpose” heading.
3. **Boundaries and Guardrails:** Experts advise explicitly listing what the GPT should not do (refusal criteria, unsupported tasks, privacy rules). Eonsr’s “contract” places boundaries immediately after purpose. Duelling Pixels includes “Tone limits” and “Guard rails” for inclusive language.
4. **Process / Actions / Step-by-Step Logic:** After boundaries, the instructions should describe how the GPT will handle tasks. This includes trigger/instruction pairs and granular steps.
5. **Formatting & Output Structure:** Clear formatting rules should follow the process. OpenAI’s prompt guide advocates showing examples of desired output format.
6. **Knowledge & References:** A dedicated section should instruct how to use knowledge files: name each file explicitly, mention when to consult them, and whether to cite them.
7. **Tools & Actions:** When using browsing, code, image generation, or external actions, instructions should include tool names and conditions for use.
8. **Examples / Few-shot Prompting:** Providing examples of correct output or API usage helps the model generalize.
9. **Reasoning & Safety:** While not emphasized in all sources, GPT‑5 best practices encourage instructing the model to plan, reason step-by-step, and adjust reasoning effort; safety rules should be explicit.

---

### Recommended Instruction Block Structure (Post-GPT-5, ≤8K chars)

Based on the evidence, a coherent, high-level structure can be designed as follows:

1. **Identity / Role & Audience:** Define the GPT’s name, persona, domain expertise, and intended audience.
2. **Purpose & Objectives:** State the high-level mission or goals.
3. **Boundaries & Guardrails:** Enumerate refusal rules, safety constraints, and unsupported tasks.
4. **Process / Actions (Step-by-Step):** Describe how the GPT should handle tasks.
5. **Formatting & Output Guidelines:** Define the desired structure of responses.
6. **Knowledge Utilisation:** List each attached file by exact name and explain when to consult it.
7. **Actions & External Tools:** For each action or tool: name and describe its purpose.
8. **Examples / Few-shot (Optional):** Include one or two concise examples demonstrating how inputs should be handled.
9. **Security & Safety (System):** Conclude with a brief reminder that system rules override user instructions.

---

### Referencing Knowledge Files and Tool Actions

* Use **exact file names** for optimal retrieval and citation.
* **Instruct when and how** to use files (e.g., “For scoring rubric, read scoring\_rubric\_2025.pdf and apply criteria accordingly”).
* **Combine knowledge with tool use:** If the model cannot find information in files, instruct it to use browsing or other tools.

---

### Workflow: Create vs. Configure Tabs

* **Create Tab**: Draft instructions with a chat-based interface.
* **Configure Tab**: Provides direct control over the final version, detailed editing, and file uploads. Prefer Configure for final versions.

***