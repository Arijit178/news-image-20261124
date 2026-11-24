// The World in One Day — Tuesday, 24 November 2026.
// A tiny Node 22 program, standard library only. The poster image
// lives next to this file as entry.png, and this program writes an
// exact copy of it into the directory the grader provides in
// MAKEFUN_OUTPUT_DIR (or /output when that is not set).
// Run it like this:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
// Nothing here uses the network, the clock, or any randomness, so
// running it twice writes the same bytes twice.

import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const inputPath = join(here, 'entry.png');
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const outputPath = join(outputDir, 'entry.png');

const bytes = readFileSync(inputPath);
mkdirSync(outputDir, { recursive: true });
writeFileSync(outputPath, bytes);
if (readFileSync(outputPath).length !== bytes.length) {
  throw new Error('entry.png was not copied whole');
}
