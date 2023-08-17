# universal-migration-agent
UMA is an LLM-Agent that automates the process of migrating existing codebases.

## How do I set UMA up?
1. Define what migration process you desire in ```migration_config.json```.
2. Extract your codebase in the ```to-migrate/``` directory. Upon load UMA will scan this dir and analyze it.
3. Your migrated codebase will be found in the ```/migrated``` directory.