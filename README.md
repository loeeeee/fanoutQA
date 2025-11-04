# FanoutQA Data Pipeline

## Goals

### Overall Project Goal

- Investigate the FanOutQA dataset to determine its suitability as a "difficult" dataset for training a small model.
- The ultimate aim is to create a dataset that teaches a model to **plan its evidence gathering*- (as a compact, parallel list of information needs) *before- it reads long documents.

---

### Task 1: Data Analysis and Labeling

- Go through the FanOutQA dataset.
- Manually review and label at least 50 examples.
- For each example, label its reasoning chain as either:
    - **Sequential:**- Steps depend on previous answers.
    - **Parallel / Independent:**- Steps can be performed alone.

---

### Task 2: Data Curation and Transformation

- Identify and select **20 usable examples*- from the labeled set that are either already parallel or can be easily rewritten to be parallel.
- For each of these 20 examples, rewrite the reasoning chain into the new **Evidence Plan*- format.
- This Evidence Plan must contain 2-5 **independent*- evidence goals.
- Each goal must adhere to the specific JSON format: `{"goal": "Describe the information needed", "query": "Search phrase to find it"}`.

---

### Task 3: Dataset Assembly and Population

- For each of the 20 selected examples, create a final JSON object that follows the provided dataset schema.
- Populate the `id`, `question`, `gold_answer`, and the new `evidence_plan` for each object.
- Populate the `supporting_docs` field using the Wikipedia articles linked by FanOutQA.
    - Each entry must be formatted as: `{"title": "Exact Wikipedia title", "text": "Full paragraph or first ~300 tokens..."}`.
- Populate the `distractor_docs` field by sampling 3–5 unrelated Wikipedia pages.
    - Ensure these pages do not overlap with the supporting documents.
    - Each entry must be formatted as: `{"title": "Unrelated page title", "text": "A paragraph from that page"}`.
- Ensure the total text length (supporting + distractor) stays within an **8k token limit**, truncating text if necessary.

---

### Task 4: Final Deliverables

- Produce a JSON file named `parallel_reasoning_examples.json` containing the 10–20 fully-formatted dataset examples.
- Produce a CSV file named `reasoning_type_labels.csv` containing the 50 examples labeled as sequential or parallel.
- Write a **short summary paragraph*- for the pull request that includes:
    - The dataset used (FanOutQA).
    - The criteria used to select questions.
    - How the Evidence Plan was generated.
    - Any patterns or observations noticed (e.g., "comparison questions work well...").

## Processed Data

- QA with parallel answering steps
    - data/processed/fanout-parallel-small.json
    - extracted from data/raw/fanout-dev.json
    - small and manually picked data
    - data structure
        - copy and paste of the raw data
- QA with mixed answering steps
    - data/processed/fanout-mixed-small.json
    - extracted from data/raw/fanout-dev.json
    - small and manually picked data
    - data structure
        - copy and paste of the raw data
- QA with sequential answering steps
    - data/processed/fanout-sequential-small.json
    - extracted from data/raw/fanout-dev.json
    - small and manually picked data
    - data structure
        - copy and paste of the raw data