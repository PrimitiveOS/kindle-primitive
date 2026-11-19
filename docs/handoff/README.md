# PrimitiveOS handoff

Updated 20 November 2026. Store is a standalone app, and Launcher offers one Store tile to open or install it.
The **Study and work** collection is live with seven new apps and four updates. Oasis 3 testing for these eleven
releases remains open. [Current state](STATE.md) · [Implementation plan](../implementation-plan.md)

## Current references

1. [State](STATE.md) records the published versions, the checks that passed, and the latest device observation.
2. [Implementation plan](../implementation-plan.md) tracks milestones and outstanding device checks.
3. [Rules](RULES.md) records the owner's instructions for Git, releases, icons, licences, and device access.
4. [Environment](ENVIRONMENT.md) describes the build tools, SSH helper, and log locations.
5. [Install and update apps](../store-install-apps.md) describes the current setup and Store flows.
6. [App directory](../../README.md#the-apps) links to each first-party GitHub repository and its Store release.

Primitive Launcher is the only app installed manually during initial setup. For an existing setup, open the installed
Launcher and use Store for the other apps. Prepare device checks on the Mac, then coordinate any required taps or
restarts with the owner.

## Original Store handoff

The [architecture snapshot](ARCHITECTURE.md), [Store implementation notes](STORE-APP.md), and [original pipeline](PIPELINE.md)
record the 19 November 2026 standalone Store handoff. Use the [current implementation plan](../implementation-plan.md)
for release and milestone status. The [local verification report](../local-verification.md) records the desktop work
that followed the original snapshot.
