import os
from enum import Enum, auto

import dspy

from dspygen.utils.dspy_tools import init_dspy

from dspygen.mixin.fsm.fsm_mixin import FSMMixin, trigger
from dspygen.modules.condition_sufficient_info_module import condition_sufficient_info_call
from dspygen.modules.query_generator_module import query_generator_call
#from dspygen.modules.refine_results_module import refine_results_module_call
from dspygen.modules.source_selector_module import source_selector_call
from dspygen.utils.scraping_tools import execute_brave_search_queries, scrape_urls, execute_duckduckgo_queries


class LearningAgentState(Enum):
    """ Enum representing the states in the learning objectives lifecycle. """
    INPUT_OBJECTIVES = auto()
    GENERATE_QUERIES = auto()
    EXECUTE_SEARCH = auto()
    SELECT_URLS = auto()
    SCRAPE_AND_CONVERT = auto()
    DISCARD_IRRELEVANT = auto()
    DECIDE_SUFFICIENCY = auto()
    REGENERATE_QUERIES = auto()
    COMPLETING_TASK = auto()
    END = auto()

class LearningAgent(FSMMixin):
    def __init__(self, objectives):
        # super().setup_fsm(LearningAgentState, initial=LearningAgentState.EXECUTE_SEARCH)
        super().setup_fsm(LearningAgentState, initial=LearningAgentState.INPUT_OBJECTIVES)
        self.objectives = objectives
        self.current_objective = None
        self.queries = {}
        self.search_results = {}
        self.selected_urls = {}
        self.scraped_content = {}
        self.refined_content = {}
        self.sufficient_info = {}

    @trigger(source=LearningAgentState.INPUT_OBJECTIVES, dest=LearningAgentState.GENERATE_QUERIES)
    def process_input(self):
        """Processes the initial input of learning objectives."""
        # Placeholder: processing input and setting up initial data
        # print("Processing input objectives.")

    @trigger(source=LearningAgentState.GENERATE_QUERIES, dest=LearningAgentState.EXECUTE_SEARCH)
    def generate_queries(self):
        """Generate search queries for each learning objective using the query_generator module."""
        self.queries = {objective: query_generator_call(objective) for objective in self.objectives}
        # print(f"Generated search queries: {self.queries}")

    @trigger(source=LearningAgentState.EXECUTE_SEARCH, dest=LearningAgentState.SELECT_URLS)
    def execute_search(self):
        """Execute the generated search queries using the Brave Search API."""
        # api_key = os.getenv("BRAVE_API_KEY")
        # self.search_results = execute_brave_search_queries(self.queries, api_key)
        self.search_results = execute_duckduckgo_queries(self.queries)
        print(f"Search results: {self.search_results}")

    @trigger(source=LearningAgentState.SELECT_URLS, dest=LearningAgentState.SCRAPE_AND_CONVERT)
    def select_urls(self):
        """Select URLs based on search results using the source_selector module."""
        # Assuming self.search_results is populated with search results for each objective
        self.selected_urls = {objective: source_selector_call(self.search_results[objective]) for objective in self.objectives}
        print(f"Selected URLs: {self.selected_urls}")

    @trigger(source=LearningAgentState.SCRAPE_AND_CONVERT, dest=LearningAgentState.DISCARD_IRRELEVANT)
    def scrape_and_convert(self):
        """Scrape the selected URLs and convert to text."""
        for objective, urls in self.selected_urls.items():
            # Extract only the URLs to pass to the scrape_urls function
            url_list = [url['url'] for url in urls]
            self.scraped_content[objective] = scrape_urls(url_list)
        print(f"Scraped and converted content.")

    @trigger(source=LearningAgentState.DISCARD_IRRELEVANT, dest=LearningAgentState.DECIDE_SUFFICIENCY)
    def discard_irrelevant(self):
        """Directly relay the scraped content without refining."""
        self.refined_content = self.scraped_content
        print(f"Refined content: {self.refined_content}")
        
        
        #self.refined_content = {objective: refine_results_module_call(self.scraped_content[objective]) for objective in self.objectives}
        #print(f"Refined content: {self.refined_content}")

    @trigger(source=LearningAgentState.DECIDE_SUFFICIENCY, dest=LearningAgentState.COMPLETING_TASK, conditions=['is_information_sufficient'])
    def decide_sufficiency(self):
        """Decide if the information gathered for each learning objective is sufficient."""
        for objective, contents in self.refined_content.items():
            # Assuming `contents` is a list of contents from different sources
            # Evaluate the combined sufficiency across all sources for the current objective
            sufficiency_results = [condition_sufficient_info_call(objective, content) for content in contents]
            # Objective is considered sufficient if all source checks return 1
            self.sufficient_info[objective] = all(sufficiency_results)
            print(f"Information for '{objective}' sufficient across all sources: {self.sufficient_info[objective]}")

    @trigger(source=LearningAgentState.DECIDE_SUFFICIENCY, dest=LearningAgentState.REGENERATE_QUERIES, unless=['is_information_sufficient'])
    def regenerate_queries(self):
        """Regenerate queries for insufficient information and limit to one loop."""
        # Placeholder: regenerating queries
        print("Regenerating queries for insufficient information.")

    @trigger(source=LearningAgentState.REGENERATE_QUERIES, dest=LearningAgentState.EXECUTE_SEARCH)
    def loop_back(self):
        """Loop back to execute search with new queries."""
        print("Looping back to execute search with new queries.")

    @trigger(source=LearningAgentState.COMPLETING_TASK, dest=LearningAgentState.END)
    def complete_task(self):
        """Complete the learning task."""
        print("Task completed.")

    def is_information_sufficient(self):
        """Check if the information gathered is sufficient across all objectives."""
        # Check if all values in sufficient_info are True
        return all(self.sufficient_info.values())


def main():
    # Example objectives
    init_dspy(dspy.OllamaLocal, model="llama3")
    objectives = ["how to finetune a llama 3 lora model"]
    agent = LearningAgent(objectives)
    print("Initial state:", agent.state)

    # Manually triggering each step to simulate workflow
    agent.process_input()
    agent.generate_queries()
    agent.execute_search()
    agent.select_urls()
    agent.scrape_and_convert()
    agent.discard_irrelevant()
    agent.decide_sufficiency()

    # Check if there is a need to regenerate queries
    if not agent.is_information_sufficient():
        agent.regenerate_queries()
        agent.execute_search()
        agent.select_urls()
        agent.scrape_and_convert()
        agent.discard_irrelevant()
        agent.decide_sufficiency()

    agent.complete_task()
    print("Final state:", agent.state)

if __name__ == "__main__":
    main()

