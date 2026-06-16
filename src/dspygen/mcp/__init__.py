"""
dspygen MCP (Model Context Protocol) server package.

Exposes the entire dspygen framework as MCP tools, resources, and prompts.

Tool surface (maximized):
  Module tools     — list_modules, get_module_info, run_module, generate_dspy_signature,
                     generate_dspy_module, scaffold_module
  Agent tools      — list_agents, get_agent_info, run_agent, trigger_transition, get_agent_state
  Workflow tools   — execute_pipeline, execute_workflow, list_workflow_examples,
                     validate_pipeline, run_pipeline_from_file
  Retrieval tools  — retrieve_from_chroma, retrieve_from_web, retrieve_from_code
  RDDDY tools      — create_aggregate, create_command, create_event, create_query,
                     create_saga, create_policy, create_value_object, create_read_model,
                     event_storm, create_inhabitant, list_rdddy_patterns, scaffold_domain
  Module tools+    — generate_tweet, summarize_document, natural_language_to_sql,
                     generate_blog_post, generate_code_comments, translate_data_format,
                     classify_customer_feedback, generate_mermaid_diagram, cobol_to_python,
                     generate_pydantic_class, generate_cli_module, generate_jsx,
                     ask_dataframe, ask_data, generate_nuxt_component, chatbot_response,
                     check_condition, generate_test, optimize_bytecode, translate_bpmn_to_bpel
  Retrieval tools+ — retrieve_from_chatgpt_chroma, retrieve_from_python_code,
                     retrieve_from_natural_language_data, retrieve_from_google_sheets,
                     retrieve_from_document, retrieve_with_wizard,
                     save_structured_code_description, get_dynamic_signature
  LM tools         — configure_lm, list_available_models, sample_completion,
                     chain_of_thought, run_program_of_thought, optimize_module, get_lm_history
  Writer tools     — list_writers, run_writer, generate_from_template

Resource surface (maximized):
  dspygen://modules, dspygen://agents, dspygen://workflows, dspygen://signatures,
  dspygen://help, dspygen://rdddy, dspygen://signatures/all, dspygen://lm/providers,
  dspygen://rm/catalog, dspygen://writers/catalog,
  dspygen://modules/{name}, dspygen://agents/{name},
  dspygen://workflows/examples/{name}

Prompt surface (maximized — 25 prompts):
  Domain (10): design-bounded-context, create-aggregate-root, event-storm-domain,
    design-saga, create-value-object, design-api, write-command-handler,
    implement-policy, generate-read-model, scaffold-microservice
  Module (10): generate-module, create-signature, optimize-module, debug-module,
    document-module, test-module, compose-pipeline, chain-modules,
    benchmark-module, refactor-module
  Workflow (5): design-workflow, debug-pipeline, convert-to-yaml-dsl,
    optimize-pipeline, generate-workflow-tests
"""

from dspygen.mcp.server import create_server, run_sse, run_stdio

__version__ = "1.0.0"

__all__ = ["create_server", "run_stdio", "run_sse", "__version__"]
