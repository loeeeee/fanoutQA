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

## How Fan Out

The dataset has several distinct fan out mode.

### 1 Hop

- Query question
    - Revised question
        - Breakdown question 0
        - Breakdown question 1
        - Breakdown question 2
        - ...

Example:

- What is the batting hand of each of the first five picks in the 1998 MLB draft?
    - Who were the first 5 picks in the 1998 MLB Draft?
        - What is the batting hand of Pat Burrell?
        - What is the batting hand of Mark Mulder?
        - What is the batting hand of Corey Patterson?
        - What is the batting hand of Jeff Austin?
        - What is the batting hand of JD Drew?

This is the majority of the questions in the dataset.

### 2 Hop (deep)

- Query question
    - Revised question
        - Breakdown question 0
            - Deep-dive question
        - Breakdown question 1
            - Deep-dive question
        - Breakdown question 2
            - Deep-dive question
        - Breakdown question 3
            - Deep-dive question
        - ...

Example:

- What law schools did the most recent four Supreme Court justices attend?
    - Who are the last four justices appointed to the Supreme Court?
    - What law school did Ketanji Brown Jackson attend?
        - Where did Ketanji Brown Jackson study law?
    - What law school did Amy Coney Barrett attend?
        - Where did Amy Coney Barrett study law?
    - What law school did Brett Kavanaugh attend?
        - Where did Brett Kavanaugh study law?
    - What law school did Neil Gorsuch attend?
        - Where did Neil Gorsuch study law?

Only a few of the questions in the dataset structured like this.

### 2 Hop (wide)

- Query question
    - Revised question
    - Deep-dive question
        - Breakdown question 0
        - Breakdown question 1
        - Breakdown question 2
        - Breakdown question 3
        - ...

Example:

- What is Google's online video platform and how old are its founders?
    - What is Google's online video platform?
    - Who are the founders of YouTube?
        - Who are the founders of YouTube?
        - How old is Steve Chen?
        - How old is Chad Hurley?
        - How old is Jawed Karim?

Only a few of the questions in the dataset structured like this.

### 3 Hop

Examples:

- Which currently sitting US Supreme Court Justices graduated from a top 14 law school?
    - Who are the current sitting US Supreme Court Judges?
    - What are the T14 law schools and which of the supreme court justices attended them?
        - What are the T14 law schools?
            - Did John Roberts graduate from law school at one of the following universities: Columbia, Cornell, Duke, Georgetown, Harvard, New York University, Northwestern, Stanford, University of California at Berkeley, University of Chicago, University of Michigan, University of Pennslyvania, University of Virginia or Yale?
            - Did Thomas Clarence graduate from law school at one of the following universities: Columbia, Cornell, Duke, Georgetown, Harvard, New York University, Northwestern, Stanford, University of California at Berkeley, University of Chicago, University of Michigan, University of Pennslyvania, University of Virginia or Yale?
            - Did Samuel Alito graduate from law school at one of the following universities: Columbia, Cornell, Duke, Georgetown, Harvard, New York University, Northwestern, Stanford, University of California at Berkeley, University of Chicago, University of Michigan, University of Pennslyvania, University of Virginia or Yale?
            - Did Sonia Sotomayor graduate from law school at one of the following universities: Columbia, Cornell, Duke, Georgetown, Harvard, New York University, Northwestern, Stanford, University of California at Berkeley, University of Chicago, University of Michigan, University of Pennslyvania, University of Virginia or Yale?
            - Did Elena Kagan graduate from law school at one of the following universities: Columbia, Cornell, Duke, Georgetown, Harvard, New York University, Northwestern, Stanford, University of California at Berkeley, University of Chicago, University of Michigan, University of Pennslyvania, University of Virginia or Yale?
            - Did Neil Gorsuch graduate from law school at one of the following universities: Columbia, Cornell, Duke, Georgetown, Harvard, New York University, Northwestern, Stanford, University of California at Berkeley, University of Chicago, University of Michigan, University of Pennslyvania, University of Virginia or Yale?
            - Did Brett Kavanaugh graduate from law school at one of the following universities: Columbia, Cornell, Duke, Georgetown, Harvard, New York University, Northwestern, Stanford, University of California at Berkeley, University of Chicago, University of Michigan, University of Pennslyvania, University of Virginia or Yale?
            - Did Amy Coney Barrett graduate from law school at one of the following universities: Columbia, Cornell, Duke, Georgetown, Harvard, New York University, Northwestern, Stanford, University of California at Berkeley, University of Chicago, University of Michigan, University of Pennslyvania, University of Virginia or Yale?
            - Did Ketanji Brown Jackson graduate from law school at one of the following universities: Columbia, Cornell, Duke, Georgetown, Harvard, New York University, Northwestern, Stanford, University of California at Berkeley, University of Chicago, University of Michigan, University of Pennslyvania, University of Virginia or Yale?

### 4 Hop

- Query question
    - Revised question
    - Deep-dive question
        - Breakdown question 0
            - Deep-dive question
            - Deeper-dive question
        - Breakdown question 1
            - Deep-dive question
            - Deeper-dive question
        - Breakdown question 2
            - Deep-dive question
            - Deeper-dive question
        - Breakdown question 3
            - Deep-dive question
            - Deeper-dive question
        - ...

Example:

- Which heads of state of the founding countries of the European Union are older than 80 years old?
    - What countries founded the European Union?
    - Who is the head of state of Belgium and how old are they?
        - Who is the head of state of Belgium?
        - How old is King Philippe?
    - Who is the head of state of France and how old are they?
        - Who is the head of state of France?
        - How old is Emmanuel Macron?
    - Who is the head of state of Germany and how old are they?
        - Who is the head of state of Greece?
        - How old is Frank-Walter Steinmeier?
    - Who is the head of state of Italy and a how old are they?
        - Who is the head of state of Italy?
        - How old is Sergio Mattarella?
    - Who is the head of state of Luxembourg and how old are they?
        - Who is the head of state of Luxembourg?
        - How old is Grand Duke Henri?
    - Who is the head of state of Netherlands and how old are they?
        - Who is the head of state of the Netherlands?
        - How old is King Willem-Alexander?

### 5 Hop

Example:

- Which actors played Spider-man in the latest live-action Spider-man movie, and who directed their respective Spider-man movies?
    - What is the latest live-action Spider-man movie?
    - Which actors played Spider-man in 'Spider-Man: No Way Home (2021)'?
    - Who directed Tom Holland's, Tobey Maguire's and Andrew Garfield's respective Spider-man movies?
        - Who directed Tom Holland's Spider-man movies?
            - What is the title of Tom Holland's last Spider-man movie?
            - Who was the director of Spider-Man: No Way Home (2021)?
        - Who directed Tobey Maguire's Spider-man movies?
            - What is the title of Tobey Magquire's last Spider-man movie?
            - Who was the director of Spider-Man 3 (2007)?
        - Who directed Andrew Garfield's Spider-man movies?
            - What is the title of Andrew Garfield's last Spider-man movie?
            - Who was the director of The Amazing Spider-Man 2 (2014)?

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