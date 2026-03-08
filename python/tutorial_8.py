import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import math
import heapq


def calculate_distance(node1, node2):
    """Calculate Euclidean distance between two nodes (lat, lon)."""
    return math.sqrt((node1[0] - node2[0]) ** 2 + (node1[1] - node2[1]) ** 2)


def main():
    osm_file = "data/poruba.osm"

    # 1. Parse OSM file
    print(f"Parsing {osm_file}...")
    tree = ET.parse(osm_file)
    root = tree.getroot()

    # 2. Extract nodes
    nodes = {}  # id -> (lat, lon)
    for node in root.findall("node"):
        node_id = node.get("id")
        lat_str = node.get("lat")
        lon_str = node.get("lon")
        # skip any malformed entries
        if node_id is None or lat_str is None or lon_str is None:
            continue
        lat = float(lat_str)
        lon = float(lon_str)
        nodes[node_id] = (lat, lon)

    # 3. Extract ways and build graph
    graph = {}  # node_id -> list of (neighbor_id, distance)
    all_roads = []  # list of node_id sequences for visualization

    # Target street search
    polska_nodes = set()
    vietnamska_nodes = set()

    for way in root.findall("way"):
        way_node_ids = [
            nd.get("ref") for nd in way.findall("nd") if nd.get("ref") in nodes
        ]
        if not way_node_ids:
            continue

        tags = {tag.get("k"): tag.get("v") for tag in way.findall("tag")}
        highway = tags.get("highway")
        # tags.get() may return None; coalesce to empty string for safe membership tests
        name: str = tags.get("name") or ""

        # Collect nodes for target streets
        if "Polská" in name:
            polska_nodes.update(way_node_ids)
        if "Vietnamská" in name:
            vietnamska_nodes.update(way_node_ids)

        # Filter relevant roads for navigation (primary, secondary, residential)
        if highway in ["primary", "secondary", "residential"]:
            all_roads.append(way_node_ids)

            # Add to graph
            for i in range(len(way_node_ids) - 1):
                u, v = way_node_ids[i], way_node_ids[i + 1]
                dist = calculate_distance(nodes[u], nodes[v])

                if u not in graph:
                    graph[u] = []
                if v not in graph:
                    graph[v] = []

                # OSM ways are usually two-way unless specified
                graph[u].append((v, dist))
                graph[v].append((u, dist))

    # 4. Find Start and End Nodes
    # End: Intersection of Polská and Vietnamská
    intersection = polska_nodes.intersection(vietnamska_nodes)
    if intersection:
        end_node = list(intersection)[0]
    else:
        # Fallback: search for closest nodes if no direct intersection
        end_node = list(polska_nodes)[0] if polska_nodes else None
        print(
            "Warning: Direct intersection of Polská and Vietnamská not found in ways. Using fallback."
        )

    # Start: Near FEI (approx 49.8308, 18.1628)
    fei_target = (49.8308, 18.1628)
    start_node = min(
        graph.keys(), key=lambda n: calculate_distance(nodes[n], fei_target)
    )

    if not start_node or not end_node:
        print("Error: Could not find start or end nodes.")
        return

    print(f"Start Node: {start_node} at {nodes[start_node]}")
    print(f"End Node: {end_node} at {nodes[end_node]}")

    # 5. Dijkstra's Algorithm
    print("Running Dijkstra's algorithm...")
    distances = {node: float("inf") for node in graph}
    previous = {node: None for node in graph}
    distances[start_node] = 0
    pq = [(0, start_node)]

    while pq:
        curr_dist, u = heapq.heappop(pq)

        if u == end_node:
            break

        if curr_dist > distances[u]:
            continue

        for v, weight in graph.get(u, []):
            new_dist = curr_dist + weight
            if new_dist < distances[v]:
                distances[v] = new_dist
                previous[v] = u
                heapq.heappush(pq, (new_dist, v))

    # 6. Reconstruct Path
    path = []
    curr = end_node
    while curr:
        path.append(curr)
        curr = previous[curr]
    path.reverse()

    if len(path) < 2:
        print("Error: No path found.")
    else:
        print(f"Path found with {len(path)} nodes.")

    # 7. Visualization
    print("Visualizing...")
    plt.figure(figsize=(12, 12))

    # Draw all roads
    for road_ids in all_roads:
        road_coords = [nodes[nid] for nid in road_ids]
        lats, lons = zip(*road_coords)
        plt.plot(lons, lats, color="gray", linewidth=0.5, alpha=0.5)

    # Draw Dijkstra path
    if len(path) >= 2:
        path_coords = [nodes[nid] for nid in path]
        p_lats, p_lons = zip(*path_coords)
        plt.plot(
            p_lons, p_lats, color="red", linewidth=3, label="Shortest Path", zorder=10
        )

    # Mark start and end
    plt.scatter(
        nodes[start_node][1],
        nodes[start_node][0],
        color="green",
        s=100,
        label="Start (FEI)",
        zorder=11,
    )
    plt.scatter(
        nodes[end_node][1],
        nodes[end_node][0],
        color="blue",
        s=100,
        label="End (Intersection)",
        zorder=11,
    )

    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title("Dijkstra Navigation - Poruba (Tutorial 8)")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.7)

    output_png = "data/tutorial_8_result.png"
    plt.savefig(output_png, dpi=300)
    print(f"Result saved to {output_png}")
    plt.show()


if __name__ == "__main__":
    main()
