import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math
import logging
import sys

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Conversion factor
IN_TO_CM = 2.54

# Helper Functions
def dist(p1, p2):
    """Calculate distance between two points."""
    try:
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
    except Exception as e:
        logger.error(f"Error calculating distance: {e}")
        raise

def get_path_length(points_list):
    """Calculate length of a path defined by points."""
    try:
        length = 0
        for i in range(len(points_list) - 1):
            length += dist(points_list[i], points_list[i + 1])
        return length
    except Exception as e:
        logger.error(f"Error calculating path length: {e}")
        raise

def quadratic_bezier(p0, p1, p2, t):
    """Calculate a point on a quadratic Bezier curve."""
    try:
        x = (1 - t)**2 * p0[0] + 2 * (1 - t) * t * p1[0] + t**2 * p2[0]
        y = (1 - t)**2 * p0[1] + 2 * (1 - t) * t * p1[1] + t**2 * p2[1]
        return (x, y)
    except Exception as e:
        logger.error(f"Error in quadratic Bezier calculation: {e}")
        raise

def generate_bezier_points(p0, p1, p2, num_points=30):
    """Generate points along a quadratic Bezier curve."""
    try:
        return [quadratic_bezier(p0, p1, p2, i / num_points) for i in range(num_points + 1)]
    except Exception as e:
        logger.error(f"Error generating Bezier points: {e}")
        raise

def offset_bezier_curve(p0, p1, p2, offset=0.375, num_points=10):
    """Generate offset points for a Bezier curve."""
    try:
        offset_points = []
        for i in range(num_points + 1):
            t = i / num_points
            x, y = quadratic_bezier(p0, p1, p2, t)
            dx_dt = 2 * (1 - t) * (p1[0] - p0[0]) + 2 * t * (p2[0] - p1[0])
            dy_dt = 2 * (1 - t) * (p1[1] - p0[1]) + 2 * t * (p2[1] - p1[1])
            normal = (-dy_dt, dx_dt)
            normal_length = math.sqrt(normal[0]**2 + normal[1]**2)
            if normal_length > 0:
                normal_unit = (normal[0] / normal_length, normal[1] / normal_length)
                x_offset = x + offset * normal_unit[0]
                y_offset = y + offset * normal_unit[1]
                offset_points.append((x_offset, y_offset))
        return offset_points
    except Exception as e:
        logger.error(f"Error offsetting Bezier curve: {e}")
        raise

def draw_straight_seam_allowance(ax, p1, p2, offset=0.375):
    """Draw seam allowance for a straight edge."""
    try:
        v = (p2[0] - p1[0], p2[1] - p1[1])
        length = math.sqrt(v[0]**2 + v[1]**2)
        if length == 0:
            return
        n = (-v[1] / length, v[0] / length)
        p1_offset = (p1[0] + offset * n[0], p1[1] + offset * n[1])
        p2_offset = (p2[0] + offset * n[0], p2[1] + offset * n[1])
        ax.plot([p1_offset[0], p2_offset[0]], [p1_offset[1], p2_offset[1]], color='red', linestyle='--', lw=1)
    except Exception as e:
        logger.error(f"Error drawing straight seam allowance: {e}")
        raise

def draw_bezier_seam_allowance(ax, p0, p1, p2, offset=0.375, num_points=10):
    """Draw seam allowance for a Bezier edge."""
    try:
        offset_points = offset_bezier_curve(p0, p1, p2, offset, num_points)
        ax.plot([p[0] for p in offset_points], [p[1] for p in offset_points], color='red', linestyle='--', lw=1)
    except Exception as e:
        logger.error(f"Error drawing Bezier seam allowance: {e}")
        raise

def draw_grainline(ax, x, y_start, y_end, arrow_size=0.5):
    """Draw a vertical grainline with arrows."""
    try:
        ax.plot([x, x], [y_start, y_end], color='black', lw=1)
        ax.arrow(x, y_end, 0, arrow_size, head_width=0.2, head_length=0.2, fc='black', ec='black')
        ax.arrow(x, y_start, 0, -arrow_size, head_width=0.2, head_length=0.2, fc='black', ec='black')
    except Exception as e:
        logger.error(f"Error drawing grainline: {e}")
        raise

def find_max_y_bezier(p0, p1, p2, num_points=20):
    """Find the point with maximum y-coordinate on a Bezier curve."""
    try:
        max_y = -float('inf')
        max_point = None
        for i in range(num_points + 1):
            t = i / num_points
            x, y = quadratic_bezier(p0, p1, p2, t)
            if y > max_y:
                max_y = y
                max_point = (x, y)
        return max_point
    except Exception as e:
        logger.error(f"Error finding max y on Bezier: {e}")
        raise

def draw_notch(ax, point, direction, length=0.25):
    """Draw a notch at a point."""
    try:
        p1 = (point[0] + length * direction[0], point[1] + length * direction[1])
        ax.plot([point[0], p1[0]], [point[1], p1[1]], color='black', lw=1.5)
    except Exception as e:
        logger.error(f"Error drawing notch: {e}")
        raise

def annotate_straight_edges(ax, edges, offset_x, offset_y, offset=0.3):
    """Annotate lengths of straight edges in complex pieces."""
    try:
        for edge_type, points in edges:
            if edge_type == 'straight':
                p1 = (points[0][0] + offset_x, points[0][1] + offset_y)
                p2 = (points[1][0] + offset_x, points[1][1] + offset_y)
                length = dist(points[0], points[1])
                midpoint = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
                v = (p2[0] - p1[0], p2[1] - p1[1])
                length_v = math.sqrt(v[0]**2 + v[1]**2)
                if length_v > 0:
                    n = (v[1] / length_v, -v[0] / length_v)
                    annotation_pos = (midpoint[0] + n[0] * offset, midpoint[1] + n[1] * offset)
                    angle = math.degrees(math.atan2(v[1], v[0]))
                    ax.annotate(f"{length:.2f}\"", xy=annotation_pos, ha='center', va='center',
                                rotation=angle, fontsize=8, color='blue')
    except Exception as e:
        logger.error(f"Error annotating straight edges: {e}")
        raise

def annotate_rectangle_dimensions(ax, x, y, width, height):
    """Annotate dimensions of rectangular pieces."""
    try:
        ax.annotate(f"{width:.2f}\"", xy=(x + width / 2, y - 0.5), ha='center', va='top', fontsize=8, color='blue')
        ax.annotate(f"{height:.2f}\"", xy=(x - 0.5, y + height / 2), ha='right', va='center', rotation=90, fontsize=8, color='blue')
    except Exception as e:
        logger.error(f"Error annotating rectangle dimensions: {e}")
        raise

# Predefined Measurements (Corrected)
PREDEFINED_MEASUREMENTS = {
    'S': {
        'half_chest_flat': 18, 'garment_length': 24.5, 'neck_width_half': 3.0,
        'front_neck_drop': 2.75, 'back_neck_drop': 0.75, 'shoulder_width': 4.5,
        'shoulder_slope': 1.5, 'armhole_depth': 8.0, 'sleeve_length_outer': 7,
        'sleeve_bicep_flat': 7, 'sleeve_cuff_flat': 6, 'collar_height_flat': 3,
        'placket_width': 1.5, 'placket_length': 5
    },
    'M': {
        'half_chest_flat': 20, 'garment_length': 25.5, 'neck_width_half': 3.25,
        'front_neck_drop': 3.0, 'back_neck_drop': 1.0, 'shoulder_width': 5.0,
        'shoulder_slope': 1.75, 'armhole_depth': 9.0, 'sleeve_length_outer': 7.5,
        'sleeve_bicep_flat': 7.5, 'sleeve_cuff_flat': 6.5, 'collar_height_flat': 3,
        'placket_width': 1.5, 'placket_length': 5.5
    },
    'L': {
        'half_chest_flat': 22, 'garment_length': 26.5, 'neck_width_half': 3.5,
        'front_neck_drop': 3.25, 'back_neck_drop': 1.0, 'shoulder_width': 5.5,
        'shoulder_slope': 2.0, 'armhole_depth': 9.5, 'sleeve_length_outer': 8,
        'sleeve_bicep_flat': 8, 'sleeve_cuff_flat': 7, 'collar_height_flat': 3.25,
        'placket_width': 1.5, 'placket_length': 6
    },
}

def get_user_measurements():
    """Prompt user for size and measurements."""
    try:
        print("Available sizes:", ", ".join(PREDEFINED_MEASUREMENTS.keys()))
        chosen_size = ""
        while chosen_size not in PREDEFINED_MEASUREMENTS:
            chosen_size_input = input("Enter size (e.g., S, M, L) or 'quit': ").upper()
            if chosen_size_input == 'QUIT':
                return None, None
            if chosen_size_input in PREDEFINED_MEASUREMENTS:
                chosen_size = chosen_size_input
            else:
                print(f"Invalid size. Choose from: {', '.join(PREDEFINED_MEASUREMENTS.keys())} or 'quit'.")

        current_measurements = PREDEFINED_MEASUREMENTS[chosen_size].copy()
        print(f"\nDefault Measurements for Size {chosen_size} (in inches):")
        for key, value in current_measurements.items():
            print(f"- {key.replace('_', ' ').title()}: {value}\"")

        print("\nCustomize Measurements (optional):")
        print("Enter new value in inches or press Enter. Type 'cancel' to restart.")
        customized_measurements = current_measurements.copy()
        for key, default_value in current_measurements.items():
            display_key = key.replace('_', ' ').title()
            while True:
                try:
                    user_input = input(f"  {display_key} (current: {default_value}\"): ")
                    if user_input.lower() == 'cancel':
                        print("Customization cancelled. Restarting...")
                        return get_user_measurements()
                    if not user_input:
                        break
                    new_value = float(user_input)
                    if new_value <= 0:
                        print("  Measurement must be positive.")
                        continue
                    customized_measurements[key] = new_value
                    break
                except ValueError:
                    print("  Invalid input. Enter a number or press Enter.")

        print("\nFinal Measurements Selected (in inches):")
        for key, value in customized_measurements.items():
            print(f"- {key.replace('_', ' ').title()}: {value}\"")
        
        while True:
            confirm = input("\nPress Enter to generate, 'e' to edit, 's' to select size: ").lower()
            if confirm == '':
                return chosen_size, customized_measurements
            elif confirm == 'e':
                for key, default_value in current_measurements.items():
                    display_key = key.replace('_', ' ').title()
                    while True:
                        try:
                            user_input = input(f"  {display_key} (current: {customized_measurements[key]}\"): ")
                            if not user_input:
                                break
                            new_value = float(user_input)
                            if new_value <= 0:
                                print("  Must be positive.")
                                continue
                            customized_measurements[key] = new_value
                            break
                        except ValueError:
                            print("  Invalid input.")
                print("\nUpdated Measurements:")
                for key, value in customized_measurements.items():
                    print(f"- {key.replace('_', ' ').title()}: {value}\"")
            elif confirm == 's':
                return get_user_measurements()
            else:
                print("Invalid option. Press Enter, 'e', or 's'.")
    except Exception as e:
        logger.error(f"Error in get_user_measurements: {e}")
        return None, None

def draw_pattern_piece_with_details(ax, piece_title, patches_list, details_text_lines, grid=True):
    """Draw a pattern piece with details."""
    try:
        ax.set_title(piece_title, fontsize=12, pad=10)
        y_start_text = 0.95
        line_spacing = 0.07 if len(details_text_lines) <= 5 else 0.06
        for i, line in enumerate(details_text_lines):
            ax.text(0.05, y_start_text - (i * line_spacing), line, transform=ax.transAxes,
                    fontsize=8, va='top', ha='left')
        
        if not isinstance(patches_list, list):
            patches_list = [patches_list]
        
        all_x, all_y = [], []
        for patch in patches_list:
            ax.add_patch(patch)
            if isinstance(patch, patches.Polygon):
                x, y = zip(*patch.get_xy())
            elif isinstance(patch, patches.Rectangle):
                x = [patch.get_x(), patch.get_x() + patch.get_width()]
                y = [patch.get_y(), patch.get_y() + patch.get_height()]
            elif isinstance(patch, patches.Circle):
                x = [patch.center[0] - patch.radius, patch.center[0] + patch.radius]
                y = [patch.center[1] - patch.radius, patch.center[1] + patch.radius]
            else:
                try:
                    x, y = zip(*patch.get_path().vertices)
                except AttributeError:
                    x, y = [0, 1], [0, 1]
            all_x.extend(x)
            all_y.extend(y)
        
        if all_x and all_y:
            x_min, x_max = min(all_x), max(all_x)
            y_min, y_max = min(all_y), max(all_y)
            x_range = x_max - x_min if x_max > x_min else 1.0
            y_range = y_max - y_min if y_max > y_min else 1.0
            x_pad = max(x_range * 0.15, 1.0)
            y_pad_lower = max(y_range * 0.10, 1.0)
            y_pad_upper = max(y_range * 0.25, 2.0)
            ax.set_xlim(x_min - x_pad, x_max + x_pad)
            ax.set_ylim(y_min - y_pad_lower, y_max + y_pad_upper)
        else:
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
        
        if grid:
            ax.grid(True, linestyle='--', alpha=0.6)
        ax.set_aspect('equal', adjustable='box')
        ax.axis('off')
    except Exception as e:
        logger.error(f"Error drawing pattern piece: {e}")
        raise

def generate_pattern_visuals(size_name, measurements):
    """Generate and display pattern visuals."""
    try:
        logger.info("Starting pattern generation")
        piece_edgecolor = 'black'
        interfacing_alpha = 0.4
        base_offset_x, base_offset_y = 1, 1
        m = measurements

        if m['shoulder_width'] < m['shoulder_slope']:
            m['shoulder_slope'] = m['shoulder_width'] * 0.98
        dx_shoulder = math.sqrt(max(0, m['shoulder_width']**2 - m['shoulder_slope']**2))

        # Page 1: Front and Back Body
        logger.info("Generating Page 1: Body Pieces")
        fig1, axs1 = plt.subplots(1, 2, figsize=(12, 8))
        fig1.suptitle(f"Polo Shirt - Size {size_name} - Page 1/3: Body Pieces", fontsize=14)

        # Back Body (Cut 1 on Fold)
        p1_b = (0, 0)
        p2_b = (m['half_chest_flat'] / 2, 0)
        p3_b = (m['half_chest_flat'] / 2, m['garment_length'] - m['armhole_depth'])
        p4_b = (m['neck_width_half'] + dx_shoulder, m['garment_length'] - m['shoulder_slope'])
        p5_b = (m['neck_width_half'], m['garment_length'])
        p6_b = (0, m['garment_length'] - m['back_neck_drop'])
        p_neck_ctrl_b = (m['neck_width_half'] * 0.5, (p6_b[1] + p5_b[1]) / 2 + m['back_neck_drop'] * 0.2)
        p_arm_ctrl_b = ((p4_b[0] + p3_b[0]) / 2 + (m['half_chest_flat']/2 - (m['neck_width_half'] + dx_shoulder)) * 0.2,
                        (p4_b[1] + p3_b[1]) / 2 - m['armhole_depth'] * 0.1)

        back_pts_local_smooth = (
            [p1_b, p2_b, p3_b] +
            generate_bezier_points(p3_b, p_arm_ctrl_b, p4_b)[1:-1] +
            [p4_b, p5_b] +
            generate_bezier_points(p5_b, p_neck_ctrl_b, p6_b)[1:-1] +
            [p6_b]
        )
        back_pts_plot_smooth = [(x + base_offset_x, y + base_offset_y) for x, y in back_pts_local_smooth]
        back_shape = patches.Polygon(back_pts_plot_smooth, edgecolor=piece_edgecolor, facecolor='lightgreen', lw=1.5)

        back_edges = [
            ('straight', [p1_b, p2_b]),
            ('straight', [p2_b, p3_b]),
            ('bezier', [p3_b, p_arm_ctrl_b, p4_b]),
            ('straight', [p4_b, p5_b]),
            ('bezier', [p5_b, p_neck_ctrl_b, p6_b])
        ]
        for edge in back_edges:
            if edge[0] == 'straight':
                p1 = (edge[1][0][0] + base_offset_x, edge[1][0][1] + base_offset_y)
                p2 = (edge[1][1][0] + base_offset_x, edge[1][1][1] + base_offset_y)
                draw_straight_seam_allowance(axs1[1], p1, p2)
            elif edge[0] == 'bezier':
                p0 = (edge[1][0][0] + base_offset_x, edge[1][0][1] + base_offset_y)
                p1 = (edge[1][1][0] + base_offset_x, edge[1][1][1] + base_offset_y)
                p2 = (edge[1][2][0] + base_offset_x, edge[1][2][1] + base_offset_y)
                draw_bezier_seam_allowance(axs1[1], p0, p1, p2)

        grainline_x_back = base_offset_x + 1
        grainline_y_start_back = base_offset_y + 1
        grainline_y_end_back = base_offset_y + m['garment_length'] - 1
        draw_grainline(axs1[1], grainline_x_back, grainline_y_start_back, grainline_y_end_back)

        max_y_point_local = find_max_y_bezier(p3_b, p_arm_ctrl_b, p4_b)
        max_y_point_plot = (max_y_point_local[0] + base_offset_x, max_y_point_local[1] + base_offset_y)
        draw_notch(axs1[1], max_y_point_plot, (0, 1))

        annotate_straight_edges(axs1[1], back_edges, base_offset_x, base_offset_y)

        fold_line_back = patches.Polygon([(base_offset_x, p1_b[1] + base_offset_y), (base_offset_x, p6_b[1] + base_offset_y)],
                                        edgecolor='darkgreen', linestyle='-.', lw=1.5)
        axs1[1].text(base_offset_x + 0.3, base_offset_y + m['garment_length'] / 2, "FOLD\nLINE",
                    ha='center', va='center', fontsize=8, rotation=90, color='darkgreen',
                    bbox=dict(boxstyle='round,pad=0.1', fc='white', alpha=0.5))
        
        back_neck_path = [p5_b, p_neck_ctrl_b, p6_b]
        half_back_neckline_length = get_path_length(back_neck_path)
        back_details = [
            "Cut 1 on Fold",
            f"HPS to Hem: {m['garment_length']:.1f}\"",
            f"Half Chest: {m['half_chest_flat']/2:.1f}\"",
            f"Half Back Neckline: {half_back_neckline_length:.2f}\""
        ]
        draw_pattern_piece_with_details(axs1[1], "2. Back Body", [back_shape, fold_line_back], back_details)

        # Front Body (Cut 1 Fabric)
        p_cf_neck = (0, m['garment_length'] - m['front_neck_drop'])
        p_hps_r = (m['neck_width_half'], m['garment_length'])
        p_st_r = (m['neck_width_half'] + dx_shoulder, m['garment_length'] - m['shoulder_slope'])
        p_au_r = (m['half_chest_flat'] / 2, m['garment_length'] - m['armhole_depth'])
        p_sh_r = (m['half_chest_flat'] / 2, 0)
        p_fn_ctrl_r = (m['neck_width_half'] * 0.4, p_cf_neck[1] + (p_hps_r[1] - p_cf_neck[1]) * 0.3)
        p_fa_ctrl_r = ((p_st_r[0] + p_au_r[0])/2 + (m['half_chest_flat']/2 - (m['neck_width_half'] + dx_shoulder))*0.15,
                    (p_st_r[1] + p_au_r[1])/2 - m['armhole_depth'] * 0.05)

        front_polygon_pts_smooth = (
            [p_cf_neck] + generate_bezier_points(p_cf_neck, p_fn_ctrl_r, p_hps_r)[1:-1] +
            [p_hps_r, p_st_r] + generate_bezier_points(p_st_r, p_fa_ctrl_r, p_au_r)[1:-1] +
            [p_au_r, p_sh_r, (-p_sh_r[0], p_sh_r[1]), (-p_au_r[0], p_au_r[1])] +
            generate_bezier_points((-p_au_r[0], p_au_r[1]), (-p_fa_ctrl_r[0], p_fa_ctrl_r[1]), (-p_st_r[0], p_st_r[1]))[1:-1] +
            [(-p_st_r[0], p_st_r[1]), (-p_hps_r[0], p_hps_r[1])] +
            generate_bezier_points((-p_hps_r[0], p_hps_r[1]), (-p_fn_ctrl_r[0], p_fn_ctrl_r[1]), p_cf_neck)[1:-1]
        )
        front_plot_offset_x = base_offset_x + m['half_chest_flat'] / 2
        front_pts_plot_smooth = [(x + front_plot_offset_x, y + base_offset_y) for x, y in front_polygon_pts_smooth]
        front_shape = patches.Polygon(front_pts_plot_smooth, edgecolor=piece_edgecolor, facecolor='lightblue', lw=1.5)

        front_edges = [
            ('bezier', [p_cf_neck, p_fn_ctrl_r, p_hps_r]),
            ('straight', [p_hps_r, p_st_r]),
            ('bezier', [p_st_r, p_fa_ctrl_r, p_au_r]),
            ('straight', [p_au_r, p_sh_r]),
            ('straight', [p_sh_r, (-p_sh_r[0], p_sh_r[1])]),
            ('straight', [(-p_sh_r[0], p_sh_r[1]), (-p_au_r[0], p_au_r[1])]),
            ('bezier', [(-p_au_r[0], p_au_r[1]), (-p_fa_ctrl_r[0], p_fa_ctrl_r[1]), (-p_st_r[0], p_st_r[1])]),
            ('straight', [(-p_st_r[0], p_st_r[1]), (-p_hps_r[0], p_hps_r[1])]),
            ('bezier', [(-p_hps_r[0], p_hps_r[1]), (-p_fn_ctrl_r[0], p_fn_ctrl_r[1]), p_cf_neck])
        ]
        for edge in front_edges:
            if edge[0] == 'straight':
                p1 = (edge[1][0][0] + front_plot_offset_x, edge[1][0][1] + base_offset_y)
                p2 = (edge[1][1][0] + front_plot_offset_x, edge[1][1][1] + base_offset_y)
                draw_straight_seam_allowance(axs1[0], p1, p2)
            elif edge[0] == 'bezier':
                p0 = (edge[1][0][0] + front_plot_offset_x, edge[1][0][1] + base_offset_y)
                p1 = (edge[1][1][0] + front_plot_offset_x, edge[1][1][1] + base_offset_y)
                p2 = (edge[1][2][0] + front_plot_offset_x, edge[1][2][1] + base_offset_y)
                draw_bezier_seam_allowance(axs1[0], p0, p1, p2)

        grainline_x_front = front_plot_offset_x
        grainline_y_start_front = base_offset_y + 1
        grainline_y_end_front = base_offset_y + m['garment_length'] - 1
        draw_grainline(axs1[0], grainline_x_front, grainline_y_start_front, grainline_y_end_front)

        v = (p_fn_ctrl_r[0] - p_cf_neck[0], p_fn_ctrl_r[1] - p_cf_neck[1])
        length_v = math.sqrt(v[0]**2 + v[1]**2)
        n = (-v[1] / length_v, v[0] / length_v) if length_v > 0 else (1, 0)
        p_cf_neck_plot = (p_cf_neck[0] + front_plot_offset_x, p_cf_neck[1] + base_offset_y)
        draw_notch(axs1[0], p_cf_neck_plot, n)
        max_y_point_local = find_max_y_bezier(p_st_r, p_fa_ctrl_r, p_au_r)
        max_y_point_plot = (max_y_point_local[0] + front_plot_offset_x, max_y_point_local[1] + base_offset_y)
        draw_notch(axs1[0], max_y_point_plot, (0, 1))

        annotate_straight_edges(axs1[0], front_edges, front_plot_offset_x, base_offset_y)

        placket_w, placket_l = m['placket_width'], m['placket_length']
        placket_indicator_x = p_cf_neck[0] + front_plot_offset_x - placket_w / 2
        placket_indicator_y = p_cf_neck[1] + base_offset_y - placket_l
        placket_area_indicator = patches.Rectangle((placket_indicator_x, placket_indicator_y),
                                                placket_w, placket_l, edgecolor='red', facecolor='none', linestyle='--', lw=1)
        
        front_neck_path_right = [p_cf_neck, p_fn_ctrl_r, p_hps_r]
        half_front_neckline_length = get_path_length(front_neck_path_right)
        front_details = [
            "Cut 1 Fabric",
            f"HPS to Hem: {m['garment_length']:.1f}\"",
            f"Chest Width: {m['half_chest_flat']:.1f}\"",
            f"Half Front Neckline: {half_front_neckline_length:.2f}\""
        ]
        draw_pattern_piece_with_details(axs1[0], "1. Front Body", [front_shape, placket_area_indicator], front_details)

        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.savefig('pattern_page1.png')
        logger.info("Page 1 saved as pattern_page1.png")
        try:
            plt.show()
        except Exception as e:
            logger.warning(f"Failed to display Page 1: {e}")
        plt.close(fig1)

        # Calculate collar length
        m['collar_length_calculated'] = (half_back_neckline_length + half_front_neckline_length) * 2
        logger.info(f"Calculated Collar Length: {m['collar_length_calculated']:.2f}\"")

        # Page 2: Sleeves and Collars
        logger.info("Generating Page 2: Sleeves & Collars")
        fig2, axs2 = plt.subplots(2, 2, figsize=(12, 10))
        fig2.suptitle(f"Polo Shirt - Size {size_name} - Page 2/3: Sleeves & Collars", fontsize=14)

        # Sleeve
        sL, sWB, sWC = m['sleeve_length_outer'], m['sleeve_bicep_flat'], m['sleeve_cuff_flat']
        cap_height = sL * 0.25
        underarm_length = sL - cap_height
        if sWC > sWB:
            sWC = sWB
        plot_sleeve_offset_x, plot_sleeve_offset_y = base_offset_x, base_offset_y
        p1_cuff_left = (plot_sleeve_offset_x + (sWB - sWC) / 2, plot_sleeve_offset_y)
        p2_cuff_right = (plot_sleeve_offset_x + (sWB - sWC) / 2 + sWC, plot_sleeve_offset_y)
        p5_underarm_left = (plot_sleeve_offset_x, plot_sleeve_offset_y + underarm_length)
        p3_underarm_right = (plot_sleeve_offset_x + sWB, plot_sleeve_offset_y + underarm_length)
        cap_peak_x = plot_sleeve_offset_x + sWB / 2
        cap_peak_y = plot_sleeve_offset_y + sL
        p_carrier_left = (plot_sleeve_offset_x + sWB * 0.1, plot_sleeve_offset_y + underarm_length + cap_height * 0.5)
        p_carrier_right = (plot_sleeve_offset_x + sWB * 0.9, plot_sleeve_offset_y + underarm_length + cap_height * 0.5)
        sleeve_pts_smooth = (
            [p1_cuff_left, p2_cuff_right, p3_underarm_right] +
            generate_bezier_points(p3_underarm_right, p_carrier_right, (cap_peak_x, cap_peak_y))[1:-1] +
            [(cap_peak_x, cap_peak_y)] +
            generate_bezier_points((cap_peak_x, cap_peak_y), p_carrier_left, p5_underarm_left)[1:-1] +
            [p5_underarm_left]
        )
        sleeve_patch_1 = patches.Polygon(sleeve_pts_smooth, edgecolor=piece_edgecolor, facecolor='thistle', lw=1.5)
        sleeve_patch_2 = patches.Polygon(sleeve_pts_smooth, edgecolor=piece_edgecolor, facecolor='thistle', lw=1.5)

        sleeve_edges = [
            ('straight', [p1_cuff_left, p2_cuff_right]),
            ('straight', [p2_cuff_right, p3_underarm_right]),
            ('bezier', [p3_underarm_right, p_carrier_right, (cap_peak_x, cap_peak_y)]),
            ('bezier', [(cap_peak_x, cap_peak_y), p_carrier_left, p5_underarm_left]),
            ('straight', [p5_underarm_left, p1_cuff_left])
        ]
        for ax in [axs2[0, 0], axs2[0, 1]]:
            for edge in sleeve_edges:
                if edge[0] == 'straight':
                    draw_straight_seam_allowance(ax, edge[1][0], edge[1][1])
                elif edge[0] == 'bezier':
                    draw_bezier_seam_allowance(ax, edge[1][0], edge[1][1], edge[1][2])
            annotate_straight_edges(ax, sleeve_edges, 0, 0)

        sleeve_details = [
            "Cut 2 Fabric",
            f"Length: {sL:.1f}\"",
            f"Bicep (flat): {sWB:.1f}\"",
            f"Cuff (flat): {sWC:.1f}\"",
            "Sleeve cap to be refined"
        ]
        draw_pattern_piece_with_details(axs2[0, 0], "3. Sleeve (Piece 1)", sleeve_patch_1, sleeve_details)
        draw_pattern_piece_with_details(axs2[0, 1], "4. Sleeve (Piece 2)", sleeve_patch_2, sleeve_details)

        # Collar
        collar_l, collar_h = m['collar_length_calculated'], m['collar_height_flat']
        collar_shape_1 = patches.Rectangle((base_offset_x, base_offset_y), collar_l, collar_h,
                                        edgecolor=piece_edgecolor, facecolor='moccasin', lw=1.5)
        collar_shape_2 = patches.Rectangle((base_offset_x, base_offset_y), collar_l, collar_h,
                                        edgecolor=piece_edgecolor, facecolor='moccasin', lw=1.5)
        collar_fold_1 = patches.Polygon([(base_offset_x, base_offset_y + collar_h / 2), (base_offset_x + collar_l, base_offset_y + collar_h / 2)],
                                        edgecolor='orange', linestyle='--', lw=1)
        collar_fold_2 = patches.Polygon([(base_offset_x, base_offset_y + collar_h / 2), (base_offset_x + collar_l, base_offset_y + collar_h / 2)],
                                        edgecolor='orange', linestyle='--', lw=1)
        for ax, shape in zip([axs2[1, 0], axs2[1, 1]], [collar_shape_1, collar_shape_2]):
            draw_straight_seam_allowance(ax, (base_offset_x, base_offset_y), (base_offset_x + collar_l, base_offset_y))
            draw_straight_seam_allowance(ax, (base_offset_x + collar_l, base_offset_y), (base_offset_x + collar_l, base_offset_y + collar_h))
            draw_straight_seam_allowance(ax, (base_offset_x + collar_l, base_offset_y + collar_h), (base_offset_x, base_offset_y + collar_h))
            draw_straight_seam_allowance(ax, (base_offset_x, base_offset_y + collar_h), (base_offset_x, base_offset_y))
            annotate_rectangle_dimensions(ax, base_offset_x, base_offset_y, collar_l, collar_h)
        
        collar_details = [
            "Cut 2 Fabric, Cut 1 Interfacing",
            f"Length: {collar_l:.2f}\"",
            f"Height: {collar_h:.1f}\""
        ]
        draw_pattern_piece_with_details(axs2[1, 0], "5. Collar (Piece 1)", [collar_shape_1, collar_fold_1], collar_details)
        draw_pattern_piece_with_details(axs2[1, 1], "6. Collar (Piece 2)", [collar_shape_2, collar_fold_2], collar_details)
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.savefig('pattern_page2.png')
        logger.info("Page 2 saved as pattern_page2.png")
        try:
            plt.show()
        except Exception as e:
            logger.warning(f"Failed to display Page 2: {e}")
        plt.close(fig2)

        # Page 3: Plackets and Interfacing
        logger.info("Generating Page 3: Plackets & Interfacing")
        fig3, axs3 = plt.subplots(2, 2, figsize=(12, 10))
        fig3.suptitle(f"Polo Shirt - Size {size_name} - Page 3/3: Plackets & Interfacing", fontsize=14)

        placket_w, placket_l = m['placket_width'], m['placket_length']
        placket_shape_1 = patches.Rectangle((base_offset_x, base_offset_y), placket_w, placket_l,
                                            edgecolor=piece_edgecolor, facecolor='sandybrown', lw=1.5)
        placket_shape_2 = patches.Rectangle((base_offset_x, base_offset_y), placket_w, placket_l,
                                            edgecolor=piece_edgecolor, facecolor='sandybrown', lw=1.5)
        buttons = []
        num_buttons = 3
        if placket_l > 1 and placket_w > 0.2:
            button_spacing = placket_l / (num_buttons + 1)
            button_radius = min(placket_w * 0.15, 0.18)
            for i in range(num_buttons):
                button_y = base_offset_y + (i + 1) * button_spacing
                button_x = base_offset_x + placket_w / 2
                buttons.append(patches.Circle((button_x, button_y), button_radius, edgecolor='black', facecolor='darkgrey'))
        
        for ax, shape in zip([axs3[0, 0], axs3[0, 1]], [placket_shape_1, placket_shape_2]):
            draw_straight_seam_allowance(ax, (base_offset_x, base_offset_y), (base_offset_x + placket_w, base_offset_y))
            draw_straight_seam_allowance(ax, (base_offset_x + placket_w, base_offset_y), (base_offset_x + placket_w, base_offset_y + placket_l))
            draw_straight_seam_allowance(ax, (base_offset_x + placket_w, base_offset_y + placket_l), (base_offset_x, base_offset_y + placket_l))
            draw_straight_seam_allowance(ax, (base_offset_x, base_offset_y + placket_l), (base_offset_x, base_offset_y))
            annotate_rectangle_dimensions(ax, base_offset_x, base_offset_y, placket_w, placket_l)
        
        placket_details_buttons = [
            "Cut 2 Fabric", "Cut 1-2 Interfacing",
            f"Piece: {placket_w:.1f}\" x {placket_l:.1f}\""
        ]
        draw_pattern_piece_with_details(axs3[0, 0], "7. Placket (Button Side)", [placket_shape_1] + buttons, placket_details_buttons)
        draw_pattern_piece_with_details(axs3[0, 1], "8. Placket (Buttonhole Side)", placket_shape_2, placket_details_buttons)

        interfacing_collar_shape = patches.Rectangle((base_offset_x, base_offset_y), collar_l, collar_h,
                                                    edgecolor='dimgray', facecolor='lightgray', lw=1, alpha=interfacing_alpha)
        interfacing_placket_shape = patches.Rectangle((base_offset_x, base_offset_y), placket_w, placket_l,
                                                    edgecolor='dimgray', facecolor='lightgray', lw=1, alpha=interfacing_alpha)
        for ax, shape in zip([axs3[1, 0], axs3[1, 1]], [interfacing_collar_shape, interfacing_placket_shape]):
            annotate_rectangle_dimensions(ax, base_offset_x, base_offset_y, collar_l if shape == interfacing_collar_shape else placket_w,
                                        collar_h if shape == interfacing_collar_shape else placket_l)
        
        interfacing_details = [
            "Cut 1 Interfacing",
            f"Collar: {collar_l:.2f}\" x {collar_h:.1f}\"",
            f"Placket: {placket_w:.1f}\" x {placket_l:.1f}\""
        ]
        draw_pattern_piece_with_details(axs3[1, 0], "9. Collar Interfacing", interfacing_collar_shape, interfacing_details)
        draw_pattern_piece_with_details(axs3[1, 1], "10. Placket Interfacing", interfacing_placket_shape, interfacing_details)
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.savefig('pattern_page3.png')
        logger.info("Page 3 saved as pattern_page3.png")
        try:
            plt.show()
        except Exception as e:
            logger.warning(f"Failed to display Page 3: {e}")
        plt.close(fig3)
    except Exception as e:
        logger.error(f"Error in generate_pattern_visuals: {e}")
        raise

def output_product_details(size_name, measurements):
    """Print final garment dimensions in cm."""
    try:
        m = measurements
        print(f"\nProduct Details for Size {size_name}:")
        print("Approximate finished garment dimensions in cm:")
        print(f"Chest (circumference): {2 * m['half_chest_flat'] * IN_TO_CM:.1f} cm")
        print(f"Length (HPS to hem): {m['garment_length'] * IN_TO_CM:.1f} cm")
        print(f"Sleeve Length: {m['sleeve_length_outer'] * IN_TO_CM:.1f} cm")
        print(f"Bicep (circumference): {2 * m['sleeve_bicep_flat'] * IN_TO_CM:.1f} cm")
        print(f"Cuff (circumference): {2 * m['sleeve_cuff_flat'] * IN_TO_CM:.1f} cm")
        if 'collar_length_calculated' in m:
            print(f"Collar Opening: {m['collar_length_calculated'] * IN_TO_CM:.1f} cm")
    except Exception as e:
        logger.errormapsto(f"Error in output_product_details: {e}")
        raise

if __name__ == '__main__':
    try:
        logger.info("Starting Polo Shirt Pattern Generator")
        print("Welcome to the Enhanced Polo Shirt Pattern Generator!")
        selected_size, final_measurements = get_user_measurements()
        if final_measurements:
            print("\nGenerating patterns... Check for PNG files: pattern_page1.png, pattern_page2.png, pattern_page3.png")
            generate_pattern_visuals(selected_size, final_measurements)
            output_product_details(selected_size, final_measurements)
            print("\nPattern generation complete.")
        else:
            print("Pattern generation exited.")
    except Exception as e:
        logger.error(f"Main execution failed: {e}")
        print("An error occurred. Check the log for details.")
