# ragator-v2

### RAG workflow

```mermaid
---
config:
  flowchart:
    curve: linear
---
graph TD;
        __start__([<p>__start__</p>]):::first
        classify_question(classify_question)
        generate_static_answer(generate_static_answer)
        retrieve_documents(retrieve_documents)
        generate_llm_answer(generate_llm_answer)
        __end__([<p>__end__</p>]):::last
        __start__ --> classify_question;
        generate_llm_answer --> __end__;
        generate_static_answer --> __end__;
        retrieve_documents --> generate_llm_answer;
        classify_question -. &nbsp;OFF_TOPIC&nbsp; .-> generate_static_answer;
        classify_question -. &nbsp;ON_TOPIC&nbsp; .-> retrieve_documents;
        classDef default fill:#f2f0ff,line-height:1.2
        classDef first fill-opacity:0
        classDef last fill:#bfb6fc

```
