# Learner runtime v2

Runtime v2 keeps the maintained source fully auditable while making each learner unit operate from a minimal temporary workspace.

The public behavior and architecture are documented in the root README and `docs/ARCHITECTURE.md`. This file records only the migration invariant: learner-visible lesson content lives in the course Issue; temporary exercise artifacts are created only for the active unit and cleaned after validation.
