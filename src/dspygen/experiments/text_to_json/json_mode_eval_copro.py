def main():
    from dspygen.experiments.text_to_json.json_mode_error_dataset import JsonModeErrorDataset
    from dspygen.modules.prompt_to_json_module import compare_example_to_prediction

    """Main function"""
    from dspygen.utils.dspy_tools import init_ol
    init_ol(model="phi3:medium-128k")

    # dataset = JsonModeEvalDataset()
    dataset = JsonModeErrorDataset()

    from dspy.teleprompt import COPRO

    teleprompter = COPRO(
        metric=compare_example_to_prediction,
        verbose=True,
        depth=3,
        breadth=3,
    )

    kwargs = dict(num_threads=1,
                  display_progress=True,
                  display_table=0)  # Used in Evaluate class in the optimization process
    from dspygen.modules.prompt_to_json_module import PromptToJSONModule
    cot = PromptToJSONModule()
    compiled_prompt_opt = teleprompter.compile(cot,
                                               trainset=dataset.train[:5],
                                               eval_kwargs=kwargs)
    from datetime import datetime

    # Get the current time in UTC
    current_time_utc = datetime.utcnow()

    # Convert the datetime object to a string in the format 'YYYY-MM-DD HH:MM:SS'
    zulu_time_str = current_time_utc.strftime('%Y-%m-%d_%H-%M-%S')

    compiled_prompt_opt.save(f"compiled_prompt_opt_advanced_{zulu_time_str}.json")
    cot.save(f"cot_{zulu_time_str}.json")


if __name__ == '__main__':
    while True:
        main()
