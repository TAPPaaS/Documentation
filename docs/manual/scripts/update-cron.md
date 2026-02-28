---
title: update-cron.sh
description: Set up hourly update cron job
---

# update-cron.sh

Creates a cron entry to run the TAPPaaS update scheduler every hour.

## Usage

```bash
update-cron.sh
```

## What it does

- Removes any existing `update-tappaas` cron entries
- Creates a new cron entry for user `tappaas` to run hourly (at minute 0)
- The `update-tappaas` command handles all scheduling logic internally, checking the global `updateSchedule` to determine if updates should run

## Cron entry created

```
0 * * * * /home/tappaas/bin/update-tappaas
```

## Why hourly?

Running hourly ensures the scheduled hour will be matched. The `update-tappaas` script only performs updates when the current hour matches the global `updateSchedule` hour.

## See Also

- [Update Scheduler](../update-tappaas.md) - Automated update system
