import React from 'react';
import Steps from '../Steps';

/* The three steps of the API guide's "First request", on the same numbered rail as Start here
 * on the CLI guide. Props come from tools/gen-lepic-api.py:
 *   steps = [{lead: null, text: parts, cmd: string, answer?: string}]
 * The answer is the source's JSON, pretty-printed by the generator. */
export default function FirstRequest({steps, label = 'First request'}) {
  return <Steps steps={steps} label={label} />;
}
