// PreToolUse hook (Bash|PowerShell): refuses a review-contour page launch under `timeout` — the page server dies with the
// launcher and the owner sees «СЕРВЕР КОНТУРА НЕДОСТУПЕН» (EXP-0013 2026-11-13, EXP-0024 2026-11-17). Print-and-exit flags
// (--list, --check, --call, --mark-*, --search, --selftest, --why, --where) pass. Wire: .claude/settings.json →
// hooks.PreToolUse [{ matcher: "Bash|PowerShell", hooks: [{ type: "command", command: "node",
// args: ["${CLAUDE_PROJECT_DIR}/tools/hooks/pretool-deny-server-timeout.mjs"] }] }].
// Self-test: node tools/hooks/pretool-deny-server-timeout.mjs --selftest
const PRINT_FLAGS = /--(list|check|call|mark-[a-z]+|search|selftest|why|where|close)\b/;
const UNDER_TIMEOUT = /(^|[\s;&|(])timeout\s+[^;&|]*review\.mjs/;

export function verdict(command) {
  if (typeof command !== 'string' || !UNDER_TIMEOUT.test(command)) return null;
  if (PRINT_FLAGS.test(command)) return null;
  return 'review.mjs serves a page the owner looks at; under `timeout` its server dies with the launcher (EXP-0013, ' +
    'EXP-0024). Launch it with run_in_background and check the port with curl instead.';
}

if (process.argv.includes('--selftest')) {
  const cases = [
    ['timeout 20 node .kaif/tools/contour/review.mjs --queue --silent', true],
    ['timeout 60 node .kaif/tools/contour/review.mjs interviews/x.md', true],
    ['node .kaif/tools/contour/review.mjs --queue --silent', false],
    ['timeout 20 node .kaif/tools/contour/review.mjs --queue --list', false],
    ['timeout 5 node .kaif/tools/contour/review.mjs x.md --check', false],
    ['timeout 30 sh tools/sim_run.sh a b c', false],
  ];
  let bad = 0;
  for (const [cmd, deny] of cases) {
    const got = verdict(cmd) !== null;
    if (got !== deny) { bad++; console.log('FAIL', deny ? 'should deny:' : 'should pass:', cmd); }
  }
  console.log(bad ? `selftest: ${bad} failed` : `selftest: ${cases.length} ok`);
  process.exit(bad ? 1 : 0);
}

let input = '';
process.stdin.on('data', (chunk) => { input += chunk; });
process.stdin.on('end', () => {
  let command = '';
  try { command = JSON.parse(input || '{}')?.tool_input?.command ?? ''; } catch { /* not ours to judge */ }
  const reason = verdict(command);
  if (reason) {
    process.stdout.write(JSON.stringify({ hookSpecificOutput: { hookEventName: 'PreToolUse',
      permissionDecision: 'deny', permissionDecisionReason: reason } }));
  }
});
