<p align="center">
  <img src="assets/visual-authoring-symbol.png" alt="Visual Authoring symbol: source fragments become an intentional visual form inside a review loop, with human release authority" width="360">
</p>

<h1 align="center">Visual Authoring</h1>

<p align="center">
  <a href="README.md">한국어</a> · <a href="README.en.md">English</a>
</p>

<p align="center">
  <strong>Turn complex material into visual work people can understand, review, and act on.</strong><br>
  <em>Complex material, made visible for human understanding, review, and decisions.</em>
</p>

## About the project

Visual Authoring is an authoring skill for work that combines explanation and judgment: documents, slide decks, landing pages, app UI, and learning materials. It does not stop at making polished screens quickly. It first decides **what to show and why**, then turns that decision into structures and scenes readers can understand.

The symbol condenses this flow. Scattered pieces stand for source material; the ordered form stands for authoring; and the outer orbit stands for review and revision. The fingertip reaching the frame marks a boundary: a person, not AI, decides whether to publish, revise, or release the work.

~~~mermaid
flowchart LR
  A["Source material"] --> B["Reader and decision"]
  B --> C["Visual strategy"]
  C --> D["Document · slides · interface"]
  D --> E["Review and revision"]
  E --> F["Human approval"]
~~~

## What it helps with

| Situation | What Visual Authoring does |
|---|---|
| Presentation | Organizes the central claim, sequence, and message of each scene into a slide structure people can follow. |
| Document or learning material | Designs meaning and visual hierarchy so readers can follow the flow without stripping away essential information. |
| Landing page or app UI | Makes the states, actions, and decision points a user needs to understand concrete in the screen structure. |
| Improving existing material | Does more than decorate a source: separates what to keep, create, and verify before proposing a new candidate. |

## Install it: step by step

This package is more than a one-line prompt. `SKILL.md` works with its references, validation scripts, and assets, so **install the entire `visual-authoring` folder rather than copying `SKILL.md` alone**. Installation does not add a separate design app. It lets an AI agent read and use this working method.

### 1. Choose the route that fits you

| If this sounds like you | Use this route |
|---|---|
| You want to start in ChatGPT without a terminal | **A. Install in ChatGPT** below |
| You use Codex or another agent compatible with `SKILL.md` | **B. Add the folder to your agent** below |
| You are unsure which route applies | Try A first. If a work or school account blocks uploading, ask your administrator whether Skills are available to you. |

### A. Install in ChatGPT — no terminal required

1. In a browser, [download the latest ZIP of this repository](https://github.com/vibeworkers/visual-authoring/archive/refs/heads/main.zip).
2. Open ChatGPT on the web or desktop and go to **Plugins → Skills → Create → Upload**. Menu names and placement can vary slightly by account and workspace.
3. Choose the ZIP you downloaded. If the upload dialog asks for an extracted folder instead, select the `visual-authoring-main` folder—the folder where `SKILL.md` appears immediately inside it.
4. Review the displayed description and license, then select **Install**.
5. Open a new chat and select **Visual Authoring** from Skills. If your interface offers skill mentions, select `@Visual Authoring`.
6. Send this message to confirm the first run:

~~~text
Use Visual Authoring to help me decide what to make from this material.
First, show what you can confirm in the material and what still needs confirmation.
~~~

If you cannot find Skills or Upload, the installation may not be at fault. Your plan, role, or workspace settings may have Skills or skill uploading disabled. Ask an administrator or check [OpenAI’s Skills guide](https://help.openai.com/en/articles/20001066).

### B. Add the folder to Codex or another `SKILL.md`-compatible agent

1. If you are comfortable with a terminal, clone the repository from the place where you work. If you are not, download and extract the ZIP as in route A instead.

~~~sh
git clone https://github.com/vibeworkers/visual-authoring.git
~~~

2. In your agent’s settings or official documentation, look for **Skills**, **Import skill**, **Custom skills**, or a **skill folder**. Menu names and locations differ by tool, so use the location your agent documents rather than creating a guessed personal path.
3. Import or copy the complete `visual-authoring` folder. After installation, the structure should look like this:

~~~text
<the skill folder documented by your agent>/
  visual-authoring/
    SKILL.md
    references/
    scripts/
    assets/
    agents/
    fixtures/
    evals/
~~~

4. Start a new chat or session in the agent. Some tools discover new skills only when a session starts.
5. Select **Visual Authoring** from the Skills list. In tools that support calling a skill by name, you can add `$visual-authoring` and make a request like this:

~~~text
$visual-authoring
I want to turn these meeting notes into something a teammate seeing them for the first time can understand and use to choose a next action.
I am not sure what to make, so ask no more than three questions first.
~~~

### 2. Check that installation worked

On the first request, the AI should ask about the source, reader, desired change, or artifact—or separate what it can confirm in the material from what is `Needs confirmation`. That is an early signal that the skill was read; it does not establish final artifact quality, reader understanding, or completed publication.

### 3. If you get stuck, check in this order

| Symptom | First thing to do |
|---|---|
| The upload fails | Check whether the dialog expects an extracted folder instead of a ZIP. On a work or school account, ask an administrator whether you have permission to upload Skills. |
| The skill is not in the list | Confirm that `SKILL.md` sits immediately inside the `visual-authoring` folder, then open a new chat or session. |
| You get a general answer instead | Select Visual Authoring directly in Skills, or explicitly use `$visual-authoring` or `@Visual Authoring` where the tool supports it. |
| You are asked to install another program | No separate credentials are needed for basic document structuring. Optional work such as image conversion or web-screen checks can require Python, a browser, or a conversion tool; review the reason and permission request before deciding. |

To update, download the latest ZIP or repository again, replace the installed copy, and open a new session. If you cloned with Git, run `git pull` inside the repository, then follow the same check.

## New here? A 10-minute starting guide

Visual Authoring is not a separate design application. It is a working guide for sharing material and a purpose with an AI agent that can use this skill, then reviewing the result together. You do not need design-tool experience. Start with any draft, note, table, link, or existing asset you have, plus **who needs to understand or decide what**.

### 1. Write down just these four things

| What to note | A question to consider | Example |
|---|---|---|
| Source | What material do you have now? | Meeting notes, a 20-slide deck, a price table, a document link |
| Reader | Who will see this result for the first time? | A new teammate, a customer, a student |
| Desired change | What should the reader understand, compare, choose, or do? | Understand the difference among three options and choose one |
| Artifact | Where will they read or see it? | An 8-slide presentation, a four-page document, a landing page |

Rough source material is fine. If you cannot attach a file, a title, outline, key sentences, and numbers that must not change are enough. When improving an existing artifact, say whether you want to **continue from it** or **start fresh**.

### 2. If you cannot think of a request, send the material and one sentence

You do not need to define the purpose, reader, and format from the beginning. Share a file, link, image, or note, then send a plain-language message like this:

~~~text
I’m not sure how this material should be shown.
Please ask no more than three questions first,
then draft a Visual Authoring request from my answers.
Do not guess what is unknown; show options or mark it as "Needs confirmation."
~~~

Even a single short line is enough:

- “I need this for next week’s meeting.”
- “I want students to understand this.”
- “This document is too complicated; I want it to be easier to read.”
- “Help me decide what to make before we make it.”

The AI agent should first identify what it can confirm in the material, then ask in turn **who will see it**, **what they need to understand or decide**, and **where it will be used**. It is fine to answer, “I’m not sure.” In that case, the agent should show possible choices and explain their differences so you can choose. A person confirms the final request and direction before they are fixed.

### 3. Or copy this starter request

~~~text
Use Visual Authoring to turn this material into a visual artifact.

Source: [file, link, or pasted notes]
Reader: [for example, a teammate joining for the first time]
What the reader needs to do: [for example, understand three options and choose one]
Artifact: [for example, an 8-slide presentation / a four-page document / a landing page]
Existing artifact: [continue from it if present / otherwise start fresh]
Constraints: [for example, use the logo, fit a 10-minute presentation, remain readable on mobile]

First, separate what to keep, what to improve, and what needs confirmation in the source.
If the choice changes the outcome, show different visual strategies and sample key screens.
Create the main body after I choose a direction.
Do not invent numbers, quotations, or facts; leave unknown information marked as "Needs confirmation."
~~~

### 4. The work proceeds in this order

1. **Confirm the material and goal.** Separate what to keep, what needs to be added, and what is still unknown.
2. **Choose a structure for the reader’s task.** A comparison can use contrast, a sequence can use flow, a choice can use branching, and evidence can use tables or annotations.
3. **Compare directions when needed.** When format or expression substantially changes the result, review representative screens and choose which direction to develop.
4. **Build and review the artifact together.** Check reading order, factual accuracy, and legibility in the actual context of use.
5. **A person decides publication and final approval.** A completed screen does not automatically prove that people understood it, that it opens in the original editing tool, or that it has been deployed.

### 5. When you receive a result, check these five things

- After three seconds on the first screen, can you tell **what it is and who it is for**?
- Does it make a needed comparison, sequence, relationship, or risk easier to read instead of merely decorating the page?
- Do the key numbers, quotations, and claims match the source, with assumptions kept separate from confirmed facts?
- Are the type and contrast legible where the artifact will actually be used: in a presentation, in print, or on a mobile screen?
- Is it clear what you need to choose in the next revision and what still needs human final judgment?

### Turn common stuck requests into useful ones

| Instead of only saying | Try saying |
|---|---|
| “Make it pretty.” | “Make a one-page piece that helps a first-time customer understand the price difference and request a consultation.” |
| “Make a PowerPoint.” | “Create eight slides for a 12-minute presentation that help the team choose next week’s priority.” |
| Sharing only brand colors | Also state the reader, the decision you want, artifact type, and length. |
| Fixing numbers without source material | Leave blanks as `Needs confirmation` and ask what must be verified first. |
| Stopping after looking at the screen | Check separately in the real device, editing tool, and reader review. |

## Examples of finished work

The examples below were selected because they make distinct visual grammars visible. The point is not to collect attractive images. It is to show how the same content can be read as a map, branch, timeline, layer, boundary, or report page. We do not claim reader understanding or work outcomes without separate user validation.

### 1. A learning guide divided into map, choice, time, verification, and boundary

For a learning guide about AI collaboration tools, we did not rely on a single all-purpose diagram. Instead, five scenes prompt different questions at each step: a map for the overall relationship, a branch for choosing a work surface, a timeline for the first practice, layers for completion criteria, and a permission boundary for risky actions.

<p align="center">
  <img src="assets/examples/vibeworking-learning-map.png" alt="An overall learning map that moves from work situations through work-surface selection to repeated verification" width="48%">
  <img src="assets/examples/vibeworking-surface-map.png" alt="A branching map for choosing Chat, Cowork, Code, or Design for the task at hand" width="48%">
</p>
<p align="center">
  <img src="assets/examples/vibeworking-practice-timeline.png" alt="A 15-minute practice flow from opening a project through verification and record keeping" width="32%">
  <img src="assets/examples/vibeworking-verification-layers.png" alt="A three-layer verification structure for file, runtime, and user perspectives" width="32%">
  <img src="assets/examples/vibeworking-permission-boundary.png" alt="Permission and risk boundaries for low, medium, and high risk levels" width="32%">
</p>

### 2. A decision report that leaves assumptions and verification boundaries visible

In a business-scenario report, the cover states up front that the analysis rests on assumptions, then brings price, capacity, and gross revenue together on one page. Arithmetic values and unverified market demand appear separately in the same scene so a large number is not mistaken for a conclusion.

<p align="center">
  <img src="assets/examples/ai-study-scenario-cover.png" alt="The cover of an assumed AI-study business scenario with its evidence boundary" width="35%">
  <img src="assets/examples/ai-study-scenario-price-page.png" alt="A report page with 49,000 and 59,000 won pricing scenarios, gross seat revenue, and a warning that this does not establish market demand or profit" width="47%">
</p>

### 3. An analytical guide that recasts product screens as learning scenes

The PostHog content-behavior analysis guide does not simply place the product screens for Heatmap, Replay, and Funnel side by side. Each screen is paired with the question to ask first, the next dimension to inspect, and a stopping rule that keeps observations separate from causes. The result is organized as a 12-page learning sequence. Product screens in this example belong to their original rights holder, so they are not copied into this repository; the asset record below explains the rights boundary and why they are excluded.

See [`assets/examples/README.md`](assets/examples/README.md) for the selection criteria and the rights and claim boundaries for each asset.

## Working principles

- **Put content fit before decoration.** Use visual effects only when they help the message and the reader’s judgment.
- **Keep the system fixed and the scenes open.** Retain shared structure and quality criteria without forcing every artifact into the same layout.
- **Make review possible.** Do not collapse structure, reading, rendering, native runtime, and human judgment into one “pass.”
- **Keep final authority with people.** AI can make candidates and review material, but it does not replace approval or publication.

## Explore the repository

| Path | Contents |
|---|---|
| [`SKILL.md`](SKILL.md) | The full authoring flow and execution contract |
| [`references/`](references/) | Visual strategies, review guidance, and document/slide implementation standards |
| [`scripts/`](scripts/) | Structure and implementation checks |
| [`fixtures/`](fixtures/) · [`evals/`](evals/) | Test inputs and evaluation material |
| [`assets/`](assets/) | Project symbol, finished-work examples, and asset metadata |

## Scope and license

This project does not infer that people understood an artifact, that it opens in the original editing tool, or that it has been deployed simply because an output screen exists. The necessary evidence and human approval must be confirmed separately in the work context.

Unless noted otherwise, original work in this repository is licensed under [CC BY-NC 4.0](LICENSE). The creation and rights boundaries of the symbol and example assets are recorded in [`assets/visual-authoring-symbol.provenance.md`](assets/visual-authoring-symbol.provenance.md) and [`assets/examples/README.md`](assets/examples/README.md).
