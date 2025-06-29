# Fabric Fast-Track Gotchas & Lessons Learned

*Living document - update whenever we hit a snag*

## Deployment Issues
- **F-SKU capacity**: F2 minimum required for Direct Lake; F4+ recommended for production
- **Region availability**: Not all Azure regions support Fabric capacity yet
- **Workspace limits**: 100 workspace limit per tenant (can request increase)

## Data Pipeline Issues  
- **Dataflow Gen2 refresh**: Sometimes fails silently - always check logs
- **Delta table optimization**: Run OPTIMIZE after large ingests for better performance
- **Gateway connections**: On-premises gateway can timeout with large datasets

## Power BI & Semantic Model
- **Direct Lake limitations**: Some DAX functions not supported in Direct Lake mode
- **Refresh timing**: Semantic model refresh can take 5-10min on first run
- **RLS performance**: Complex RLS rules can slow query performance significantly

## AI Assistant
- **Token limits**: GPT-4 has 8K context limit - chunk large prompts
- **Cost monitoring**: Daily spend can spike during development - set alerts
- **Offline mode**: Always test offline fallbacks before demos

## DevOps & CI/CD
- **Fabric API delays**: Workspace operations can take 30-60 seconds to propagate
- **Deployment pipeline**: Test -> Prod promotion requires admin approval
- **Version control**: .bim files are XML - use proper merge strategies

---
*Last updated: 2025-06-28*

## Python Development Issues

### F-String Quote Escaping Hell
**Problem**: Complex f-strings with mixed single/double quotes create impossible bash command line escaping scenarios when trying to fix via sed or inline Python commands.

**Example**: 


**Root Cause**: Multiple quote escaping layers (bash → Python → regex → f-string) become unmanageable.

**Solutions**:
1. **Use .format() method instead** - eliminates nested quote issues entirely
2. **Create Python scripts in separate files** - avoid bash command line quote complexity  
3. **Use triple quotes** for complex strings when possible
4. **Avoid sed for complex Python string manipulation** - use dedicated Python scripts

**Lesson**: When automated fixes fail repeatedly due to quote escaping, step back and change the approach rather than fighting the escaping layers.

---
*Updated: 2025-06-29 - Claude Code f-string fix attempts*


## Python Development Issues

### F-String Quote Escaping Hell
**Problem**: Complex f-strings with mixed single/double quotes create impossible bash command line escaping scenarios when trying to fix via sed or inline Python commands.

**Example**: 


**Root Cause**: Multiple quote escaping layers (bash → Python → regex → f-string) become unmanageable.

**Solutions**:
1. **Use .format() method instead** - eliminates nested quote issues entirely
2. **Create Python scripts in separate files** - avoid bash command line quote complexity  
3. **Use triple quotes** for complex strings when possible
4. **Avoid sed for complex Python string manipulation** - use dedicated Python scripts

**Lesson**: When automated fixes fail repeatedly due to quote escaping, step back and change the approach rather than fighting the escaping layers.

---
*Updated: 2025-06-29 - Claude Code f-string fix attempts*


## Python Development Issues

### F-String Quote Escaping Hell
**Problem**: Complex f-strings with mixed single/double quotes create impossible bash command line escaping scenarios when trying to fix via sed or inline Python commands.

**Example**: 


**Root Cause**: Multiple quote escaping layers (bash → Python → regex → f-string) become unmanageable.

**Solutions**:
1. **Use .format() method instead** - eliminates nested quote issues entirely
2. **Create Python scripts in separate files** - avoid bash command line quote complexity  
3. **Use triple quotes** for complex strings when possible
4. **Avoid sed for complex Python string manipulation** - use dedicated Python scripts

**Lesson**: When automated fixes fail repeatedly due to quote escaping, step back and change the approach rather than fighting the escaping layers.

---
*Updated: 2025-06-29 - Claude Code f-string fix attempts*
