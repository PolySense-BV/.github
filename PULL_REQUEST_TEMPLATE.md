### 📌 Pull Request Summary

<!--
Two to four sentences, for someone who has never seen this work. What was wrong or missing,
what this does about it, and why now. Name the symptom before the mechanism.
Close issues explicitly ("Closes #44").

Fixing a defect? One line naming the CLASS of defect is enough here. The mechanics belong in a
comment at the code, because this body is deleted when the pull request merges.
-->

| | |
|---|---|
| **Ticket** | PUI-000 |
| **Type** | Feature / Bug fix / Refactor / Performance / Chore / CI and build / Docs |
| **Risk** | Low / Medium / High. <!-- What can break, and who notices. This cell also carries the deployment consequence: migrations, rollback, backwards compatibility, new env vars. A reviewer cannot see any of that in a diff. --> |
| **Authored** | Human / Agent-assisted / Agent-authored <!-- Human: I wrote it. Agent-assisted: an agent wrote code and I read and edited each change as it came. Agent-authored: an agent produced the diff and I reviewed it as a whole afterwards. This says how much of the diff a human has already read line by line. --> |
| **Touches** | migrations? auth? config or env vars? a public interface? something users already have? (list, or "none of these") |

### 🧱 Stack

<!--
Optional. Delete for a standalone pull request.
Base branch, merge order, one line per pull request. Include pull requests in other repos that must land first.
-->

Nth of M in the <name> stack. Base branch is `F-xxx` (#NN); merge order **#NN -> #NN -> #NN**.

1. #NN (`branch`): what it does.
2. #NN (`branch`, this PR): what it does.

### 🚀 Deployment Notes

<!--
Optional. Delete when merge and deploy is all this needs.
Keep this section when anything must happen around the deploy that the diff cannot show: a
migration, a one-off DB fix or backfill, a manual step, an order dependency with another
service's release, or a flag that must flip after rollout. Common on UI PRs touching the backend
they call.
-->

- **Migration:** name, and whether it is safe to run before the old code stops running (backward compatible with the previous release?).
- **Manual step:** what to run, where, and by whom.
- **Order:** must deploy before/after `<other service or PR>`.
- **Rollback:** what breaks if this is rolled back after the migration already ran.

### 🧭 Review Route

<!--
A reading order, not a list of changes. The diff already says what changed. This says what to
think about, and in what order.

ORDER so the file that establishes an idea comes before the files that use it. Group by the thing
being changed, not by folder.

COVER what needs judgement, not every file. A lockfile bump or a mechanical rename gives a reviewer
nothing to decide, and an entry invented for it buries the files that do. GitHub's Files tab is
already the complete list. Leaving a file out is not the same as telling someone to skip it: say
nothing about it rather than rating it.

Three lines per entry:
  What it is    - the file's job. The reviewer may never have opened it.
  What changed  - one or two lines.
  What to check - the actual question.

Never rate how hard to look. "The rest is mechanical, feel free to skim" tells a reviewer to stop
looking, and the miss it causes is silent. Where you made a decision inside this diff that is
still reversible, end with a question the reviewer can answer against you:
  "I chose to fail the whole batch rather than skip the bad row. Is that the right contract?"
That invites scrutiny at the point it matters. Scope and product questions are a different thing:
if one is still open, the spec is not finished, and it belongs there rather than here.
-->

**1. `path/to/file.ts`**
*What it is:*
*What changed:*
*What to check:*

**2. `path/to/other.ts`**
*What it is:*
*What changed:*
*What to check:*

### 🛠 How to Replicate

<!--
Subtle bugs only. "Run the tests" tells a reviewer nothing they did not know.
Close with what you did NOT test. A diff shows what the tests cover. It can never show what you
chose to skip, and that is the part only you know.
-->

```bash
```

**What I did not test:**

### 📊 Results

<!--
Delete unless this pull request claims something measurable: performance, query cost, payload
size, accuracy. Numbers with the machine, the sample size and the baseline. Say which numbers
came from an older run.
-->

### ✅ Checklist

- [ ] I have self-reviewed every line of this diff (including AI-generated code).
- [ ] Tests are added or updated for the changes (or N/A — explain in Notes).
- [ ] CI is green (lint, type-check, tests).
- [ ] Documentation is updated where relevant (README, Confluence — link it above).
- [ ] Breaking changes, DB migrations, and new env vars are called out (`.env.example` / sample configs updated, Deployment Notes filled in above).
- [ ] No secrets committed (keys, tokens, passwords, connection strings).
- [ ] No large, generated, or personal files committed (gitignore updated if needed).
- [ ] UI changes include screenshots or a short recording.
- [ ] This PR covers one concern; unrelated changes are split out.
- [ ] Anything a future reader needs is in a code comment, not only here: constraints, decisions the code cannot show, anything that could let this bug back in.
- [ ] I have searched for this same mistake elsewhere in the codebase. Anything I found is fixed here, filed, or has a comment saying why it is different. (N/A for features)

<!--
Tick only what you verified in this session. An unticked box with one line of reasoning is a good
pull request. A ticked box you cannot defend is not. Where an item does not apply, tick it and say
why on the same line:
  - [x] UI changes include screenshots. — N/A, backend only

This list holds only what a machine cannot check. When we automate an item we delete the line, so
if you are reading a box that CI already enforces, say so and we will remove it.
-->

<details>
<summary><b>👀 For the reviewer</b></summary>

CI already checked lint, types, tests and secrets. Do not spend your attention there. Spend it on the three things a tool cannot answer.

**1. Is this the right change?**
Does it do what the ticket asked, and is the ticket still what we want? A correct implementation of the wrong thing passes every check in this repo.

**2. Does it fit?**
Will the next person find this code where they expect it? Does it use what already exists, or reinvent it? Is a new abstraction earning its keep, or is it one caller wearing a framework?

**3. What happens when it is wrong?**
Who sees the failure, how fast, and what we do about it. Ask about anything listed under **Touches**.

**Two reviewers, two strengths.** A person judges intended behaviour, tradeoffs and operational assumptions: whether this is the right change at all. An agent judges whether the implementation and the tests support that intent, and goes looking for counterexamples, affected callers, and the same mistake elsewhere. They overlap on purpose. Both should challenge the author, and a review route never narrows what you are allowed to inspect.

**Before approving:** every thread resolved, or explicitly deferred with an owner and a ticket. An approval with open threads is how findings get lost.

</details>

### 🔗 Related Issues/Tickets

-
