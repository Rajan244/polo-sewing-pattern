import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math # For math.sqrt

# Conversion factor
IN_TO_CM = 2.54

# --- Helper Functions ---
def dist(p1, p2):
    """Calculates distance between two points (tuples or lists of x,y)."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def get_path_length(points_list):
    """Calculates the length of a path defined by a list of points."""
    length = 0
    for i in range(len(points_list) - 1):
        length += dist(points_list[i], points_list[i+1])
    return length

# --- Predefined Measurements ---
# Note: 'collar_length_flat' is removed as it will be calculated.
# New measurements: 'neck_width_half', 'front_neck_drop', 'back_neck_drop',
# 'shoulder_width', 'shoulder_slope'.
# 'armhole_depth' is added now for future use in armhole shaping (Stage 2).
PREDEFINED_MEASUREMENTS = {
    'S': {
        'chest_panel_width': 18, 'garment_length': 24.5,
        'neck_width_half': 3.0, 'front_neck_drop': 2.75, 'back_neck_drop': 0.75,
        'shoulder_width': 4.5, 'shoulder_slope': 1.5, 'armhole_depth': 8.0, # armhole_depth from HPS
        'sleeve_length_outer': 7, 'sleeve_bicep_flat': 7, 'sleeve_cuff_flat': 6,
        'collar_height_flat': 3, 'placket_width': 1.5, 'placket_length': 5
    },
    'M': {
        'chest_panel_width': 20, 'garment_length': 25.5,
        'neck_width_half': 3.25, 'front_neck_drop': 3.0, 'back_neck_drop': 1.0,
        'shoulder_width': 5.0, 'shoulder_slope': 1.75, 'armhole_depth': 9.0,
        'sleeve_length_outer': 7.5, 'sleeve_bicep_flat': 7.5, 'sleeve_cuff_flat': 6.5,
        'collar_height_flat': 3, 'placket_width': 1.5, 'placket_length': 5.5
    },
    'L': {
        'chest_panel_width': 22, 'garment_length': 26.5,
        'neck_width_half': 3.5, 'front_neck_drop': 3.25, 'back_neck_drop': 1.0,
        'shoulder_width': 5.5, 'shoulder_slope': 2.0, 'armhole_depth': 9.5,
        'sleeve_length_outer': 8, 'sleeve_bicep_flat': 8, 'sleeve_cuff_flat': 7,
        'collar_height_flat': 3.25, 'placket_width': 1.5, 'placket_length': 6
    },
}

def get_user_measurements():
    """
    Prompts the user to select a size and customize measurements.
    Returns a tuple: (chosen_size_str, dictionary_of_final_measurements_in_inches).
    If customization is cancelled, returns (None, None).
    """
    print("Available sizes:", ", ".join(PREDEFINED_MEASUREMENTS.keys()))
    chosen_size = ""
    while chosen_size not in PREDEFINED_MEASUREMENTS:
        chosen_size_input = input(f"Enter desired size (e.g., S, M, L) or type 'quit' to exit: ").upper()
        if chosen_size_input == 'QUIT':
            return None, None, None # Added None for calculated collar length
        if chosen_size_input in PREDEFINED_MEASUREMENTS:
            chosen_size = chosen_size_input
        else:
            print(f"Invalid size. Please choose from: {', '.join(PREDEFINED_MEASUREMENTS.keys())} or type 'quit'.")

    current_measurements = PREDEFINED_MEASUREMENTS[chosen_size].copy()
    # collar_length_flat is now calculated, so not shown as customizable here
    # but we will calculate it after all other measurements are finalized.

    print(f"\n--- Default Measurements for Size {chosen_size} (in inches) ---")
    for key, value in current_measurements.items():
        display_key = key.replace('_', ' ').title()
        print(f"- {display_key}: {value}\"")

    print("\n--- Customize Measurements (optional) ---")
    print("For each measurement, enter a new value in inches or press Enter to keep the default.")
    print("Type 'cancel' at any measurement prompt to restart size selection.")

    customized_measurements = current_measurements.copy()
    for key, default_value in current_measurements.items():
        display_key = key.replace('_', ' ').title()
        while True:
            try:
                user_input = input(f"  {display_key} (current: {default_value}\"): ")
                if user_input.lower() == 'cancel':
                    print("Measurement customization cancelled. Restarting size selection...")
                    return get_user_measurements() # Recursive call to restart
                if not user_input:  # User pressed Enter
                    break
                new_value = float(user_input)
                if new_value <= 0:
                    print("  Measurement must be a positive number.")
                    continue
                customized_measurements[key] = new_value
                break
            except ValueError:
                print("  Invalid input. Please enter a number (e.g., 18.5) or press Enter.")

    # --- Calculate derived measurements (like collar length) ---
    # For now, we'll calculate this in generate_pattern_visuals once piece points are defined
    # Or we can do a preliminary calculation here if needed for display,
    # but it's better tied to the actual drafted neckline lengths.
    # For now, just pass customized_measurements.

    print("\n--- Final Measurements Selected (in inches) ---")
    for key, value in customized_measurements.items():
        display_key = key.replace('_', ' ').title()
        print(f"- {display_key}: {value}\"")
    # We will print calculated collar length later, after it's derived from necklines.

    while True:
        confirm_generate = input("\nPress Enter to generate pattern, 'e' to edit these measurements again, or 's' to select a different size: ").lower()
        if confirm_generate == '':
            return chosen_size, customized_measurements # Collar length will be calculated in generate_pattern_visuals
        elif confirm_generate == 'e':
            print(f"Re-editing measurements for size {chosen_size}...")
            for key, default_value in current_measurements.items():
                display_key = key.replace('_', ' ').title()
                while True:
                    try:
                        user_input = input(f"  {display_key} (current: {customized_measurements[key]}\", default: {default_value}\"): ")
                        if not user_input: break
                        new_value = float(user_input)
                        if new_value <=0: print("Must be positive."); continue
                        customized_measurements[key] = new_value
                        break
                    except ValueError: print("Invalid input.")
            print("\n--- Updated Final Measurements Selected (in inches) ---")
            for key, value in customized_measurements.items():
                display_key = key.replace('_', ' ').title()
                print(f"- {display_key}: {value}\"")
        elif confirm_generate == 's':
            print("Restarting size selection...")
            return get_user_measurements()
        else:
            print("Invalid option. Please press Enter, or type 'e' or 's'.")


def draw_pattern_piece_with_details(ax, piece_title, patches_list, details_text_lines, grid=True):
    """
    Draws a pattern piece and its details below the title.
    (This function remains largely the same but will now handle Polygons more often)
    """
    ax.set_title(piece_title, fontsize=12, pad=10) # Main title for the piece

    y_start_text = 0.95
    line_spacing = 0.07 # Adjust if more lines are needed
    # If details_text_lines is very long, consider reducing line_spacing or font size
    if len(details_text_lines) > 5: # example threshold
        line_spacing = 0.06
        y_start_text = 0.98


    for i, line in enumerate(details_text_lines):
        ax.text(0.05, y_start_text - (i * line_spacing), line,
                transform=ax.transAxes, fontsize=8, va='top', ha='left') # Reduced font size for more text

    if not isinstance(patches_list, list):
        patches_list = [patches_list]

    all_x = []
    all_y = []

    for patch_item in patches_list:
        ax.add_patch(patch_item)
        if isinstance(patch_item, patches.Polygon):
            x, y = zip(*patch_item.get_xy())
        elif isinstance(patch_item, patches.Rectangle):
            x = [patch_item.get_x(), patch_item.get_x() + patch_item.get_width()]
            y = [patch_item.get_y(), patch_item.get_y() + patch_item.get_height()]
        elif isinstance(patch_item, patches.Circle):
            x = [patch_item.center[0] - patch_item.radius, patch_item.center[0] + patch_item.radius]
            y = [patch_item.center[1] - patch_item.radius, patch_item.center[1] + patch_item.radius]
        else: # Fallback for other patch types if any
            try:
                # Attempt to get bounds for generic paths if possible
                path_vertices = patch_item.get_path().vertices
                x, y = zip(*path_vertices)
            except AttributeError:
                x, y = [0,1], [0,1] # Default if bounds can't be determined
        all_x.extend(x)
        all_y.extend(y)

    if all_x and all_y:
        x_min, x_max = min(all_x), max(all_x)
        y_min, y_max = min(all_y), max(all_y)

        x_range = x_max - x_min if x_max > x_min else 1.0
        y_range = y_max - y_min if y_max > y_min else 1.0

        x_pad = max(x_range * 0.15, 1.0)
        # Adjust y_pad to ensure text visibility, especially with more details
        y_pad_lower = max(y_range * 0.10, 1.0)
        y_pad_upper = max(y_range * 0.25, 2.0) # More upper padding for text space

        ax.set_xlim(x_min - x_pad, x_max + x_pad)
        ax.set_ylim(y_min - y_pad_lower, y_max + y_pad_upper)

    else: # Fallback if no patches
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)

    if grid:
        ax.grid(True, linestyle='--', alpha=0.6)

    ax.set_aspect('equal', adjustable='box')
    ax.axis('off')


def generate_pattern_visuals(size_name, measurements):
    """
    Generates and displays the pattern visuals with more detailed drafting.
    """
    piece_edgecolor = 'black'
    interfacing_alpha = 0.4
    # plot_offset_x, plot_offset_y are effectively piece-specific now if points are defined from (0,0) locally
    # then shifted. Or, define points globally assuming each subplot has its own (0,0) origin.
    # For simplicity, let's assume each piece's points are defined in its own local coordinate space,
    # and (0,0) of that space is then positioned. We'll use plot_offset_x, plot_offset_y as this position.
    base_offset_x, base_offset_y = 1, 1 # General offset for drawing pieces in their subplots

    m = measurements # shorthand

    # --- Body Piece Calculations ---
    # Garment length is from HPS (High Point Shoulder at neck) to hem.
    # Shoulder slope is the vertical drop from HPS to the shoulder tip.
    # Ensure shoulder_width is not less than shoulder_slope for dx_shoulder calculation
    if m['shoulder_width'] < m['shoulder_slope']:
        print(f"Warning: Shoulder slope ({m['shoulder_slope']}\") is greater than shoulder width ({m['shoulder_width']}\"). Adjusting slope for calculation.")
        m['shoulder_slope'] = m['shoulder_width'] * 0.98 # Ensure it's slightly less for sqrt

    dx_shoulder = math.sqrt(max(0, m['shoulder_width']**2 - m['shoulder_slope']**2))

    # --- Page 1: Front and Back Body ---
    fig1, axs1 = plt.subplots(1, 2, figsize=(12, 8)) # Slightly taller for more complex shapes
    fig1.suptitle(f"Polo Shirt - Size {size_name} - Page 1/3: Body Pieces (Detailed Draft)", fontsize=14)

    # 1. Back Body (Cut 1 on Fold)
    # Points are defined for the half piece, relative to (0,0) at Center Back Hem.
    # Then offset by base_offset_x, base_offset_y for plotting.
    back_pts_local = []
    # P1: CB Hem
    p1_b = (0, 0)
    # P2: Side Hem
    p2_b = (m['chest_panel_width'] / 2, 0)
    # P3: Side Underarm (armhole depth is from HPS)
    p3_b = (m['chest_panel_width'] / 2, m['garment_length'] - m['armhole_depth'])
    # P4: Shoulder Tip
    p4_b = (m['neck_width_half'] + dx_shoulder, m['garment_length'] - m['shoulder_slope'])
    # P5: HPS (High Point Shoulder at Neck)
    p5_b = (m['neck_width_half'], m['garment_length'])
    # P6: CB Neckline Point (at Center Back)
    p6_b = (0, m['garment_length'] - m['back_neck_drop'])

    # For a simple curved neckline (3 points: P6, control, P5)
    # Control point for back neck curve (approximate)
    neck_ctrl_b_x = m['neck_width_half'] * 0.5
    neck_ctrl_b_y = (p6_b[1] + p5_b[1]) / 2 + m['back_neck_drop'] * 0.2 # Slight upward curve
    p_neck_ctrl_b = (neck_ctrl_b_x, neck_ctrl_b_y)

    # For a simple curved armhole (3 points: P4, control, P3)
    # Control point for back armhole (approximate)
    arm_ctrl_b_x = (p4_b[0] + p3_b[0]) / 2 + (m['chest_panel_width']/2 - (m['neck_width_half'] + dx_shoulder)) * 0.2
    arm_ctrl_b_y = (p4_b[1] + p3_b[1]) / 2 - m['armhole_depth'] * 0.1 # Slight outward curve
    p_arm_ctrl_b = (arm_ctrl_b_x, arm_ctrl_b_y)


    back_pts_local = [p1_b, p2_b, p3_b, p_arm_ctrl_b, p4_b, p5_b, p_neck_ctrl_b, p6_b] # Order for polygon
    back_pts_plot = [(x + base_offset_x, y + base_offset_y) for x, y in back_pts_local]
    back_shape = patches.Polygon(back_pts_plot, edgecolor=piece_edgecolor, facecolor='lightgreen', lw=1.5)

    # Back Neckline Length (half)
    back_neckline_curve_pts = [p_neck_ctrl_b, p6_b] # from HPS to CB_Neck (reversed for path calc)
    back_neck_path_for_length = [p5_b] + [p_neck_ctrl_b] + [p6_b] # HPS -> Control -> CB Neck
    half_back_neckline_length = get_path_length(back_neck_path_for_length)


    fold_line_y_start = p1_b[1] + base_offset_y
    fold_line_y_end = p6_b[1] + base_offset_y # CB neck point
    fold_line_back = patches.Polygon([(base_offset_x, fold_line_y_start), (base_offset_x, fold_line_y_end)],
                                     closed=False, edgecolor='darkgreen', linestyle='-.', lw=1.5)
    axs1[1].text(base_offset_x + 0.3, base_offset_y + (fold_line_y_end - fold_line_y_start) / 2, "FOLD\nLINE",
                 ha='center', va='center', fontsize=8, rotation=90, color='darkgreen',
                 bbox=dict(boxstyle='round,pad=0.1', fc='white', alpha=0.5))

    back_details = [
        f"Cut 1 on Fold",
        f"HPS to Hem: {m['garment_length']:.1f}\"",
        f"Half Chest: {m['chest_panel_width']/2:.1f}\"",
        f"Calculated Half Back Neckline: {half_back_neckline_length:.2f}\"",
        "Armhole/Neckline are simplified curves."
    ]
    draw_pattern_piece_with_details(axs1[1], "2. Back Body", [back_shape, fold_line_back], back_details)


    # 2. Front Body (Cut 1 Fabric)
    # Points defined relative to (0,0) at Center Front Hem. Symmetrical.
    front_pts_local_right_half = [] # CF to Right Side Seam
    # P1_f: CF Hem
    p1_f_cf = (0, 0)
    # P_CF_Neck: Center Front Neckline lowest point
    p_cf_neck = (0, m['garment_length'] - m['front_neck_drop'])

    # Right Side points
    p_hps_r = (m['neck_width_half'], m['garment_length'])
    p_st_r = (m['neck_width_half'] + dx_shoulder, m['garment_length'] - m['shoulder_slope']) # Shoulder Tip Right
    p_au_r = (m['chest_panel_width'] / 2, m['garment_length'] - m['armhole_depth']) # Armhole Underarm Right
    p_sh_r = (m['chest_panel_width'] / 2, 0) # Side Hem Right

    # Control point for Front Neck Curve (right half: p_cf_neck -> control -> p_hps_r)
    fn_ctrl_r_x = m['neck_width_half'] * 0.4
    fn_ctrl_r_y = p_cf_neck[1] + (p_hps_r[1] - p_cf_neck[1]) * 0.3 # Adjust for desired curve
    p_fn_ctrl_r = (fn_ctrl_r_x, fn_ctrl_r_y)

    # Control point for Front Armhole Curve (right half: p_st_r -> control -> p_au_r)
    fa_ctrl_r_x = (p_st_r[0] + p_au_r[0])/2 + (m['chest_panel_width']/2 - (m['neck_width_half'] + dx_shoulder))*0.15
    fa_ctrl_r_y = (p_st_r[1] + p_au_r[1])/2 - m['armhole_depth'] * 0.05 # Flatter than back
    p_fa_ctrl_r = (fa_ctrl_r_x, fa_ctrl_r_y)

    # Front Neckline path (right half) for length calculation
    front_neck_path_right_half = [p_cf_neck, p_fn_ctrl_r, p_hps_r]
    half_front_neckline_length = get_path_length(front_neck_path_right_half)

    # Polygon points for Right Half (from CF_Neck clockwise)
    # CF_Neck -> Neck_Ctrl_R -> HPS_R -> ST_R -> Arm_Ctrl_R -> AU_R -> SH_R -> (CF_Hem needs to be midpoint)
    # We need to construct the full polygon
    front_polygon_pts = [
        p_cf_neck, p_fn_ctrl_r, p_hps_r, p_st_r, p_fa_ctrl_r, p_au_r, p_sh_r, # Right side top down to hem
        (-p_sh_r[0], p_sh_r[1]), # Left side hem (mirrored x)
        (-p_au_r[0], p_au_r[1]), # Left AU
        (-p_fa_ctrl_r[0], p_fa_ctrl_r[1]), # Left Arm Ctrl
        (-p_st_r[0], p_st_r[1]), # Left ST
        (-p_hps_r[0], p_hps_r[1]), # Left HPS
        (-p_fn_ctrl_r[0], p_fn_ctrl_r[1]), # Left Neck Ctrl
        # p_cf_neck is the close point, already listed
    ]
    # Adjust all points by base_offset_x (for centering if needed) and base_offset_y
    # Local (0,0) is CF Hem. We want to plot it centered perhaps, or from bottom-left of bounding box.
    # For now, let's make the plot_offset effectively shift the (0,0) of this local system.
    # The front piece is symmetric around Y-axis. Its width is m['chest_panel_width'].
    # So, shift X by base_offset_x + m['chest_panel_width']/2 to make left edge appear at base_offset_x.
    front_plot_offset_x = base_offset_x + m['chest_panel_width']/2
    front_pts_plot = [(x + front_plot_offset_x, y + base_offset_y) for x, y in front_polygon_pts]
    front_shape = patches.Polygon(front_pts_plot, edgecolor=piece_edgecolor, facecolor='lightblue', lw=1.5)

    # Placket indicator - position relative to CF Neck point
    placket_w = m['placket_width']
    placket_l = m['placket_length']
    # CF Neck point in plot coordinates:
    cf_neck_plot_x = p_cf_neck[0] + front_plot_offset_x
    cf_neck_plot_y = p_cf_neck[1] + base_offset_y

    placket_indicator_x = cf_neck_plot_x - placket_w / 2
    placket_indicator_y = cf_neck_plot_y - placket_l # Placket extends downwards from CF neck
    placket_area_indicator = patches.Rectangle((placket_indicator_x, placket_indicator_y),
                                             placket_w, placket_l,
                                             edgecolor='red', facecolor='none', linestyle='--', lw=1)

    front_details = [
        f"Cut 1 Fabric",
        f"HPS to Hem: {m['garment_length']:.1f}\"",
        f"Chest Width: {m['chest_panel_width']:.1f}\"",
        f"Calculated Half Front Neckline: {half_front_neckline_length:.2f}\"",
        "Armhole/Neckline are simplified curves.",
        "Placket placement indicated."
    ]
    draw_pattern_piece_with_details(axs1[0], "1. Front Body", [front_shape, placket_area_indicator], front_details)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

    # --- CALCULATE COLLAR LENGTH ---
    calculated_collar_length = (half_back_neckline_length * 2) + (half_front_neckline_length * 2)
    print(f"\n--- Calculated Collar Dimensions ---")
    print(f"Total Neckline Circumference: {calculated_collar_length:.2f}\"")
    print(f"This will be used as the Collar Length (flat).")
    # Store it back in measurements for other pieces to use
    m['collar_length_calculated'] = calculated_collar_length


    # --- Figure 2: Sleeves and Collars ---
    fig2, axs2 = plt.subplots(2, 2, figsize=(12, 10))
    fig2.suptitle(f"Polo Shirt - Size {size_name} - Page 2/3: Sleeves & Collars", fontsize=14)

    # SLEEVE (Still using old simplified drafting for now)
    sL = m['sleeve_length_outer']
    sWB = m['sleeve_bicep_flat']
    sWC = m['sleeve_cuff_flat']
    cap_proportion = 0.25 # This will be improved in Stage 2/3
    cap_height_old_method = sL * cap_proportion
    underarm_length = sL - cap_height_old_method
    if sWC > sWB : sWC = sWB

    # Sleeve points using old method for now, offset for plotting
    plot_sleeve_offset_x, plot_sleeve_offset_y = base_offset_x, base_offset_y
    p1_cuff_left = (plot_sleeve_offset_x + (sWB - sWC) / 2, plot_sleeve_offset_y)
    p2_cuff_right = (plot_sleeve_offset_x + (sWB - sWC) / 2 + sWC, plot_sleeve_offset_y)
    p5_underarm_left = (plot_sleeve_offset_x, plot_sleeve_offset_y + underarm_length)
    p3_underarm_right = (plot_sleeve_offset_x + sWB, plot_sleeve_offset_y + underarm_length)
    cap_peak_x = plot_sleeve_offset_x + sWB / 2
    cap_peak_y = plot_sleeve_offset_y + sL
    cap_control_inset_factor = 0.1
    cap_control_lift_factor = 0.5
    p_cap_ctrl_left = (plot_sleeve_offset_x + sWB * cap_control_inset_factor,
                       plot_sleeve_offset_y + underarm_length + cap_height_old_method * cap_control_lift_factor)
    p_cap_ctrl_right = (plot_sleeve_offset_x + sWB * (1 - cap_control_inset_factor),
                        plot_sleeve_offset_y + underarm_length + cap_height_old_method * cap_control_lift_factor)
    sleeve_polygon_points = [p1_cuff_left, p2_cuff_right, p3_underarm_right,
                             p_cap_ctrl_right, (cap_peak_x, cap_peak_y), p_cap_ctrl_left, p5_underarm_left]

    sleeve_details_text = [
        f"Cut 2 Fabric",
        f"Length: {sL:.1f}\", Bicep (flat): {sWB:.1f}\"",
        f"Cuff (flat): {sWC:.1f}\"",
        f"(L: {sL * IN_TO_CM:.1f} cm, Bicep: {sWB * IN_TO_CM:.1f} cm, Cuff: {sWC * IN_TO_CM:.1f} cm)",
        "Note: Sleeve cap drafting is simplified (to be updated)."
    ]
    if sL <=0 or sWB <=0 or sWC <=0 or underarm_length <0 or cap_height_old_method <0 :
        sleeve_patch_1 = patches.Rectangle((plot_sleeve_offset_x, plot_sleeve_offset_y), 1, 1, edgecolor='red', facecolor='lightcoral', lw=1)
        sleeve_patch_2 = patches.Rectangle((plot_sleeve_offset_x, plot_sleeve_offset_y), 1, 1, edgecolor='red', facecolor='lightcoral', lw=1)
        sleeve_details_text.append("Sleeve Error: Invalid Dimensions")
    else:
        sleeve_patch_1 = patches.Polygon(sleeve_polygon_points, edgecolor=piece_edgecolor, facecolor='thistle', lw=1.5)
        sleeve_patch_2 = patches.Polygon(sleeve_polygon_points, edgecolor=piece_edgecolor, facecolor='thistle', lw=1.5)

    draw_pattern_piece_with_details(axs2[0, 0], "3. Sleeve (Piece 1)", sleeve_patch_1, sleeve_details_text)
    draw_pattern_piece_with_details(axs2[0, 1], "4. Sleeve (Piece 2)", sleeve_patch_2, sleeve_details_text)


    # COLLAR (Using calculated length)
    collar_l = m['collar_length_calculated'] # Use calculated length
    collar_h = m['collar_height_flat']
    collar_shape_1 = patches.Rectangle((base_offset_x, base_offset_y), collar_l, collar_h,
                                       edgecolor=piece_edgecolor, facecolor='moccasin', lw=1.5)
    collar_shape_2 = patches.Rectangle((base_offset_x, base_offset_y), collar_l, collar_h,
                                       edgecolor=piece_edgecolor, facecolor='moccasin', lw=1.5)
    fold_line_y_collar = base_offset_y + collar_h / 2
    collar_fold_1 = patches.Polygon([(base_offset_x, fold_line_y_collar), (base_offset_x + collar_l, fold_line_y_collar)],
                                  edgecolor='orange', linestyle='--', lw=1)
    collar_fold_2 = patches.Polygon([(base_offset_x, fold_line_y_collar), (base_offset_x + collar_l, fold_line_y_collar)],
                                  edgecolor='orange', linestyle='--', lw=1)
    collar_details = [
        f"Cut 2 Fabric, Cut 1 Interfacing",
        f"Calculated Length: {collar_l:.2f}\"", # Show calculated length
        f"Height: {collar_h:.1f}\"",
        f"({collar_l * IN_TO_CM:.1f} cm L x {collar_h * IN_TO_CM:.1f} cm H)",
        "Fold line indicated (for collar stand if part of design, or simple fold)."
    ]
    draw_pattern_piece_with_details(axs2[1, 0], "5. Collar (Piece 1)", [collar_shape_1, collar_fold_1], collar_details)
    draw_pattern_piece_with_details(axs2[1, 1], "6. Collar (Piece 2)", [collar_shape_2, collar_fold_2], collar_details)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

    # --- Figure 3: Plackets and Interfacings ---
    # (This section remains mostly the same, uses original placket_width/length, collar_h)
    fig3, axs3 = plt.subplots(2, 2, figsize=(12, 10))
    fig3.suptitle(f"Polo Shirt - Size {size_name} - Page 3/3: Plackets & Interfacing", fontsize=14)

    placket_w = m['placket_width']
    placket_l = m['placket_length']
    # (Rest of placket and interfacing drawing code from your original, no changes here for Stage 1)
    placket_shape_1 = patches.Rectangle((base_offset_x, base_offset_y), placket_w, placket_l,
                                        edgecolor=piece_edgecolor, facecolor='sandybrown', lw=1.5)
    placket_shape_2 = patches.Rectangle((base_offset_x, base_offset_y), placket_w, placket_l,
                                        edgecolor=piece_edgecolor, facecolor='sandybrown', lw=1.5)
    buttons = []
    num_buttons = 3
    if placket_l > 1 and placket_w > 0.2:
        button_spacing = placket_l / (num_buttons +1)
        button_radius = min(placket_w * 0.15, 0.18)
        for i in range(num_buttons):
            button_y_placket = base_offset_y + (i + 1) * button_spacing # Y relative to placket piece
            button_x_placket = base_offset_x + placket_w / 2
            buttons.append(patches.Circle((button_x_placket, button_y_placket), button_radius, edgecolor='black', facecolor='darkgrey'))

    placket_details_buttons = [
        f"Cut 2 Fabric", f"Cut 1-2 Interfacing (as needed)",
        f"Piece: {placket_w:.1f}\" x {placket_l:.1f}\"",
        f"({placket_w * IN_TO_CM:.1f} cm x {placket_l * IN_TO_CM:.1f} cm)",
        "Button placement indicative."
    ]
    placket_details_no_buttons = [
        f"Cut 2 Fabric", f"Typically Interfaced",
        f"Piece: {placket_w:.1f}\" x {placket_l:.1f}\"",
        f"({placket_w * IN_TO_CM:.1f} cm x {placket_l * IN_TO_CM:.1f} cm)"
    ]
    draw_pattern_piece_with_details(axs3[0, 0], "7. Placket (Button Side)", [placket_shape_1] + buttons, placket_details_buttons)
    draw_pattern_piece_with_details(axs3[0, 1], "8. Placket (Buttonhole Side)", placket_shape_2, placket_details_no_buttons)

    # Interfacing for collar (using calculated length)
    interfacing_collar_shape = patches.Rectangle((base_offset_x, base_offset_y), collar_l, collar_h,
                                                 edgecolor='dimgray', facecolor='lightgray', lw=1, alpha=interfacing_alpha)
    interfacing_collar_details = [
        f"Cut 1 Interfacing", f"Piece: {collar_l:.2f}\" x {collar_h:.1f}\"",
        f"({collar_l * IN_TO_CM:.1f} cm x {collar_h * IN_TO_CM:.1f} cm)"
    ]
    draw_pattern_piece_with_details(axs3[1, 0], "9. Collar Interfacing", interfacing_collar_shape, interfacing_collar_details)

    interfacing_placket_shape = patches.Rectangle((base_offset_x, base_offset_y), placket_w, placket_l,
                                                  edgecolor='dimgray', facecolor='lightgray', lw=1, alpha=interfacing_alpha)
    interfacing_placket_details = [
        f"Cut 1-2 Interfacing (as needed)", f"Piece: {placket_w:.1f}\" x {placket_l:.1f}\"",
        f"({placket_w * IN_TO_CM:.1f} cm x {placket_l * IN_TO_CM:.1f} cm)"
    ]
    draw_pattern_piece_with_details(axs3[1, 1], "10. Placket Interfacing", interfacing_placket_shape, interfacing_placket_details)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()


def output_product_details(size_name, measurements):
    """Prints the final garment dimensions in CM for website product details."""
    # This function remains largely the same, but will now also show calculated collar length
    m = measurements
    print(f"\n--- Product Details for Size {size_name} (Polo Shirt) ---")
    print(f"All measurements are approximate finished garment dimensions in CM, based on input pattern piece values.")

    shoulder_panel_cm = m['chest_panel_width'] * IN_TO_CM
    print(f"Shoulder / Chest Panel Width (one side, flat panel): {shoulder_panel_cm:.1f} cm")
    print(f"  (Note: Actual shoulder point-to-point on finished garment may vary after construction and depends on armhole shape).")

    length_cm = m['garment_length'] * IN_TO_CM
    print(f"Length (from HPS/neck to hem): {length_cm:.1f} cm")

    sleeve_length_cm = m['sleeve_length_outer'] * IN_TO_CM
    print(f"Sleeve Length (outer arm, from approx. shoulder point): {sleeve_length_cm:.1f} cm")

    bust_circumference_cm = 2 * m['chest_panel_width'] * IN_TO_CM
    print(f"Bust (circumference, from 2x chest panel width): {bust_circumference_cm:.1f} cm")

    cuff_circumference_cm = 2 * m['sleeve_cuff_flat'] * IN_TO_CM
    print(f"Cuff Opening (circumference): {cuff_circumference_cm:.1f} cm")

    bicep_circumference_cm = 2 * m['sleeve_bicep_flat'] * IN_TO_CM
    print(f"Bicep (circumference): {bicep_circumference_cm:.1f} cm")

    if 'collar_length_calculated' in m:
        collar_length_cm = m['collar_length_calculated'] * IN_TO_CM
        print(f"Collar Opening (approx. circumference from calculated length): {collar_length_cm:.1f} cm")
    print("--- End of Product Details ---")


if __name__ == '__main__':
    print("Welcome to the Interactive Polo Shirt Pattern Generator (Enhanced Drafting)!")
    selected_size, final_measurements = get_user_measurements()

    if final_measurements:
        print("\nGenerating pattern visuals based on your selections...")
        print("Please close each pattern figure window to proceed to the next.")
        print("Note on 'Cut on Fold' pieces (like the Back Body):")
        print("  The pattern piece shown is HALF the width of the final piece.")
        print("  It's designed to be placed on the FOLD of the fabric.")
        print("  When cut and unfolded, it creates the full-width symmetrical piece.")
        generate_pattern_visuals(selected_size, final_measurements) # This now calculates and adds collar_length_calculated
        output_product_details(selected_size, final_measurements)
        print("\nPattern generation process complete.")
        print("Note: These are more detailed pattern shapes for visualization.")
        print("Necklines/Armholes are simplified curves. Sleeve cap is still basic.")
        print("For actual garment construction, add seam allowances and refine shapes further.")
    else:
        print("Pattern generation exited.")
