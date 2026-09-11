<!-- agent-work-mode:start -->
# Work mode: direct

Work directly. The owner retired the orchestra (the Conductor Protocol, its
subagent seats, routes, Judges and spend tables) on 2026-09-11, a day after
making it opt-in: it cost more time than it saved. This applies to every
assistant and every authorized team member.

Use the current session agent for ordinary work. Do not hire an implementer,
architect, verifier or judge on your own, switch models, prepare staffing or
cost tables, or offer a brief for an already clear request. A request for one
reviewer or one subagent authorizes that bounded role and nothing more.
Independent review is asked for, not routed: CLAUDE.md, "Independent review,
on request", says when and how.

## Verification in direct mode

Choose checks from the actual diff and its consequences:

- Documentation, indexes, handoffs, and agent instructions: review the diff,
  references, links and paths, and syntax. These changes alone do not
  require a build, a browser, or a re-run of the audit.
- Scripts: run the changed script against a realistic input and paste the
  output. Reasoning about unrun code is not evidence.
- The archived evidence: a change that touches the reports, screenshots,
  tickets or release evidence is a change to the historical record; verify
  it is the change that was asked for and nothing more, and never present
  the archive as verification of a later application change. Complexity or
  risk is the cue to ask for an independent review (CLAUDE.md, "Independent
  review, on request"), never to skip these checks.

This check scope replaces blanket local commands required for every task or
every PR elsewhere in the agent instructions. Explicit task-specific
verification, data/secret safeguards, and unresolved findings relevant to the
change remain binding. Disclose unrelated baseline failures; do not call them
passing. An unrelated baseline failure does not create a new local gate for a
docs-only edit.
<!-- agent-work-mode:end -->

# This repository is a completed QA audit

This repository contains a completed QA audit. Preserve the original reports,
screenshots, tickets, and release evidence; do not present historical evidence
as verification of a later application change. The repository is public:
nothing committed here may carry credentials, personal data, or internal
hostnames (rule 5 below).

# Rules for any AI agent (read first)

These apply to every AI assistant working in this repo, Claude Code,
Codex/ChatGPT, or any other, and are not optional. "The user" is whoever is
directing the agent: the repo owner or an authorized team member.
Tool-specific workflow (the shipping/merge flow, the review-on-request note)
lives in CLAUDE.md and binds Claude Code; the rules here bind every tool.
These rules are a floor, not a ceiling: where CLAUDE.md or another
repo-specific rule is stricter, the stricter one wins. Host-specific parts
(model names, spawning syntax) live in CLAUDE.md; never let a host's limits
lower the floor below.

1. Autonomy above a hard floor. Routine, reversible, in-scope changes that pass
   their gates (any review that was asked for passed, and the change staying
   inside a scope the user already approved) may deploy, merge, migrate, and
   self-run without asking. For anything on the floor the agent stops for the
   user's explicit, per-action word; it also stops for anything CLAUDE.md or
   another repo rule adds to the floor, and it never lowers the floor on its
   own. The floor, never crossed autonomously:
   - Landing or triggering a send to an external or customer-facing service:
     email, SMS, third-party posts, an outbound webhook. This covers the deploy
     or merge that starts the send, not only the agent calling the service by
     hand, and it covers the flag, settings toggle, or variable whose flip
     starts one. It does not cover this repo's own git host, which the agent
     uses to do its work.
   - Destructive or bulk data mutations, and anything that moves money or
     crosses a tenant boundary. Removing or rewriting archived evidence is
     a destructive mutation here.
   - A schema change that is irreversible or wide in blast radius: a drop, a
     rename, a backfill, or a migration whose mis-ordering could take
     production down. A forward-only additive migration is not on the floor and
     ships on its own.
   Not on the floor, by Brian's standing authorization of 2026-09-11:
   environment and service variables, feature flags and settings that start
   no send, and the secrets and credentials the work needs, in any
   environment including production. Set, change, and rotate them without
   asking, say what changed in the PR or the chat, and keep the values
   themselves out of anything written down (rule 5). Brian does not want to
   be asked.
   A standing authorization the user has written down is their word given in
   advance: it grants autonomy for exactly the action and scope it names, no
   wider, and does not loosen the floor for anything else.
2. Schema before code, in the safe order for the change. For an additive
   migration, apply and confirm it first, then land the code that reads it. For
   a removal (a drop or rename), deploy the code that stops using the column or
   table first, then run the migration that removes it. Never sequence a schema
   change and its code so that production reads a shape that is not there yet.
3. Verify, don't guess. Check primary sources; never fabricate data, prices,
   IDs, results, or file contents. If unsure or blocked, say so plainly.
4. Prove it. Anything user-visible gets looked at rendered whenever the
   tooling to render it is at hand; anything executable gets run with its
   real output pasted. A claim with no evidence behind it is not done, and
   evidence is never invented. When the environment cannot produce a piece
   of it, say exactly what is missing and why, in the chat and in the PR,
   and carry on: missing evidence is reported, never faked, and never on its
   own a reason to hold a merge.
5. Keep secrets and data in. No credentials, tokens, or keys in commits, PR
   text, code comments, or anything sent to an external service, and no
   customer or personal data (names, contact details, policy or lead records)
   in any of those either. This repository is public, so the rule covers
   every file in it, not only PR text. Keep internal hostnames out of
   everything committed and sent outward.
6. Attribution is not a gate (Brian, 2026-09-11). Commit with the author
   identity and trailers your host sets by default: Claude Code sets
   `Claude <noreply@anthropic.com>` and its own `Co-Authored-By` and
   `Claude-Session` trailers; ChatGPT's connected GitHub tool commits as the
   connected account; Codex CLI can set `ChatGPT <noreply@openai.com>`. Where
   the host does not name the assistant in the author field, one line in the
   message crediting the assistant is enough. Never pause, ask for an
   exception, amend, or re-author a commit over attribution, and never strip
   a model name or session link from a trailer the host wrote. This replaces
   the "Assistant attribution" rule and its connector permission; nothing in
   this repo checks the author.
7. Smallest reversible change. Don't widen scope on your own; for anything hard
   to reverse or outward-facing, confirm first.
8. When no human is watching, carry the work through. In a headless,
   scheduled, or board-dispatched run with no attended requester, take the
   confirmed task through every safe, reversible step the run's existing
   authorization already covers. Do not invent missing requirements: record a
   material unresolved question on the PR or the card and keep going on the
   work that does not depend on it, stopping only the branch of work that
   question actually blocks, and stopping the task only when nothing useful
   remains. Never take a floor action (rule 1) in such a run, and a run
   authorized only to prepare a pull request stays a PR-only run.

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
