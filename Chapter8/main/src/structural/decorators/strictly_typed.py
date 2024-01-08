import inspect
import functools


def strictly_typed(function):
    #Данный декоратор требует, чтобы все аргументы и возвращаемое значение были аннотированы соответствуцющими типами данных.
    #Проверяет наличие в указанной функции аннотаций с типами для всех аргументов и возвращаемого значения и во время выполнения проверяет
    #соответствие фактических аргументов ожидаемым типам данных
    annotations = function.__annotations__
    arg_spec = inspect.getfullargspec(function)

    assert "return" in annotations, "missing type for return value"
    for arg in arg_spec.args + arg_spec.kwonlyargs:
        assert arg in annotations, ("missing type for parameter '" + arg + "'")

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        for name, arg in (list(zip(arg_spec.args, args)) +
                          list(kwargs.items())):
            assert isinstance(arg, annotations[name]), (
                    "expected argument '{0}' of {1} got {2}".format(
                        name, annotations[name], type(arg)))
        result = function(*args, **kwargs)
        assert isinstance(result, annotations["return"]), (
                "expected return of {0} got {1}".format(
                    annotations["return"], type(result)))
        return result
    return wrapper