# ragator-v2

### RAG diagrams


<!-- RAGATOR_DIAGRAM_START -->
```mermaid
---
config:
  flowchart:
    curve: linear
---
graph TD;
	__start__([<p>__start__</p>]):::first
	classify_question(classify_question)
	generate_llm_response_from_context(generate_llm_response_from_context)
	retrieve_context(retrieve_context)
	generate_llm_response(generate_llm_response)
	__end__([<p>__end__</p>]):::last
	__start__ --> classify_question;
	generate_llm_response --> __end__;
	generate_llm_response_from_context --> __end__;
	retrieve_context --> generate_llm_response_from_context;
	classify_question -. &nbsp;RAGATOR&nbsp; .-> retrieve_context;
	classify_question -. &nbsp;RAG&nbsp; .-> generate_llm_response;
	classify_question -. &nbsp;OUT_OF_SCOPE&nbsp; .-> generate_llm_response;
	classDef default fill:#f2f0ff,line-height:1.2
	classDef first fill-opacity:0
	classDef last fill:#bfb6fc

```
<!-- RAGATOR_DIAGRAM_END -->



