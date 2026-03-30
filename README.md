# Lab 9 - Quiz and Hackathon

- [About the lab](#about-the-lab)
- [Quiz](#quiz)
- [Hackathon](#hackathon)
  - [Task 1 — Ideation and Requirements](#task-1--ideation-and-requirements)
    - [Ideation](#ideation)
    - [Stakeholders](#stakeholders)
    - [User stories](#user-stories)
  - [Task 2 — Proof of Concept](#task-2--proof-of-concept)
  - [Task 3 — Planning](#task-3--planning)
    - [Refine the backlog](#refine-the-backlog)
    - [Scope the MVP](#scope-the-mvp)
  - [Task 4 — MVP](#task-4--mvp)
  - [Task 5 — Delivery](#task-5--delivery)
    - [Submit a presentation on Moodle](#submit-a-presentation-on-moodle)
    - [Publish the product code on GitHub](#publish-the-product-code-on-github)

## About the lab

Lab opens with a [quiz](#quiz) and then kicks off the [hackathon](#hackathon).

You must complete both to get the full point for Lab 9.

During the lab (2 hours):

<!-- no toc -->
- Write a [quiz](#quiz)
- Complete [Task 1](#task-1--ideation-and-requirements) — get TA approval
- Complete [Task 2](#task-2--proof-of-concept) — get TA approval

Use agents and LLMs throughout — for ideation, writing stories, scaffolding code, and prototyping.

By Thursday 23:59, complete:

<!-- no toc -->
- [Task 3](#task-3--planning) through [Task 5](#task-5--delivery)

## Quiz

Pen and paper quiz.

- Closed-book, no devices allowed.
- You get random 3 questions from the question bank (available on Moodle).
- Answer at least 2 out of 3 correctly.

## Hackathon

Each student goes from own idea to own deployed product.

> [!NOTE]
>
> We simplify definitions because you'll study these concepts more in-depth during the SWP course.

| Task | What | Gate |
| ---- | ---- | ---- |
| [Task 1](#task-1--ideation-and-requirements) | Ideation and Requirements — idea, stakeholders, user stories, and what the PoC will test | TA approves during lab |
| [Task 2](#task-2--proof-of-concept) | Proof of Concept — prove the riskiest technical assumption | TA approves during lab |
| [Task 3](#task-3--planning) | Planning — refine stories based on PoC learnings, scope the MVP | — |
| [Task 4](#task-4--mvp) | MVP — fully implement the most important requirements, deploy | — |
| [Task 5](#task-5--delivery) | Delivery — presentation slides and published code | Moodle + GitHub |

You can't know all user stories before you've built anything. Requirements emerge through building and feedback. Task 1 captures what you can imagine now. Task 2 tests feasibility. Task 3 is where you revise your understanding based on what you learned.

### Task 1 — Ideation and Requirements

#### Ideation

Define:

- End users of the product
- Which problem your product solves for the end users
- The product idea

The product idea must be:

- Easy to explain in one sentence
- Easy to implement using an agent
- Clearly solve the problem for end users
- Different from the project used in SET labs

The product must have at least these components:

- The nanobot agent
- Frontend
- Backend
- Database

Each component must:

- Interact with at least one other component
- Be necessary for solving the end users' problem

#### Stakeholders

A stakeholder is a person affected by the project.

List all stakeholders of your project (including yourself).

During the hackathon, assume that end users are your main stakeholders and focus on them.

#### User stories

A user story specifies:

1. The persona who wants the feature
2. What the feature is
3. Which value the feature brings to the persona

Each user story must have acceptance criteria — concrete, testable conditions that define when the story is done.

> 🟪 **Example**
>
> **User story:**
>
> As a DevOps team member, I want the chatbot to answer questions about logs and traces so that I can analyze incidents without writing `LogsQL` by hand.
>
> **Acceptance criteria:**
>
> - User can type a natural-language question about logs
> - Chatbot returns relevant log entries within 10 seconds
> - Chatbot cites which log source it queried

Write user stories for the main product features. Prioritize the ones focusing on end users.

These are your *initial* stories — you will revise them in [Task 3](#task-3--planning) after the PoC.

Discuss with the TA what your PoC should test — the riskiest assumption behind your idea.

**Gate:** TA approves your idea, stakeholders, user stories, and PoC plan before you proceed.

### Task 2 — Proof of Concept

Prove that the riskiest technical assumption behind your idea actually works.

The goal is learning, not building. The sooner you learn what doesn't work, the less effort you waste.

Ask yourself: *what is the one thing that, if it fails, kills the idea?* Build the minimum to test that.

> 🟪 **Example**
>
> If your product is a `Telegram` bot deployed on a university VM, the riskiest assumption might be that the bot can receive messages when hosted there. Build the simplest bot, deploy it, and verify.

> [!TIP]
>
> Use `Build` in `Google AI Studio`.

**Gate:** Show the PoC to the TA. If it worked, proceed. If it failed, discuss how to pivot.

### Task 3 — Planning

The PoC likely changed your understanding of what's possible, what's hard, and what matters. This task has two steps: update your backlog, then scope the MVP.

#### Refine the backlog

Based on what you learned in the PoC:

- Add new user stories that emerged
- Revise or remove stories that turned out to be infeasible or unimportant
- Update acceptance criteria to reflect what you now know

#### Scope the MVP

Decide which user stories the MVP must cover. Prioritize the ones that deliver the most value to end users.

### Task 4 — MVP

Implement your product, fully covering the most important user stories and their acceptance criteria.

Dockerize all services.

Deploy the product so that it's accessible by course instructors and students from the university network.

### Task 5 — Delivery

<!-- no toc -->
1. [Submit a presentation on Moodle](#submit-a-presentation-on-moodle)
2. [Publish the product code on GitHub](#publish-the-product-code-on-github)

#### Submit a presentation on Moodle

Submit on Moodle a 5-minute presentation with at most ten slides:

- Title slide:
  - Product title
  - Your name
  - Your university email
  - Your group

- Agenda slide:
  - List of sections in the presentation

- Context slide(s):
  - Your end users
  - The problem of end users you are solving
  - Your solution

- Implementation slide(s):
  - How you built the product

- Demo slide(s):
  - Pre-recorded demo with live commentaries (no longer than 2 minutes)

- Final slide:
  - Link and QR code for each of these:
    - The GitHub repo with the product code
    - Product deployed on a VM

#### Publish the product code on GitHub

- Publish the product code in a repository on `GitHub`.

  The repository name must be `se-toolkit-<product-name>` (without `<` and `>`).

- Add the MIT license file to make your product truly free and open-source.

- Add `README.md` in the product repository.

  Recommended structure of the `README.md`:

  - Product name

  - One-line description

  - Demo:
    - A couple of relevant screenshots of the product

  - Product context:

    - End users
    - Problem that your product solves for end users
    - Your solution

  - Features:

    - Implemented and not not yet implemented features

  - Usage:

    - Explain how to use your product

  - Deployment:

    - Which OS the VM should run (you may assume `Ubuntu 24.04` like on your university VMs)
    - What should be installed on the VM
    - Step-by-step deployment instructions
