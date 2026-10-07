# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools and the planning loop are implemented. Outfit suggestions
> and fit cards require a working model connection.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->

FitFindr helps a shopper find thrifted clothing by describing an item, optionally
including a size and maximum price. It searches the provided listings dataset,
selects the highest-scoring match, and asks a model for outfit ideas using the
shopper's wardrobe, or general styling advice when the wardrobe is empty.
It then asks the model for a short fit-card caption mentioning the item, price,
and selling platform. If no listings match, it stops and suggests changing the
keywords, price limit, or size filter.


---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:** Searches the thrift listings by keyword, with an optional size and price ceiling, without calling the model.
- **Inputs:** `description` (str), `size` (str | None, optional), `max_price` (float | None, optional, inclusive)
- **Returns:** A list of listing dicts (each with id, title, description, category, style_tags, size, condition, price, colors, brand, platform), best keyword match first, at most `config.SEARCH_RESULT_LIMIT` items.
- **When it has nothing:** An empty list `[]` — never `None`, never an exception.
- **Matching rules:** A size matches if, compared case-insensitively, it equals the requested size or equals one part of a combined size such as "S/M" split on "/" (so "M" matches "S/M", but "s" does not match "us 9" or "xl"). Each listing scores one point per distinct description word found in its title, description, category, style_tags or colors; listings scoring zero are dropped. `max_price` keeps listings priced at or below it.

### `suggest_outfit`

- **What it does:** Suggests one or two outfits built around a thrifted item and the user's wardrobe.
- **Inputs:** `new_item` (dict, one listing), `wardrobe` (dict with an `items` list, which may be empty)
- **Returns:** A non-empty string of outfit suggestions that name pieces the user already owns.
- **When it has nothing:** With an empty wardrobe, returns a non-empty string of general styling advice for the item (no exception, never `""`).

### `create_fit_card`

- **What it does:** Writes a short, post-style caption about the find.
- **Inputs:** `outfit` (str), `new_item` (dict, one listing)
- **Returns:** A 2-4 sentence caption string that mentions the item, its price, and its platform.
- **When it has nothing:** If `outfit` is empty or whitespace, returns a descriptive message string (no exception).

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:** If `search_listings` returns an empty list, put a message in `session["error"]` telling the user what to change (loosen the price, drop the size, or use different keywords) and stop without calling `suggest_outfit`. Otherwise, take the first result as `session["selected_item"]`, pass it with the wardrobe to `suggest_outfit`, then pass that outfit and the item to `create_fit_card`.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** Regex and string splitting, no model call. A regex pulls the price ceiling from phrases like "under $30" into `max_price`, another pulls a size token like "size M" into `size`, and the remaining words become `description`. The result goes in `session["parsed"]`.

**What moves through the session:** `query` → `parsed` (description, size, max_price) → `search_results` → `selected_item` (first result) → `outfit_suggestion` → `fit_card`. `error` stays `None` unless the run stops early.

Each tool's result is stored in the session before the next tool reads it.
The loop checks `trace.check_iterations(count)` before each tool step. The
no-match branch returns immediately, leaving `outfit_suggestion` and `fit_card`
as `None` and skipping both model tools.

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->



### 1. The Effortless "Off-Duty" Look (Casual & Cool)
Lean into the streetwear vibe and let the jeans be the star of the show by keeping the top relaxed and simple.
* **The Top:** A crisp, boxy white t-shirt (tucked in just a little bit at the front) or an oversized, slouchy grey crewneck sweatshirt. 
* **The Layer:** An oversized leather biker jacket or a classic canvas utility jacket.
* **The Shoes:** Retro sneakers (think Adidas Sambas, New Balance, or classic Converse). 
* **The Vibe:** Perfect for weekend errands, grabbing coffee, or casual hangouts. 

### 2. High-Low Chic (Polished & Edgy)
Take those rugged, classic jeans and dress them up by pairing them with more tailored, sophisticated pieces.
* **The Top:** A fitted black ribbed bodysuit or a silky, minimalist black camisole. 
* **The Layer:** An oversized, structured blazer in a neutral plaid, houndstooth, or solid black. 
* **The Shoes:** Pointed-toe ankle boots or sleek black loafers.
* **The Vibe:** Great for dinner dates, art galleries, or casual Friday at the office. 

**Pro-styling tip for 501s:** Because vintage Levi's 100% cotton denim doesn't have much stretch, play with proportions! If the jeans are a bit straight-leg or relaxed, balance them with something slightly more fitted on top, or lean fully into the oversized look by cinching the waist with a simple leather belt. 

Are you thinking about grabbing them? (Honestly, if you don't, someone else will!)

**One full query**

```
$ python app.py ask '...'

```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"

[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'description': 'Y2K era low-rise cargo pants. Lots of pockets. Khaki color, slightly distressed at the hems. Great for layering with a long tee.', 'category': 'bottoms', 'style_tags': ['y2k', 'cargo', '2000s', 'streetwear'], 'size': 'W29', 'condition': 'fair', 'price': 27.0, 'colors': ['khaki', 'tan'], 'brand': None, 'platform': 'poshmark'}, {'id': 'lst_012', 'title': 'Oversized Crewneck Sweatshirt — Vintage Navy', 'description': 'Perfectly faded navy crewneck. Genuinely vintage — not manufactured distressed. Ribbed cuffs and hem. No graphics, clean.', 'category': 'tops', 'style_tags': ['vintage', 'basics', 'oversized', 'classic'], 'size': 'XL (fits oversized)', 'condition': 'good', 'price': 20.0, 'colors': ['navy'], 'brand': None, 'platform': 'thredUp'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}]
```

```
$ python -c "from tools import suggest_outfit; from utils.data_loader import load_listings, get_example_wardrobe; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"

Hey there! Those vintage Levi's are a total closet staple, and at $38, they're a steal. Since your dark wash jeans are super baggy, these 501s will give you that classic, straight-leg fit you’re missing. 

Here are two easy ways to style them using what you already own:

**Outfit 1: Effortless & Cozy**
*   **Top:** Oversized grey crewneck sweatshirt
*   **Shoes:** Chunky white sneakers
*   **Accessory:** Black crossbody bag
*   *Why it works:* The slouchy grey sweatshirt tucked in slightly balances the straight-leg cut for an easy, everyday streetwear vibe.

**Outfit 2: Streetwear Edge**
*   **Top:** White ribbed tank top
*   **Outerwear:** Vintage black denim jacket
*   **Shoes:** Black combat boots
*   **Accessory:** Brown leather belt
*   *Why it works:* A fitted white tank under a black denim jacket lets the medium-wash denim pop, finished off with combat boots for a cool 90s edge. 

Go for it—you'll wear these all the time!
```

```
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"

Found my holy grail medium wash vintage Levi's 501 jeans while digging through the racks this weekend. Only $38 for the absolute best 90s slouchy fit! Just dropped these over on my depop, so run don't walk if you want to pair them with your favorite white sneakers.
```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:* I asked Codex to add three acceptance criteria, including one about state and one about the fit card, and then to explain the target under each of the five criteria.
- *What came back:* Codex proposed checking that the selected item's ID, title, and price survive the handoff to `suggest_outfit` in 5 of 5 tries, that 4 of 5 fit cards include the required details in 2–4 sentences, and that search respects the price ceiling in 5 of 5 tries.
- *What I changed:* With Codex's help, I replaced the three placeholders in `criteria.md` with those measurable targets and added reasons tied to keyword matching, session state, numeric filtering, and model variability.

**Moment 2**

- *What I asked for:* I asked Codex to implement `agent.py::run_agent`, save each tool result in the session, and check both a matching query and a query with no results.
- *What came back:* Codex implemented query parsing and the branch rule, and added `test_agent.py`. The checks used real search with controlled model responses to verify the exact item passed to `suggest_outfit`; they also verified that an empty search skips both later tools and leaves `fit_card` as `None`.
- *What I changed:* With Codex's help, I replaced the placeholder loop with the session-based implementation and added complete-session printing and repeatable checks. The local checks passed, but the attempted live model run was blocked by the Python environment and a missing dependency, so I have not treated the controlled responses as a successful live run.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```

```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```

```

**Empty search**

```

```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
