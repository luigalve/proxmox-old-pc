#!/usr/bin/env python3
"""Generate docs/full-walkthrough.md from index.html: the whole app in one file.

The companion to generate_docs.py. Where that script produces the
troubleshooting summary, this one exports EVERYTHING: every step's
intro, prerequisites, actions (with code blocks and both fork
variants), every cheat table, every issue, and every checkpoint,
as one well-formatted Markdown file. It exists so someone who cannot
finish inside the app can take the complete guide with them, and so
a README can link one printable version of the whole journey.

Run it from inside the app's folder after any data change:

    Windows:       python tools\\generate_full_guide.py
    Mac or Linux:  python3 tools/generate_full_guide.py

The app's data block stays the single source of truth: edit copy
there, rerun this, and never edit the generated file by hand.
Plain Python, no installs needed.
"""
import json
import os
import sys

START = '/*' + '__STEPS_DATA_START__' + '*/'
END = '/*' + '__STEPS_DATA_END__' + '*/'


def cell(text):
    """Make one table cell safe for a Markdown table row."""
    return text.replace('|', '\\|').replace('\n', ' ')


def main():
    if not os.path.exists('index.html'):
        sys.exit("No index.html here. Run this from inside the app's folder, "
                 "for example: python3 tools/generate_full_guide.py")

    src = open('index.html', encoding='utf-8').read()
    if START not in src or END not in src:
        sys.exit('Could not find the data markers in index.html.')

    data = json.loads(src.split(START)[1].split(END)[0])
    steps = data['steps']
    forks = data.get('forkTags', {'older': 'Older', 'newer': 'Newer'})

    lines = []
    out = lines.append

    out(f"# {data['title']}: the complete guide")
    out('')
    out('Generated from the data inside index.html by tools/generate_full_guide.py.')
    out('Never edit this file by hand: change the app data and regenerate.')
    out('')
    out(f"> {data['tagline']}")
    out('')
    out(f"This is the whole walkthrough in one file: every step, action, "
        f"cheat sheet, and fix. Where instructions differ by setup, both "
        f"versions appear, labeled **{forks['older']}** and **{forks['newer']}**. "
        f"The interactive version of this guide is the index.html app in this repo.")
    out('')

    # ---- Table of contents ----
    out('## The journey at a glance')
    out('')
    for idx, s in enumerate(steps, 1):
        out(f"{idx}. {s['title']}")
    out('')

    def emit_action_line(num, text):
        out(f"{num}. {text}")

    def emit_code(code, indent='    '):
        out('')
        out(indent + '```')
        for cl in code.split('\n'):
            out(indent + cl)
        out(indent + '```')
        out('')

    def emit_actions(action_list):
        for n, a in enumerate(action_list, 1):
            if isinstance(a, str):
                emit_action_line(n, a)
                continue
            newer, older = a.get('text'), a.get('older')
            if older and newer and older != newer:
                emit_action_line(n, f"**{forks['newer']}:** {newer}")
                out(f"    **{forks['older']}:** {older}")
            else:
                emit_action_line(n, newer or older)
            code = a.get('code')
            if isinstance(code, str):
                emit_code(code)
            elif isinstance(code, dict):
                for side in ('older', 'newer'):
                    if code.get(side):
                        out('')
                        out(f"    {forks[side]}:")
                        emit_code(code[side])

    def emit_table(t):
        out(f"**{t['title']}**" if t.get('title') else '**Cheat sheet**')
        out('')
        cols = t['cols']
        out('| ' + ' | '.join(cell(c) for c in cols) + ' |')
        out('|' + '---|' * len(cols))
        for r in t['rows']:
            if isinstance(r, dict):
                for side in ('older', 'newer'):
                    if r.get(side):
                        row = list(r[side])
                        row[0] = f"{row[0]} ({forks[side]})"
                        out('| ' + ' | '.join(cell(c) for c in row) + ' |')
            else:
                out('| ' + ' | '.join(cell(c) for c in r) + ' |')
        out('')

    # ---- The full walkthrough ----
    for idx, s in enumerate(steps, 1):
        out(f"## Step {idx}: {s['title']}")
        out('')
        out(s['intro'])
        out('')

        if s.get('prereqs'):
            out('**What you need:**')
            out('')
            for p in s['prereqs']:
                out(f"- {p}")
            out('')

        if s.get('methods'):
            label = s.get('methodsLabel', 'Pick your path')
            out(f"*{label}: this step has {len(s['methods'])} paths. Follow one.*")
            out('')
            for mname, m in s['methods'].items():
                out(f"### Path: {mname}")
                out('')
                emit_actions(m['actions'])
                out('')
        else:
            out('**Actions:**')
            out('')
            emit_actions(s.get('actions', []))
            out('')

        for t in ([s['cheat']] if isinstance(s.get('cheat'), dict) else s.get('cheat') or []):
            emit_table(t)

        issues = s.get('issues', [])
        if issues:
            out('**If something goes wrong:**')
            out('')
            for issue in issues:
                tags = ', '.join(issue['tags'])
                out(f"- **{issue['problem']}** ({tags})")
                out(f"  {issue['fix']}")
                out('')

        out(f"**You're done when:** {s['done']}")
        out('')

    if data.get('congratsAfter'):
        out('## The finish line')
        out('')
        out(data['congratsAfter'])
        out('')

    os.makedirs('docs', exist_ok=True)
    path = os.path.join('docs', 'full-walkthrough.md')
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines).rstrip() + '\n')
    print(f"wrote {path} ({len(lines)} lines, {len(steps)} steps)")


if __name__ == '__main__':
    main()
