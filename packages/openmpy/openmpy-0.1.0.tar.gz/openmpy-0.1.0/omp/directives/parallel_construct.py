from omp.core.openmp import Directive, OpenMP
from omp.core.threading import Team
from omp.core.ast_tools import LinenoStripper

import ast
import random


@OpenMP.directive('parallel')
class ParallelConstruct(Directive):

    """
    OpenMP parallel construct implementation.
    """

    @property
    def template(self):
        nonce = random.randint(0, 100000)
        return f"""\
with _omp_internal.core.openmp.OpenMP():
    if False:
        pass # Replaced by shared variables declarations
    @_omp_internal.directives.parallel_construct.run_parallel
    def _omp_internal_inner_func{nonce}():
        pass # Replaced by user code
    _omp_internal_inner_func{nonce}()
        """

    def parse(self, node: ast.With) -> ast.With:
        # Parse the template to AST.
        ast_template = LinenoStripper().visit(ast.parse(self.template, mode='exec'))

        # Extract the if statement.
        if_stmt: ast.If = ast_template.body[0].body[0]

        # Extract the inner function definition.
        inner_func: ast.FunctionDef = ast_template.body[0].body[1]

        shared = self.list_locals(node.body)

        # Replace the pass statement in the if body.
        if_stmt.body = self.replace(if_stmt.body, self.assign_shared(shared))

        # List the shared variables
        nonlocals = []
        if len(shared) > 0:
            nonlocals = [ast.Nonlocal(names=list(shared))]

        # Replace the pass statement in the inner function body.
        inner_func.body = self.replace(inner_func.body, nonlocals + node.body)
        return ast_template.body[0]


def run_parallel(func):
    """
    When the new function is called, creates a team of threads that will each run the given function concurrently.
    Decorates the given function.
    """

    def wrapped(*args, **kwargs):
        team = Team(size=None, target=func, args=args, kwargs=kwargs)

        team.start()
        team.join()
    return wrapped
