# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:** I picked 4 of 5 because the planned search uses keyword matching, so a query describing an available item may use words that do not appear in its listing. Requiring 5 of 5 would assume the search understands every phrasing even though it does not use a model to interpret meaning.

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:** I picked 5 of 5 because an empty search result should trigger a fixed branch that returns a helpful message without calling the model. This is already the strictest success rate, and there is no generated output on this path to justify allowing a miss.

---

## 3. The selected item stays the same between tools

For five queries that each return at least one listing, the first search result, `session["selected_item"]`, and the `new_item` argument actually passed to `suggest_outfit` must have the same item ID, title, and price — 5 of 5 tries. Check the captured tool arguments against the session values for each run.

**Why this target:** The loop copies an existing listing into the session and passes it to the next tool without asking the model to choose or rewrite it. This handoff should be exact every time; a mismatch would mean the outfit is being made for the wrong item or with changed listing details.

---

## 4. The fit card includes the find's details in a short caption

Given five different listings and a non-empty outfit suggestion for each, `create_fit_card` returns a caption of 2–4 sentences that identifies the item and includes its correct price and platform — in at least 4 of 5 tries. A try passes only when all of these requirements are met.

**Why this target:** The item, price, and platform come from the listing, so there is enough information to include all three. The model can vary its wording and sentence count, so 4 of 5 allows one miss while still requiring most captions to be accurate and short enough to post.

---

## 5. Search respects the user's price ceiling

For five calls to `search_listings` with a `max_price`, every returned listing must have a price at or below that limit — 5 of 5 tries. Use keywords that match listings both below and above the limit, and include one case where a matching listing costs exactly the limit; that listing must remain eligible. Each call must return at least one matching listing within the budget.

**Why this target:** Price filtering compares numeric values without calling the model, so it should enforce the budget every time. Testing an exact-price match also checks the inclusive limit promised in the tool inventory, while requiring a result prevents an always-empty search from passing.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
