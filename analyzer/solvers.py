from cvxpy.reductions.solvers.defines import CONIC_SOLVERS, QP_SOLVERS, SOLVER_MAP_CONIC
from cvxpy.atoms import EXP_ATOMS, PSD_ATOMS, SOC_ATOMS, NONPOS_ATOMS
from cvxpy.constraints import (
    ExpCone,
    PSD,
    SOC,
    NonNeg,
    NonPos,
    Inequality,
    Equality,
    Zero,
)
from cvxpy.error import DCPError
import cvxpy as cp


def get_solvers(problem):
    """Get valid solvers.
    """

    if problem.is_dcp():
        # Our choice of solver depends upon which atoms are present in the
        # problem. The types of atoms to check for are SOC atoms, PSD atoms,
        # and exponential atoms.
        atoms = problem.atoms()
        cones = []
        if any(atom in SOC_ATOMS for atom in atoms) or any(
            type(c) == SOC for c in problem.constraints
        ):
            cones.append(SOC)
        if any(atom in EXP_ATOMS for atom in atoms) or any(
            type(c) == ExpCone for c in problem.constraints
        ):
            cones.append(ExpCone)
        if any(atom in NONPOS_ATOMS for atom in atoms) or any(
            type(c) in [Inequality, NonPos, NonNeg] for c in problem.constraints
        ):
            cones.append(NonNeg)
        if any(type(c) in [Equality, Zero] for c in problem.constraints):
            cones.append(Zero)
        if (
            any(atom in PSD_ATOMS for atom in atoms)
            or any(type(c) == PSD for c in problem.constraints)
            or any(v.is_psd() or v.is_nsd() for v in problem.variables())
        ):
            cones.append(PSD)

        # Here, we make use of the observation that canonicalization only
        # increases the number of constraints in our problem.
        has_constr = len(cones) > 0 or len(problem.constraints) > 0

        valid_solvers = []
        for solver in CONIC_SOLVERS:
            solver_instance = SOLVER_MAP_CONIC[solver]
            if all(c in solver_instance.SUPPORTED_CONSTRAINTS for c in cones) and (
                has_constr or not solver_instance.REQUIRES_CONSTR
            ):
                valid_solvers.append(solver)

        # Report valid solvers.
        print("The following solvers can be used to solve the problem:")
        print(valid_solvers)
        # Report installed solvers.
        installed = [slv for slv in valid_solvers if slv in cp.installed_solvers()]
        print("Of these solvers, the following are installed already:")
        print(installed)
        return installed
    elif prob.is_dgp():
        print("DGP not yet supported.")
    elif prob.is_dqcp():
        print("DQCP not yet supported.")
    else:
        raise DCPError
