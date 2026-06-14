"""DSPyGen IPython magic commands for notebook workflows."""

import importlib
import inspect
import pkgutil
import sys
from typing import Any, Optional

import yaml

try:
    from IPython.core.magic import (
        Magics,
        cell_magic,
        line_cell_magic,
        line_magic,
        magics_class,
        register_cell_magic,
        register_line_magic,
    )
    from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
    from IPython.display import display
    _IPYTHON_AVAILABLE = True
except ImportError:
    _IPYTHON_AVAILABLE = False
    # Provide stubs so the module can still be imported outside IPython
    def magics_class(cls):
        return cls

    class Magics:
        def __init__(self, shell=None, **kwargs):
            self.shell = shell

    def line_magic(fn):
        return fn

    def cell_magic(fn):
        return fn

    def magic_arguments(fn):
        return fn

    def argument(*args, **kwargs):
        def decorator(fn):
            return fn
        return decorator

    def parse_argstring(fn, arg_string):
        return arg_string

    def display(*args, **kwargs):
        pass


from dspygen.jupyter.display import (
    display_agent_state,
    display_module_output,
    display_pipeline_result,
)


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _scan_package_modules(package_name: str):
    """Return a list of (module_name, module_path) tuples for a package."""
    try:
        package = importlib.import_module(package_name)
    except ImportError:
        return []

    package_path = getattr(package, "__path__", [])
    results = []
    for importer, modname, ispkg in pkgutil.iter_modules(package_path):
        if not ispkg and not modname.startswith("_"):
            results.append((modname, f"{package_name}.{modname}"))
    return results


def _import_dspygen_module(module_name: str):
    """
    Attempt to import a DSPyGen module by short name.

    Tries the following locations in order:
      1. dspygen.modules.<module_name>
      2. dspygen.modules.<module_name>_module
      3. The raw name as a fully-qualified import path
    """
    candidates = [
        f"dspygen.modules.{module_name}",
        f"dspygen.modules.{module_name}_module",
        module_name,
    ]
    for candidate in candidates:
        try:
            return importlib.import_module(candidate)
        except ImportError:
            continue
    raise ImportError(
        f"Cannot find dspygen module '{module_name}'. "
        "Use %dspygen_modules to list available modules."
    )


def _find_callable_in_module(mod):
    """
    Return the first DSPy Module subclass or a `forward` / `module_call`
    callable found in the imported Python module.
    """
    try:
        import dspy
        dspy_module_cls = dspy.Module
    except ImportError:
        dspy_module_cls = None

    # Prefer a DSPy Module subclass
    for name, obj in inspect.getmembers(mod, inspect.isclass):
        if dspy_module_cls and issubclass(obj, dspy_module_cls) and obj is not dspy_module_cls:
            return obj

    # Fall back to a module-level `module_call` function
    if hasattr(mod, "module_call"):
        return mod.module_call

    # Fall back to any public callable named *forward*
    for name, obj in inspect.getmembers(mod, callable):
        if name == "forward":
            return obj

    return None


# ---------------------------------------------------------------------------
# Magics class
# ---------------------------------------------------------------------------

@magics_class
class DSPyGenMagics(Magics):
    """IPython magic commands for the DSPyGen framework."""

    # ------------------------------------------------------------------
    # %dspygen <module_name> [args...]
    # ------------------------------------------------------------------
    @line_magic
    def dspygen(self, line: str):
        """
        Run a DSPyGen module inline.

        Usage::

            %dspygen text_summarizer_module "text to summarize"
            %dspygen blog_module topic="AI trends" length=500
        """
        parts = line.strip().split(None, 1)
        if not parts:
            print("Usage: %dspygen <module_name> [args]")
            return

        module_name = parts[0]
        raw_args = parts[1] if len(parts) > 1 else ""

        # Parse trailing args: key=value pairs and positional strings
        kwargs = {}
        positional = []
        for token in _tokenize_args(raw_args):
            if "=" in token:
                k, _, v = token.partition("=")
                kwargs[k.strip()] = v.strip().strip('"').strip("'")
            else:
                positional.append(token.strip().strip('"').strip("'"))

        try:
            mod = _import_dspygen_module(module_name)
        except ImportError as exc:
            print(f"[dspygen] Error: {exc}")
            return

        callable_obj = _find_callable_in_module(mod)
        if callable_obj is None:
            print(f"[dspygen] No callable found in module '{module_name}'.")
            return

        try:
            # If it's a class, instantiate then call .forward() or __call__
            if inspect.isclass(callable_obj):
                instance = callable_obj()
                if hasattr(instance, "forward"):
                    result = instance.forward(*positional, **kwargs)
                else:
                    result = instance(*positional, **kwargs)
            else:
                result = callable_obj(*positional, **kwargs)

            display_module_output(result)
            # Store result in IPython namespace for reuse
            if self.shell is not None:
                self.shell.user_ns["_dspygen_result"] = result

        except Exception as exc:
            print(f"[dspygen] Runtime error: {exc}")
            import traceback
            traceback.print_exc()

    # ------------------------------------------------------------------
    # %%dspygen_pipeline
    # ------------------------------------------------------------------
    @cell_magic
    def dspygen_pipeline(self, line: str, cell: str):
        """
        Execute a YAML DSL pipeline.

        Usage::

            %%dspygen_pipeline
            steps:
              - module: text_summarizer_module
                args:
                  text: "Long article text here"
              - module: blog_module
                args:
                  topic: "{{ previous_output }}"
        """
        try:
            pipeline_def = yaml.safe_load(cell)
        except yaml.YAMLError as exc:
            print(f"[dspygen_pipeline] YAML parse error: {exc}")
            return

        if not isinstance(pipeline_def, dict) or "steps" not in pipeline_def:
            print("[dspygen_pipeline] Pipeline must have a top-level 'steps' key.")
            return

        steps = pipeline_def["steps"]
        results = []
        previous_output = None

        for i, step in enumerate(steps):
            module_name = step.get("module")
            step_args = step.get("args", {})
            step_name = step.get("name", f"step_{i + 1}")

            if not module_name:
                print(f"[dspygen_pipeline] Step {i + 1} has no 'module' key; skipping.")
                continue

            # Simple template substitution for {{ previous_output }}
            resolved_args = {}
            for k, v in step_args.items():
                if isinstance(v, str) and "{{ previous_output }}" in v:
                    v = v.replace("{{ previous_output }}", str(previous_output or ""))
                resolved_args[k] = v

            print(f"\n[dspygen_pipeline] Running {step_name}: {module_name} ...")
            try:
                mod = _import_dspygen_module(module_name)
                callable_obj = _find_callable_in_module(mod)
                if callable_obj is None:
                    print(f"  No callable found in '{module_name}'; skipping.")
                    continue

                if inspect.isclass(callable_obj):
                    instance = callable_obj()
                    if hasattr(instance, "forward"):
                        result = instance.forward(**resolved_args)
                    else:
                        result = instance(**resolved_args)
                else:
                    result = callable_obj(**resolved_args)

                previous_output = result
                results.append({"step": step_name, "module": module_name, "result": result})
                print(f"  Done. Output preview: {str(result)[:120]}")

            except Exception as exc:
                print(f"  Error in step '{step_name}': {exc}")
                results.append({"step": step_name, "module": module_name, "result": None, "error": str(exc)})

        display_pipeline_result(results)

        if self.shell is not None:
            self.shell.user_ns["_dspygen_pipeline_results"] = results

    # ------------------------------------------------------------------
    # %%dspygen_signature <name>
    # ------------------------------------------------------------------
    @cell_magic
    def dspygen_signature(self, line: str, cell: str):
        """
        Define a DSPy Signature from cell content.

        Usage::

            %%dspygen_signature MySummarizer
            text: str = dspy.InputField(desc="Text to summarize")
            summary: str = dspy.OutputField(desc="Concise summary")
        """
        sig_name = line.strip()
        if not sig_name:
            print("Usage: %%dspygen_signature <ClassName>")
            return

        try:
            import dspy
        except ImportError:
            print("[dspygen_signature] dspy is not installed.")
            return

        # Build class body with dspy in scope
        class_src = f"class {sig_name}(dspy.Signature):\n"
        for raw_line in cell.splitlines():
            stripped = raw_line.strip()
            if stripped:
                class_src += f"    {stripped}\n"

        namespace = {"dspy": dspy}
        try:
            exec(compile(class_src, "<dspygen_signature>", "exec"), namespace)
        except Exception as exc:
            print(f"[dspygen_signature] Error compiling signature: {exc}")
            print("Generated source:\n", class_src)
            return

        sig_cls = namespace.get(sig_name)
        if sig_cls is None:
            print(f"[dspygen_signature] Class '{sig_name}' was not created.")
            return

        # Inject into IPython namespace so the user can reference it
        if self.shell is not None:
            self.shell.user_ns[sig_name] = sig_cls

        print(f"[dspygen_signature] Signature '{sig_name}' defined and available in the notebook namespace.")
        try:
            print(f"  Fields: {list(sig_cls.fields.keys())}")
        except AttributeError:
            pass

    # ------------------------------------------------------------------
    # %dspygen_init [model]
    # ------------------------------------------------------------------
    @line_magic
    def dspygen_init(self, line: str):
        """
        Configure DSPy with an LM backend.

        Usage::

            %dspygen_init                     # defaults to gpt-4o-mini
            %dspygen_init gpt-4o
            %dspygen_init ollama/llama3
        """
        from dspygen.utils.dspy_tools import init_dspy

        model = line.strip() or "gpt-4o-mini"

        # Basic heuristic: if model starts with "ollama/" use OllamaLocal
        try:
            import dspy
            if model.startswith("ollama/"):
                from dspygen.utils.dspy_tools import init_ol
                actual_model = model[len("ollama/"):]
                lm = init_ol(model=actual_model)
                print(f"[dspygen_init] Configured DSPy with OllamaLocal model '{actual_model}'.")
            else:
                lm = init_dspy(model=model)
                print(f"[dspygen_init] Configured DSPy with model '{model}'.")

            if self.shell is not None:
                self.shell.user_ns["_dspygen_lm"] = lm

        except Exception as exc:
            print(f"[dspygen_init] Error: {exc}")

    # ------------------------------------------------------------------
    # %dspygen_history
    # ------------------------------------------------------------------
    @line_magic
    def dspygen_history(self, line: str):
        """
        Display the LM call history stored in dspy.settings.lm.

        Usage::

            %dspygen_history
            %dspygen_history 5   # show last N entries
        """
        try:
            import dspy
            lm = dspy.settings.lm
            if lm is None:
                print("[dspygen_history] No LM configured. Run %dspygen_init first.")
                return

            history = getattr(lm, "history", None)
            if history is None:
                print("[dspygen_history] LM does not expose a history attribute.")
                return

            limit_str = line.strip()
            limit = int(limit_str) if limit_str.isdigit() else None
            entries = list(history)[-limit:] if limit else list(history)

            if not entries:
                print("[dspygen_history] No LM calls recorded yet.")
                return

            print(f"[dspygen_history] Showing {len(entries)} call(s):\n")
            for idx, entry in enumerate(entries, 1):
                print(f"  [{idx}] prompt={str(entry.get('prompt', entry))[:80]}...")

        except Exception as exc:
            print(f"[dspygen_history] Error: {exc}")

    # ------------------------------------------------------------------
    # %dspygen_modules
    # ------------------------------------------------------------------
    @line_magic
    def dspygen_modules(self, line: str):
        """
        List all available DSPyGen modules in a formatted table.

        Usage::

            %dspygen_modules
        """
        modules = _scan_package_modules("dspygen.modules")
        if not modules:
            print("[dspygen_modules] No modules found in dspygen.modules.")
            return

        try:
            from IPython.display import HTML, display as ip_display

            rows = "".join(
                f"<tr><td style='padding:4px 12px'>{i}</td>"
                f"<td style='padding:4px 12px'><code>{name}</code></td>"
                f"<td style='padding:4px 12px; color:#666'>{full}</td></tr>"
                for i, (name, full) in enumerate(modules, 1)
            )
            html = (
                "<table style='border-collapse:collapse'>"
                "<thead><tr>"
                "<th style='padding:4px 12px'>#</th>"
                "<th style='padding:4px 12px'>Module</th>"
                "<th style='padding:4px 12px'>Full path</th>"
                "</tr></thead>"
                f"<tbody>{rows}</tbody></table>"
            )
            ip_display(HTML(html))
        except Exception:
            print(f"{'#':<4} {'Module':<45} {'Full path'}")
            print("-" * 80)
            for i, (name, full) in enumerate(modules, 1):
                print(f"{i:<4} {name:<45} {full}")

    # ------------------------------------------------------------------
    # %dspygen_agents
    # ------------------------------------------------------------------
    @line_magic
    def dspygen_agents(self, line: str):
        """
        List all available DSPyGen agents.

        Usage::

            %dspygen_agents
        """
        agents = _scan_package_modules("dspygen.agents")
        if not agents:
            print("[dspygen_agents] No agents found in dspygen.agents.")
            return

        try:
            from IPython.display import HTML, display as ip_display

            rows = "".join(
                f"<tr><td style='padding:4px 12px'>{i}</td>"
                f"<td style='padding:4px 12px'><code>{name}</code></td>"
                f"<td style='padding:4px 12px; color:#666'>{full}</td></tr>"
                for i, (name, full) in enumerate(agents, 1)
            )
            html = (
                "<table style='border-collapse:collapse'>"
                "<thead><tr>"
                "<th style='padding:4px 12px'>#</th>"
                "<th style='padding:4px 12px'>Agent</th>"
                "<th style='padding:4px 12px'>Full path</th>"
                "</tr></thead>"
                f"<tbody>{rows}</tbody></table>"
            )
            ip_display(HTML(html))
        except Exception:
            print(f"{'#':<4} {'Agent':<45} {'Full path'}")
            print("-" * 80)
            for i, (name, full) in enumerate(agents, 1):
                print(f"{i:<4} {name:<45} {full}")


# ---------------------------------------------------------------------------
# Argument tokenizer (handles quoted strings)
# ---------------------------------------------------------------------------

def _tokenize_args(raw: str):
    """Split a raw argument string respecting quoted substrings."""
    import shlex
    try:
        return shlex.split(raw)
    except ValueError:
        return raw.split()


# ---------------------------------------------------------------------------
# Extension entry points
# ---------------------------------------------------------------------------

def load_ipython_extension(ip):
    """Register all DSPyGen magics and print a welcome banner."""
    ip.register_magics(DSPyGenMagics)
    print(
        "\n"
        "  DSPyGen Jupyter extension loaded.\n"
        "\n"
        "  Available magics:\n"
        "    %dspygen_init [model]           — configure the LM backend\n"
        "    %dspygen <module> [args]        — run a DSPyGen module\n"
        "    %dspygen_modules                — list available modules\n"
        "    %dspygen_agents                 — list available agents\n"
        "    %dspygen_history [n]            — show LM call history\n"
        "    %%dspygen_signature <Name>      — define a DSPy Signature\n"
        "    %%dspygen_pipeline              — run a YAML pipeline\n"
        "\n"
        "  Get started: %dspygen_init gpt-4o-mini\n"
    )


def unload_ipython_extension(ip):
    """Clean up when the extension is unloaded."""
    # IPython does not provide a built-in way to deregister magics;
    # remove our names from the magic registry if they exist.
    for magic_name in (
        "dspygen",
        "dspygen_init",
        "dspygen_modules",
        "dspygen_agents",
        "dspygen_history",
    ):
        ip.magics_manager.magics.get("line", {}).pop(magic_name, None)

    for magic_name in ("dspygen_pipeline", "dspygen_signature"):
        ip.magics_manager.magics.get("cell", {}).pop(magic_name, None)

    print("[DSPyGen] Jupyter extension unloaded.")
