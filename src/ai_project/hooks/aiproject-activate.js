#!/usr/bin/env node
/**
 * AI Project - Claude Code SessionStart Activation Hook
 *
 * Runs on every session start:
 *   1. Writes flag file at ~/.aiproject/.aiproject-active
 *   2. Emits ruleset as hidden SessionStart context
 *   3. Detects missing statusline config and emits setup nudge
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

const DEFAULT_MODE = process.env.AIPROJECT_DEFAULT_MODE || 'full';

const homeDir = os.homedir();
const aiProjectDir = path.join(homeDir, '.aiproject');
const flagPath = path.join(aiProjectDir, '.aiproject-active');
const settingsPath = path.join(homeDir, '.claude', 'settings.json');

const mode = DEFAULT_MODE;

if (mode === 'off') {
    try { fs.unlinkSync(flagPath); } catch (e) {}
    process.stdout.write('OK');
    process.exit(0);
}

try {
    fs.mkdirSync(path.dirname(flagPath), { recursive: true });
    fs.writeFileSync(flagPath, mode);
} catch (e) {
    // Silent fail -- flag is best-effort, don't block the hook
}

const INDEPENDENT_MODES = new Set(['commit', 'review', 'compress']);

if (INDEPENDENT_MODES.has(mode)) {
    process.stdout.write('AI PROJECT MODE ACTIVE — level: ' + mode);
    process.exit(0);
}

process.stdout.write('AI PROJECT MODE ACTIVE — level: ' + mode + '\n\n' +
    'Respond terse. All technical substance stay. Only fluff die.\n\n' +
    'Rules:\n' +
    '- Drop: articles (a/an/the), filler (just/really/basically/actually/simply), pleasantries\n' +
    '- Fragments OK\n' +
    '- Short synonyms\n' +
    '- Code blocks unchanged\n' +
    '- Errors quoted exact\n\n' +
    'Pattern: [thing] [action] [reason]. [next step].'
);
