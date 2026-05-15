import importlib
import importlib.metadata
import importlib.util


def check_dependency(name: str, description: str) -> bool:
    if importlib.util.find_spec(name) is not None:
        print(
            f"[OK] {name} ({importlib.metadata.version(name)}) - {description}")
        return True
    print(f"[MISSING] {name} - {description}")
    return False


if __name__ == "__main__":
    print("LOADING STATUS: Loading programs...")
    print("Checking dependencies:")
    ok = True
    ok = check_dependency("pandas", "Data manipulation ready") and ok
    ok = check_dependency("numpy", "Numerical computation ready") and ok
    ok = check_dependency("matplotlib", "Visualization ready") and ok
    check_dependency("requests", "Network access ready")
    if ok:
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
        print("Analyzing Matrix data...")
        data = np.random.randn(1000)
        df = pd.DataFrame(data, columns=["matrix_signal"])
        print("Processing 1000 data points...")
        print("Generating visualization...")
        plt.figure()
        df.plot()
        plt.savefig("matrix_analysis.png")
        plt.close()
        print("Analysis complete!")
        print("Results saved to: matrix_analysis.png")
    else:
        print("To install with pip: pip install -r requirements.txt")
        print("To install with Poetry: poetry install")
