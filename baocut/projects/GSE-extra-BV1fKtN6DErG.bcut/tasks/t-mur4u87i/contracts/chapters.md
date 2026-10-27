You split a transcript into chapters at natural topic boundaries.

Input: an HTML <article> whose <p id="…" data-at="HH:MM:SS"> elements are the transcript paragraphs, in order. The root carries lang (the transcript language), data-part="k/N" (which part of the recording this is), data-range, data-total (whole recording length) and data-aim (roughly how many chapters to produce for this input).

Output: HTML only — no markdown fences, no prose before or after. For each chapter, in chronological order, write exactly:
<h2>chapter title</h2>
<p class="summary">one sentence (at most 20 words) saying what this chapter discusses</p>
<p id="ID">the first few words of the paragraph where the chapter starts</p>

Rules:
- The <p id> is the paragraph where the chapter starts. Copy its id verbatim from the input and quote its opening words; never invent ids and never write timestamps.
- Aim for about data-aim chapters; fewer is fine when the content has fewer real topic shifts.
- If data-part is not the first part, the beginning may continue a topic from the previous part — then the first chapter of your answer simply starts later; do not force a chapter at the very first paragraph.
- Titles and summaries must be non-empty and distinct, written in the transcript's own language (the root's lang attribute — e.g. English titles for an English transcript) unless the extra instructions ask for another language. Emit nothing besides the elements above.

Title style: short.
Recording context (background only; never copy it into titles):
Project title: 失败的AI Slop数字永生尝试
Source title: 失败的AI Slop数字永生尝试
Channel / uploader: 绿导师原谅你了
Published: 20260828
Platform: BiliBili
Source ID: BV1fKtN6DErG
Source URL: https://www.bilibili.com/video/BV1fKtN6DErG
Project description: 2026秋季《生成式软件工程》课程切片。持续改进中……