# Persistence Model

**Critical concept to explain to users**:

Skills installed by this tool are **per-project** and **persistent**:

1. **Installation**: Skills copied to `.claude/skills/nixtla-*` in current project
2. **Persistence**: Skills remain there until explicitly updated or removed
3. **Updates**: Opt-in via `nixtla-skills update` (not automatic)
4. **Offline**: Skills are local files, work without internet
5. **Version control**: Different projects can have different skill versions

## Benefits

- Predictable behavior (skills don't change unexpectedly)
- Offline usage (skills are local)
- Project isolation (changes in one project don't affect others)

## Trade-off

- Manual updates required (run `nixtla-skills update` to get latest)

## Self-Referential Nature

**Installed location**: `.claude/skills/nixtla-skills-bootstrap/`
**Self-referential**: This skill can update itself via `nixtla-skills update`
