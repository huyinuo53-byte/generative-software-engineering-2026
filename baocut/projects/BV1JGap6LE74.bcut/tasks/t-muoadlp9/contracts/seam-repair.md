You are checking paragraph boundaries at PAGE SEAMS in a transcript that has already been copy-edited and paragraphed.

The transcript was processed in pages. Where one page ends and the next begins, the text was cut mechanically, so the paragraph break at that point may or may not be real. You receive ONE OR MORE blocks as PLAIN TEXT. Each block is a window around one seam (occasionally several): the last sentences before the seam followed by the first sentences after it, ONE SENTENCE PER LINE, every line prefixed with its 1-based line number. The header names the seam: `page seam before line N` means the previous page ended with line N-1 and the next page started with line N.

<<<BLOCK 1 | 30 sentences | 410 characters | page seam before line 17>>>
1| …
…
30| …
<<<BLOCK-END>>>

Answer with LINE-NUMBER RANGES ONLY — one paragraph per range, do NOT copy any sentence text back:

<<<BLOCK 1>>>
1-16
17-30
<<<BLOCK-END>>>

Rules:
- Ranges must start at 1, be contiguous (each starts right after the previous one ends) and end at the block's last line — no gaps, no overlaps, no numbers outside the block.
- The window may begin and end in the middle of a paragraph; that is expected. What matters is where the paragraph boundaries fall INSIDE the window.
- If the sentence at the seam continues the thought of the sentences before it, do NOT start a range there — let one range span the seam. A single range covering the whole block (`1-30`) is a valid answer when the window is one paragraph.
- Start a range at the seam only when a new topic, question, example or story really begins there.
- A boundary elsewhere in the window is welcome when the topic actually turns there — for example when the paragraph that continues across the seam really started a few sentences before it.
- Never break just to keep paragraphs short. Paragraphs of spoken language stay under 300 words (500 characters for Chinese/Japanese/Korean), but a window this size is often a single paragraph.
- Answer for every block, in the same order, each with its own `<<<BLOCK k>>>` … `<<<BLOCK-END>>>` fences, and emit NOTHING else: no sentence text, no preamble, no explanations, no code block wrapper.