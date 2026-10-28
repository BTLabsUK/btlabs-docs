import React from 'react';
import MDXComponents from '@theme-original/MDXComponents';

/**
 * Wraps every markdown table in its own horizontal scroll container, as on the Developer Hub:
 * custom.css gives tables `display: table` so `width: 100%` works, which removes Infima's scroll
 * box, so a wide table would otherwise widen the whole page on a phone.
 */
function Table(props) {
  return (
    <div className="epicTableWrap" tabIndex={0}>
      <table {...props} />
    </div>
  );
}

export default {...MDXComponents, table: Table};
