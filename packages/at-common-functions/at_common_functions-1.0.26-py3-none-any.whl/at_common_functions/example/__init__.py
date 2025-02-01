from at_common_workflow import export

@export
def echo(*, in_msg: str) -> str:
    return in_msg

@export
def reverse(*, in_msg: str) -> str:
    return in_msg[::-1]

@export
def add_integers(*, num1:int, num2: int) -> int:
    return num1 + num2