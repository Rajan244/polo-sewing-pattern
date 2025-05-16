import matplotlib.pyplot as plt
import matplotlib.patches as patches
%matplotlib inline

# Setup figure with subplots (5x2 to include interfacing)
plt.rcParams['figure.figsize'] = (15, 18)
fig, axs = plt.subplots(5, 2)

# Conversion factor for inches to cm
in_to_cm = 2.54

# Front Body
axs[0, 0].set_title("Front Body (Size S)")
axs[0, 0].set_xlim(0, 20)
axs[0, 0].set_ylim(0, 30)
axs[0, 0].grid(True, linestyle='--', alpha=0.7)
front = patches.Polygon([(2, 2), (18, 2), (18, 26), (2, 26)], edgecolor='blue', facecolor='lightblue', lw=2)
axs[0, 0].add_patch(front)
# Indicate placket area with a dashed line
placket_area = patches.Rectangle((8.25, 21), 1.5, 5, edgecolor='red', facecolor='none', linestyle='--', lw=1)
axs[0, 0].add_patch(placket_area)
axs[0, 0].text(10, 14, f"Front Body\n(18\" x 24.5\")\n({18*in_to_cm:.1f} cm x {24.5*in_to_cm:.1f} cm)", ha='center', va='center')
axs[0, 0].axis('equal')

# Back Body
axs[0, 1].set_title("Back Body (Size S, Cut on Fold)")
axs[0, 1].set_xlim(0, 20)
axs[0, 1].set_ylim(0, 30)
axs[0, 1].grid(True, linestyle='--', alpha=0.7)
back = patches.Polygon([(2, 2), (18, 2), (18, 26), (2, 26)], edgecolor='green', facecolor='lightgreen', lw=2)
axs[0, 1].add_patch(back)
axs[0, 1].text(10, 14, f"Back Body\n(18\" x 24.5\")\n({18*in_to_cm:.1f} cm x {24.5*in_to_cm:.1f} cm)", ha='center', va='center')
axs[0, 1].axis('equal')

# Sleeve 1 (with integrated armhole)
axs[1, 0].set_title("Sleeve 1 (Size S)")
axs[1, 0].set_xlim(0, 10)
axs[1, 0].set_ylim(0, 10)
axs[1, 0].grid(True, linestyle='--', alpha=0.7)
# Define sleeve with a curved armhole
sleeve1_points = [(1, 1), (8, 1), (8, 7), (4, 9), (1, 7)]
sleeve1 = patches.Polygon(sleeve1_points, edgecolor='purple', facecolor='thistle', lw=2)
axs[1, 0].add_patch(sleeve1)
axs[1, 0].text(4.5, 4, f"Sleeve\n(7\" x 7\")\n({7*in_to_cm:.1f} cm x {7*in_to_cm:.1f} cm)", ha='center', va='center')
axs[1, 0].axis('equal')

# Sleeve 2
axs[1, 1].set_title("Sleeve 2 (Size S)")
axs[1, 1].set_xlim(0, 10)
axs[1, 1].set_ylim(0, 10)
axs[1, 1].grid(True, linestyle='--', alpha=0.7)
sleeve2_points = [(1, 1), (8, 1), (8, 7), (4, 9), (1, 7)]
sleeve2 = patches.Polygon(sleeve2_points, edgecolor='purple', facecolor='thistle', lw=2)
axs[1, 1].add_patch(sleeve2)
axs[1, 1].text(4.5, 4, f"Sleeve\n(7\" x 7\")\n({7*in_to_cm:.1f} cm x {7*in_to_cm:.1f} cm)", ha='center', va='center')
axs[1, 1].axis('equal')

# Collar 1
axs[2, 0].set_title("Collar 1 (Size S)")
axs[2, 0].set_xlim(0, 20)
axs[2, 0].set_ylim(0, 5)
axs[2, 0].grid(True, linestyle='--', alpha=0.7)
collar1 = patches.Rectangle((2, 1), 15, 3, edgecolor='orange', facecolor='moccasin', lw=2)
axs[2, 0].add_patch(collar1)
# Indicate fold line
axs[2, 0].plot([2, 17], [2.5, 2.5], color='orange', linestyle='--', lw=1)
axs[2, 0].text(9.5, 2.5, f"Collar\n(15\" x 3\")\n({15*in_to_cm:.1f} cm x {3*in_to_cm:.1f} cm)", ha='center', va='center')
axs[2, 0].axis('equal')

# Collar 2
axs[2, 1].set_title("Collar 2 (Size S, Interfaced)")
axs[2, 1].set_xlim(0, 20)
axs[2, 1].set_ylim(0, 5)
axs[2, 1].grid(True, linestyle='--', alpha=0.7)
collar2 = patches.Rectangle((2, 1), 15, 3, edgecolor='orange', facecolor='moccasin', lw=2)
axs[2, 1].add_patch(collar2)
axs[2, 1].plot([2, 17], [2.5, 2.5], color='orange', linestyle='--', lw=1)
axs[2, 1].text(9.5, 2.5, f"Collar\n(15\" x 3\")\n({15*in_to_cm:.1f} cm x {3*in_to_cm:.1f} cm)", ha='center', va='center')
axs[2, 1].axis('equal')

# Placket 1
axs[3, 0].set_title("Placket 1 (Size S)")
axs[3, 0].set_xlim(0, 5)
axs[3, 0].set_ylim(0, 10)
axs[3, 0].grid(True, linestyle='--', alpha=0.7)
placket1 = patches.Rectangle((1, 1), 1.5, 5, edgecolor='brown', facecolor='sandybrown', lw=2)
axs[3, 0].add_patch(placket1)
# Add button placeholders
for y in [5, 4, 3]:
    axs[3, 0].add_patch(patches.Circle((1.75, y), 0.1, edgecolor='black', facecolor='black'))
axs[3, 0].text(2, 3, f"Placket\n(1.5\" x 5\")\n({1.5*in_to_cm:.1f} cm x {5*in_to_cm:.1f} cm)", ha='center', va='center')
axs[3, 0].axis('equal')

# Placket 2
axs[3, 1].set_title("Placket 2 (Size S, Interfaced)")
axs[3, 1].set_xlim(0, 5)
axs[3, 1].set_ylim(0, 10)
axs[3, 1].grid(True, linestyle='--', alpha=0.7)
placket2 = patches.Rectangle((1, 1), 1.5, 5, edgecolor='brown', facecolor='sandybrown', lw=2)
axs[3, 1].add_patch(placket2)
axs[3, 1].text(2, 3, f"Placket\n(1.5\" x 5\")\n({1.5*in_to_cm:.1f} cm x {5*in_to_cm:.1f} cm)", ha='center', va='center')
axs[3, 1].axis('equal')

# Interfacing for Collar
axs[4, 0].set_title("Interfacing for Collar (Size S)")
axs[4, 0].set_xlim(0, 20)
axs[4, 0].set_ylim(0, 5)
axs[4, 0].grid(True, linestyle='--', alpha=0.7)
collar_int = patches.Rectangle((2, 1), 15, 3, edgecolor='gray', facecolor='lightgray', lw=2, alpha=0.5)
axs[4, 0].add_patch(collar_int)
axs[4, 0].text(9.5, 2.5, f"Collar Interfacing\n(15\" x 3\")\n({15*in_to_cm:.1f} cm x {3*in_to_cm:.1f} cm)", ha='center', va='center')
axs[4, 0].axis('equal')

# Interfacing for Placket
axs[4, 1].set_title("Interfacing for Placket (Size S)")
axs[4, 1].set_xlim(0, 5)
axs[4, 1].set_ylim(0, 10)
axs[4, 1].grid(True, linestyle='--', alpha=0.7)
placket_int = patches.Rectangle((1, 1), 1.5, 5, edgecolor='gray', facecolor='lightgray', lw=2, alpha=0.5)
axs[4, 1].add_patch(placket_int)
axs[4, 1].text(2, 3, f"Placket Interfacing\n(1.5\" x 5\")\n({1.5*in_to_cm:.1f} cm x {5*in_to_cm:.1f} cm)", ha='center', va='center')
axs[4, 1].axis('equal')

# Adjust layout and add fabric note
plt.tight_layout()
fig.suptitle("Pattern Pieces for Women's Polo T-Shirt (Size S)\nFabric: 100% Cotton, 170-190 GSM, ~1.3 yd (1.2 m) needed for 150 cm width", fontsize=12, y=1.02)
plt.show()
