"""Contains main Benchmark Test."""

import json
import os
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any, Optional

import pandas as pd

from .DocumentMatch import DocumentMatchScore
from .LexicalMetrics import evaluate_exact_f1_rouge
from .semanticSimilarity import calculate_semantic_similarity_score
from ..test_utils.database_utils import save_benchmark_results


@dataclass
class Document:
    """
    Represents a base document with its page_content and metadata.

    Attributes:
        page_content (str): Content of the page.
        metadata (dict[str, Any]): Metadata for the document.
        id (str): ID for the document.
        parent_id (Optional[str]): Parent ID if this document has a parent in a hierarchical vector store.
    """

    page_content: str
    metadata: Dict[str, Any]
    id: str
    parent_id: Optional[str] = None


class BenchmarkTest:
    """Class for testing LLM and RAGs.

    :param question_set_path: Path to json file containing generated questions and answers

    USAGE:

    ```python

    # Import the benchmarking module
    from chATLAS_Benchmark import BenchmarkTest

    # Initialize the test set
    test = BenchmarkTest(question_set_path)

    # --- Run the RAG on the questions ---
    # Assuming RAG.run() returns an answer and list of docs for each question
    gen_answers = []
    gen_docs = []
    for q in test.questions:
        answer, docs = RAG.run(q)
        gen_answers.append(answer)
        gen_docs.append(docs)

    # Set generated answers and documents on the test instance
    test.set_generated_data(gen_answers, gen_docs)

    # Run the scoring with any metrics you want
    scores = test.score_test_set("LexicalMetrics", "SemanticSimilarity", "DocumentMatch")

    # Save the results to the db
    test_1.store_results(scores, db_dir="database.db", name="NameOfRAG")
    ```

    **ADDITIONAL NOTES**
    For DocumentMatch test, RAG needs to return documents with attribute `metadata` (dict) with key ("name")
     i.e. it finds document names via `document.metadata["name"]`
    """

    def __init__(self, question_set_path: Path | str):
        """
        Inputs:
        question_set_path: Path to json file containing test questions and answers
        """

        # UPDATE WHENEVER NEW TEST ADDED WITH NAME AND FUNCTION TO BE CALLED
        # Define implemented tests
        self.implemented_tests = {
            "LexicalMetrics": evaluate_exact_f1_rouge,
            "SemanticSimilarity": calculate_semantic_similarity_score,
            "DocumentMatch": DocumentMatchScore,
        }

        self.questions: List[List[str]] = [[]]  # Placeholder for test questions
        self.answers = []  # Placeholder for generated answers
        self.documents: List[List[Document]] | List[List[str]] = [
            []
        ]  # Placeholder for retrieved document contexts

        self.test_answers = []  # Placeholder for test answers
        self.test_documents: List[List[str]] = [
            []
        ]  # Placeholder for test document contexts

        self.question_set_path = (
            question_set_path  # Storing path of qa pairs for results saving
        )

        # Load questions if a path is provided
        if question_set_path:
            question_set = self.load_question_set(question_set_path)
            self.set_test_data(question_set)

    @staticmethod
    def load_question_set(json_path: Path | str) -> List[Dict[str, str]]:
        """Load a set of questions from a JSON file.

        Args:
            json_path (Path): Path to the JSON file containing question-answer pairs.

        Returns:
            List[Dict[str, str]]: List of questions with associated metadata.
        """

        json_path_relative = Path(json_path).resolve()

        json_path_relative = os.path.join(os.getcwd(), json_path)

        with open(json_path_relative, "r") as file:
            data = json.load(file)

        return data

    def set_test_data(self, question_set: List[Dict[str, str]]):
        """Sets the questions, answers, and documents variables based on
        provided question set.

        Args:
            question_set (List[Dict[str, str]]): List of questions and their answers and document contexts.
        """
        self.questions = [item["question"] for item in question_set]
        self.test_answers = [item["answer"] for item in question_set]
        self.test_documents = [[item["document"]] for item in question_set]

    def set_generated_data(
        self, answers: List[str], documents: List[List[Document]] | List[List[str]]
    ):
        """Sets the generated answers and documents from an external model for
        evaluation.

        Args:
            answers (List[str]): List of generated answers.
            documents (List[List[Document]]): List of retrieved document contexts, with each sub list containing each
            document for the corresponding question. NOTE: This should be passed in as standard document form from Embed
            with attributes .page_content, .metadata and .similarity
        """
        if len(answers) != len(documents):
            raise ValueError(
                "Length of answers and documents do not match! If no documents are returned by RAG make "
                "sure it returns an empty list instead."
            )
        self.answers = answers
        self.documents = documents

    def store_results(self, scores, db_name="benchmark.db", name="Unknown_RAG"):
        """Stores the results from the various tests run to a SQL database for
        later retrieval. Also stores the question path used to generate the
        results.

        :param scores: (pd.Dataframe) - Scores generated from this test
        :param db_name: (str) - name of the database to store results in -> currently stores in current working directory
        :param name: (str) - name of the model to store in the db
        """

        save_benchmark_results(
            model_name=name,
            db_name=db_name,
            question_path=self.question_set_path,
            scores=scores,
        )

    def score_test_set(self, *args: str) -> Dict[str, pd.DataFrame]:
        """Evaluates answer relevancy on the current test set using stored
        answers and documents.

        Args:
            *args (str): Names of the tests to run. Possible options are:
                "LexicalMetrics",
                "SemanticSimilarity",
                "DocumentMatch"
        Returns:
            Dict[str, pd.DataFrame]: Dictionary where keys are test names and values are DataFrames of scoring results.
        """

        # Data for testing functions
        data = {
            "questions": self.questions,
            "answers": self.answers,
            "documents": self.documents,
            "test_answers": self.test_answers,
            "test_documents": self.test_documents,
        }

        # Collect scores for each requested test
        scores = {}
        for test_name in args:
            if test_name in self.implemented_tests:
                print(f"Running {test_name} test...")
                scores[test_name] = self.implemented_tests[test_name](data)
            else:
                raise ValueError(
                    f"""'{test_name}' test is not implemented.

                Possible options are:
                {self.implemented_tests.keys()}"""
                )

        return scores
