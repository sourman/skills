# Skills

Collection of reusable skills for AI coding agents.

## Structure

Each skill is in its own directory at the repository root:

```
skills/
├── supabase-workflow/
│   └── SKILL.md
├── skill-create/
│   └── SKILL.md
└── [other-skills]/
    └── SKILL.md
```

## Usage

Install individual skills using `bun x skills`:

```bash
# Install a specific skill
bun x skills add sourman/skills/supabase-workflow

# List installed skills
bun x skills list

# Check for updates
bun x skills check
```

## Skills

### [supabase-workflow](supabase-workflow/SKILL.md)
Supabase database migrations, type generation, edge function management, and best practices.

### [skill-create](skill-create/SKILL.md)
Instructions for AI agents to create new skills and add them to this repository.

## Contributing

To add a new skill to this repository:

```bash
# Clone the repository
git clone git@github.com:sourman/skills.git /tmp/skills
cd /tmp/skills

# Install the skill-create skill first
bun x skills add sourman/skills/skill-create

# Then invoke the skill to create new skills
```

The `skill-create` skill provides complete instructions for:
- Creating new skill directories
- Writing proper SKILL.md files with frontmatter
- Committing and pushing changes
- Best practices for skill structure

## Resources

- [skills.sh](https://skills.sh/) - Directory and leaderboard for skill packages
- [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) - Reference implementation
