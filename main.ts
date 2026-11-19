// Entry for make.fun's "Sum up 19 November's world news in one image".
//
// The image itself is entry.png beside this file: a 1024x1024 poster built by
// build_image.py from the day's reporting (Reuters, Yonhap, the Guardian,
// Al Jazeera). This program is what the grader runs: it validates the poster
// against the bounty's gate (a whole PNG or JPEG, at most 1 MiB and
// 1024x1024) and copies it to the output directory as entry.png, the name
// the judge expects.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const MAX_BYTES = 1024 * 1024; // the gate's 1 MiB cap

function looksLikeImage(bytes: Buffer): string | null {
  const isPng =
    bytes.length > 8 &&
    bytes[0] === 0x89 && bytes[1] === 0x50 && bytes[2] === 0x4e && bytes[3] === 0x47;
  const isJpeg = bytes.length > 3 && bytes[0] === 0xff && bytes[1] === 0xd8 && bytes[2] === 0xff;
  if (isPng) return 'png';
  if (isJpeg) return 'jpeg';
  return null;
}

function pngSize(bytes: Buffer): { width: number; height: number } | null {
  // PNG IHDR: width and height are big-endian uint32 at offsets 16 and 20.
  if (bytes.length < 24 || bytes[0] !== 0x89 || bytes[1] !== 0x50) return null;
  return { width: bytes.readUInt32BE(16), height: bytes.readUInt32BE(20) };
}

function main(): void {
  const source = new URL('./entry.png', import.meta.url);
  const bytes = readFileSync(source);

  const kind = looksLikeImage(bytes);
  if (kind === null) {
    throw new Error('entry.png is neither a PNG nor a JPEG image');
  }
  if (bytes.length > MAX_BYTES) {
    throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB gate`);
  }
  const size = pngSize(bytes);
  if (size !== null && (size.width > 1024 || size.height > 1024)) {
    throw new Error(`entry.png is ${size.width}x${size.height}, over the 1024x1024 gate`);
  }

  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
  const target = join(outDir, 'entry.png');
  copyFileSync(source, target);
  console.log(`wrote ${target}: ${bytes.length} bytes of ${kind}`);
}

main();
