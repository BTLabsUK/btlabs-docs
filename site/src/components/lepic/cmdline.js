import React from 'react';
import {Cmd} from './kit';

/* A command as LEPIC's docs write it, on the terminal surface. A trailing `  # comment` on a
 * line shows dim on its own line under the command and is left out of what the copy button
 * copies. Several lines stay several
 * lines (a backslash continuation or two commands). */
const NOTE = /^(.*?\S)(\s{2,}#\s?.*)$/;

export function splitCmd(cmd) {
  const lines = cmd.split('\n').map((ln) => {
    const m = ln.match(NOTE);
    return m ? {code: m[1], note: m[2]} : {code: ln, note: ''};
  });
  return {lines, copy: lines.map((l) => l.code).join('\n')};
}

export default function CmdLine({cmd, prompt = true, label = 'Copy command', className}) {
  const {lines, copy} = splitCmd(cmd);
  if (lines.every((l) => !l.note)) {
    return (
      <Cmd prompt={prompt} label={label} className={className}>
        {cmd}
      </Cmd>
    );
  }
  return (
    <Cmd prompt={prompt} label={label} className={className} copy={copy}>
      {lines.map((l, i) => (
        <React.Fragment key={i}>
          {i > 0 && '\n'}
          {l.code}
          {l.note && '\n'}
          {l.note && <span className="ldCmd-note">{l.note.trim()}</span>}
        </React.Fragment>
      ))}
    </Cmd>
  );
}
