# PrimitiveOS handoff

Status date: 2026-11-19. Written for: one autonomous agent that continues the work without stopping, until it needs the
owner. The owner is away for a while.

The [local verification report](../local-verification.md) records the implementation and simulation that followed this snapshot.

Read in this order:

1. [STATE.md](STATE.md): every repo, its branch, its last commit, the versions, and what is on the Kindle.
2. [RULES.md](RULES.md): the owner's rules (secrets, staging, commits, deploys, icons, releases). Follow them exactly.
3. [ENVIRONMENT.md](ENVIRONMENT.md): how to build, test, and reach the Kindle from this Mac, and the known traps.
4. [ARCHITECTURE.md](ARCHITECTURE.md): how the pieces fit: the launcher, the store, the shared kit, the catalog, the build.
5. [STORE-APP.md](STORE-APP.md): every function in the store app and the shared code it uses, what each does, and the
   design of every feature not built yet.
6. [PIPELINE.md](PIPELINE.md): the ordered work to do, with the checks and the stop points. Start at the first open item.

The application to finish is **Primitive Store** (`doannt-kindle-store`). The launcher only needs a small bootstrap change
later. Everything else (catalog, build, browser package, shared kit) is in place and tested on the Mac.

Testing on the real Kindle: the owner must be present for every device step (the Kindle's screen is the test). Everything
that can be built and tested on the Mac is done without the owner. A device step is prepared on the Mac first, and the
owner is asked for the one action that needs a hand (a tap, a button press, a restart).
