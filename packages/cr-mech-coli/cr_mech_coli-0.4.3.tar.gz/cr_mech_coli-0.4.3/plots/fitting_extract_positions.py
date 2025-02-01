import cr_mech_coli as crm
import numpy as np
import cv2 as cv
from pathlib import Path
import matplotlib.pyplot as plt
from tqdm import tqdm

def calculate_lengths_distances(args) -> tuple[list, list, list]:
    cells_at_iteration, cell_container, colors, config = args
    mask = crm.render_mask(config, cells_at_iteration, colors)
    positions = np.array(crm.extract_positions(mask))

    distances_i = []
    lengths_i_1 = []
    lengths_i_2 = []
    for p in positions:
        color = mask[int(p[0][1]), int(p[0][0])]
        ident = cell_container.get_cell_from_color([*color])
        cell = cells_at_iteration[ident][0]
        q = cell.pos[:,:2]
        p = crm.convert_pixel_to_position(p, config.domain_size, mask.shape[:2])

        # Determine if we need to use the reverse order
        d1 = np.sum(np.sum((p-q)**2, axis=1)**0.5)
        d2 = np.sum(np.sum((p-q[::-1])**2, axis=1)**0.5)
        d = min(d1, d2) / len(p)
        distances_i.append(d)

        # Compare total length
        l1 = np.sum((p[1:] - p[:-1])**2)**0.5
        l2 = np.sum((q[1:] - q[:-1])**2)**0.5
        lengths_i_1.append(l1)
        lengths_i_2.append(l2)
    return distances_i, lengths_i_1, lengths_i_2

if __name__ == "__main__":
    config = crm.Configuration(
        t0=0.0,
        dt=0.1,
        t_max=200.0,
        save_interval=4.0,
        n_agents=4,
        domain_size=100,
    )
    agent_settings = crm.AgentSettings(
        growth_rate = 0.05,
    )
    agent_settings.mechanics.rigidity = 2.0
    config.domain_height = 0.2

    cell_container = crm.run_simulation(config, agent_settings)

    all_cells = cell_container.get_cells()
    iterations = cell_container.get_all_iterations()
    colors = cell_container.cell_to_color

    # Pick one iteration to plot results
    iter_masks = [
        (iterations[9], crm.render_mask(config, all_cells[iterations[9]], colors)),
        (iterations[19], crm.render_mask(config, all_cells[iterations[18]], colors)),
        (iterations[29], crm.render_mask(config, all_cells[iterations[29]], colors)),
        (iterations[39], crm.render_mask(config, all_cells[iterations[39]], colors)),
        (iterations[49], crm.render_mask(config, all_cells[iterations[49]], colors)),
    ]
    for iteration, mask in tqdm(iter_masks):
        positions = crm.extract_positions(mask)
        positions = np.round(np.array(positions))
        positions = np.array(positions, dtype=int).reshape((len(positions), -1, 1, 2))

        dl = 2**0.5 * config.domain_size
        domain_pixels = np.array(mask.shape[:2], dtype=float)
        pixel_per_length = domain_pixels / dl

        # Calculate differences in positions
        pos_exact = []
        for p1 in positions:
            # Get color
            color = mask[p1[0][0][1], p1[0][0][0]]
            ident = cell_container.get_cell_from_color([*color])
            cell = all_cells[iteration][ident][0]
            p1 = np.array(p1[:,0,:], dtype=float)
            p2 = crm.convert_cell_pos_to_pixels(cell.pos, config.domain_size, mask.shape[:2])
            pos_exact.append(p2)

        pos_exact = np.round(np.array(pos_exact)).reshape((len(pos_exact), -1, 1, 2))
        pos_exact = np.array(pos_exact, dtype=int)
        # mask = cv.polylines(mask, positions, False, (50, 50, 50), 2)
        mask = cv.polylines(mask, pos_exact, False, (150, 150, 150), 2)
        mask = cv.polylines(mask, pos_exact, False, (250, 250, 250), 1)
        for p in positions.reshape((-1, 2)):
            mask = cv.drawMarker(mask, p, (50, 50, 50), cv.MARKER_TILTED_CROSS, 14, 2)
        path = Path("docs/source/_static/fitting-methods/")
        cv.imwrite(
            filename=str(path / "extract_positions-{:06}.png".format(iteration)),
            img=mask[200:-200,200:-200],
        )

    arglist = [(all_cells[n_iter], cell_container, colors, config) for n_iter in iterations]
    results = [calculate_lengths_distances(a) for a in tqdm(arglist)]
    distances = [r[0] for r in results]
    lengths1 = [r[1] for r in results]
    lengths2 = [r[2] for r in results]

    fig, ax1 = plt.subplots()

    x = np.arange(len(distances)) * config.save_interval
    ax1.plot(
        x,
        [np.mean(li) for li in lengths1],
        # yerr=[np.std(li) for li in lengths1],
        linestyle="--",
        color="k",
        label="Average Rod Length (Fit)",
    )
    ax1.fill_between(
        x,
        y1=[np.mean(lengths1[i])-np.mean(distances[i]) for i in range(len(lengths1))],
        y2=[np.mean(lengths1[i])+np.mean(distances[i]) for i in range(len(lengths1))],
        alpha=0.3,
        color="gray",
        label="Average Vertex Difference",
    )
    ax1.plot(
        x,
        [np.mean(li) for li in lengths2],
        # yerr=[np.std(li) for li in lengths2],
        linestyle=":",
        color="k",
        label="Average Rod Length",
    )
    ax1.legend()
    ax1.set_ylabel("Length [µm]")
    ax1.set_xlabel("Time [min]")
    fig.tight_layout()
    fig.savefig("docs/source/_static/fitting-methods/displacement-calculations.png")
    plt.show()
