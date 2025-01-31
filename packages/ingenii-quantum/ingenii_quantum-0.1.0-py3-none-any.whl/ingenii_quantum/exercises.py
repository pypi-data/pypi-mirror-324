import numpy as np
from qiskit.quantum_info import Statevector
import pennylane as qml
from qiskit import QuantumCircuit
        
#################
# Exercises chapter 2
#################

def exercise2_1(vector):
    vector = np.array(vector)
    assert np.isclose(np.abs(vector[0])**2, 1/2),  f"Wrong state, try again. The probability of state |0⟩ should be 0.5."
    assert np.angle(vector[0]) == np.angle(vector[1]), f"Wrong state, try again. The two components should have equal sign."
    assert len(vector)==2, f"Wrong state, try again.  Incorrect vector dimension."


def exercise2_2(vector):
    vector = np.array(vector)
    assert np.isclose(np.abs(vector[0])**2, 1/4),  f"Wrong state, try again. The probability of state |0⟩ should be 0.5."
    assert np.angle(vector[0]) == np.angle(vector[1]), f"Wrong state, try again. The two components should have equal sign."
    assert len(vector)==2, f"Wrong state, try again.  Incorrect vector dimension."

def exercise2_3(vector):
    vector = np.array(vector)
    assert np.isclose(np.abs(vector[0])**2, 1/2), f"Wrong state, try again. The probability of state |0⟩ should be 0.25."
    assert np.isclose(np.abs(np.angle(vector[0]) - np.angle(vector[1])), np.pi), f"Wrong state, try again. The two components should have opposite sign."
    assert len(vector)==2, f"Wrong state, try again.  Incorrect vector dimension."


def exercise2_4(counts):
    total_counts = np.sum(list(counts.values()))
    assert total_counts == 4096, f'Incorrect number of runs.'
    assert np.isclose(counts['00']/total_counts, 1/2, 0.1) and np.isclose(counts['11']/total_counts, 1/2, 0.1), f'Incorrect distribution.'

def exercise2_5(vector):
    vector = np.array(vector)
    assert np.isclose(np.abs(vector[0])**2, 1/2) and np.isclose(np.abs(vector[3])**2, 0.3) and np.isclose(np.abs(vector[7])**2, 0.2), f"Wrong state, try again. The probability of the basis states are incorrect."
    assert np.isclose(np.angle(vector[0]), np.pi/2) and np.isclose(np.angle(vector[3]), np.pi) and np.isclose(np.angle(vector[7]), 0), f"Wrong state, try again. The two components should have opposite sign."
    assert len(vector)==2**3, f"Wrong state, try again.  Incorrect vector dimension."

        
#################
# Exercises chapter 3
#################

def exercise3_1(qc):
    vector = Statevector(qc).data
    assert np.isclose(np.abs(vector[0])**2, 1),  f"Wrong state, try again. The probability of state |0⟩ should be 1."
    assert len(vector)==2, f"Wrong state, try again.  Incorrect vector dimension."

def exercise3_2(qc):
    vector = Statevector(qc).data
    assert np.isclose(np.abs(vector[0b0101])**2, 1),  f"Wrong state, try again. The state should be |0101⟩"
    assert len(vector)==2**4, f"Wrong state, try again.  Incorrect vector dimension."

def exercise3_3(qc):
    vector = Statevector(qc)
    assert len(vector)==4, f"Wrong state, try again.  Incorrect vector dimension."
    assert np.isclose(np.abs(vector[1])**2 + np.abs(vector[3])**2, 0.8),  f"Wrong state, try again. The probability of qubit 1 being on state |1⟩ should be 0.8."
    
def exercise3_4(qc):
    vector = Statevector(qc)
    assert len(vector)==4, f"Wrong state, try again.  Incorrect vector dimension."
    assert np.isclose(np.abs(vector[1])**2, 0.5),  f"Wrong state, try again. The probability of state |01⟩ should be 0.5."
    assert np.isclose(np.abs(vector[2])**2, 0.5),  f"Wrong state, try again. The probability of state |10⟩ should be 0.5."
    assert np.isclose(np.abs(np.angle(vector[1]) - np.angle(vector[2])), np.pi), f"Wrong state, try again. The two components should have opposite sign."

def exercise3_5(qc):
    vector = Statevector(qc)
    assert len(vector)==2**3, f"Wrong state, try again.  Incorrect vector dimension."
    assert np.isclose(np.abs(vector[0])**2, 0.5),  f"Wrong state, try again. The probability of state |000⟩ should be 0.5."
    assert np.isclose(np.abs(vector[7])**2, 0.5),  f"Wrong state, try again. The probability of state |111⟩ should be 0.5."
    assert np.isclose(np.abs(np.angle(vector[0]) - np.angle(vector[7])),0), f"Wrong state, try again. The two components should have the same sign."
    
def exercise3_6(qc):
    gate_names = [op[0].name for op in qc.data]
    for g in gate_names:
        assert g in ['cx', 'x', 'h', 'rx', 'rz', 'ry', 'z'], f"Use the gates you learned in this lesson!"
    assert qc.num_qubits==2, f"Wrong state, try again.  Incorrect vector dimension."
    # Try state 00
    qc_init = QuantumCircuit(2)
    qc_all = qc_init.compose(qc, qubits=[0,1])
    vector = Statevector(qc_all)
    assert np.isclose(np.abs(vector[0])**2, 1),  f"Wrong state, try again. The circuit shoud map the state |00⟩ to the state |00⟩"
    # Try state 01
    qc_init = QuantumCircuit(2)
    qc_init.x(0)
    qc_all = qc_init.compose(qc, qubits=[0,1])
    vector = Statevector(qc_all)
    assert np.isclose(np.abs(vector[2])**2, 1),  f"Wrong state, try again. The circuit shoud map the state |01⟩ to the state |10⟩"
    # Try state 01
    qc_init = QuantumCircuit(2)
    qc_init.x(1)
    qc_all = qc_init.compose(qc, qubits=[0,1])
    vector = Statevector(qc_all)
    assert np.isclose(np.abs(vector[1])**2, 1),  f"Wrong state, try again. The circuit shoud map the state |10⟩ to the state |01⟩"
    # Try state 11
    qc_init = QuantumCircuit(2)
    qc_init.x(0)
    qc_init.x(1)
    qc_all = qc_init.compose(qc, qubits=[0,1])
    vector = Statevector(qc_all)
    assert np.isclose(np.abs(vector[3])**2, 1),  f"Wrong state, try again. The circuit shoud map the state |11⟩ to the state |11⟩"

def get_secret_state(theta=np.pi, phi = np.pi/2):
    qc = QuantumCircuit(1)
    qc.ry(2 * theta, 0)
    qc.rz(phi, 0)
    return qc

def exercise3_7(qc):
    vector = Statevector(qc)
    assert np.isclose(np.abs(vector[0])**2, 1),  f"Wrong state, try again. The circuit should output state |0⟩"
    
def exercise3_8(qc, phi):
    vector = Statevector(qc)
    assert len(vector)==2, f"Wrong state, try again.  Incorrect vector dimension."
    assert np.isclose(np.abs(vector[0])**2, 0.5),  f"Wrong state, try again. The probability of state |0⟩ should be 0.5."
    assert np.isclose(np.abs(vector[1])**2, 0.5),  f"Wrong state, try again. The probability of state |1⟩ should be 0.5."
    assert np.isclose(np.abs(np.angle(vector[0]) - np.angle(vector[1])),phi), f"Wrong state, try again. The relative phase should be {phi:.5f}"
    
def exercise3_9(result_x, result_y, phi):
    total_counts = np.sum(list(result_x.values()))
    p_plus = result_x['0']/total_counts
    p_iplus = result_y['0']/total_counts
    assert np.isclose(p_plus,(1 + np.cos(phi))/2, atol=0.1), f'Incorrect measurement in the X basis.'
    assert np.isclose(p_iplus,(1 + np.sin(phi))/2, atol=0.1), f'Incorrect measurement in the X basis.'

def exercise3_10(phi_reconstructed, phi):
    assert np.isclose(phi_reconstructed, phi, atol=0.1), f'Incorrect value of phi = {phi_reconstructed}'

#################
# Exercises chapter 4
#################


def exercise4_1(num_qubits, num_gates, depth, gates):
    print(f"Number of qubits: {num_qubits}, Number of gates: {num_gates}, Depth: {depth}, Gates: {gates}")
    assert num_qubits==4, f'Wrong number of qubits'
    assert num_gates==80, f'Wrong number of gates'
    assert depth==41, f'Wrong depth'
    assert gates=={'Rot':40, 'CNOT':40}, f'Wrong number of qubits'    


def exercise4_3(qnode, num_qubits, num_gates, depth, X_train, random_weights):
    print(f"Number of qubits: {num_qubits}, Number of gates: {num_gates}, Depth: {depth}")
    num_qubits2 = []
    num_gates2 = []
    depth2 = []
    for X in X_train[:10]:
        qnode(X, random_weights)
        expanded_tape = qnode.qtape.expand(depth=2)
        specs = expanded_tape.specs
        num_qubits2.append(specs['resources'].num_wires)
        num_gates2.append(specs['resources'].num_gates)
        depth2.append(specs['resources'].depth)
    num_qubits2 = np.mean(num_qubits2)
    num_gates2 = np.mean(num_gates2)
    depth2 = np.mean(depth2)
    assert num_qubits==num_qubits2, f'Wrong number of qubits'
    assert num_gates==num_gates2, f'Wrong number of gates'
    assert depth==depth2, f'Wrong depth'

#################
# Exercises chapter 5 and 6
#################
def exercise5_7(total_single_qubit_gates, total_entangling_gates, processor):
    total_single_qubit_gates2 = processor.info['num_circuits']*(processor.info['gates']['RX'] + processor.info['gates']['H'])
    total_entangling_gates2 = processor.info['num_circuits']*processor.info['num_nonlocal_gates']
    assert total_single_qubit_gates==total_single_qubit_gates2, f'Wrong total number of single qubit gates.'
    assert total_entangling_gates2==total_entangling_gates, f'Wrong total number of entangling qubit gates.'


def exercise6_1(n_blocks, nqbits=8):
    true_nblocks = qml.MERA.get_n_blocks(range(nqbits), 2)
    assert true_nblocks==n_blocks

def exercise6_2(template_weights):
    assert np.array(template_weights).shape==(3,2,4)

def exercise6_3(gates):
    assert gates==[84, 180, 756, 1524], f'Wrong number of gates.'

def exercise6_4(params_model_reduced):
    assert params_model_reduced==7162792, f'Wrong number of parameters for compressed model'

def exercise6_6(params_model_reduced):
    assert params_model_reduced==7897351, f'Wrong number of parameters for compressed model'