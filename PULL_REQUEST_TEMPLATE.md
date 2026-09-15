### 📌 Pull Request Summary

<!--
Write for someone who has never seen this work. Two to four sentences.
What was wrong or missing, what this does about it, and why now.
Name the symptom before the mechanism. Close issues explicitly ("Closes #44").
-->

| | |
|---|---|
| **Ticket** | PUI-000 |
| **Type** | Feature / Bug fix / Refactor / Performance / Chore / CI and build / Docs |
| **Risk** | Low / Medium / High — <!-- one sentence on why. What could this break, and who would notice? --> |
| **Authored** | Human / Agent-assisted / Agent-authored <!-- Human: I wrote it. Agent-assisted: an agent wrote code and I read and edited each change as it came. Agent-authored: an agent produced the diff and I reviewed it as a whole afterwards. This tells a reviewer how much of the diff a human has already read line by line. --> |
| **Touches** | migrations? auth? config or env vars? a public interface? something users already have? (list, or "none of these") |

### 🧱 Stack

<!--
Optional. Delete this section for a standalone PR.
Give the base branch, the merge order, and one line per PR. Include PRs in other repos that must land first.
-->

Nth of M in the <name> stack. Base branch is `F-xxx` (#NN); merge order **#NN -> #NN -> #NN**.

1. #NN (`branch`): what it does.
2. #NN (`branch`, this PR): what it does.

### 🎯 Root Cause

<!-- Bug fixes only. Delete for features and chores. This is what stops us patching the same defect five times. -->

- **What actually went wrong:**
- **Class of defect:** <!-- Name it so it is searchable. -->
- **Where else this pattern occurs:** <!-- Say what you searched for. "Only here" is an answer, but defend it. -->
- **Why the fix belongs at this layer:**

### 📝 Notes and Caveats

<!--
What a reviewer needs before they start reading, and nowhere else to put it.
Known limitations, things deliberately left out, a decision you made that the diff does not explain.
Delete if there is genuinely nothing.
-->

### 🧭 Review Route

<!--
A reading order, not a file list. A reviewer should be able to start at 1, work down, and finish
having reviewed the whole diff without reconstructing context from the code.

ORDER by what makes the change easiest to understand. Put the file that establishes the idea
first, then the files that use it. Group by the thing being changed, not by folder. That is often
not the same as risk order, so use the depth markers to say where the risk actually is.

DEPTH, marked on every entry:
  🔍 Read closely — judgement required, a mistake here costs something
  👀 Skim         — follows from the above, check it does what it claims
  ⏭️ Glance       — tests, renames, generated code, formatting. Group these into one entry.

EVERY file in the diff appears here, so nothing goes unaccounted for.

For each entry, three lines:
  What it is    — the file's job in the system. A reviewer may never have opened it.
  What changed  — one or two lines.
  What to check — the actual question. On a 🔍 entry this is the point of the whole section.
-->

**1. 🔍 `path/to/file.ts` (+79 −10)**
*What it is:* its job in the system, in one line.
*What changed:*
*What to check:*

**2. 👀 `path/to/other.ts` (+23 −6)**
*What it is:*
*What changed:*
*What to check:*

**3. ⏭️ `path/to/*.spec.ts` and 4 others (+625)**
*What it is:* tests for the above.
*What changed:*

**I am least sure about:** <!-- The thing you would most like a second opinion on. Say it here rather than hoping nobody asks. -->

### 🛠 How to Test

<!-- Commands a reviewer can paste, and what they should see. "Config only, nothing to run" is a fine answer. -->

```bash
```

### 📊 Results

<!--
Delete unless this PR claims something measurable: performance, query cost, payload size, accuracy.
Numbers with the machine, the sample size and the baseline. Say which numbers came from an older run.
-->

### 🗄 Migrations, Rollback and Compatibility

<!-- Delete if this PR changes no schema, no config, and no interface anyone else depends on. -->

- **Migration or schema change:**
- **How it reaches production:**
- **Rollback:**
- **Backwards compatibility:** <!-- Who calls this, and what happens to them mid-deploy? -->
- **New config or env vars:**

### ✅ Checklist

- [ ] I have self-reviewed every line of this diff (including AI-generated code).
- [ ] Tests are added or updated for the changes (or N/A — explain in Notes).
- [ ] CI is green (lint, type-check, tests).
- [ ] Documentation is updated where relevant (README, Confluence — link it above).
- [ ] Breaking changes, DB migrations, and new env vars are called out (`.env.example` / sample configs updated).
- [ ] No secrets committed (keys, tokens, passwords, connection strings).
- [ ] No large, generated, or personal files committed (gitignore updated if needed).
- [ ] UI changes include screenshots or a short recording.
- [ ] This PR covers one concern; unrelated changes are split out.

<!--
Tick only what you verified in this session. An unchecked box with one line of reasoning is a good PR.
A checked box you cannot defend is not. Where an item does not apply, tick it and say why on the same line:
- [x] UI changes include screenshots. — N/A, backend only
-->

<details>
<summary><b>👀 For the reviewer</b></summary>

CI already checked lint, types, tests and secrets. Do not spend your attention there. Spend it on the three things a tool cannot answer.

**1. Is this the right change?**
Does it do what the ticket asked, and is the ticket still what we want? A correct implementation of the wrong thing passes every check in this repo.

**2. Does it fit?**
Will the next person find this code where they expect it? Does it use what already exists, or reinvent it? Is a new abstraction earning its keep, or is it one caller wearing a framework?

**3. What happens when it is wrong?**
Who sees the failure, how fast, and what we do about it. Ask explicitly about anything listed under **Touches**.

**Before approving:** every thread resolved, or explicitly deferred with an owner and a ticket. An approval with open threads is how findings get lost.

</details>

### 🔗 Related Issues/Tickets

-
