# AI Assisted Box Selection System

A small Django application that helps a warehouse choose a shipping box for an order. It stores product dimensions and weight, evaluates the available box sizes, and recommends the lowest-cost box that can hold the order.

## Run locally

Use Python 3.10 or newer. From this folder:

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

Open http://127.0.0.1:8000. The demo catalog includes ten products: `MUG-01`, `BOOK-01`, `LAMP-01`, `BOTTLE-02`, `HEADPHONES-01`, `SNEAKER-01`, `PHONE-01`, `TOY-01`, `CANDLE-01`, and `KETTLE-01`. Submit an order as one `SKU, quantity` pair per line. Product dimensions and weight are per item; the order page shows total quantity and combined weight, while the recommender recalculates box fit for every submitted quantity. Use `/admin/` to manage products and boxes; create an admin account with `python manage.py createsuperuser`.

## Demo product catalog

Dimensions are length × width × height in centimeters. Weight is per product in kilograms.

| SKU | Product | Dimensions (cm) | Weight (kg) |
|---|---|---:|---:|
| `MUG-01` | Ceramic mug | 10 × 10 × 12 | 0.45 |
| `BOOK-01` | Hardcover book | 21 × 15 × 3 | 0.65 |
| `LAMP-01` | Desk lamp | 28 × 18 × 12 | 1.80 |
| `BOTTLE-02` | Reusable water bottle | 8 × 8 × 26 | 0.50 |
| `HEADPHONES-01` | Over-ear headphones | 20 × 18 × 8 | 0.35 |
| `SNEAKER-01` | Running shoe pair | 32 × 22 × 12 | 1.10 |
| `PHONE-01` | Smartphone | 16 × 8 × 2 | 0.22 |
| `TOY-01` | Building block set | 24 × 16 × 10 | 0.75 |
| `CANDLE-01` | Glass jar candle | 9 × 9 × 11 | 0.40 |
| `KETTLE-01` | Electric kettle | 24 × 20 × 22 | 1.30 |

The quantity multiplies a product's per-item weight and adds that many copies of its dimensions to the packing check. The product's own dimensions remain the same. The selected box's dimensions, weight capacity, and cost come from the box catalog.

## Recommendation behavior

- Product and box dimensions use centimeters; weights use kilograms.
- Products may rotate freely. Every item copy must fit in the box and total product weight must not exceed the box capacity.
- The packer uses a deterministic greedy 3D guillotine free-space heuristic, sorting larger items first. Among boxes it finds that fit, it picks the lowest cost, then the smallest internal volume, then the name.
- The heuristic is practical for this small assignment but is not an exact solver: a difficult arrangement might be reported as not fitting even if another arrangement exists. It does not add dunnage, clearance, or box tare weight.

## Project contents

- `orders/`: catalog, order entry, recommendation logic, admin, and tests.
- `TEST_OUTPUT.md`: captured Django test run.
- `AI_USAGE.md`: AI use and verification notes.
- `CHAT_TRANSCRIPT.md` and `WHAT_I_LEARNED.md`: manual completion files. The assignment says these must be written by the candidate and the transcript must not be AI-generated.

## Test

```bash
python manage.py test
```

See `TEST_OUTPUT.md` for the test run included with this submission.
