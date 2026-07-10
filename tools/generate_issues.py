#!/usr/bin/env python3
"""Generate docs/troubleshooting-and-lessons.md from index.html.

Run it from inside the app's folder after any data change:

    Windows:       python tools\\generate_docs.py
    Mac or Linux:  python3 tools/generate_docs.py

It reads index.html, extracts the project data between the two data
markers, and rewrites the Markdown file. The app's data block is the
single source of truth: edit copy there, run this, and never edit the
generated file by hand. Plain Python, no installs needed.
"""
import json
import os
import sys

START = '/*' + '__STEPS_DATA_START__' + '*/'
END = '/*' + '__STEPS_DATA_END__' + '*/'


def main():
    if not os.path.exists('index.html'):
        sys.exit("No index.html here. Run this from inside the app's folder, "
                 "for example: python3 tools/generate_docs.py")

    src = open('index.html', encoding='utf-8').read()
    if START not in src or END not in src:
        sys.exit('Could not find the data markers in index.html.')

    data = json.loads(src.split(START)[1].split(END)[0])
    steps = data['steps']

    lines = []
    out = lines.append

    out(f"# {data['title']}: troubleshooting and lessons")
    out('')
    out('Generated from the data inside index.html by tools/generate_docs.py.')
    out('Never edit this file by hand: change the app data and regenerate.')
    out('')
    out(f"> {data['tagline']}")
    out('')

    # ---- Global issues first: the problems that hit every setup ----
    out('## Issues that can hit any setup')
    out('')
    any_global = False
    for idx, s in enumerate(steps, 1):
        for issue in s.get('issues', []):
            if 'All setups' in issue['tags']:
                any_global = True
                out(f"### {issue['problem']}")
                out('')
                out(f"*Seen at step {idx}: {s['title']}*")
                out('')
                out(issue['fix'])
                out('')
    if not any_global:
        out('None recorded yet.')
        out('')

    # ---- Remaining issues, grouped by step, with their tags ----
    out('## Setup-specific issues, step by step')
    out('')
    any_local = False
    for idx, s in enumerate(steps, 1):
        local = [i for i in s.get('issues', []) if 'All setups' not in i['tags']]
        if not local:
            continue
        any_local = True
        out(f"### Step {idx}: {s['title']}")
        out('')
        for issue in local:
            tags = ', '.join(issue['tags'])
            out(f"**{issue['problem']}** ({tags})")
            out('')
            out(issue['fix'])
            out('')
    if not any_local:
        out('None recorded yet.')
        out('')

    # ---- The full step outline ----
    out('## The full journey, step by step')
    out('')
    for idx, s in enumerate(steps, 1):
        out(f"### Step {idx}: {s['title']}")
        out('')
        out(s['intro'])
        out('')
        out(f"You're done when: {s['done']}")
        out('')

    os.makedirs('docs', exist_ok=True)
    path = os.path.join('docs', 'troubleshooting-and-lessons.md')
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines).rstrip() + '\n')
    print(f"wrote {path} ({len(lines)} lines, {len(steps)} steps)")


if __name__ == '__main__':
    main()
