# DEUS: stated benchmark scores against independent reruns

Status: plan, written before any rerun score is read. Nothing here has been run. The frame below is fixed now and does not change after the first rerun file is read.

Amendment, 2026-11-22, before any read: five claim types in priority order (section 4a) and the conflict-of-interest line (section 0), per the operator on PR #8.

## 0. Conflict of interest

The readers and builders of this desk, including the writer of this plan, are Claude models, made by Anthropic, one of the labs measured. Same family as the writer, said here as PACK L12 requires. Every Anthropic row on the page and in the ledger carries this line. The mitigation is the method: DEUS compares a lab's printed number to someone else's rerun and makes no judgment of model outputs. Anthropic's rows get the same rules and the same outcomes as every other lab's, with no rule written for one lab alone.

Shape note: the ball asks for the shape of tornado_index/PLAN.md and ZEUS. tornado_index is not in this repository on any branch, so this plan follows zeus_index/PLAN.md: Claims read, Questions, Data, Frame fixed before any reading, outcomes four-way, and labels for preliminary data.

This is a measurement of stated scores against reruns. It is not a ranking of labs or models, and no output orders them.

## 1. Claims read

### Stated side: what a lab prints for its own model

The stated side is the score a lab prints for its own model on its own page (launch post, model card or system card), quoted with the URL, the page's date and the date read. Two pages were opened from this lane on 2026-11-22 to test how they read. No score from either is used here.

- The launch post at https://openai.com/index/gpt-5-6/ is dated "July 9, 2026". An automated read stopped at the start of its "Academic" table. Its coding table prints "SWE-Bench Pro | 64.6%", a different benchmark from SWE-bench Verified.
- The system card at https://www-cdn.anthropic.com/480e0bb54327b9622282e9c39a83a4f490ed377e/Claude%20Sonnet%205%20System%20Card.pdf is dated "June 30, 2026". The automated read stopped near page 66. Its contents list "8.2 SWE-bench Verified, Pro, Multilingual, and Multimodal 115", which is past where the read stopped.

What this means for the run: lab pages are long, and partial reads are common. A stated score enters only when it is read word for word from the page itself, together with the setup words printed beside it and its footnotes. A score seen only in a summary, a search snippet or another site is never used. A page that can't be read in full is held (section 5).

### Delivered side: who reruns these models

- **Epoch AI Benchmarking Hub,** https://epoch.ai/benchmarks/use-this-data (read 2026-11-22): "You can download the data in CSV format", from https://epoch.ai/data/benchmark_data.zip ("Updated Nov. 21, 2026"). No account or key is named. The license is "free to use, distribute, and reproduce provided the source and authors are credited" (CC BY 4.0). The hub holds two kinds of rows, "Epoch AI internal runs" and "External runs". https://epoch.ai/benchmarks/about says "External results come from official leaderboards or primary sources" and "Our internal evaluations are powered by Inspect, and are run with consistent and well documented settings across models."
- **Epoch's GPQA Diamond method,** https://epoch.ai/benchmarks/gpqa-diamond: "It contains 198 questions", "We use the prompt from the simple-evals library", and "If the model's answer is not of the form 'ANSWER: LETTER', it receives no points for that question." Shots, temperature and runs are not stated on that page. It points to a log viewer, which "is protected against bot access".
- **Vals AI,** https://vals.ai/benchmarks/gpqa: an archived GPQA Diamond board ("we no longer run this benchmark on new model releases", "Updated 9/1/2026"), with zero-shot and 5-shot chain-of-thought modes. No intervals or per-item data were seen.

Not read: the FAQ answers on Epoch's about page did not render, including "What do the error bars represent?" and "Why are some of your scores different from those reported elsewhere?". Read them by hand before the first run. Their answers decide how the interval rule in section 4 is applied, not whether it applies.

### Existing desks this plan reuses

- **MODEL,** https://indahl.ai/hermes/model: reruns open-weight models' own card results with lm-evaluation-harness, "with the shots the card gives". DEUS reuses its outcome wording ("CONSISTENT means the file agrees within the rounding of the statement"), its both-directions rule ("A row whose items fall in both directions reads CANNOT TELL") and its reason code NO_INTERVAL_FORMABLE.
- **The eleven setup fields** of our eval setup check: harness, prompt format, chat template, few-shot, max tokens, temperature, stop, extraction rule, dataset version, items and seeds. "A decided ABOVE or BELOW requires all eleven setup fields named and matching on both sides." DEUS uses these fields as they stand and adds four in section 4.
- **The interval verdict arithmetic** (stated value against an estimate and its interval) is used as it stands.
- **AILUMINATE and HFSIZE** measure safety results and model sizes, not capability scores. DEUS reads neither and duplicates neither.

DEUS does not run models. Closed frontier models can't be rerun on our hardware, so DEUS reads reruns that others have published.

## 2. Questions

1. For each lab, model and benchmark in the frame, is the score the lab states ABOVE, BELOW, CONSISTENT with, or CANNOT_TELL against the independent rerun's interval?
2. How many stated scores in the frame have no independent rerun at all? Counted, and listed by lab and benchmark.
3. For the four further claim types in section 4a, the same four-way question against the independent reading for that type.

## 3. Data (all public, no key, no account)

- **Stated:** the labs' own pages, read in full, quoted word for word with the URL, page date and date read. PDFs are read by extracting the text of the whole file.
- **Delivered:** the Epoch AI zip above, the snapshot dated Nov. 21, 2026, credited to Epoch AI under CC BY 4.0. A second source enters only if it publishes per-run or per-item data and a stated setup for a model in the frame. Vals AI's GPQA board is archived, so it covers models in the window only where it already holds a run.
- **Access from this lane:** the zip download from this lane was refused by the network on 2026-11-22 (epoch.ai is not allowed from here). The fetch runs from the operator's seat. The log viewer is protected against automated access and is not used.

## 4. Frame (fixed now, before any rerun score is read)

- **Labs:** OpenAI, Anthropic, Google DeepMind, Meta, xAI, DeepSeek and Alibaba (Qwen). This list is a choice made now, not a measure of size or rank. A change is an addendum, never an edit of this run.
- **Models:** every model from those labs whose own launch post, model card or system card is dated 2026-01-01 through 2026-10-31 and prints a score on a listed benchmark. Each printed score is one claim. A page that prints two scores for one model and benchmark (for example with and without tools) gives two claims.
- **Benchmarks:** GPQA Diamond, SWE-bench Verified, FrontierMath (Tiers 1 to 3), Humanity's Last Exam and AIME 2025. Each name means one dataset version and item set. A benchmark stays in only if the Epoch zip holds at least one run of it that counts as independent (next item). That check reads the list of benchmarks in the zip, never a score. A benchmark that fails it is dropped and named, and nothing replaces it. Pages that print a different benchmark (SWE-bench Pro in place of Verified, for example) give no claim for the listed one.
- **Independent rerun:** a row run by Epoch AI itself, or by a third party that ran the model, stated its setup and is not the model's developer. A row whose source is the developer's own page or submission is the claim repeated, not a rerun. It is left out of the delivered side and counted as "rerun is the claim".
- **Model match:** same model name and the same version or snapshot string where either side prints one. Where the claim names a reasoning effort and the rerun names another, it is a different pairing.
- **Interval rule:** the rerun's 95% interval. If the source states an error bar and what it measures, that is the interval, labeled with what it measures. If the source gives a score and an item count only, use a Wilson 95% interval on that count, labeled "item sampling, single run". It leaves out run-to-run spread, so it is a floor on width. With neither an interval nor an item count, the claim reads CANNOT_TELL (NO_INTERVAL_FORMABLE). The stated value is read at its printed rounding: a printed 88.2% means 88.15 to 88.25. Where two independent reruns of one pairing fall on opposite sides of the stated value, the claim reads CANNOT_TELL, as on MODEL.
- **Setup-match rule (PACK L):** setup is a carrier. Compare the eleven setup fields above, plus four that frontier claims turn on: reasoning effort or thinking budget, tools and scaffold, attempts (pass@1, pass@k, best of n, parallel compute) and trials averaged. A decided ABOVE or BELOW needs every field named and matching on both sides. A stated value outside the interval with any field different or unnamed reads CANNOT_TELL, with the direction written beside it. A stated value inside the interval reads CONSISTENT, with any unnamed field listed as a carrier.
- **Size that matters:** none in this first run. The test is against the stated value alone, and the card says so.

## 4a. Claim types (priority order, fixed now)

DEUS checks five kinds of claim for every lab in the frame, Anthropic included. They are taken in this order. A type with no independent public data for a claim counts that claim in `deus.no_rerun_count`, which is its own reported figure for every type. The labs, window and outcome words in section 4 hold for every type.

1. **Launch-post benchmark scores against independent reruns with released data.** Sections 4 and 5 as written. This type carries the headline.
2. **Comparative launch charts ("A beats B") against the reruns' order.** A claim is one ordered pair the lab prints for one benchmark. It is read only where one independent source ran both models under the same setup. CONSISTENT: the rerun puts A above B with the two intervals apart. ABOVE: the rerun puts B above A with the intervals apart, so the chart stated A higher than the rerun found. CANNOT_TELL: the intervals overlap, or the two runs differ in any setup field. BELOW is not reachable for an order claim. Cell: `deus.order_outcomes`, the four-way count.
3. **Stated context window against effective context window,** only where a public long-context rerun exists with released data. Effective length is the longest tested length at which the rerun stays inside that source's own stated threshold. The run uses the source's definition and invents none. ABOVE: the stated window is longer than the effective length, with the stated length tested. CONSISTENT: the effective length reaches the stated window. CANNOT_TELL: the rerun did not test up to the stated length, or the source states no threshold. Cell: `deus.context_outcomes`.
4. **Stated knowledge cutoff against probed cutoff,** only where an independent probe publishes its method and data. ABOVE: the stated cutoff is later than the probe's whole interval. BELOW: earlier than the whole interval. CONSISTENT: inside it. CANNOT_TELL: the probe gives a point with no interval, or probes disagree in direction. Cell: `deus.cutoff_outcomes`.
5. **Speed and price claims,** only with independent open data, keyless, with method stated. Otherwise each claim counts as no rerun. Cell: `deus.speed_price_outcomes`.

Sources for types 2 to 5 follow the independence rule in section 4 (not the developer, setup stated, data released). Each source is named and quoted with its URL before the first read of that type. A type with no qualifying source is reported as all no rerun, never skipped in silence. Only type 1 feeds the headline.

### Headline cell (named in advance)

`deus.stated_above_share`: among claims in the frame with an independent rerun, the share that read ABOVE (the stated score sits above the whole rerun interval with every setup field matched). It carries a 95% interval from a block bootstrap by model, because claims for one model are not independent. The card, the ledger row and the reproduce kit read this field and no other as the headline. The full four-way count is always printed beside it, because most claims are expected to read CANNOT_TELL on unnamed setup.

Secondary cell, not the headline: `deus.no_rerun_count`, the number of claims in the frame with no independent rerun, listed by lab and benchmark, with "rerun is the claim" counted apart.

## 5. Outcomes (four-way, relative to what the lab stated)

- **ABOVE:** the stated score is above the whole rerun interval, every setup field named and matching.
- **BELOW:** the stated score is below the whole rerun interval, every setup field named and matching.
- **CONSISTENT:** the stated score, at its printed rounding, falls inside the rerun interval. Unnamed fields are listed as carriers.
- **CANNOT_TELL:** the stated score is outside the interval with a setup field different or unnamed (direction written beside it), or no interval can be formed, or reruns disagree in direction. The reason is named.

Nothing returned, refused and held are counted as their own outcomes. A claim with no independent rerun is nothing returned and feeds `deus.no_rerun_count`. A lab page that refuses reading is refused. A page read only in part is held, listed by URL, and left out of the headline. No stated score is ever filled in from a summary, a snippet or memory.

## 6. Labels for preliminary data

- Until the referee's read, every output carries "PRELIMINARY: first run, not refereed". The referee reads the first run before it goes on the home banner.
- If the stated side can't be read for every lab tonight, the run is labeled "PRELIMINARY: partial frame" and lists the labs and pages covered. The frame is never narrowed silently.
- Every count on the card and in the ledger comes from the run log, never typed in by hand.

## Open questions for the operator

1. **Labs:** keep the seven named, or name another list before the first read?
2. **Headline:** `deus.stated_above_share` is named. If you would rather headline the CANNOT_TELL share, say so before the first read.
3. **Epoch FAQ:** the answers on error bars and on why Epoch's scores differ from others did not render here. Read them by hand once. They set how the interval rule is applied.
4. **Zip fetch:** epoch.ai is refused from this lane, so the download runs from your seat.
5. **Sources for types 2 to 5:** none is named yet. Each is named, quoted with its URL and checked against the independence rule before that type's first read.
