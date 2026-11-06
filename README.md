# Claude Skills

A collection of reusable skills for Claude and compatible coding assistants. Each skill lives in its own directory and is described by a `SKILL.md` file. Some skills also include scripts, reference material, templates or evals in subdirectories.

## Contents

The repository holds 530 top-level skills. Most of them come from third-party collections; a few were written for this repository, such as `n8n-workflows`.

| Source | Notes |
|---|---|
| Initial collection | About 230 skills covering development, design, marketing, security research and productivity |
| event4u-app/agent-config | 297 skills from `dist/agent-src/skills`, imported under the MIT license. Skills that already existed here (`brand`, `churn-prevention`, `customer-research`, `humanizer`) kept their earlier versions |
| [heydamir/unslop](https://github.com/heydamir/unslop) | `unslop` at commit a6f121e, CC BY 4.0 by Damir Sokolovsky. Removes AI-looking patterns from UI. Licence and credit kept in the skill directory |

Imported skills are kept as published upstream. Licence files and notices that ship inside a skill directory stay with that skill.

## Find a skill

Start with the [skill index](INDEX.md), then read the selected skill's instructions and prerequisites.

## Local setup

```bash
git clone https://github.com/jeaxes/claude-skills-public.git ~/.claude/skills-repo
```

Copy the skill directories you need into the skills directory your assistant reads, keeping their relative files. Check for an existing installation of the same name before replacing it.

## Cloud environments

Install skills at session start through your environment's setup script. This repository does not ship a setup script.

## Security

Skills can tell an assistant to run commands. Review a skill and any bundled scripts before installing it. The security-testing skills (`hunt-*`, `*-attack`, `offensive-osint` and similar) are for systems you are authorized to test. See [SECURITY.md](SECURITY.md) for reporting issues.

## Conventions

Repository documentation, issues, pull requests and new commit messages use English. Individual skills may request another language for their generated output.

See [contributing conventions](CONTRIBUTING.md).
