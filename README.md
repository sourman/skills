# Agent Skills

Collection of reusable skills for AI coding agents.

## Structure

Each skill is in its own directory under `skills/`:

```
skills/
├── supabase-workflow/
│   └── SKILL.md
└── [other-skills]/
    └── SKILL.md
```

## Usage

Install individual skills using `bun x skills`:

```bash
# Install a specific skill
bun x skills add <username>/agent-skills/skills/supabase-workflow

# List installed skills
bun x skills list
```

## Skills

### [supabase-workflow](skills/supabase-workflow/SKILL.md)
Supabase database migrations, type generation, edge function management, and best practices.

## Contributing

Add new skills by creating a new directory under `skills/` with a `SKILL.md` file.

## Resources

- [skills.sh](https://skills.sh/) - Directory and leaderboard for skill packages
- [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) - Reference implementation
