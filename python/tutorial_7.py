import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt


def main():
    osm_file = "data/poruba.osm"

    # 1. Parse OSM file
    print(f"Parsing {osm_file}...")
    tree = ET.parse(osm_file)
    root = tree.getroot()

    # 2. Extract nodes: id -> (lat, lon)
    nodes = {}
    stops = []

    for node in root.findall("node"):
        node_id = node.get("id")
        lat_str = node.get("lat")
        lon_str = node.get("lon")

        if lat_str is None or lon_str is None:
            continue

        lat = float(lat_str)
        lon = float(lon_str)
        nodes[node_id] = (lat, lon)

        # Check if it's a public transport stop
        is_stop = False
        for tag in node.findall("tag"):
            k = tag.get("k")
            v = tag.get("v")
            if (k == "public_transport" and v == "stop_position") or (
                k == "highway" and v == "bus_stop"
            ):
                is_stop = True
                break

        if is_stop:
            stops.append((lat, lon))

    # 3. Extract ways: residential and secondary roads
    secondary_roads = []
    residential_roads = []

    for way in root.findall("way"):
        way_nodes = []
        for nd in way.findall("nd"):
            ref = nd.get("ref")
            if ref in nodes:
                way_nodes.append(nodes[ref])

        if not way_nodes:
            continue

        # Check road type
        highway_type = None
        for tag in way.findall("tag"):
            if tag.get("k") == "highway":
                highway_type = tag.get("v")
                break

        if highway_type == "secondary":
            secondary_roads.append(way_nodes)
        elif highway_type == "residential":
            residential_roads.append(way_nodes)

    # 4. Visualize
    print("Visualizing data...")
    plt.figure(figsize=(12, 12))

    # Draw residential roads (blue)
    for road in residential_roads:
        lats, lons = zip(*road)
        plt.plot(
            lons,
            lats,
            color="blue",
            linewidth=0.8,
            alpha=0.6,
            label="Residential" if road == residential_roads[0] else "",
        )

    # Draw secondary roads (red)
    for road in secondary_roads:
        lats, lons = zip(*road)
        plt.plot(
            lons,
            lats,
            color="red",
            linewidth=1.5,
            alpha=0.8,
            label="Secondary" if road == secondary_roads[0] else "",
        )

    # Draw stops (green circles)
    if stops:
        stop_lats, stop_lons = zip(*stops)
        plt.scatter(
            stop_lons, stop_lats, color="green", s=20, label="MHD Stops", zorder=5
        )

    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title("OSM Vector Data - Poruba (Tutorial 7)")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.7)

    # Save the result
    output_png = 'data/tutorial_7_result.png'
    plt.savefig(output_png, dpi=300)
    print(f"Result saved to {output_png}")


    # Show plot
    plt.show()


if __name__ == "__main__":
    main()
