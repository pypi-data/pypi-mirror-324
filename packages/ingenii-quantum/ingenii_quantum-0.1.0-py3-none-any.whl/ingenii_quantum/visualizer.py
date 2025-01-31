import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.quantum_info import Statevector
from qiskit.converters import circuit_to_dag
from qiskit.visualization import circuit_drawer
from qiskit.circuit.tools.pi_check import pi_check
from qiskit.quantum_info import partial_trace, Operator, DensityMatrix, purity

from io import BytesIO
from PIL import Image

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.patches import FancyArrowPatch, Circle, Ellipse
from mpl_toolkits.mplot3d import proj3d
from mpl_toolkits.mplot3d.art3d import Patch3D
from functools import reduce
from .custom import custom_style
import warnings


class Arrow3D(Patch3D, FancyArrowPatch):
    """
    A 3D arrow class for visualizing quantum states on a Bloch sphere or Q-sphere.

    This class extends `Patch3D` and `FancyArrowPatch` to create a 3D arrow
    that can be used to represent vectors in quantum state visualization.

    Attributes:
        xs (list): X-coordinates of the arrow.
        ys (list): Y-coordinates of the arrow.
        zs (list): Z-coordinates of the arrow.
        zdir (str): Direction of the arrow (default: "z").
    """
    __module__ = "mpl_toolkits.mplot3d.art3d"

    def __init__(self, xs, ys, zs, zdir="z", **kwargs):
        """
        Initializes the 3D arrow with the given coordinates and direction.

        Args:
            xs (list): X-coordinates of the arrow.
            ys (list): Y-coordinates of the arrow.
            zs (list): Z-coordinates of the arrow.
            zdir (str, optional): Direction of the arrow. Default is "z".
            **kwargs: Additional arguments for `FancyArrowPatch`.
        """
        FancyArrowPatch.__init__(self, (0, 0), (0, 0), **kwargs)
        self.set_3d_properties(tuple(zip(xs, ys)), zs, zdir)
        self._path2d = None

    def draw(self, renderer):
        """
        Renders the 3D arrow on the given Matplotlib renderer.

        Args:
            renderer (matplotlib.backend_bases.RendererBase): The renderer to draw the arrow.
        """
        xs3d, ys3d, zs3d = zip(*self._segment3d)
        x_s, y_s, _ = proj3d.proj_transform(xs3d, ys3d, zs3d, self.axes.M)
        self._path2d = matplotlib.path.Path(np.column_stack([x_s, y_s]))
        self.set_positions((x_s[0], y_s[0]), (x_s[1], y_s[1]))
        FancyArrowPatch.draw(self, renderer)

class QuantumVisualizer:
    def __init__(self, qc):
        """
        Initialize the StateSpaceVisualizer with a quantum circuit.

        Args:
            qc (QuantumCircuit): The input quantum circuit or statevector.
        """
        self.qc = qc
        self.display_math = False
        self.arrows = []  # Stores arrow connections
        if isinstance(qc, QuantumCircuit):
            self.num_qubits = qc.num_qubits
            self.vectors, self.gate_set = self.get_statevectors()

    @staticmethod
    def bit_string_index(s):
        """
        Return the index of a string of 0s and 1s.

        Args:
            s (string): bit string

        Returns:
            int: index of the string.
        """
        n = len(s)
        k = s.count("1")
        if s.count("0") != n - k:
            raise ValueError("s must be a string of 0 and 1")
        ones = [pos for pos, char in enumerate(s) if char == "1"]
        return QuantumVisualizer.lex_index(n, k, ones)

    @staticmethod
    def n_choose_k(n, k):
        """
        Return the number of combinations for n choose k.

        Args:
            n (int): the total number of options .
            k (int): The number of elements.

        Returns:
            int: binomial coefficient
        """
        if n == 0:
            return 0
        return reduce(lambda x, y: x * y[0] / y[1], zip(range(n - k + 1, n + 1), range(1, k + 1)), 1)
    
    @staticmethod
    def lex_index( n, k, lst):
        """
        Return  the lex index of a combination..

        Args:
            n (int): the total number of options .
            k (int): The number of elements.
            lst (list): list

        Returns:
            int: returns int index for lex order

        Raises:
            VisualizationError: if length of list is not equal to k
        """
        if len(lst) != k:
            raise VisualizationError("list should have length k")
        comb = list(map(lambda x: n - 1 - x, lst))
        dualm = sum(QuantumVisualizer.n_choose_k(comb[k - 1 - i], i + 1) for i in range(k))
        return int(dualm)
    
    @staticmethod
    def count_control_num(gate_name):
        """
        Count the number of consecutive 'c' characters in a gate name.

        Args:
            gate_name (str): The name of the gate.

        Returns:
            int: The number of consecutive 'c' characters.
        """
        return len(gate_name) - len(gate_name.lstrip('c'))


    def get_transformed_bitstrings(self, unitary, tol=1e-8):
        """
        Compute the transformation of all basis states under a unitary matrix and output the transformed bitstrings.

        Args:
            unitary (np.ndarray): The unitary matrix of size (2^n, 2^n).
            tol (float): Tolerance for considering a value as non-zero.

        Returns:
            dict: A dictionary mapping input bitstrings to their transformed bitstrings.
        """
        # Determine the number of qubits
        dim = unitary.shape[0]
        n = int(np.log2(dim))

        # Prepare a dictionary for the results
        transformations = {}
        for i in range(dim):
            # Input basis state as a bitstring
            input_bitstring = format(i, f"0{n}b")
            # Transformation of the basis state (column of the unitary matrix)
            transformed_state = unitary[:, i]
            # Identify the output bitstrings with significant amplitudes
            transformed_bitstrings = [
                format(idx, f"0{n}b") for idx, amp in enumerate(transformed_state)
                if np.abs(amp) > tol
            ]
            # Store the mapping
            transformations[input_bitstring] = transformed_bitstrings
        return transformations
    
    def get_statevectors(self):
        """
        Extract statevectors and gate information from the quantum circuit.

        Returns:
            tuple: (list of statevectors, gate set)
        """
        dag = circuit_to_dag(self.qc)
        state = Statevector.from_label('0' * self.qc.num_qubits)
        vectors = [np.array(state)]
        gate_set = [{}]

        # Create new registers with desired names
        new_qr = QuantumRegister(len(self.qc.qubits), 'q')  # Renamed quantum register
        new_cr = ClassicalRegister(len(self.qc.clbits), 'c') if self.qc.clbits else None  # Renamed classical register
        self.qc_barriers =  QuantumCircuit(new_qr, new_cr) if new_cr else QuantumCircuit(new_qr)
        
        for i, layer in enumerate(dag.layers()):
            # Create new registers with desired names
            layer_circuit = QuantumCircuit(new_qr, new_cr) if new_cr else QuantumCircuit(new_qr)
            
            nodes, qargs_list = [], []
            # Iterate over all operation nodes (gates) in the layer
            for node in layer['graph'].op_nodes():
                if node.name not in ['barrier', 'measure', 'reset', 'initialize']:
                    # Map the qubits and classical bits to the new registers
                    qargs = [new_qr[self.qc.qubits.index(q)] for q in node.qargs]
                    cargs = [new_cr[self.qc.clbits.index(c)] for c in node.cargs] if node.cargs else []
                    # Add the gate to the layer circuit and the full circuit with barriers
                    layer_circuit.append(node.op, qargs=qargs, cargs=cargs) 
                    self.qc_barriers.append(node.op, qargs=qargs, cargs=cargs)
                    nodes.append(node)
                    qargs_list.append(qargs)         
                elif node.name == 'initialize':
                    warnings.warn('Initialize operation not implemented for state space vizualization.')

            if len(nodes)>0:
                # Build circuit for gate
                flattened_qargs = [item for sublist in qargs_list for item in sublist]
                flattened_qargs = sorted(flattened_qargs, key=lambda qubit: qubit._index)
                qubits = [n._index for n in flattened_qargs]
                qc_u = QuantumCircuit(flattened_qargs)
                for j, node in enumerate(nodes):
                    qc_u.append(node.op, qargs=qargs_list[j])
                # Get unitary matrix
                U = Operator(qc_u).data
                # Get bitstrings transformations
                bitstring_transformations = self.get_transformed_bitstrings(U, tol=1e-8)
                gate_set.append({
                    'layer_id': i,
                    'num_qubits': len(qubits),
                    'name': [n.name for n in nodes],
                    'qubits': qubits,
                    'bitstring_transformations': bitstring_transformations
                })

                state = state.evolve(layer_circuit)
                vectors.append(np.array(state))
                self.qc_barriers.barrier() 

        return vectors, gate_set

    @staticmethod
    def hex_to_rgb(hex_str):
        """
        Convert a hexadecimal color string to an RGB tuple.

        Args:
            hex_str (str): The hexadecimal color string.

        Returns:
            np.ndarray: The RGB color as a numpy array.
        """
        return np.array([int(hex_str[i:i+2], 16) for i in range(1, 6, 2)]) / 255

    @staticmethod
    def color_range(c1, c2, n):
        """
        Generate a color gradient between two colors.

        Args:
            c1 (str): The starting color in hexadecimal.
            c2 (str): The ending color in hexadecimal.
            n (int): The number of gradient steps.

        Returns:
            list: A list of colors in hexadecimal format.
        """
        c1_rgb = QuantumVisualizer.hex_to_rgb(c1)
        c2_rgb = QuantumVisualizer.hex_to_rgb(c2)
        return ["#" + "".join(f"{int(round(val * 255)):02x}" for val in (c1_rgb * (1 - t) + c2_rgb * t)) for t in np.linspace(0, 1, n)]

    @staticmethod
    def get_colors(n):
        """
        Generate a full cyclic color map with gradients.

        Args:
            n (int): Total number of colors.

        Returns:
            list: A list of colors in hexadecimal format.
        """
        m = n // 4
        return (
             QuantumVisualizer.color_range("#55d397", "#bb6bd6", m) 
            + QuantumVisualizer.color_range("#bb6bd6", "#ffcc3e", m)
            + QuantumVisualizer.color_range("#ffcc3e", "#c1c5c9", m)
            + QuantumVisualizer.color_range("#c1c5c9", "#55d397", m)
        )

    @staticmethod
    def phase_to_rgb(complex_number, n=64, tol=1e-3, return_black = True):
        """
        Map a phase of a complex number to a color.

        Args:
            complex_number (complex): The input complex number.
            n (int): Number of colors in the gradient.

        Returns:
            str: RGB color in hexadecimal format.
        """
        
        if np.abs(complex_number)<tol and return_black:
            return 'black'
        colors = QuantumVisualizer.get_colors(n)
        offset_colors = colors[-n // 4 :] + colors[:-n // 4]
        complex_number = np.round(complex_number, 3)
        real_part = 0 if np.isclose(abs(complex_number.real), 0) else complex_number.real
        im_part = 0 if np.isclose(abs(complex_number.imag), 0) else complex_number.imag
        corrected_num = real_part + 1j*im_part
        angle = (np.angle(corrected_num) % (2 * np.pi)) / (2 * np.pi)
        return offset_colors[int(angle * n)]



    def draw_basis_states(self):
        """
        Draw basis states as text labels on the y-axis.
        """
        basis_states = [f"|{format(i, f'0{self.num_qubits}b')}⟩" for i in range(2 ** self.num_qubits)]
        font_size = max(8, 22 - 2 * self.num_qubits) 
        for i, state in enumerate(basis_states):
            plt.text(0.5 - 0.03*len(self.vectors), i / len(basis_states), state, ha='center', fontsize=font_size)

    def draw_probabilities(self, statevector, position, tol=1e-3):
        """
        Draw probability circles for a given statevector.

        Args:
            statevector (np.ndarray): The statevector.
            position (int): The x-axis position of the circles.
            ax ( matplotlib.axes): axes to draw the probabilities
            tol (float): Tolerance for non-zero probabilities.
        """
        y_coords = np.arange(len(statevector)) / len(statevector)
        for i, value in enumerate(statevector):
            radius = np.abs(value)
            color = self.phase_to_rgb(value, 64, tol) # Map the phase of the complex number to a color
            base_size = 2500 / self.num_qubits if self.num_qubits>1 else 1800
            size = radius**2 * base_size if radius >= tol else base_size/100
            plt.scatter(position + 1, y_coords[i], s=size, color=color, zorder=1) # Plot the statevector magnitude
            # If `display_math` is enabled, overlay a rectangle and text showing the value
            if self.display_math and radius>=tol:
                plt.scatter(position + 1, y_coords[i], s=base_size, color='#73BBEF',alpha=0.5, marker='s', zorder=2)
                # Format the value string based on the real and imaginary parts
                if np.abs(value.imag)<tol:
                    value_str = str(np.round(value.real,2))
                elif np.abs(value.real)<tol:
                    value_str = str(np.round(value.imag,2)) + 'i'
                else:
                    value_str = str(np.round(value.real,2)) + str(np.round(value.imag,2)) + 'i'
                font_size = max(8, int(18 - 1.5 * self.num_qubits)) 
                # Add the text in the center of the rectangle
                plt.text(position + 1, y_coords[i], value_str, color='black', ha='center', va='center', fontsize=font_size, zorder=3)


    @staticmethod
    def flip_bit(bitstring, i):
        """
        Flip the bit at position i in a binary string.

        Args:
            bitstring (str): The binary string.
            i (int): The position of the bit to flip (0-indexed).

        Returns:
            str: The binary string with the bit at position i flipped.
        """
        binary_list = list(bitstring)[::-1]
        binary_list[i] = '1' if binary_list[i] == '0' else '0'
        return ''.join(binary_list[::-1])

    def draw_arrow(self, vector, old_vector, position, tol=1e-3):
        """
        Draw arrows connecting states between layers.

        Args:
            vector (np.ndarray): Current statevector (after the gate is applied).
            old_vector (np.ndarray): Previous statevector (before the gate is applied).
            position (int): The layer index (x-axis position in the visualization).
            tol (float): Tolerance for non-zero probabilities.
        """       
        # Generate normalized y-coordinates 
        y_coords = np.arange(len(vector)) / len(vector)
        
        # Generate binary labels for all basis states
        basis_states = [f"{format(i, f'0{self.num_qubits}b')}" for i in range(2 ** self.num_qubits)]
        idxs = np.arange(len(vector))  # Indexes of all basis states

        # Identify basis states with non-zero probabilities in the old and new vectors
        old_nonzero_states = np.array(basis_states)[idxs[np.abs(old_vector) > tol]].tolist()
        new_nonzero_states = np.array(basis_states)[idxs[np.abs(vector) > tol]].tolist()

        gate_info =  self.gate_set[position]
        for bitstr in old_nonzero_states:
            # Find the mapping frm the old vector basis state to the new one
            reduced_bitstring = "".join([bitstr[::-1][q] for q in gate_info['qubits'][::-1]]) # Reversing order to keep convention of basis states 
            reduced_bitstring_complementary = "".join([bitstr[::-1][q] for q in list(range(self.qc.num_qubits))[::-1] if q not in gate_info['qubits']])
            child_bitstr = []
            for new_bitstr_short in gate_info['bitstring_transformations'][reduced_bitstring]:
                new_bitstr = ""
                i_r = 0
                i_o = 0
                for n in list(range(self.qc.num_qubits))[::-1]:
                    if n in gate_info['qubits']:
                        new_bitstr += new_bitstr_short[i_r]
                        i_r+=1
                    else:
                        new_bitstr += reduced_bitstring_complementary[i_o] 
                        i_o+=1
                new_bitstr = new_bitstr  
                child_bitstr.append(new_bitstr)    
            child_bitstr = [b for b in child_bitstr if b in new_nonzero_states]

            # Draw arrows from parent states to the current state
            for child in child_bitstr:                
                bitstr_idx = basis_states.index(bitstr)  # Index of the current state
                child_bitstr_idx = basis_states.index(child)  # Index of the child state
                x, y = position, y_coords[bitstr_idx]  # Start point of the arrow
                dx, dy = 1, y_coords[child_bitstr_idx] - y  
                color = self.phase_to_rgb(vector[child_bitstr_idx])  # Determine the arrow color based on the state's phase
                plt.arrow(
                    x, y, dx, dy, color=color, linewidth=max(3, 3 + (7 - 3) * (5 - self.num_qubits) / 4), head_length=0, alpha=0.5  
                )

    def draw_state_space(self,  plot_circuit=False, plot_phase_disks = False, display_math = False, filename = None):
        """
        Visualize the quantum circuit's evolution. Optionally include the circuit diagram.

        Args:
            plot_circuit (bool): If True, include the quantum circuit diagram in the figure.
            plt_phase_disks (bool): If True, include the diagram of phase disks in the figure.
            display_math (bool): If True, include the value of the statevectors in the figure.
            filename (str): File name to save the figure.

        Returns:
            matplotlib.pyplot.figure: figure of the state space        
        """
        self.display_math = display_math
        base_size = 1 / (4 * self.num_qubits)
        figure_size = (
            max(8, len(self.vectors) + 2),
            max(4, (1.7) ** self.num_qubits + 1.7*self.num_qubits if plot_phase_disks else max(4, (1.7) ** self.num_qubits)),
        )  # Adjust figure size dynamically

        if plot_circuit:
            # Save the Qiskit circuit with barriers as an image
            dpi = 100
            circuit_image = BytesIO()
            circuit_drawer(
                self.qc_barriers, output="mpl", style=custom_style
            ).savefig(circuit_image, format="png", bbox_inches="tight", dpi=dpi, transparent = True)
            circuit_image.seek(0)
            circuit_img = Image.open(circuit_image)

            # Get the size of the circuit image in pixels
            img_width, img_height = circuit_img.size

            # Calculate the height of the image in inches
            image_fig_height = img_height / dpi

            # Create the figure with two subplots
            fig, (ax_top, ax_bottom) = plt.subplots(
                2, 1,
                figsize=(figure_size[0], figure_size[1] + image_fig_height * 1.6 ),
                gridspec_kw={"height_ratios": [image_fig_height * 1.6, figure_size[1] ]},
            )
            bottom_ratio = figure_size[1] / (figure_size[1] + image_fig_height * 1.6)

            # Aspect ratio and extent for the top image
            aspect_ratio = img_width / img_height
            ax_top.imshow(circuit_img, extent=[0, aspect_ratio, 0, 1])
            ax_top.axis("off")
            ax_top.set_xlim(
                -1.1 / len(self.vectors), aspect_ratio + 1.1 / len(self.vectors)
            )
            ax_top.set_ylim(0, 1)

            # Set the bottom axis for state space visualization
            ax = ax_bottom
        else:
            bottom_ratio = 1
            # Create a single-plot figure if no circuit diagram is included
            fig, ax = plt.subplots(figsize=figure_size)


        # Draw the state space visualization
        self.draw_basis_states()
        for i, vector in enumerate(self.vectors):
            if i > 0:
                self.draw_arrow(vector, self.vectors[i - 1], i)
                self.draw_probabilities(self.vectors[i - 1], i - 1)
        self.draw_probabilities(self.vectors[-1], len(self.vectors) - 1)

        # Plot the phase disks
        if plot_phase_disks:
            # Set up the state space axis
            ax.set_xlim(-0.2- 0.03*len(self.vectors), len(self.vectors) + 1)#(-0.2, len(self.vectors) + 1)
            ax.set_ylim(-base_size -(self.num_qubits + 2) / (2**self.num_qubits), 1)

            ax.axhline(y = -(1) / (2**self.num_qubits), color='black', linestyle='--')
            for i, vector in enumerate(self.vectors):
                for qubit in range(self.num_qubits):
                    pos_x = i + 1
                    pos_y = -(qubit + 2) / (2**self.num_qubits)
                    # Get partial trace
                    v = Statevector(vector)
                    partial_state = partial_trace(v, [i for i in range(self.num_qubits) if i!=qubit]).data
                    self._draw_disk(partial_state, qubit, radius = 0.45/np.sqrt(self.num_qubits), ax = ax, 
                                    pos_x=pos_x, pos_y=pos_y, plot_text = True if i == 0 else False, pos_label=0.5 - 0.05*len(self.vectors),
                                    bottom_ratio=bottom_ratio)         
        else:
            ax.set_xlim(-0.2 - 0.03*len(self.vectors), len(self.vectors) + 1)
            ax.set_ylim(-base_size, 1)
        ax.axis("off")

        if plot_circuit:
            plt.subplots_adjust(hspace=0.0)
        if filename:
            fig.savefig(filename, transparent = True)
        plt.close() 
        return fig
    
    @staticmethod
    def statevector_to_angles(phi):
        """
        Convert a quantum statevector into spherical coordinates (theta, phi) for Bloch sphere representation.

        Args:
            phi (ndarray): A 2-element array-like object representing a single-qubit statevector.

        Returns:
            theta (float): Polar angle (0 to pi).
            phi (float): Azimuthal angle (0 to 2*pi).
        """
        alpha, beta  = phi[0], phi[1]
        # Calculate theta, phi
        theta = 2 * np.arccos(np.abs(alpha))
        phi = np.angle(beta) - np.angle(alpha)
        return theta, phi

    def draw_bloch_sphere(self, theta=None, phi=None, ax = None, filename = None):
        """
        Visualize a single-qubit quantum state on the Bloch sphere.

        Args:
            theta (float): Polar angle for the Bloch vector (default 0).
            phi (float): Azimuthal angle for the Bloch vector (default 0).
            ax (matplotlib.axes): A Matplotlib axes to draw on (optional).
            filename (str): Path to save the plot (optional).

        Returns:
            matplotlib.figure.Figure: The Matplotlib figure object (if `fig` is not provided).
        """
        vector = Statevector(self.qc).data
        num_qubits = int(np.log2(len(vector)))
        if num_qubits!=1:
            raise ValueError("Input is not a single-qubit quantum state.")

        # Create Figure
        if ax is None:
            return_fig = True
            fig = plt.figure(figsize=(5,5))
            ax = fig.add_subplot(111, projection='3d')
        else:
            fig = ax.get_figure()
            return_fig = False
            
        # Draw a sphere
        ax.axes.set_xlim3d(-1.0, 1.0)
        ax.axes.set_ylim3d(-1.0, 1.0)
        ax.axes.set_zlim3d(-1.0, 1.0)
        ax.axes.grid(False)
        ax.view_init(elev=5, azim=275)

        # Force aspect ratio
        if hasattr(ax.axes, "set_box_aspect"):
            ax.axes.set_box_aspect((1, 1, 1))

        # Plot semi-transparent sphere
        u = np.linspace(0, 2 * np.pi, 25)
        v = np.linspace(0, np.pi, 25)
        x = np.outer(np.cos(u), np.sin(v))
        y = np.outer(np.sin(u), np.sin(v))
        z = np.outer(np.ones(np.size(u)), np.cos(v))
        ls = matplotlib.colors.LightSource(azdeg=0, altdeg=65)
        rgb = ls.shade(z, plt.cm.Blues)
        ax.plot_surface(
            x, y, z, rstride=3, cstride=3, color="#73BBEE", facecolors = rgb,  alpha=0.1, linewidth=0.3,
        )
        # Get rid of the panes
        ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

        # Get rid of the spines
        ax.xaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        ax.yaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        ax.zaxis.line.set_color((1.0, 1.0, 1.0, 0.0))

        # Get rid of the ticks
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
        if theta is None or phi is None:
            theta, phi = QuantumVisualizer.statevector_to_angles(vector)
        # Draw the state vector
        x_arrow = np.sin(theta) * np.cos(phi)
        y_arrow = np.sin(theta) * np.sin(phi)
        z_arrow = np.cos(theta)

        ax.plot([0, x_arrow], [0, y_arrow], [0, z_arrow], color='r', linewidth=2)
        ax.scatter([x_arrow], [y_arrow], [z_arrow], color='r', s=100)
        
        # Set the axes properties
        ax.set_xlim([-0.73, 0.73])
        ax.set_ylim([-0.73, 0.73])
        ax.set_zlim([-0.73, 0.73])

        # Draw the axes
        ax.quiver(0, 0, 0, 1, 0, 0, color='k', linewidth=1, arrow_length_ratio=0.1)
        ax.quiver(0, 0, 0, 0, 1, 0, color='k', linewidth=1, arrow_length_ratio=0.1)
        ax.quiver(0, 0, 0, 0, 0, 1, color='k', linewidth=1, arrow_length_ratio=0.1)
        
        # Label the axes
        ax.text(1.05, 0, 0, 'X', color='k', fontsize=14)
        ax.text(0, 1.05, 0, 'Y', color='k', fontsize=14)
        ax.text(-0.03, 0, 1.08, 'Z', color='k', fontsize=14)

        ax.set_title(f'Bloch Sphere (θ={theta:.2f}, φ={phi:.2f})', pad = -60)
        
        if filename:
            fig.savefig(filename, transparent = True)
        if return_fig:
            plt.close() 
            return fig

    
    def draw_qsphere(self, figsize=None, ax=None,
                    show_state_labels=True, show_state_phases=False,
                    use_degrees=False, tol = 1e-3,filename=None):
        
        """
        Plot the qsphere representation of a quantum state.
        Here, the size of the points is proportional to the probability
        of the corresponding term in the state and the color represents
        the phase.

        Args:
            figsize (tuple): Figure size in inches.
            ax (matplotlib.axes.Axes): An optional Axes object to be used for
                the visualization output. If none is specified a new matplotlib
                Figure will be created and used. Additionally, if specified there
                will be no returned Figure since it is redundant.
            show_state_labels (bool): An optional boolean indicating whether to
                show labels for each basis state.
            show_state_phases (bool): An optional boolean indicating whether to
                show the phase for each basis state.
            use_degrees (bool): An optional boolean indicating whether to use
                radians or degrees for the phase values in the plot.
            tol (float): tolerance to show basis state on the sphere
            filename (str): File to save the plot if desired

        Returns:
            Figure: A matplotlib figure instance if the ``ax`` kwarg is not set

        """
        # Get quantum statevector
        state = Statevector(self.qc).data
        num_qubits = int(np.log2(len(state)))
        if num_qubits<2:
            raise ValueError("Input is not a multi-qubit quantum state.")

        # Create Figure
        if figsize is None:
            figsize = (5, 5)

        if ax is None:
            return_fig = True
            fig = plt.figure(figsize=figsize)
            ax = fig.add_subplot(111, projection="3d")
        else:
            return_fig = False
            fig = ax.get_figure()
        
        ax.axes.set_xlim3d(-1.0, 1.0)
        ax.axes.set_ylim3d(-1.0, 1.0)
        ax.axes.set_zlim3d(-1.0, 1.0)
        ax.axes.grid(False)
        ax.view_init(elev=5, azim=275)

        # Force aspect ratio
        if hasattr(ax.axes, "set_box_aspect"):
            ax.axes.set_box_aspect((1, 1, 1))

        # Plot semi-transparent sphere
        u = np.linspace(0, 2 * np.pi, 25)
        v = np.linspace(0, np.pi, 25)
        x = np.outer(np.cos(u), np.sin(v))
        y = np.outer(np.sin(u), np.sin(v))
        z = np.outer(np.ones(np.size(u)), np.cos(v))
        ls = matplotlib.colors.LightSource(azdeg=0, altdeg=65)
        rgb = ls.shade(z, plt.cm.Blues)
        ax.plot_surface(
            x, y, z, rstride=3, cstride=3, color="#73BBEE", facecolors = rgb,  alpha=0.1, linewidth=0.05,
        )
        # Get rid of the panes
        ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

        # Get rid of the spines
        ax.xaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        ax.yaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        ax.zaxis.line.set_color((1.0, 1.0, 1.0, 0.0))

        # Get rid of the ticks
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])

        # Set the axes properties
        ax.set_xlim([-0.93, 0.93])
        ax.set_ylim([-0.93, 0.93])
        ax.set_zlim([-0.93, 0.93])
        ax.set_title(f'Q-sphere', pad = -60)

        # Add center point
        ax.plot([0], [0], [0],
                markerfacecolor="#73BBEE", markeredgecolor="#73BBEE",
                marker="o",markersize=3, alpha=1)
        
        # Add weight lines
        for weight in range(num_qubits + 1):
            theta = np.linspace(-2 * np.pi, 2 * np.pi, 100)
            z = -2 * weight / num_qubits + 1
            r = np.sqrt(1 - z**2)
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            ax.plot(x, y, z, color="#73BBEE", lw=1.5, ls=":", alpha=1)


        idxs = np.arange(len(state)) # indices quantum state in decimal form
        non_zero_probs = idxs[np.abs(state) > tol]
        for id in non_zero_probs:
            # Get basis state
            binstr = bin(id)[2:].zfill(num_qubits)
            weight = binstr.count("1")
            
            # Get position of basis state in the sphere
            number_of_divisions = QuantumVisualizer.n_choose_k(num_qubits, weight)
            weight_order = QuantumVisualizer.bit_string_index(binstr)
            angle = (float(weight) / num_qubits) * (np.pi * 2) + (
                weight_order * 2 * (np.pi / number_of_divisions))
            
            # Remove global phase
            if (weight > num_qubits / 2) or ( (weight == num_qubits / 2) and (weight_order >= number_of_divisions / 2)):
                angle = np.pi - angle - (2 * np.pi / number_of_divisions)

            # Get cartesian coordinates
            zvalue = -2 * weight / num_qubits + 1
            xvalue = np.sqrt(1 - zvalue**2) * np.cos(angle)
            yvalue = np.sqrt(1 - zvalue**2) * np.sin(angle)

            # Get size of ball (probability)
            prob = np.abs(state[id])**2
            # Get color of the ball (complex angle)
            color = QuantumVisualizer.phase_to_rgb(state[id])

            # Plot state labels and angles
            if show_state_labels:
                # Transform to spherical coordinates for text
                angle_theta, rprime = np.arctan2(np.sqrt(1 - zvalue**2), zvalue), 1.35
                xvalue_text = rprime * np.sin(angle_theta) * np.cos(angle)
                yvalue_text = rprime * np.sin(angle_theta) * np.sin(angle)
                zvalue_text = rprime * np.cos(angle_theta)
                # State label
                element_text = "$\\vert" + binstr + "\\rangle$"
                # Add phases to label in degrees or radians
                if show_state_phases:
                    element_angle = np.angle(state[id])
                    if use_degrees:
                        element_text += "\n$%.1f^\\circ$" % (element_angle * 180 / np.pi)
                    else:
                        element_angle = pi_check(element_angle, ndigits=3).replace("pi", "\\pi")
                        element_text += "\n$%s$" % (element_angle)
                # Add label to figure
                ax.text( xvalue_text, yvalue_text, zvalue_text, element_text,
                        ha="center", va="center", size=12 )
            
            # Add ball to figure
            ax.plot([xvalue],[yvalue],[zvalue],
                    markerfacecolor=color, markeredgecolor=color,
                    marker="o", markersize=np.sqrt(prob) * 50, )
            
            # Add arrow to figure
            a = Arrow3D([0, xvalue], [0, yvalue], [0, zvalue],
                        mutation_scale=20,alpha=1, arrowstyle="-",
                        color=color, lw=2)
            ax.add_artist(a)

        
        if filename:
            fig.savefig(filename, transparent = True)
        if return_fig:
            plt.close() 
            return fig
        
    @staticmethod
    def draw_color_legend(figsize=None, ax=None, n = 64, use_degrees=False, filename=None):
        """
        Plot the color legend for the qsphere and state space.

        Args:
            figsize (tuple): Figure size in inches.
            ax (matplotlib.axes.Axes): An optional Axes object to be used for
                the visualization output. If none is specified a new matplotlib
                Figure will be created and used. Additionally, if specified there
                will be no returned Figure since it is redundant.
            n (int): Number of divisions of the color legend.
            use_degrees (bool): An optional boolean indicating whether to use
            degrees or complex numbers.
            filename (str): File to save the plot if desired

        Returns:
            Figure: A matplotlib figure instance if the ``ax`` kwarg is not set

        """
        if figsize is None:
            figsize = (5, 5)

        if ax is None:
            return_fig = True
            fig = plt.figure(figsize=figsize)
            ax = fig.add_subplot()
        else:
            return_fig = False
            fig = ax.get_figure()

        # Get rid of the ticks
        ax.set_xticks([])
        ax.set_yticks([])

        theta = np.ones(n)
        colors = QuantumVisualizer.get_colors(n)

        # Draw pie
        ax.pie(theta, colors=colors[47:] + colors[: 47], radius=0.75)
        ax.add_artist(Circle((0, 0), 0.5, color="white", zorder=1))
        ax.annotate("", xy=(0, 0), xytext=(0.9, 0), arrowprops=dict(arrowstyle="<-", lw=2.5))
        ax.annotate("", xy=(0, 0), xytext=(0, 0.9), arrowprops=dict(arrowstyle="<-", lw=2.5))
        ax.annotate("", xy=(0, 0), xytext=(-0.9, 0), arrowprops=dict(arrowstyle="<-", lw=2.5))
        ax.annotate("", xy=(0, 0), xytext=(0, -0.9), arrowprops=dict(arrowstyle="<-", lw=2.5))
        offset = 0.95  # since radius of sphere is one.

        if use_degrees:
            labels = [ "0º", "90º", "180º", "270º"]
        else:
            labels = ["$1$", "$i$", "$-1$", "$-i$"]

        # Write labels
        ax.text( offset, 0, labels[0], horizontalalignment="center", verticalalignment="center", fontsize=18)
        ax.text( 0, offset, labels[1], horizontalalignment="center", verticalalignment="center", fontsize=18)
        ax.text(-offset*1.05, 0, labels[2], horizontalalignment="center", verticalalignment="center", fontsize=18)
        ax.text( 0, -offset, labels[3], horizontalalignment="center", verticalalignment="center", fontsize=18)

        ax.set_xlim(-offset*1.3, offset*1.3)
        ax.set_ylim(-offset*1.3, offset*1.3)
        ax.set_title(f'Color legend', pad = -60)

        if filename:
            fig.savefig(filename, transparent = True)
        if return_fig:
            plt.close() 
            return fig

    @staticmethod
    def height_for_probability(radius, prob, total_area):
        """
        Calculate the height (h) of a circular segment corresponding to a given probability.

        Args:
            radius (float): Radius of the circle.
            prob (float): Desired probability (fraction of the circle's area to fill).
            total_area (float): Total area of the circle.

        Returns:
            float: Height (h) of the segment.
        """
        target_area = prob * total_area  # Target area to fill
        h_low, h_high = 0, 2 * radius   # Binary search bounds

        while h_high - h_low > 1e-6:  # Precision tolerance
            h_mid = (h_low + h_high) / 2
            area = QuantumVisualizer.area_segment(radius, h_mid)
            if area < target_area:
                h_low = h_mid
            else:
                h_high = h_mid
        return h_low
    
    @staticmethod
    def area_segment(r, h):
        """
        Calculate the area of a circular segment.

        Args:
            r (float): The radius of the circle.
            h (float): The height of the segment (distance from the chord to the arc).

        Returns:
            float: The area of the circular segment.
        """
        return r*r*np.arccos((r-h)/r) - (r-h)*np.sqrt(2*r*h - h*h)


    def _draw_disk(self, partial_state, qubit, ax, radius = 1, pos_x=0, pos_y = None,
                    plot_text = False, pos_label = 0, equal_aspect_ratio = False, bottom_ratio=1,
                    ):
        """ 
        Draw phase disks ar a certain position.

        Args:
            partial_state (np.arrray): Density matrix of reduced state
            qubit (int): Qubit which corresponds to this phase disk
            ax (matplotlib.axes): Axis to draw phase disks
            radius (float): Radius of the disk
            pos_x (float): position on the x axis to plot the phase disks
            pos_y (float): position on the y axis to plot the phase disks
            plot_text (bool): If True, plot the qubit label
            equal_aspect_ratio (bool): If True, ensure equal aspect ratio
            bottom_ratio (float): Used to calculate the aspect ratio
        """

        if equal_aspect_ratio:
            x_aspect = 1
            y_aspect = 1
            ax.set_aspect('equal')
        else:
            # Adjust to axis dimensions
            # Get the axis limits
            fig = ax.get_figure()
            xlim = ax.get_xlim()
            ylim = ax.get_ylim()

            # Calculate the aspect ratio of the axis scaling
            x_aspect = (xlim[1] - xlim[0]) / fig.get_size_inches()[0]  # Data-to-figure ratio (x)
            y_aspect = (ylim[1] - ylim[0]) / (fig.get_size_inches()[1]*bottom_ratio)  # Data-to-figure ratio (y)
           
        # Get radius and color for phase disk
        prob = partial_state[0,0].real
        color = QuantumVisualizer.phase_to_rgb(partial_state[1,0], return_black = False)

        total_area = np.pi*radius**2
        # Calculate the height of the segment to fill
        h_cutoff = QuantumVisualizer.height_for_probability(radius, prob, total_area)

        # Create grid for circle
        circle_res = 300
        y = np.linspace(-radius, radius, circle_res)
        x = np.sqrt(radius**2 - y**2)

        # Find the points up to the cutoff height
        cutoff_idx = np.where(y + radius <= h_cutoff)[0]
        y_cutoff = y[cutoff_idx]
        x_cutoff = x[cutoff_idx]
       
        ellipse = Ellipse((pos_x, pos_y), width=2 * radius * x_aspect, height=2 * radius * y_aspect, edgecolor=color, fill=False, linewidth=7)
        ax.add_patch(ellipse)

        # Create the polygon for the filled segment
        filled_y = np.concatenate([y_cutoff*y_aspect + pos_y, y_cutoff[::-1]*y_aspect + pos_y])
        filled_x = np.concatenate([-x_cutoff*x_aspect + pos_x, x_cutoff[::-1]*x_aspect + pos_x])

        # Plot the filled circle segment
        ax.fill(filled_x, filled_y, color=color, alpha=1)

        
        # Draw purity circle
        pur = purity(partial_state).real
        ellipse = Ellipse((pos_x, pos_y), width=2 * radius * pur * x_aspect, height=2 * radius* pur * y_aspect, edgecolor='black', fill=False, linewidth=2)
        ax.add_patch(ellipse)
        
        # Draw the circle outline   
        if plot_text: 
            ax.text(pos_label, pos_y, f'$q_{{{qubit}}}$', fontsize=(20 - self.num_qubits))

        if self.display_math:
            # Format the value string
            value_str = str(int(prob*100)) + '%'
            font_size = max(8, int(15 - 1.5 * self.num_qubits)) 
            # Add the text in the center of the rectangle
            plt.text(pos_x, pos_y, value_str, color='black', ha='center', va='center', fontsize=font_size, zorder=3)
        

    
    def draw_phase_disks(self, ax=None, filename=None, display_math = False):
        """
        Plot the color legend for the qsphere and state space.

        Args:
            ax (matplotlib.axes.Axes): An optional Axes object to be used for
                the visualization output. If none is specified a new matplotlib
                Figure will be created and used. Additionally, if specified there
                will be no returned Figure since it is redundant.
            filename (str): File to save the plot if desired
            display_math (bool): If True, show the fullness of the disk

        Returns:
            Figure: A matplotlib figure instance if the ``ax`` kwarg is not set
        """
        self.display_math = display_math
        if ax is None:
            return_fig = True
            figsize = (3,max(3, self.num_qubits/2))
            fig, ax = plt.subplots(1,1,figsize=figsize)
        else:
            return_fig = False
            fig = ax.get_figure()
        
        for qubit in range(self.num_qubits):
            # Get partial trace
            v = Statevector(self.qc)
            if self.num_qubits==1:
                partial_state = DensityMatrix(v).data
            else:
                partial_state = partial_trace(v, [i for i in range(self.num_qubits) if i!=qubit]).data
            self._draw_disk(partial_state, qubit, ax = ax, radius = 1, pos_x=0, pos_y = 2.5*self.num_qubits - 2.5*qubit,
                            plot_text = True, pos_label = - 2.2, equal_aspect_ratio= True)
                   
        ax.set_title(f'Phase disks', pad = -60)

        # Set limits and aspect ratio
        ax.set_xlim(-3, 2)
        ax.set_ylim(1, 2.5*(self.qc.num_qubits) + 2 )
        ax.axis('off')

        if filename:
            fig.savefig(filename, transparent = True)
        if return_fig:
            plt.close() 
            return fig
        
    def draw_geometric_plots(self, filename = None, display_math = False):
        """
        Create and visualize geometric representations of a quantum state, 
        including phase disks, the Q-sphere or Bloch sphere, and a color legend.

        Args:
            filename (str, optional): If provided, saves the generated plot 
                to the specified file. Defaults to None.
            display_math (bool): If True, show the fullness of the disks

        Returns:
            matplotlib.figure.Figure: The created figure containing the plots.
        """
        
        # Define figure size dynamically based on the number of qubits
        figsize = (5 + 5 + 5, max(5, self.num_qubits/2))
        fig = plt.figure(figsize=figsize)

        # Create a GridSpec layout with 3 columns
        spec = gridspec.GridSpec(nrows=1, ncols=3, figure=fig, width_ratios=[max(3, self.num_qubits/2), 5, 5])
        spec.update(wspace=-0.3)
        
        # Phase disk
        phase_disk_ax = fig.add_subplot(spec[0])
        self.draw_phase_disks(ax = phase_disk_ax, display_math = display_math)

        if self.num_qubits>1:
            # Q-sphere
            q_sphere_ax = fig.add_subplot(spec[1], projection='3d')
            self.draw_qsphere(ax = q_sphere_ax, show_state_labels=True)
        else:
            # Bloch-sphere
            bloch_sphere_ax = fig.add_subplot(spec[1], projection='3d')
            self.draw_bloch_sphere(ax = bloch_sphere_ax)
            
        # Color legend
        color_legend_ax = fig.add_subplot(spec[2])
        self.draw_color_legend(ax = color_legend_ax)


        # Save or return
        if filename:
            fig.savefig(filename, transparent = True)
        plt.close() 
        return fig
            