# universal-migration-agent
UMA is an LLM-Agent that automates the process of migrating existing codebases.

## How do I set UMA up?
Define what migration process you desire in ```migration_config.json```.

Extract your codebase in the ```to-migrate/``` directory. Upon load UMA will scan this dir and analyze it.

Your migrated codebase will be found in the ```/migrated``` directory.