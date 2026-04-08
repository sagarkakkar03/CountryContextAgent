import asyncio
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from dotenv import load_dotenv
from langsmith import Client
from langsmith.evaluation import evaluate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

load_dotenv()

from app.agent.graph import graph

class Grade(BaseModel):
    score: int = Field(description="Score of 1 if the answer is correct, 0 if it is incorrect.")
    reasoning: str = Field(description="Step-by-step reasoning for the score.")

judge_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0).with_structured_output(Grade)

def correctness_evaluator(run, example) -> dict:
    """
    This function takes the agent's output and the expected answer, 
    and asks the Judge LLM to grade it.
    """
    user_query = example.inputs["query"]
    agent_answer = run.outputs["final_answer"]
    expected_answer = example.outputs["expected_answer"]

    judge_prompt = f"""
    You are an expert grader evaluating an AI agent.
    
    User Question: {user_query}
    Expected Fact: {expected_answer}
    Agent's Answer: {agent_answer}
    
    Did the agent correctly state the expected fact in its answer?
    It does not need to be an exact word match, but the factual meaning must be correct.
    """
    
    grade = judge_llm.invoke(judge_prompt)
    
    return {
        "key": "correctness",
        "score": grade.score,
        "comment": grade.reasoning
    }

def predict(inputs: dict) -> dict:
    """
    LangSmith calls this function for every row in our dataset.
    Since our graph is async, we use asyncio.run to execute it here.
    """
    result = asyncio.run(graph.ainvoke({"query": inputs["query"]}))
    return {"final_answer": result["final_answer"]}

def main():
    client = Client()
    dataset_name = "Country Agent Dataset"
    
    if not client.has_dataset(dataset_name=dataset_name):
        print(f"Creating dataset '{dataset_name}'...")
        dataset = client.create_dataset(dataset_name=dataset_name)
        
        examples = [
            ("What is the capital of France?", "Paris"),
            ("What currency does Japan use?", "Yen"),
            ("What is the population of Narnia?", "Narnia is not a real country / not found"),
            ("Compare the capital of Germany and Italy.", "Berlin and Rome")
        ]
        
        for query, expected in examples:
            client.create_example(
                inputs={"query": query},
                outputs={"expected_answer": expected},
                dataset_id=dataset.id
            )
    
    print("Running evaluation...")
    experiment_results = evaluate(
        predict,
        data=dataset_name,
        evaluators=[correctness_evaluator],
        experiment_prefix="llm-as-judge-test",
    )
    
    print("Evaluation complete! Check your LangSmith dashboard.")

if __name__ == "__main__":
    main()