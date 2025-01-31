from pennylane import numpy as np
from pennylane.math import partial_trace, reduce_statevector, fidelity_statevector
from scipy.special import kl_div


class EntanglingCapacity:
    def __init__(self, circuit, dev, params_shape):
        """
        Initializes the EntanglingCapacity class with the given circuit, device, and parameter shape.

        Args:
            circuit: the QNode representing the quantum circuit
            dev: quantum device used for simulation
            params_shape: shape of the parameters for the circuit
        """
        self.circuit = circuit
        self.dev = dev
        self.params_shape = params_shape
        self.N = len(dev.wires)  # Number of qubits

    def generate_random_params(self):
        """
        Generates random parameters for the quantum circuit based on the specified parameter shape.
        """
        return np.random.uniform(0, 2 * np.pi, self.params_shape)

    def meyer_wallach_entanglement(self, n_samples):
        """
        Computes the Meyer-Wallach entanglement measure for the quantum circuit.

        Args:
            n_samples (int): Number of samples to calculate the entanglement measure

        Returns:
            float: Meyer-Wallach entanglement measure averaged over multiple samples.
        """
        res = np.zeros(n_samples, dtype=complex)

        for i in range(n_samples):
            params = self.generate_random_params()  # Random parameters for the PQC
            state = self.circuit(params)  # Get quantum state from the PQC

            # Reduce the full state vector to density matrix for the entire system
            rho = reduce_statevector(state, indices=self.dev.wires)

            entropy = self._calculate_entropy(rho)

            # Meyer-Wallach measure for the current state
            res[i] = 1 - (entropy / self.N)

        # Average over the samples and return
        return float(2 * np.mean(res).real)

    def _calculate_entropy(self, rho):
        """
        Helper function to calculate the average entropy over all qubits.

        Args:
            rho: the reduced state of the quantum system (density matrix).
            
        Returns:
            float: Entropy
        """
        entropy = 0
        qb_indices = list(range(self.N))

        # Loop over each qubit, calculate the partial trace and its entropy
        for j in range(self.N):
            # Partial trace over all qubits except the j-th qubit
            dens = partial_trace(rho, qb_indices[:j] + qb_indices[j+1:])
            trace = np.trace(dens**2)  # Calculate the purity (trace of the square of density matrix)
            entropy += trace

        return entropy

class Expressibility:
    def __init__(self, pqc, params_shape, dev):
        """
        Initialize the Expressibility class.

        Args:
            pqc (qml.QNode): Parameterized quantum circuit.
            params_shape (tuple): Shape of the parameters used in the PQC.
            dev (qml.Device): Pennylane device for executing the PQC.
        """
        self.pqc = pqc       
        self.params_shape = params_shape
        self.dev = dev

    def generate_random_params(self, params_shape):
        """
        Generate random parameters for the parameterized quantum circuit.

        Args:
            params_shape (tuple): Shape of the parameters.

        Returns:
            np.ndarray: Randomly generated parameters in the range [0, 2π].
        """
        return np.random.uniform(0, 2 * np.pi, params_shape)

    def pqc_fidelity(self, n_samples):
        """
        Calculate the fidelity between quantum states produced by the PQC.

        Args:
            n_samples (int): Number of samples for fidelity computation.

        Returns:
            list: List of fidelity values for the sampled states.
        """
        fidelities = []
        for _ in range(n_samples):
            # Get random parameters for PQC1 and PQC2
            params1 = self.generate_random_params(self.params_shape)
            params2 = self.generate_random_params(self.params_shape)
            state1 = self.pqc(params1)
            state2 = self.pqc(params2)
            # Calculate fidelity between the two states
            fidelities.append(fidelity_statevector(state1, state2))
        return fidelities

    def haar_fidelity(self, n_samples):
        """
        Generate fidelities for Haar-random states.

        Args:
            n_samples (int): Number of samples for fidelity computation.

        Returns:
            np.ndarray: Array of Haar-random fidelities.
        """
        n_qubits = len(self.dev.wires)
        N = 2**n_qubits
        F = np.random.uniform(0, 1, n_samples)
        return (N-1) * (1 - F)**(N-2)

    def compute_expressibility(self, n_samples):
        """
        Compute the expressibility of the PQC by comparing its fidelity distribution
        to that of Haar-random states using KL divergence.

        Args:
            n_samples (int): Number of samples for the computation.

        Returns:
            float: Expressibility value, computed as the mean KL divergence.
        """
        pqc_f = self.pqc_fidelity(n_samples)
        haar_f = self.haar_fidelity(n_samples)
        return float(np.mean(kl_div(pqc_f, haar_f)))
