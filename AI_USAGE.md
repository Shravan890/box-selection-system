# AI Usage

## Tools used

- OpenAI Codex was used to inspect the supplied assignment, plan and implement the Django application, and review the test results.

## Prompt summaries

These summarize the requests given during the work; they are not presented as verbatim quotations.

- Build a Django application based on the supplied assignment, and place the project and requested submission materials together in a folder for review before ZIP packaging.
- Follow the assignment brief: recommend a shipping box for an order using product dimensions and weight, box internal dimensions, weight capacity, and cost.
- Include the submission items listed in the attached screenshot.
- Explain the SKU and quantity entry format, show the order's total quantity and combined weight, and check how changing quantity affects the box recommendation.
- Expand the sample catalog from three products to ten, with dimensions and weights, and ensure quantity is used in the packing recommendation.

## Output accepted and changed

- Accepted: a Django catalog for ten demo products and three boxes; order entry; a box recommendation using dimensions, weight, rotation, and cost, with a grid-fit check for repeated identical products; Django admin; order detail totals for item count and combined product weight; setup instructions; and automated tests.
- Implementation choice: “most suitable” is interpreted as the lowest-cost box that the packing heuristic finds feasible, with internal volume as a tie-breaker.
- The assignment requires the candidate to write the chat transcript and learning reflection without AI. Those files are intentionally left for the candidate to complete manually; no AI-written transcript or learning answer is supplied.

## Rejected or modified output

- Did not create a purported exported chat transcript or candidate learning reflection because the assignment expressly prohibits AI generation of those submissions.
- Did not claim to publish a GitHub repository. This folder is prepared for review; the candidate should create/push the repository and add its URL when ready.

## Mistakes and verification

- The packing method is a heuristic, not an exact 3D bin-packing solver. A valid arrangement could exist that the heuristic fails to find. This limitation is documented in `README.md`.
- The implementation was verified with Django's automated tests. The captured terminal output is in `TEST_OUTPUT.md`.
