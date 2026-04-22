import argparse
import pandas as pd
import numpy as np


def augment(df, n_sensors=3, lat_range=None, lon_range=None, seed=None):
    rng = np.random.default_rng(seed)

    if lat_range is None:
        lat_min, lat_max = -90.0, 90.0
    else:
        lat_min, lat_max = lat_range

    if lon_range is None:
        lon_min, lon_max = -180.0, 180.0
    else:
        lon_min, lon_max = lon_range

    df = df.copy()
    df["latitude"] = rng.uniform(lat_min, lat_max, size=len(df))
    df["longitude"] = rng.uniform(lon_min, lon_max, size=len(df))

    # derive a base value to seed sensor readings
    if "sensor_activity" in df.columns:
        base = pd.to_numeric(df["sensor_activity"], errors="coerce").fillna(0).to_numpy()
    elif "threat_level" in df.columns:
        base = pd.to_numeric(df["threat_level"], errors="coerce").fillna(0).to_numpy() * 10
    else:
        base = np.full(len(df), 10.0)

    for i in range(1, n_sensors + 1):
        noise = rng.normal(loc=0.0, scale=5.0, size=len(df))
        df[f"sensor_{i}"] = np.clip(base + noise + rng.normal(0, 1.0, len(df)) * i, 0, None)

    return df


def main():
    p = argparse.ArgumentParser(description="Augment defense data with lat/lon and simulated sensors")
    p.add_argument("--input", "-i", required=True, help="Input CSV path")
    p.add_argument("--output", "-o", required=True, help="Output CSV path")
    p.add_argument("--sensors", "-s", type=int, default=3, help="Number of simulated sensors to add")
    p.add_argument("--lat-min", type=float, help="Minimum latitude for random generation")
    p.add_argument("--lat-max", type=float, help="Maximum latitude for random generation")
    p.add_argument("--lon-min", type=float, help="Minimum longitude for random generation")
    p.add_argument("--lon-max", type=float, help="Maximum longitude for random generation")
    p.add_argument("--seed", type=int, help="Random seed for reproducibility")

    args = p.parse_args()

    df = pd.read_csv(args.input)

    lat_range = None
    lon_range = None
    if args.lat_min is not None and args.lat_max is not None:
        lat_range = (args.lat_min, args.lat_max)
    if args.lon_min is not None and args.lon_max is not None:
        lon_range = (args.lon_min, args.lon_max)

    out = augment(df, n_sensors=args.sensors, lat_range=lat_range, lon_range=lon_range, seed=args.seed)
    out.to_csv(args.output, index=False)
    print(f"Saved augmented data to {args.output}")


if __name__ == "__main__":
    main()
