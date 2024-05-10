from collections import defaultdict

import dsp
import dspy
from dspy.evaluate.evaluate import Evaluate
from dspy.signatures import Signature
from dspy.teleprompt.teleprompt import Teleprompter

"""
USAGE SUGGESTIONS:

The following code can be used to compile a optimized signature teleprompter, and evaluate it on an end task:

teleprompter = COPRO(prompt_model=prompt_model, metric=metric, breadth=BREADTH, depth=DEPTH, init_temperature=INIT_TEMPERATURE)
kwargs = dict(num_threads=NUM_THREADS, display_progress=True, display_table=0)
compiled_prompt_opt = teleprompter.compile(program.deepcopy(), trainset=trainset[:DEV_NUM], eval_kwargs=kwargs)
eval_score = evaluate(compiled_prompt_opt, devset=evalset[:EVAL_NUM], **kwargs)

Note that this teleprompter takes in the following parameters:

* prompt_model: The model used for prompt generation. When unspecified, defaults to the model set in settings (ie. dspy.settings.configure(lm=task_model)).
* metric: The task metric used for optimization.
* breadth: The number of new prompts to generate at each iteration. Default=10.
* depth: The number of times we should ask our prompt model to generate new prompts, with the history of the past prompts as input. Default=3.
* init_temperature: The temperature used to generate new prompts. Higher roughly equals more creative. Default=1.4.
* track_stats: Tells the method whether or not to track statistics about the optimization process.
                If True, the method will track the following statistics:
                    * results_best: The min,max,avg,stddev of top 10 scores for each predictor at each depth.
                    * results_latest: The min,max,avg,stddev of newest prompt scores for each predictor at each depth.
                    * total_calls: The total number of calls to the task metric.
                These statistics will be returned as attributes of the best program.
"""


class BasicGenerateInstruction(Signature):
    """
    As an Instruction Optimizer utilizing Lean Six Sigma principles for language model operations, this signature aims to enhance the effectiveness and efficiency of language model tasks. By receiving an initial set of instructions, your objective is to refine these instructions to maximize operational performance and minimize variability in outputs, adhering to Six Sigma quality levels.

    Utilize DMAIC (Define, Measure, Analyze, Improve, Control) methodologies to propose improvements that enhance clarity, reduce process cycle time, and ensure high accuracy in model responses, aligning with Six Sigma standards for minimal defects.
    """
    basic_instruction = dspy.InputField(
        desc="Initial instructions provided for language model operation, serving as the baseline for process improvement.")
    proposed_instruction = dspy.OutputField(
        desc="Enhanced instructions optimized for language model performance, focusing on precision and efficiency.")
    proposed_prefix_for_output_field = dspy.OutputField(
        desc="Optimized prefix that initiates the language model's task-solving process, designed to reduce lead time and improve response accuracy.")



class GenerateInstructionGivenAttempts(dspy.Signature):
    """
    This signature supports a Lean Six Sigma approach to iterative improvement for language model instruction sets. By analyzing a series of previously attempted instructions and their corresponding performance metrics, you are tasked with synthesizing a superior instruction set that drives higher quality and efficiency in language model outputs.

    Emphasize the Six Sigma goal of reducing defects (errors in language comprehension and task execution) and improving the predictability of operational outputs. Leverage insights from previous attempts to propose a new instruction that excels in clarity, effectiveness, and efficiency, supporting continuous quality improvement in line with Six Sigma KPIs.
    """
    attempted_instructions = dspy.InputField(
        format=dsp.passages2text,
        desc="Collection of prior instructions with performance scores, used to identify areas for improvement and measure the impact of iterative refinements.")
    proposed_instruction = dspy.OutputField(
        desc="Newly developed instructions expected to enhance the language model's performance, focusing on reducing variability and achieving near-zero defect rates.")
    proposed_prefix_for_output_field = dspy.OutputField(
        desc="A refined prompt beginning that facilitates faster and more accurate initiation of tasks by the language model, contributing to reduced process cycle times.")



class JSONPRO(Teleprompter):
    def __init__(
        self,
        prompt_model=None,
        metric=None,
        breadth=10,
        depth=3,
        init_temperature=1.4,
        track_stats=False,
        **_kwargs,
    ):
        if breadth <= 1:
            raise ValueError("Breadth must be greater than 1")
        self.metric = metric
        self.breadth = breadth
        self.depth = depth
        self.init_temperature = init_temperature
        self.prompt_model = prompt_model
        self.track_stats = track_stats

        if "verbose" in _kwargs:
            dspy.logger.warning("DeprecationWarning: 'verbose' has been deprecated. To see all information for debugging, use 'dspy.set_log_level('debug')'. In the future this will raise an error.")

    def _check_candidates_equal(self, candidate1, candidate2):
        for p1, p2 in zip(candidate1["program"].predictors(), candidate2["program"].predictors()):
            if self._get_signature(p1).instructions != self._get_signature(p2).instructions:
                return False
            *_, p1_last_field = self._get_signature(p1).fields.values()
            *_, p2_last_field = self._get_signature(p2).fields.values()
            if p1_last_field != p2_last_field:
                return False
        return True

    def _drop_duplicates(self, candidates):
        final_candidates = []
        last_batch = []
        last_batch_score = -1
        for c in candidates:
            repeat = False
            if c["score"] == last_batch_score:
                for c2 in last_batch:
                    if self._check_candidates_equal(c, c2):
                        repeat = True
                        break
                if not repeat:
                    last_batch.append(c)
            else:
                last_batch = [c]
                last_batch_score = c["score"]
            if not repeat:
                final_candidates.append(c)
        return final_candidates

    def _print_signature(self, predictor):
        signature = self._get_signature(predictor)

        dspy.logger.debug(f"i: {signature.instructions}")
        dspy.logger.debug(f"p: {list(signature.fields.values())[-1].json_schema_extra['prefix']}")

    def _get_signature(self, predictor):
        if hasattr(predictor, "extended_signature"):
            return predictor.extended_signature
        elif hasattr(predictor, "signature"):
            return predictor.signature

    def _set_signature(self, predictor, updated_signature):
        if hasattr(predictor, "extended_signature"):
            predictor.extended_signature = updated_signature
        elif hasattr(predictor, "signature"):
            predictor.signature = updated_signature

    def compile(self, student, *, trainset, eval_kwargs):
        """student is a program that needs to be optimized, note that it may be zero-shot or already pre-optimized for demos != []"""
        module = student.deepcopy()
        evaluate = Evaluate(devset=trainset, metric=self.metric, **eval_kwargs)
        total_calls = 0
        results_best = {
            id(p): {"depth": [], "max": [], "average": [], "min": [], "std": []} for p in module.predictors()
        }
        results_latest = {
            id(p): {"depth": [], "max": [], "average": [], "min": [], "std": []} for p in module.predictors()
        }

        if self.track_stats:
            import numpy as np

        candidates = {}
        evaluated_candidates = defaultdict(dict)

        # Seed the prompt optimizer zero shot with just the instruction, generate BREADTH new prompts
        for predictor in module.predictors():
            basic_instruction = None
            basic_prefix = None
            *_, last_key = self._get_signature(predictor).fields.keys()
            basic_instruction = self._get_signature(predictor).instructions
            basic_prefix = self._get_signature(predictor).fields[last_key].json_schema_extra["prefix"]
            if self.prompt_model:
                with dspy.settings.context(lm=self.prompt_model):
                    instruct = dspy.Predict(
                        BasicGenerateInstruction,
                        n=self.breadth - 1,
                        temperature=self.init_temperature,
                    )(basic_instruction=basic_instruction)
            else:
                instruct = dspy.Predict(
                    BasicGenerateInstruction,
                    n=self.breadth - 1,
                    temperature=self.init_temperature,
                )(basic_instruction=basic_instruction)
            # Add in our initial prompt as a candidate as well
            instruct.completions.proposed_instruction.append(basic_instruction)
            instruct.completions.proposed_prefix_for_output_field.append(basic_prefix)
            candidates[id(predictor)] = instruct.completions
            evaluated_candidates[id(predictor)] = {}

        if self.prompt_model:
            dspy.logger.debug(f"{self.prompt_model.inspect_history(n=1)}")

        latest_candidates = candidates
        all_candidates = candidates

        module_clone = module.deepcopy()

        # For each iteration in depth...
        for d in range(
            self.depth,
        ):  # TODO: fix this so that we eval the new batch of predictors with the new best followoing predictors
            dspy.logger.info(f"Iteration Depth: {d+1}/{self.depth}.")

            latest_scores = []

            # Go through our module's predictors
            for p_i, (p_old, p_new) in enumerate(zip(module.predictors(), module_clone.predictors())):
                candidates_ = latest_candidates[id(p_old)]  # Use the most recently generated candidates for evaluation
                if len(module.predictors()) > 1:
                    candidates_ = all_candidates[
                        id(p_old)
                    ]  # Unless our program has multiple predictors, in which case we need to reevaluate all prompts with the new prompt(s) for the other predictor(s)

                # For each candidate
                for c_i, c in enumerate(candidates_):
                    # Get the candidate instruction and prefix
                    instruction, prefix = (
                        c.proposed_instruction.strip('"').strip(),
                        c.proposed_prefix_for_output_field.strip('"').strip(),
                    )

                    # Set this new module with our instruction / prefix
                    *_, last_key = self._get_signature(p_new).fields.keys()
                    updated_signature = (
                        self._get_signature(p_new)
                        .with_instructions(instruction)
                        .with_updated_fields(last_key, prefix=prefix)
                    )
                    self._set_signature(p_new, updated_signature)

                    # Score the instruction / prefix
                    for i, predictor in enumerate(module_clone.predictors()):
                        dspy.logger.debug(f"Predictor {i+1}")
                        self._print_signature(predictor)
                    dspy.logger.info(
                        f"At Depth {d+1}/{self.depth}, Evaluating Prompt Candidate #{c_i+1}/{len(candidates_)} for Predictor {p_i+1} of {len(module.predictors())}.",
                    )
                    score = evaluate(module_clone, devset=trainset, **eval_kwargs)
                    if self.prompt_model:
                        dspy.logger.debug(f"prompt_model.inspect_history(n=1) {self.prompt_model.inspect_history(n=1)}")
                    total_calls += 1

                    replace_entry = True
                    dspy.logger.debug(f"(instruction, prefix) {(instruction, prefix)}")
                    if (instruction, prefix) in evaluated_candidates[id(p_old)]:
                        if evaluated_candidates[id(p_old)][(instruction, prefix)]["score"] >= score:
                            replace_entry = False

                    if replace_entry:
                        # Add it to our evaluated candidates list
                        evaluated_candidates[id(p_old)][(instruction, prefix)] = {
                            "score": score,
                            "program": module_clone.deepcopy(),
                            "instruction": instruction,
                            "prefix": prefix,
                            "depth": d,
                        }

                    if len(candidates_) - self.breadth <= c_i:
                        latest_scores.append(score)

                if self.track_stats:
                    results_latest[id(p_old)]["depth"].append(d)
                    results_latest[id(p_old)]["max"].append(max(latest_scores))
                    results_latest[id(p_old)]["average"].append(sum(latest_scores) / len(latest_scores))
                    results_latest[id(p_old)]["min"].append(min(latest_scores))
                    results_latest[id(p_old)]["std"].append(np.std(latest_scores))

                # Now that we've evaluated the candidates, set this predictor to the best performing version
                # to ensure the next round of scores reflect the best possible version
                best_candidate = max(evaluated_candidates[id(p_old)].values(), key=lambda candidate: candidate["score"])
                *_, last_key = self._get_signature(p_old).fields.keys()
                updated_signature = (
                    self._get_signature(p_new)
                    .with_instructions(best_candidate["instruction"])
                    .with_updated_fields(last_key, prefix=best_candidate["prefix"])
                )
                self._set_signature(p_new, updated_signature)

                dspy.logger.debug(
                    f"Updating Predictor {id(p_old)} to:\ni: {best_candidate['instruction']}\np: {best_candidate['prefix']}",
                )
                dspy.logger.debug("Full predictor with update: ")
                for i, predictor in enumerate(module_clone.predictors()):
                    dspy.logger.debug(f"Predictor {i}")
                    self._print_signature(predictor)

            if d == self.depth - 1:
                break

            new_candidates = {}
            for p_base in module.predictors():
                # Build Few-Shot Example of Optimized Prompts
                attempts = []
                shortest_len = self.breadth
                shortest_len = min(len(evaluated_candidates[id(p_base)]), shortest_len)
                best_predictors = list(evaluated_candidates[id(p_base)].values())

                # best_predictors = evaluated_candidates[id(p_base)].values()[:]
                best_predictors.sort(key=lambda x: x["score"], reverse=True)

                if self.track_stats:
                    scores = [x["score"] for x in best_predictors][:10]
                    results_best[id(p_base)]["depth"].append(d)
                    results_best[id(p_base)]["max"].append(max(scores))
                    results_best[id(p_base)]["average"].append(sum(scores) / len(scores))
                    results_best[id(p_base)]["min"].append(min(scores))
                    results_best[id(p_base)]["std"].append(np.std(scores))

                for i in range(shortest_len - 1, -1, -1):
                    # breakpoint()
                    attempts.append(f'Instruction #{shortest_len-i}: {best_predictors[i]["instruction"]}')
                    attempts.append(f'Prefix #{shortest_len-i}: {best_predictors[i]["prefix"]}')
                    attempts.append(f'Resulting Score #{shortest_len-i}: {best_predictors[i]["score"]}')

                # Generate next batch of potential prompts to optimize, with previous attempts as input
                if self.prompt_model:
                    with dspy.settings.context(lm=self.prompt_model):
                        instr = dspy.Predict(
                            GenerateInstructionGivenAttempts,
                            n=self.breadth,
                            temperature=self.init_temperature,
                        )(attempted_instructions=attempts)
                else:
                    instr = dspy.Predict(
                        GenerateInstructionGivenAttempts,
                        n=self.breadth,
                        temperature=self.init_temperature,
                    )(attempted_instructions=attempts)

                if self.prompt_model:
                    dspy.logger.debug(f"(self.prompt_model.inspect_history(n=1)) {self.prompt_model.inspect_history(n=1)}")
                # Get candidates for each predictor
                new_candidates[id(p_base)] = instr.completions
                all_candidates[id(p_base)].proposed_instruction.extend(instr.completions.proposed_instruction)
                all_candidates[id(p_base)].proposed_prefix_for_output_field.extend(
                    instr.completions.proposed_prefix_for_output_field,
                )

            if self.prompt_model:
                dspy.logger.debug(f"{self.prompt_model.inspect_history(n=1)}")
            latest_candidates = new_candidates

        candidates = []
        for predictor in module.predictors():
            candidates.extend(list(evaluated_candidates[id(predictor)].values()))

            if self.track_stats:
                best_predictors = list(evaluated_candidates[id(predictor)].values())
                best_predictors.sort(key=lambda x: x["score"], reverse=True)

                scores = [x["score"] for x in best_predictors][:10]
                results_best[id(predictor)]["depth"].append(d)
                results_best[id(predictor)]["max"].append(max(scores))
                results_best[id(predictor)]["average"].append(sum(scores) / len(scores))
                results_best[id(predictor)]["min"].append(min(scores))
                results_best[id(predictor)]["std"].append(np.std(scores))

        candidates.sort(key=lambda x: x["score"], reverse=True)

        candidates = self._drop_duplicates(candidates)

        best_program = candidates[0]["program"]
        best_program.candidate_programs = candidates
        best_program.total_calls = total_calls
        if self.track_stats:
            best_program.results_best = results_best
            best_program.results_latest = results_latest

        return best_program
