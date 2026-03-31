# Lab 9 - Quiz and Hackathon

Lab opens with a [quiz](#quiz) and then kicks off the [hackathon](#hackathon).

To get the full point for the lab, you need to get Tasks 1-3 done during the lab. Tasks 4-5 must be finished by the usual deadline of Thursday 23:59.

Use agents and LLMs throughout — for ideation, requirements, scaffolding code, and implementing.

**Task 1 (graded by TA after the lab).**
Pen and paper quiz.
- closed book, no devices allowed.
- you get random 3 questions from the question bank.
- answer at least 2 out of 3 correctly.

**Task 2 (approved by TA during the lab).**
The project idea must:
- Be something simple to build, clearly useful, and easy to explain;
- Involve backend + db + web dashboard + user-facing agent;
- Not be an LMS (different from the course project).

Define:
- End users of the product
- Which problem your product solves for the end users
- The product idea in one short sentence

The product must have these components each fulfilling a useful function:
- The nanobot agent
- Frontend
- Backend
- Database

> 🟪 **Note**
> `Telegram` bots deployed on a university VM can fail to receive messages when hosted there.

**Task 3 (approved by TA during the lab).**
Produce a plan including:
- prioritized requirements;
- a clear breakdown of requirements into three product phases.

Give priority to features that deliver the most value to end users and are easier to implement. Each phase should be a functioning product in itself.

**Task 4.**
- Implement your product with the core features.
- Publish all code as a repo on github.
- Dockerize all services.
- Deploy it to be accessible to use.

**Task 5.**
Submit presentation with five slides:
- Product title, your name, email, group
- The problem you are solving and your end-user
- How you built it
- Video demo with live commentaries (<2 mins)
- Links to try.


Submit on Moodle a 5-minute presentation with five slides:

- Title slide:
  - Product title
  - Your name
  - Your university email
  - Your group

- Context slide(s):
  - Your end users
  - The problem of end users you are solving
  - Your solution

- Implementation slide(s):
  - How you built the product

- Demo slide(s):
  - Pre-recorded demo with live commentaries (no longer than 2 minutes)
  - _Note:_ This is the most important part of the presentation.

- Final slide:
  - Link and QR code for each of these:
    - The GitHub repo with the product code
    - Deployed product



#### Publishing the product code on GitHub

- Publish the product code in a repository on `GitHub`.

  The repository name must be called `se-toolkit-hackathon`.

- Add the MIT license file to make your product open-source.

- Add `README.md` in the product repository.

  `README.md` structure:

  - Product name (as title)

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
