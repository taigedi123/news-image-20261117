// news-image-20261117 entry (Node 22, standard library only).
//
// The image is drawn by draw.py (Pillow) into entry.png beside this file:
// a 1024x1024 infographic summing up Tuesday 17 November 2026 — the Kerch
// Bridge strike, the Hormuz tanker mines, the Xi-Trump-Putin summit, the
// five-state Rwanda return hub, and the UK's West Bank sanctions. This
// program's only job is to place that exact image at the grader's output
// path, so both runs write identical bytes.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const dest = join(outDir, 'entry.png');

mkdirSync(dirname(dest), { recursive: true });
copyFileSync(new URL('./entry.png', import.meta.url), dest);
