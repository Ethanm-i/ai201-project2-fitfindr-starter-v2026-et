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
- **Inputs:** `description` (str), `size` (str | None, optional, defaults to None), `max_price` (float | None, optional, defaults to None, inclusive ceiling in dollars)
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

- *What I asked for:* I asked claude to write the tools in tools.py based on the spec and expaine to me and make sure that it follows the spec.
- *What came back:* Claude returned the tools implemented and the explanation each tool and what it does.
- *What I changed:*  I made sure that tthe three placeholders in criteria.md are had measurable targets and added resons tried to keyword matching, session state, numeric filtering and model variability with the help of claaude
**Moment 2**

- *What I asked for:* I asked to double check and see it  the tools are doing what the spec said they would do and return.
- *What came back:* claude return an explanations and evidence to show that the tools are following the spec.
- *What I changed:* with cladue, i replaced the placed holder lop with the sesstion-based implementation and added complete-sessio printing and repeatable checks. 


<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

Source: [full evaluation report](results/run_2026-10-13_2253_before.md).
All 13 scenarios ran five times with caching off. Criteria 3 and 4 combine the
five fixed queries within each Try column; all five cases must pass for that
column to pass. The five selected item IDs were lst_001, lst_002, lst_003,
lst_004, and lst_013.

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. A matching query completes all three tools | 4 of 5 | FAIL | PASS | PASS | PASS | PASS | MET (4/5) |
| 2. An impossible query stops before the second tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. The selected item stays the same between tools | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. The fit card includes the find's details in a short caption | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Search respects the user's price ceiling | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

Criterion 1's first try stopped during `create_fit_card` because the model
could not be reached. All 25 handoffs for criterion 3 matched ID, title, and
price. All 25 captions for criterion 4 identified the item, included the correct
price and platform, and contained 2–4 sentences. Platform capitalization was
ignored. Criterion 5 returned the same two listings at $18 and $15 in every try,
retaining the exact-limit item.

**Criterion 1 — try 2**, `agent.py::run_agent`; caption from `tools.py::create_fit_card`:

```
Obsessed with this Y2K baby tee with the cutest butterfly print I just snagged for only $18. I’m already planning to style it with baggy jeans, and it’s officially live on my depop shop if you want to steal the look!
```

**Criterion 2 — try 1**, `agent.py::run_agent`:

```
No matching listings. Try different keywords, increase your price limit, or remove the size filter.
```

The recorded search results were `[]` and captured `suggest_outfit` calls were `[]`.

**Criterion 3 — try 1, Levi's query**, `agent.py::run_agent`;
actual arguments captured by `run_eval.py::run_once`. Recorded ID, title, and
price fields are shown below:

```json
{
    "first_search_result":  {
                                "id":  "lst_001",
                                "title":  "Vintage Levi\u0027s 501 Jeans — Medium Wash",
                                "price":  38.0
                            },
    "selected_item":  {
                          "id":  "lst_001",
                          "title":  "Vintage Levi\u0027s 501 Jeans — Medium Wash",
                          "price":  38.0
                      },
    "suggest_outfit_new_item":  {
                                    "id":  "lst_001",
                                    "title":  "Vintage Levi\u0027s 501 Jeans — Medium Wash",
                                    "price":  38.0
                                }
}
```

**Criterion 4 — try 1, Levi's query**, `tools.py::create_fit_card`:

```
Finally snagged the perfect pair of vintage Levi's 501s for just $38! I’m obsessed with how the structured fit balances out my baggier pieces, and I found them listed on depop.
```

**Criterion 5 — try 1**, `tools.py::search_listings` via
`mcp_server.py::search_listings`. Recorded listing IDs, titles, and prices
for `graphic tee under $18`:

```json
[
    {
        "id":  "lst_002",
        "title":  "Y2K Baby Tee — Butterfly Print",
        "price":  18.0
    },
    {
        "id":  "lst_017",
        "title":  "Mesh Long-Sleeve Top — Black",
        "price":  15.0
    }
]
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

Recorded from the four terminal runs. Each attempted tool has one trace entry;
search is labeled `search_listings (via MCP)`.

**Happy path**

All three tools completed. One model response came from cache.

```
python app.py ask 'vintage graphic tee under $30, size M' --trace
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 8 items: Y2K Baby Tee — Butterfly Print, Mesh Long-Sleeve Top — Black, 90s Silk Slip Dress — Floral, Midi Length … +5 more
[2] suggest_outfit
      in:  dict with keys: new_item, wardrobe
      out: This Y2K baby tee is a perfect addition to your wardrobe—the fitted silhouette will balance out your wider-cut…
[3] create_fit_card
      in:  dict with keys: outfit, new_item
      out: Obsessed with this Y2K butterfly baby tee I just scored for only $18! It’s giving such a nostalgic early 2000s…

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   This Y2K baby tee is a perfect addition to your wardrobe—the fitted silhouette will balance out your wider-cut bottoms beautifully. Here are two ways to style it:

**Option 1: The Y2K Streetwear Look**
Pair the **Y2K Baby Tee** with your **Baggy straight-leg jeans, dark wash**. Add the **Black cropped zip hoodie** on top (leave it unzipped to show off the graphic) and finish with your **Chunky white sneakers** for an effortless, trendy vibe.

**Option 2: Effortless Minimalist**
Tuck the **Y2K Baby Tee** into your **Wide-leg khaki trousers**. Use the **Brown leather belt** to cinch the waist, and pair it with your **Black combat boots** to give the "cottagecore" butterfly print a bit of an edgy, grounded contrast.

  Fit card: Obsessed with this Y2K butterfly baby tee I just scored for only $18! It’s giving such a nostalgic early 2000s vibe, so make sure to check my depop shop before it’s gone.

1 model calls this session, 1 served from cache, 274 prompt + 50 output tokens
```

**Empty search**

Stopped after search with zero model calls and named three changes the user can try.

```
python app.py ask 'spacesuit size XXS under $1' --trace
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)

  No matching listings. Try different keywords, increase your price limit, or remove the size filter.

0 model calls this session
```

**Empty wardrobe**

Returned general styling advice and a fit card without crashing or returning an empty string.

```
python app.py ask 'graphic tee under $30' --empty-wardrobe --trace
(running with an empty wardrobe)
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 7 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Mesh Long-Sleeve Top — Black … +4 more
[2] suggest_outfit
      in:  dict with keys: new_item, wardrobe
      out: That butterfly baby tee is such a fun find! Those Y2K-inspired pieces are super versatile because they bridge …
[3] create_fit_card
      in:  dict with keys: outfit, new_item
      out: Found the cutest Y2K baby tee with the dreamiest butterfly print today! Honestly obsessed with this find for o…

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   That butterfly baby tee is such a fun find! Those Y2K-inspired pieces are super versatile because they bridge the gap between "playful nostalgia" and "effortless everyday."

Since it’s a fitted crop, the general rule of thumb is to balance it out with the volume of your bottoms. Here are two ways to style it:

### 1. The "Off-Duty Model" Look (Casual & Cool)
To lean into the Y2K aesthetic, pair the tee with a pair of **low-to-mid-rise baggy cargo pants or relaxed-fit light-wash denim.**
*   **Why it works:** The snug fit of the baby tee balances the volume of the baggy pants, creating a classic early-2000s silhouette.
*   **Complete the look:** Add a pair of chunky platform sneakers (like FILAs or New Balance) and a nylon shoulder bag or a butterfly hair clip to lean into the theme.

### 2. The "Modern Cottagecore" Look (Soft & Sweet)
If you want to emphasize the cottagecore side of the tags, pair the tee with a **flowy, floral-print midi skirt or a pleated tennis skirt.**
*   **Why it works:** The structured, graphic nature of the tee adds an "edge" to a feminine, flowy skirt. A midi skirt in a solid neutral (like sage green, cream, or lavender) would pull the colors out of the butterfly print beautifully.
*   **Complete the look:** Throw on some simple white canvas sneakers or leather loafers, and maybe a delicate beaded necklace to keep the vibe breezy and light.

**Stylist Tip:** Since this is a fitted crop, if you ever feel like you want a bit more coverage, it looks incredible layered under a **loose-fitting unbuttoned flannel shirt or a cropped zip-up hoodie.** It lets the butterfly graphic peek through without you having to commit to a super-cropped look all day!

**Is it worth $18?** If the fabric is in excellent condition and isn't pilling, $18 is a very fair price for a cute, authentic-feeling vintage graphic tee. It’s a staple piece that will likely get a ton of wear!

  Fit card: Found the cutest Y2K baby tee with the dreamiest butterfly print today! Honestly obsessed with this find for only $18, you can grab it on my depop shop now before I decide to keep it for myself.

2 model calls this session, 699 prompt + 517 output tokens
```

**Model unavailable**

Stopped at `suggest_outfit` with an actionable message and no stack trace.
The usage line confirms one model call and no cached response.
`run_agent()` catches `ModelUnavailable` and stores the message in the session.

```
python app.py ask 'black denim jacket under $55' --trace
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Denim Jacket — Light Wash, Cropped, Straight Leg Black Jeans — Faded, Vintage Levi's 501 Jeans — Medium Wash … +7 more
[2] suggest_outfit
      in:  dict with keys: new_item, wardrobe
      →    The model couldn't be reached during suggest_outfit. Check GEMINI_API_KEY in .env and your internet connection; if the service is busy, try again later.

  The model couldn't be reached during suggest_outfit. Check GEMINI_API_KEY in .env and your internet connection; if the service is busy, try again later.

1 model calls this session
```

**On the MCP move:** Registered `search_listings` and switched `run_agent()`
to `mcp_client.call_tool`. Tool discovery listed the correct inputs, the direct
comparison printed `PASS: results match`, and the full query completed.

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
