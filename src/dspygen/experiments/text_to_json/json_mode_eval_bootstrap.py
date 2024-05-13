

def main():
    """Main function"""
    from dspy.teleprompt import BootstrapFewShot
    from dspygen.experiments.text_to_json.json_mode_eval_dataset import JsonModeEvalDataset
    from dspygen.utils.dspy_tools import init_ol
    # Set up the LM
    lm = init_ol(model="phi3:instruct", max_tokens=20000)
    # lm = init_ol(model="llama3", max_tokens=20000)

    # Load the SWE-bench dataset
    swe_bench = JsonModeEvalDataset()
    swe_bench_trainset, swe_bench_devset = swe_bench.train, swe_bench.dev

    # print(swe_bench_trainset)

    # Set up the optimizer: we want to "bootstrap" (i.e., self-generate) 4-shot examples of our CoT program.
    config = dict(max_bootstrapped_demos=4, max_labeled_demos=4)

    from dspygen.modules.prompt_to_json_module import compare_example_to_prediction, PromptToJSONModule
    teleprompter = BootstrapFewShot(metric=compare_example_to_prediction, **config)
    optimized_cot = teleprompter.compile(PromptToJSONModule(), trainset=swe_bench_trainset)

    from datetime import datetime

    # Get the current time in UTC
    current_time_utc = datetime.utcnow()

    # Convert the datetime object to a string in the format 'YYYY-MM-DD HH:MM:SS'
    zulu_time_str = current_time_utc.strftime('%Y-%m-%d_%H_%M_%S')
    optimized_cot.save(f"optimized_cot_bootstrap_sig_{zulu_time_str}.json")

    from dspy.evaluate import Evaluate

    # Set up the evaluator, which can be used multiple times.
    evaluate = Evaluate(devset=swe_bench_devset, metric=compare_example_to_prediction, num_threads=1, display_progress=True,
                        display_table=0)

    # Evaluate our `optimized_cot` program.
    evaluate(optimized_cot)

    print(lm.inspect_history(n=1))


if __name__ == '__main__':
    main()
