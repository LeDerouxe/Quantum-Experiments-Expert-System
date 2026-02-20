import tkinter as tk
from tkinter import ttk, messagebox
from experta import *
import matplotlib
matplotlib.use('TkAgg')  # مهم برای tkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# ========== Facts ==========
class Experiment(Fact): pass
class Particle(Fact): pass
class Light(Fact): pass
class Environment(Fact): pass
class Barrier(Fact): pass
class Potential(Fact): pass
class Measurement(Fact): pass
class Surface(Fact): pass


# ========== Knowledge Engine ==========
class QuantumExpertSystem(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.final_result = None
        self.confidence = 0
        self.explanations = []

    def reset_results(self):
        self.final_result = None
        self.confidence = 0
        self.explanations = []

    # ---------------- Stern–Gerlach (خیلی پوشش‌دار) ----------------

    @Rule(Experiment(name='stern_gerlach'),
          Particle(type='electron', spin='unknown'),
          Environment(field_dir='z', sequence='single_pass'),
          salience=10)
    def sg_basic_split(self):
        self.final_result = "Beam splits into two discrete spin states (up / down)."
        self.confidence = 90
        self.explanations.extend([
            "Electron spin along z is in a superposition of +ħ/2 and −ħ/2 before measurement.",
            "Magnetic field gradient along z separates the two spin components spatially.",
            "Roughly half of the electrons go to each output channel."
        ])

    @Rule(Experiment(name='stern_gerlach'),
          Particle(type='electron', spin='prepared_up'),
          Environment(field_dir='z', sequence='single_pass'),
          salience=10)
    def sg_prepared_up_single(self):
        self.final_result = "All electrons are detected in the spin-up channel."
        self.confidence = 93
        self.explanations.extend([
            "Input state is already an eigenstate of Sz with eigenvalue +ħ/2.",
            "A projective measurement along the same axis is fully deterministic.",
            "No particles appear in the spin-down output port."
        ])

    @Rule(Experiment(name='stern_gerlach'),
          Particle(type='electron', spin='prepared_up'),
          Environment(field_dir='z', sequence='repeated'),
          salience=10)
    def sg_prepared_sequence(self):
        self.final_result = "Repeated z-measurements preserve the spin-up result."
        self.confidence = 94
        self.explanations.extend([
            "Once projected onto an eigenstate, further measurements along the same axis do not change the state.",
            "The statistics become purely deterministic after the first measurement."
        ])

    @Rule(Experiment(name='stern_gerlach'),
          Particle(type='silver_atom'),
          Environment(field_dir='z'),
          salience=9)
    def sg_silver_atom(self):
        self.final_result = "Silver atoms split into two well-separated beams."
        self.confidence = 92
        self.explanations.extend([
            "A single unpaired valence electron dominates the atomic magnetic moment.",
            "Effectively the atom behaves as a spin-½ particle in this setup.",
            "The experiment confirms space quantization of angular momentum."
        ])

    @Rule(Experiment(name='stern_gerlach'),
          Particle(spin='prepared_up'),
          Environment(field_dir='x'),
          salience=9)
    def sg_axis_change_from_z_to_x(self):
        self.final_result = "Prepared z-up beam splits 50/50 into x-up and x-down outputs."
        self.confidence = 88
        self.explanations.extend([
            "The eigenstate of Sz is a balanced superposition of Sx eigenstates.",
            "Changing the measurement axis introduces intrinsic randomness.",
            "This directly illustrates non-commutativity of spin components."
        ])

    @Rule(Experiment(name='stern_gerlach'),
          Particle(type='electron', spin='unknown'),
          Environment(field_dir='reversed_z'),
          salience=8)
    def sg_reversed_field_unknown(self):
        self.final_result = "Two beams appear but the geometric up/down labels are swapped."
        self.confidence = 83
        self.explanations.extend([
            "Reversing the field gradient flips the force on the magnetic moment.",
            "The physical spin state is the same; only the reference direction changes.",
            "‘Up’ and ‘down’ are defined relative to the local field orientation."
        ])

    # DEFAULT / GENERIC Stern–Gerlach (می‌گیرد اکثر حالت‌ها)
    @Rule(Experiment(name='stern_gerlach'),
          Particle(type='electron', spin=MATCH.s),
          Environment(field_dir=MATCH.d, sequence=MATCH.seq),
          salience=1)
    def sg_generic_electron(self, s, d, seq):
        if self.final_result is None:
            if s == 'unknown':
                self.final_result = f"Electron beam shows quantized splitting along the {d}-axis."
                self.confidence = 80
                self.explanations.extend([
                    "Even without state preparation, spin measurements yield only two discrete outcomes.",
                    "The exact beam profile depends on the field strength and gradient."
                ])
            else:
                self.final_result = f"Prepared spin state along a different axis causes probabilistic outcomes along {d}."
                self.confidence = 78
                self.explanations.extend([
                    "Prepared eigenstates of one component become superpositions in another basis.",
                    "Measurement outcomes follow |projection|² probabilities."
                ])

    # ---------------- Double Slit ----------------

    @Rule(Experiment(name='double_slit'),
          Particle(type='electron'),
          Environment(detector='none'),
          Light(wavelength='de_broglie'),
          salience=10)
    def ds_electron_interference(self):
        self.final_result = "A clear interference fringe pattern appears on the screen."
        self.confidence = 95
        self.explanations.extend([
            "The electron wavefunction passes coherently through both slits.",
            "Probability amplitudes from each path interfere constructively and destructively.",
            "The fringe spacing is controlled by the de Broglie wavelength and slit separation."
        ])

    @Rule(Experiment(name='double_slit'),
          Particle(type='electron'),
          Environment(detector='which_path'),
          salience=10)
    def ds_electron_which_path(self):
        self.final_result = "No interference; only two broad single-slit-like bands are observed."
        self.confidence = 98
        self.explanations.extend([
            "Recording which-path information entangles the electron with the detector.",
            "Phase coherence between the two paths is destroyed.",
            "Wave-like interference is replaced by particle-like behavior."
        ])

    @Rule(Experiment(name='double_slit'),
          Particle(type='photon'),
          Environment(detector='none'),
          salience=9)
    def ds_photon_interference(self):
        self.final_result = "Single-photon interference fringes appear over time."
        self.confidence = 93
        self.explanations.extend([
            "Even individual photons interfere with themselves when no path information is available.",
            "The pattern builds up gradually from many detection events."
        ])

    @Rule(Experiment(name='double_slit'),
          Environment(slit_width='narrow'),
          Particle(type='electron'),
          salience=8)
    def ds_narrow_slit(self):
        self.final_result = "Fringes become wider due to stronger diffraction from narrow slits."
        self.confidence = 86
        self.explanations.extend([
            "Narrower apertures increase transverse momentum uncertainty.",
            "This broadens the diffraction envelope that modulates the interference pattern."
        ])

    @Rule(Experiment(name='double_slit'),
          Particle(type='electron', velocity='high'),
          Environment(detector='none'),
          salience=7)
    def ds_high_velocity(self):
        self.final_result = "Fringe spacing decreases at higher electron velocity."
        self.confidence = 84
        self.explanations.extend([
            "Higher momentum implies shorter de Broglie wavelength.",
            "Smaller wavelength produces more closely spaced fringes on the screen."
        ])

    # DEFAULT Double Slit
    @Rule(Experiment(name='double_slit'),
          Particle(type=MATCH.ptype),
          Environment(detector=MATCH.det),
          salience=1)
    def ds_generic(self, ptype, det):
        if self.final_result is None:
            if det == 'none':
                self.final_result = f"{ptype.capitalize()} beam shows a quantum interference pattern through two slits."
                self.confidence = 80
                self.explanations.extend([
                    "Absence of which-path detection preserves coherence between the two paths.",
                    "Interference is a generic feature of coherent quantum propagation."
                ])
            else:
                self.final_result = f"{ptype.capitalize()} behaves like classical particles passing independently through each slit."
                self.confidence = 82
                self.explanations.extend([
                    "Path information collapses the superposition into a statistical mixture.",
                    "Pattern approximates the sum of two single-slit intensity distributions."
                ])

    # ---------------- Quantum Tunneling ----------------

    @Rule(Experiment(name='quantum_tunneling'),
          Barrier(width='thin'),
          Particle(energy='above_barrier'),
          salience=10)
    def qt_classical_over_barrier(self):
        self.final_result = "Transmission is close to unity with small reflection."
        self.confidence = 88
        self.explanations.extend([
            "When E exceeds the barrier height and the barrier is thin, wave matching gives almost full transmission.",
            "Residual reflection arises from impedance mismatch at the interfaces."
        ])

    @Rule(Experiment(name='quantum_tunneling'),
          Barrier(width='thick'),
          Particle(energy='below_barrier'),
          salience=10)
    def qt_strong_tunneling_suppression(self):
        self.final_result = "Transmission is exponentially suppressed but non-zero."
        self.confidence = 96
        self.explanations.extend([
            "Inside the classically forbidden region the wavefunction decays exponentially.",
            "Transmission probability scales roughly as exp(-2 κ L) with barrier thickness L."
        ])

    @Rule(Experiment(name='quantum_tunneling'),
          Barrier(height='low'),
          Particle(mass='light', energy='below_barrier'),
          salience=9)
    def qt_light_particle(self):
        self.final_result = "Light particles with low barriers show appreciable tunneling."
        self.confidence = 90
        self.explanations.extend([
            "Tunneling exponent κ is proportional to sqrt(m (V0 − E)); smaller mass lowers κ.",
            "This is the basis of electron tunneling in STM junctions."
        ])

    @Rule(Experiment(name='quantum_tunneling'),
          Environment(temperature='high'),
          Particle(energy='below_barrier'),
          salience=8)
    def qt_thermal_assisted(self):
        self.final_result = "Thermal excitation enhances tunneling rate."
        self.confidence = 83
        self.explanations.extend([
            "A hot environment populates higher energy states closer to the barrier top.",
            "Combined thermal activation and tunneling increases overall transmission."
        ])

    # DEFAULT tunneling
    @Rule(Experiment(name='quantum_tunneling'),
          Barrier(width=MATCH.w),
          Particle(energy=MATCH.e),
          salience=1)
    def qt_generic(self, w, e):
        if self.final_result is None:
            self.final_result = "Wavefunction partially transmits and partially reflects at the barrier."
            self.confidence = 78
            self.explanations.extend([
                "Quantum mechanics predicts finite transmission even when classical motion is forbidden.",
                f"Barrier width ({w}) and relative energy ({e}) control the magnitude of the tunneling probability."
            ])

    # ---------------- Photoelectric Effect ----------------

    @Rule(Experiment(name='photoelectric'),
          Light(frequency='above_threshold'),
          Surface(material='clean'),
          salience=10)
    def pe_above_clean(self):
        self.final_result = "Photoelectrons are emitted with kinetic energy KE = hν − φ."
        self.confidence = 97
        self.explanations.extend([
            "Each photon delivers a quantum of energy hν to a single electron.",
            "If this exceeds the work function φ, the electron escapes the surface.",
            "The maximum kinetic energy grows linearly with frequency."
        ])

    @Rule(Experiment(name='photoelectric'),
          Light(frequency='below_threshold'),
          salience=10)
    def pe_below_any(self):
        self.final_result = "No photoelectric emission occurs, regardless of intensity."
        self.confidence = 99
        self.explanations.extend([
            "Photons with energy hν below the work function cannot liberate electrons.",
            "Increasing intensity only increases the number of insufficient photons, not their energy."
        ])

    @Rule(Experiment(name='photoelectric'),
          Light(frequency='above_threshold'),
          Light(intensity='high'),
          salience=9)
    def pe_high_intensity(self):
        self.final_result = "Emission current increases with intensity, stopping voltage unchanged."
        self.confidence = 94
        self.explanations.extend([
            "Higher intensity means more photons per unit time, hence more emitted electrons.",
            "The maximum electron energy depends only on photon frequency, not on intensity."
        ])

    @Rule(Experiment(name='photoelectric'),
          Surface(material='cesium'),
          salience=8)
    def pe_cesium_low_work(self):
        self.final_result = "Cesium emits electrons even under relatively low-frequency visible light."
        self.confidence = 88
        self.explanations.extend([
            "Alkali metals have unusually small work functions.",
            "They are ideal for photosensitive cathodes in detectors."
        ])

    @Rule(Experiment(name='photoelectric'),
          Light(frequency=MATCH.f),
          salience=1)
    def pe_generic(self, f):
        if self.final_result is None:
            if f == 'above_threshold':
                self.final_result = "Photoelectric emission occurs with a finite photocurrent."
                self.confidence = 85
            else:
                self.final_result = "Photon energy is insufficient to eject electrons from the surface."
                self.confidence = 90
            self.explanations.append("Overall behavior follows Einstein’s photoelectric equation.")

    # ---------------- Quantum Harmonic Oscillator ----------------

    @Rule(Experiment(name='harmonic_oscillator'),
          Potential(state='ground'),
          Measurement(type='energy'),
          salience=10)
    def qho_ground(self):
        self.final_result = "Measured energy corresponds to the zero-point level E0 = ħω / 2."
        self.confidence = 96
        self.explanations.extend([
            "Exact cancellation of kinetic and potential energy at zero is forbidden by the uncertainty principle.",
            "The ground-state wavefunction is Gaussian with minimal uncertainty."
        ])

    @Rule(Experiment(name='harmonic_oscillator'),
          Potential(state='excited_n1'),
          salience=9)
    def qho_n1(self):
        self.final_result = "First excited state with energy E1 = 3ħω / 2 is populated."
        self.confidence = 93
        self.explanations.extend([
            "Energy levels are equally spaced by ħω.",
            "The first excited state has one node in its spatial probability distribution."
        ])

    @Rule(Experiment(name='harmonic_oscillator'),
          Environment(temperature='zero'),
          salience=8)
    def qho_at_zero_temp(self):
        self.final_result = "Only the ground state is populated at T = 0."
        self.confidence = 90
        self.explanations.extend([
            "At zero temperature, the system relaxes into the lowest energy eigenstate.",
            "Residual zero-point motion persists even in the absence of thermal excitations."
        ])

    @Rule(Experiment(name='harmonic_oscillator'),
          Potential(anharmonic='present'),
          salience=7)
    def qho_anharmonic(self):
        self.final_result = "Energy-level spacing decreases at high n due to anharmonicity."
        self.confidence = 84
        self.explanations.extend([
            "Additional x⁴ and higher terms in the potential distort the ideal spectrum.",
            "Real molecular vibrations deviate from perfect harmonic behavior at large amplitudes."
        ])

    @Rule(Experiment(name='harmonic_oscillator'),
          salience=1)
    def qho_default(self):
        if self.final_result is None:
            self.final_result = "System exhibits discrete, equally spaced energy levels of a quantum oscillator."
            self.confidence = 80
            self.explanations.append("The quantum harmonic oscillator is a universal model for bound small oscillations.")

    # ---------------- Uncertainty Principle ----------------

    @Rule(Experiment(name='uncertainty_principle'),
          Measurement(position_precision='high'),
          Measurement(momentum_precision='low'),
          salience=10)
    def up_pos_high(self):
        self.final_result = "Sharp position measurement leads to large momentum uncertainty."
        self.confidence = 94
        self.explanations.extend([
            "Heisenberg’s relation ∆x ∆p ≥ ħ/2 forbids arbitrarily precise knowledge of both variables.",
            "Localizing the particle in space broadens its momentum distribution."
        ])

    @Rule(Experiment(name='uncertainty_principle'),
          Measurement(position_precision='low'),
          Measurement(momentum_precision='high'),
          salience=10)
    def up_mom_high(self):
        self.final_result = "Well-defined momentum implies a highly delocalized position."
        self.confidence = 92
        self.explanations.extend([
            "Momentum eigenstates correspond to plane waves spread over all space.",
            "Precise momentum knowledge comes at the cost of spatial uncertainty."
        ])

    @Rule(Experiment(name='uncertainty_principle'),
          Measurement(time_precision='short'),
          salience=9)
    def up_time_short(self):
        self.final_result = "Short measurement times imply a broad energy spread."
        self.confidence = 88
        self.explanations.extend([
            "Transient states exhibit large natural linewidths in spectroscopy.",
            "The energy–time uncertainty relation constrains the lifetime of excited states."
        ])

    @Rule(Experiment(name='uncertainty_principle'),
          Particle(type='localized_wavepacket'),
          salience=8)
    def up_wavepacket(self):
        self.final_result = "A localized wavepacket spreads as it evolves in time."
        self.confidence = 86
        self.explanations.extend([
            "Components with different momenta travel at different group velocities.",
            "This dispersion increases the spatial width of the packet over time."
        ])

    @Rule(Experiment(name='uncertainty_principle'),
          salience=1)
    def up_default(self):
        if self.final_result is None:
            self.final_result = "Reducing uncertainty in one observable increases uncertainty in its conjugate."
            self.confidence = 80
            self.explanations.append("The uncertainty principle is a fundamental feature of quantum states, not a limitation of instruments.")

    # ---------------- Decoherence ----------------

    @Rule(Experiment(name='decoherence'),
          Environment(interaction='strong'),
          Particle(superposition='cat_state'),
          salience=10)
    def deco_strong_cat(self):
        self.final_result = "Macroscopic superposition rapidly decoheres into a classical mixture."
        self.confidence = 96
        self.explanations.extend([
            "Strong coupling to many environmental degrees of freedom destroys phase relations.",
            "Interference between macroscopically distinct branches becomes unobservable."
        ])

    @Rule(Experiment(name='decoherence'),
          Environment(isolation='high'),
          salience=9)
    def deco_isolated(self):
        self.final_result = "Quantum coherence is preserved for a long time in an isolated system."
        self.confidence = 90
        self.explanations.extend([
            "Weak environmental coupling greatly reduces the decoherence rate.",
            "Superconducting qubits at cryogenic temperatures operate in this regime."
        ])

    @Rule(Experiment(name='decoherence'),
          Environment(temperature='high'),
          salience=8)
    def deco_hot(self):
        self.final_result = "High-temperature environments cause very fast decoherence."
        self.confidence = 92
        self.explanations.extend([
            "Frequent scattering with thermal photons and phonons randomizes phases.",
            "Coherence times decrease roughly as temperature increases."
        ])

    @Rule(Experiment(name='decoherence'),
          salience=1)
    def deco_default(self):
        if self.final_result is None:
            self.final_result = "The system gradually loses interference visibility through entanglement with its environment."
            self.confidence = 82
            self.explanations.append("Decoherence explains the emergence of classical statistics from underlying quantum dynamics.")


# ========== UI ==========
class QuantumUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Quantum Expert System")
        self.root.geometry("1200x800")
        self.root.configure(bg="#fff0e6")

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#e6f3ff')
        style.configure('TNotebook.Tab', background='#b3d9ff', padding=[20, 8])
        style.map('TNotebook.Tab', background=[('selected', '#4a90e2'), ('active', '#80bfff')])
        style.configure('TLabel', background='#e6f3ff', font=('Arial', 10))
        style.configure('TFrame', background='#e6f3ff')
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), background='#e6f3ff')

        self.engine = QuantumExpertSystem()
        self.canvas = None
        self.param_widgets = {}

        self.tabs = ttk.Notebook(root)
        self.tab_setup = ttk.Frame(self.tabs)
        self.tab_results = ttk.Frame(self.tabs)
        self.tabs.add(self.tab_setup, text="⚛️ Experiment Setup")
        self.tabs.add(self.tab_results, text="📊 Results & Graphs")
        self.tabs.pack(expand=1, fill="both", padx=10, pady=10)

        self.build_setup_tab()
        self.build_results_tab()
        self.load_ui()

    def build_setup_tab(self):
        title = ttk.Label(self.tab_setup, text="Quantum Experiments Expert System", style='Title.TLabel')
        title.pack(pady=20)

        frame = ttk.Frame(self.tab_setup, padding=30, relief='ridge', borderwidth=2)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Select Experiment:", font=('Arial', 12, 'bold')).grid(row=0, column=0, sticky="w", pady=10)
        self.exp_var = tk.StringVar(value="stern_gerlach")
        experiments = [
            "stern_gerlach",
            "double_slit",
            "quantum_tunneling",
            "photoelectric",
            "harmonic_oscillator",
            "uncertainty_principle",
            "decoherence"
        ]
        self.exp_combo = ttk.Combobox(frame, textvariable=self.exp_var, values=experiments,
                                      state="readonly", width=25)
        self.exp_combo.grid(row=0, column=1, sticky="w", padx=10)
        self.exp_combo.bind("<<ComboboxSelected>>", self.load_ui)

        self.dynamic = ttk.LabelFrame(frame, text="Parameters (3–8 conditions)", padding=20)
        self.dynamic.grid(row=1, column=0, columnspan=2, pady=20, sticky="ew")

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=20)
        ttk.Button(btn_frame, text="Run Experiment", command=self.run).pack(pady=10)
        ttk.Button(btn_frame, text="Reset", command=self.reset_ui).pack()

        frame.columnconfigure(1, weight=1)

    def build_results_tab(self):
        text_frame = ttk.Frame(self.tab_results, padding=20)
        text_frame.pack(fill="both", expand=True)

        ttk.Label(text_frame, text="Expert Analysis:", font=('Arial', 12, 'bold')).pack(anchor="w")
        self.out = tk.Text(text_frame, wrap=tk.WORD, height=15, font=('Consolas', 10), bg='#f8fcff')
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.out.yview)
        self.out.configure(yscrollcommand=scrollbar.set)
        self.out.pack(side="left", fill="both", expand=True, pady=(0, 10))
        scrollbar.pack(side="right", fill="y")

        self.graph_frame = ttk.LabelFrame(self.tab_results, text="Visual Result", padding=10)
        self.graph_frame.pack(fill="both", expand=True)

    def load_ui(self, event=None):
        for widget in self.dynamic.winfo_children():
            widget.destroy()
        self.param_widgets = {}

        exp = self.exp_var.get()
        row = 0

        param_configs = {
            "stern_gerlach": [
                ("particle_type", "Particle Type", ["electron", "silver_atom"]),
                ("spin", "Spin State", ["unknown", "prepared_up"]),
                ("field_dir", "Field Direction", ["z", "x", "reversed_z"]),
                ("sequence", "Sequence", ["single_pass", "repeated"])
            ],
            "double_slit": [
                ("particle_type", "Particle Type", ["electron", "photon"]),
                ("detector", "Detector", ["none", "which_path"]),
                ("slit_width", "Slit Width", ["narrow", "wide"]),
                ("wavelength", "Wavelength", ["de_broglie", "short"]),
                ("velocity", "Velocity", ["low", "high"])
            ],
            "quantum_tunneling": [
                ("mass", "Particle Mass", ["light", "heavy"]),
                ("energy", "Energy", ["below_barrier", "above_barrier"]),
                ("barrier_width", "Barrier Width", ["thin", "thick"]),
                ("barrier_height", "Barrier Height", ["low", "high"]),
                ("temperature", "Temperature", ["low", "high"])
            ],
            "photoelectric": [
                ("frequency", "Light Frequency", ["above_threshold", "below_threshold"]),
                ("intensity", "Intensity", ["low", "high"]),
                ("material", "Surface Material", ["clean", "cesium"])
            ],
            "harmonic_oscillator": [
                ("state", "Energy State", ["ground", "excited_n1"]),
                ("temperature", "Temperature", ["zero", "room"]),
                ("anharmonic", "Anharmonic", ["absent", "present"]),
                ("meas_type", "Measurement Type", ["energy", "position"])
            ],
            "uncertainty_principle": [
                ("pos_precision", "Position Precision", ["high", "low"]),
                ("mom_precision", "Momentum Precision", ["high", "low"]),
                ("time_precision", "Time Precision", ["short", "long"]),
                ("packet", "Wavepacket Type", ["localized_wavepacket", "delocalized"])
            ],
            "decoherence": [
                ("superposition", "Superposition Type", ["cat_state", "spin"]),
                ("interaction", "Environment Interaction", ["strong", "weak"]),
                ("isolation", "Isolation", ["high", "low"]),
                ("temperature", "Temperature", ["cryogenic", "room"])
            ]
        }

        params = param_configs.get(exp, [])
        for key, label, values in params:
            ttk.Label(self.dynamic, text=f"{label}:").grid(row=row, column=0, sticky="w", pady=6, padx=(0, 15))
            cb = ttk.Combobox(self.dynamic, values=values, state="readonly", width=18)
            cb.current(0)
            cb.grid(row=row, column=1, sticky="w", pady=6)
            self.param_widgets[key] = cb
            row += 1

    def reset_ui(self):
        self.exp_var.set("stern_gerlach")
        self.load_ui()

    def create_visual(self, result, exp):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(9, 4), facecolor='white')
        fig.patch.set_facecolor('#f0f8ff')

        if "stern_gerlach" in exp:
            x = np.linspace(0, 10, 200)
            up = np.exp(-(x-3)**2/0.5)
            down = np.exp(-(x-7)**2/0.5)
            ax.plot(x, up, 'b-', lw=2, label='Up')
            ax.plot(x, down, 'r-', lw=2, label='Down')
            ax.set_title('Stern–Gerlach Beam Split')
            ax.set_xlabel('Screen position')
            ax.set_ylabel('Intensity')
            ax.legend()
        elif "double_slit" in exp:
            x = np.linspace(0, 10, 1000)
            fringes = (np.sin(8*x)**2) * np.exp(-0.1*(x-5)**2)
            ax.plot(x, fringes, 'g-', lw=2)
            ax.set_title('Double Slit Interference')
            ax.set_xlabel('Screen position')
            ax.set_ylabel('Probability density')
        elif "quantum_tunneling" in exp:
            x = np.linspace(-2, 5, 800)
            barrier = np.where((x >= 0) & (x <= 2), 1.5, 0)
            ax.fill_between(x, 0, barrier, alpha=0.3, color='black', label='Barrier')
            wave = np.exp(-0.7*(x+2)**2) + 0.2*np.exp(-0.7*(x-2.5)**2)
            ax.plot(x, wave, 'b-', lw=2, label='Wavefunction')
            ax.set_title('Quantum Tunneling')
            ax.legend()
        elif "photoelectric" in exp:
            nu = np.linspace(0.5, 3.0, 200)
            phi = 1.5
            ke = np.maximum(0, 2*(nu - phi))
            ax.plot(nu, ke, 'm-', lw=2)
            ax.axvline(phi, color='orange', ls='--', label='Threshold')
            ax.set_title('Photoelectron KE vs Frequency')
            ax.set_xlabel('Frequency ν (arb.)')
            ax.set_ylabel('KE (arb.)')
            ax.legend()
        elif "harmonic_oscillator" in exp:
            n = np.arange(0, 6)
            E = n + 0.5
            ax.bar(n, E, width=0.6, color='purple', alpha=0.8)
            ax.set_title('Quantum Harmonic Oscillator Levels')
            ax.set_xlabel('Quantum number n')
            ax.set_ylabel('E / ħω')
        elif "uncertainty_principle" in exp:
            theta = np.linspace(0, 2*np.pi, 200)
            x_ell = 1.2*np.cos(theta)
            y_ell = 0.4*np.sin(theta)
            ax.fill(x_ell, y_ell, 'lightblue', alpha=0.6)
            ax.plot(0, 0, 'ko', markersize=8)
            ax.set_title('Uncertainty Ellipse (Δx, Δp)')
            ax.axis('equal')
            ax.axis('off')
        elif "decoherence" in exp:
            t = np.linspace(0, 4, 200)
            coherence = np.exp(-t)
            ax.plot(t, coherence, 'orange', lw=3)
            ax.fill_between(t, 0, coherence, alpha=0.3, color='orange')
            ax.set_title('Coherence Decay vs Time')
            ax.set_xlabel('Time (arb.)')
            ax.set_ylabel('Coherence')

        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def run(self):
        self.engine.reset()
        self.engine.reset_results()
        exp_name = self.exp_var.get()
        self.engine.declare(Experiment(name=exp_name))

        for key, widget in self.param_widgets.items():
            value = widget.get()
            if key == "particle_type":
                self.engine.declare(Particle(type=value))
            elif key == "spin":
                self.engine.declare(Particle(spin=value))
            elif key == "field_dir":
                self.engine.declare(Environment(field_dir=value))
            elif key == "sequence":
                self.engine.declare(Environment(sequence=value))
            elif key == "detector":
                self.engine.declare(Environment(detector=value))
            elif key == "slit_width":
                self.engine.declare(Environment(slit_width=value))
            elif key == "wavelength":
                self.engine.declare(Light(wavelength=value))
            elif key == "velocity":
                self.engine.declare(Particle(velocity=value))
            elif key == "mass":
                self.engine.declare(Particle(mass=value))
            elif key == "energy":
                self.engine.declare(Particle(energy=value))
            elif key == "barrier_width":
                self.engine.declare(Barrier(width=value))
            elif key == "barrier_height":
                self.engine.declare(Barrier(height=value))
            elif key == "temperature":
                self.engine.declare(Environment(temperature=value))
            elif key == "frequency":
                self.engine.declare(Light(frequency=value))
            elif key == "intensity":
                self.engine.declare(Light(intensity=value))
            elif key == "material":
                self.engine.declare(Surface(material=value))
            elif key == "state":
                self.engine.declare(Potential(state=value))
            elif key == "anharmonic":
                self.engine.declare(Potential(anharmonic=value))
            elif key == "meas_type":
                self.engine.declare(Measurement(type=value))
            elif key == "pos_precision":
                self.engine.declare(Measurement(position_precision=value))
            elif key == "mom_precision":
                self.engine.declare(Measurement(momentum_precision=value))
            elif key == "time_precision":
                self.engine.declare(Measurement(time_precision=value))
            elif key == "packet":
                self.engine.declare(Particle(type=value))
            elif key == "superposition":
                self.engine.declare(Particle(superposition=value))
            elif key == "interaction":
                self.engine.declare(Environment(interaction=value))
            elif key == "isolation":
                self.engine.declare(Environment(isolation=value))

        self.engine.run()

        self.out.delete("1.0", tk.END)
        self.out.insert("end", f"Experiment: {exp_name}\n")
        self.out.insert("end", "="*60 + "\n\n")

        if not self.engine.final_result:
            self.out.insert("end", "No matching expert rule activated. Try adjusting parameters.\n")
        else:
            self.out.insert("end", f"Result: {self.engine.final_result}\n\n")
            self.out.insert("end", f"Confidence: {self.engine.confidence}%\n\n")
            self.out.insert("end", "Explanation:\n")
            for ex in self.engine.explanations:
                self.out.insert("end", f"- {ex}\n")

        self.create_visual(self.engine.final_result or "", exp_name)
        self.tabs.select(self.tab_results)


if __name__ == "__main__":
    root = tk.Tk()
    app = QuantumUI(root)
    root.mainloop()
