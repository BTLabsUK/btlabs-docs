import React, {useCallback, useEffect, useRef, useState} from 'react';
import clsx from 'clsx';

/* The parts every LEPIC docs component shares. Their classes are in src/css/lepic.css. */

const ICONS = {
  copy: (
    <g fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinejoin="round">
      <rect x="8.5" y="8.5" width="11" height="11" rx="2" />
      <path d="M15.5 8.5v-2a2 2 0 0 0-2-2h-7a2 2 0 0 0-2 2v7a2 2 0 0 0 2 2h2" strokeLinecap="round" />
    </g>
  ),
  check: <path fill="none" stroke="currentColor" strokeWidth="1.9" strokeLinecap="round" strokeLinejoin="round" d="m5 12.5 4.5 4.5L19 7.5" />,
  search: (
    <g fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round">
      <circle cx="11" cy="11" r="6.5" />
      <path d="m16 16 4.5 4.5" />
    </g>
  ),
  arrowRight: <path fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round" d="M4.5 12h15m-6-6 6 6-6 6" />,
  arrowDown: <path fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m-6-6 6 6 6-6" />,
  chevron: <path fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round" d="m9 5.5 6.5 6.5L9 18.5" />,
  link: (
    <g fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round">
      <path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1" />
      <path d="M14 10a4 4 0 0 0-5.7 0l-3 3A4 4 0 0 0 11 18.7l1-1" />
    </g>
  ),
};

/** A 24px line icon. Decorative: the text beside it says what it is. */
export function LdIcon({name, className}) {
  return (
    <svg className={className} viewBox="0 0 24 24" aria-hidden="true" focusable="false">
      {ICONS[name]}
    </svg>
  );
}

/** Copies `text`. `label` names what is copied for a screen reader ("Copy command"). */
export function CopyButton({text, label = 'Copy', plain = false, className}) {
  const [copied, setCopied] = useState(false);
  const timer = useRef(null);
  useEffect(() => () => clearTimeout(timer.current), []);
  const copy = useCallback(async () => {
    try {
      await navigator.clipboard.writeText(text);
    } catch {
      const area = document.createElement('textarea');
      area.value = text;
      area.setAttribute('readonly', '');
      area.style.position = 'fixed';
      area.style.opacity = '0';
      document.body.appendChild(area);
      area.select();
      document.execCommand('copy');
      area.remove();
    }
    setCopied(true);
    clearTimeout(timer.current);
    timer.current = setTimeout(() => setCopied(false), 1600);
  }, [text]);
  return (
    <button
      type="button"
      className={clsx('ldCopy', plain && 'ldCopy--plain', className)}
      data-copied={copied}
      aria-label={label}
      onClick={copy}>
      <LdIcon name={copied ? 'check' : 'copy'} />
      <span className="ldSr" aria-live="polite">
        {copied ? 'Copied' : ''}
      </span>
    </button>
  );
}

/** One command line on the terminal surface with its copy button.
 *  `prompt={false}` drops the `$` (for a call such as `POST /payments`). */
export function Cmd({children, copy, prompt = true, label = 'Copy command', className}) {
  const text = typeof children === 'string' ? children : copy;
  return (
    <div className={clsx('ldTerm ldCmd', !prompt && 'ldCmd--bare', className)}>
      <code className="ldCmd-text" translate="no">{children}</code>
      {(copy ?? text) != null && <CopyButton text={copy ?? text} label={label} />}
    </div>
  );
}

/** `kind`: core, repair, or an HTTP method (get, post, put, patch, delete). The word is always shown. */
export function Tag({kind, children}) {
  const k = String(kind || '').toLowerCase();
  const method = ['get', 'post', 'put', 'patch', 'delete'].includes(k);
  return <span className={clsx('ldTag', method && 'ldTag--method', k && `ldTag--${k}`)}>{children ?? (method ? k.toUpperCase() : k)}</span>;
}
