<!-- agent-work-mode:start -->
# Work mode: direct by default

The owner changed Orchestra to explicit opt-in on 2026-09-10. This applies to
every assistant and every authorized team member. It supersedes older standing
requests to hire agents and automatic Conductor routing in this repository.

Use the current session agent for ordinary work. Do not automatically hire an
implementer, Architect, verifier, Judge, or handoff auditor; switch models;
prepare staffing/cost tables; or offer a brief for an already clear request.

Activate Orchestra only when the requester explicitly says "use orchestra",
"use the Conductor Protocol", or invokes `/orchestra` (or `$orchestra` on a
host that supports it). Activation covers that task and its follow-ups, then
expires. A new unrelated task or session starts in direct mode unless the
requester explicitly chose a wider scope. "Orchestra off" or "work directly"
ends activation. "Continue", "go ahead", a difficult task, a quoted example,
or a historical handoff is not an activation. A request for one reviewer or
one subagent authorizes that bounded role, not the whole orchestra. Symphony
remains separately opt-in. Do not repeatedly offer orchestration for small work.

When Orchestra is active, follow the repository's Conductor Protocol and its
independent review requirements. Otherwise its route/seat/model/Judge rules are
inactive. Existing board, QA-bench, CI, or scheduled workflows keep their own
explicitly configured behavior; this mode does not rewrite or launch them.

## Verification in direct mode

Choose checks from the actual diff and its consequences:

- Documentation, comments, handoffs, and agent instructions: review the diff,
  references and syntax. Check changed metadata and hook wiring; run changed
  scripts and existing relevant tests. Keep generated documentation in sync.
  These changes alone do not require application dependency installation,
  a full app build, browser screenshots, or unrelated application test suites.
- Executable behavior: run focused checks of the affected behavior. Expand to
  typecheck, lint, integration tests, or a full build when the affected code,
  dependencies, configuration, or concrete risk warrants them.
- Visible product changes: inspect the rendered result at desktop and phone
  widths; test the real interaction when behavior changes. The detailed UI
  evidence rules below still apply. Generated reference-document updates alone
  are documentation, unless their rendering or application behavior changes.
- Authentication, tenancy, payments, migrations, security, and production data:
  verify the specific risk and retain every applicable approval and release
  prerequisite. Complexity or risk does not silently activate Orchestra.

This check scope replaces blanket local commands required for every task or
every PR elsewhere in the agent instructions. GitHub-required checks and reviews,
explicit task-specific verification, production approvals, data/secret safeguards,
and unresolved findings relevant to the change remain binding. Disclose unrelated
baseline failures; do not call them passing or weaken a protected check. An
unrelated baseline failure does not create a new local gate for a docs-only edit.
<!-- agent-work-mode:end -->

# Instructions for every AI agent

These instructions apply to Claude Code, ChatGPT, Codex, and other assistants.
The Conductor routes and independent reviews in CLAUDE.md apply on every host;
only model names, registration syntax, and hooks are host-specific. Existing
task scope, project safeguards, required checks, and release gates still apply.
These instructions grant no new permission for production changes, outbound
sends, secrets, credentials, destructive or bulk data changes, migrations,
payments, or crossing tenant boundaries.

This repository contains a completed QA audit. Preserve the original reports,
screenshots, tickets, and release evidence; do not present historical evidence
as verification of a later application change.

## Assistant attribution

Commit with explicit assistant attribution. A commit is attributable to the
assistant that made it, never silently to a human. Where the commit path
lets you set the author, including native git and Codex CLI, use your own
assistant identity: Claude Code: `Claude <noreply@anthropic.com>`;
Codex or ChatGPT: `ChatGPT <noreply@openai.com>`.
Where the commit path cannot set the author (such as ChatGPT's connected
GitHub tool), the user gives standing authorization, across sessions and
tasks, to commit under the connector's default connected account, provided
every such commit credits the assistant explicitly in its message: the
trailer `Co-Authored-By: ChatGPT <noreply@openai.com>`, or the matching
identity for another assistant, and, wherever the commit path allows a body
at all, a first line or body sentence naming the assistant that authored the
change through the connector. Do not pause or ask for a per-task authorship
exception solely because the connector cannot set the author: this rule is
that permission in advance. A commit under a person's account with no
assistant credit is still a violation. The permission covers only that
commit path's author limitation: a path that can set the author must use the
assistant identity, and no model names belong in the identity, trailer, or
credit sentence. Host-specific examples and historical handoff summaries do
not override this rule for another host. This attribution permission does
not expand the task's authorized scope or waive existing authorization
boundaries, required checks, independent review, or release and merge gates.

# Spec before build

Before large or materially ambiguous work, assemble a short brief covering the
goal, the scope, and the success criteria, after reading the relevant code, the
task's requirements, and the decisions already recorded. An existing request, an
accepted brief, or a task card that resolves those points is sufficient on its
own and is never re-confirmed; a brief that only restates already authorized
work is a progress update, so share it and proceed. Ask only about unresolved
choices that materially affect the outcome, the scope, permissions, data, or
behavior that is hard to reverse; state the reasonable reversible implementation
assumptions you are making and continue. Large work alone is not a reason to
seek another approval. Grilling stays optional, used when the requester asks for
it or accepts the offer. Routine fixes, questions, and clearly specified asks
need no brief.

# Continue past blockers

**Work around a blocked dependency.** When something the task needs is
unavailable, continue the authorized work: name exactly which steps depend on
the blocked thing, and do the rest. Reuse an existing tool or environment that
suits the job where you are already authorized to use it. Never weaken an
access control, change the requested outcome, expand the scope, or treat
missing evidence as a pass.

**Do not let a temporary capability problem consume the task.** Diagnose the
failure and try one reasonable supported recovery. When the same failure
recurs with no new evidence, change approach or defer the step that depends on
it; retry only when a changed condition or a concrete diagnosis makes another
attempt worth something. If authenticated testing is unavailable, state exactly
what stays unverified, continue the other authorized work, and keep any release
gate that depends on that evidence closed.

**Post progress updates.** In an attended session, report at meaningful
milestones and whenever a blocker changes the plan: what is complete, what is
blocked, what comes next. An update is not a request for permission. An
unattended run uses the job progress mechanism it already has.

**Never end a turn with only a promise to continue.** If authorized work
remains and a next step is available, perform it. If nothing can proceed, say
plainly that the work is paused, why, and the smallest action that resumes it.
Never imply work is continuing when nothing is running.

**Finish the authorized work that can be finished.** Pause the whole task only
when every useful remaining step depends on missing access, a decision only the
user can make, or authorization not yet given, and leave a precise record of
the remaining step and what would unblock it.

## Unattended work

In headless, scheduled, or board-dispatched work, continue the safe, reversible
steps the run is already authorized to take. Record material unresolved
questions on the PR or task card and stop only the dependent work. Existing
production and release boundaries still apply, and a run authorized only to
prepare a PR stays a PR-only run.
