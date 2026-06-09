# Rollback Runbook

## Before AD Promotion

- Remove created artifacts, logs, and state files.
- Revert network and hostname changes as needed.

## After Role Installation but Before Promotion

- Uninstall explicitly added roles if approved.
- Remove DHCP scopes, DNS zones, and GPOs created by automation.

## After AD Promotion

- Evaluate whether rollback is riskier than rebuild.
- Follow AD DS recovery policy; use restore runbook for supported recovery steps.

## DHCP Scope Rollback

- Remove created scopes and reservations in reverse order.
- Verify no production clients depend on removed scopes.

## GPO Rollback

- Unlink created GPOs.
- Remove GPO objects only after impact assessment.

## DNS Rollback

- Remove reverse zones and forwarders set by automation.
- Validate AD-integrated DNS dependencies before deletion.

## Service Account and Group Cleanup

- Remove created service accounts and groups when no longer referenced.

## When Rebuild Is Cleaner Than Rollback

- If domain promotion completed and rollback risk is high, rebuild from known-good image and restore from validated backups.
