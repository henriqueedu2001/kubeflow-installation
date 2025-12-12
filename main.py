from kfp import dsl
from kfp import compiler

@dsl.component
def square_a(n: float) -> float:
    return n**2

@dsl.component
def square_b(n: float) -> float:
    return n**2

@dsl.component
def square_sum(squared_a: float, squared_b: float) -> float:
    return squared_a + squared_b

@dsl.component
def calc_hypotenuse(square_sum: float) -> float:
    return square_sum**0.5

@dsl.pipeline
def hello_pipeline(side_a: float, side_b: float) -> float:
    square_a_task = square_a(n=side_a)
    square_b_task = square_b(n=side_b)
    square_sum_task = square_sum(squared_a=square_a_task.output, squared_b=square_b_task.output)
    hypo = calc_hypotenuse(square_sum=square_sum_task.output)
    return hypo.output

compiler.Compiler().compile(hello_pipeline, 'pipeline.yaml')