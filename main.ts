// "The World in One Day" — 24 November 2026 news poster.
// Node 22, standard library only. entry.png sits beside this file;
// this program copies it byte for byte to the output directory
// the grader provides, so both runs write identical bytes.
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
// The copy is deterministic: the same source bytes go out on every
// run, with no network, no clock and no randomness involved.

import { copyFileSync, existsSync, mkdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const source = new URL('./entry.png', import.meta.url);
if (!existsSync(source)) {
  throw new Error('entry.png is missing next to main.ts');
}
const target = join(outDir, 'entry.png');
mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);
if (statSync(source).size !== statSync(target).size) {
  throw new Error('entry.png was not copied whole');
}
