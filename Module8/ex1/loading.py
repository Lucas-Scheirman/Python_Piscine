import importlib
import importlib.metadata
import importlib.util


def check_dependency(name: str, description: str) -> bool:
    if importlib.util.find_spec(name) is not None:
        version = importlib.metadata.version(name)
        print(f"[OK] {name} ({version}) - {description}")
        return True
    print(f"[MISSING] {name} - {description}")
    return False


def compare_managers() -> None:
    print("\nDependency management (pip vs Poetry):")
    print("  pip    -> requirements.txt | exact pins '==' "
          "| pip install -r requirements.txt")
    print("  Poetry -> pyproject.toml + poetry.lock | ranges '^' "
          "| poetry install")


if __name__ == "__main__":
    print("LOADING STATUS: Loading programs...\n")
    print("Checking dependencies:")
    ok = True
    ok = check_dependency("pandas", "Data manipulation ready") and ok
    ok = check_dependency("numpy", "Numerical computation ready") and ok
    ok = check_dependency("matplotlib", "Visualization ready") and ok
    compare_managers()
    if ok:
        try:
            import numpy as np
            import pandas as pd
            import matplotlib.pyplot as plt
            print("\nAnalyzing Matrix data...")
            data = np.random.randn(1000)
            df = pd.DataFrame(data, columns=["matrix_signal"])
            print("Processing 1000 data points...")
            print("Generating visualization...")
            plt.figure()
            df.plot()
            plt.savefig("matrix_analysis.png")
            plt.close()
            print("\nAnalysis complete!")
            print("Results saved to: matrix_analysis.png")
        except Exception as error:
            print(f"Analysis failed: {error}")
    else:
        print("\nTo install with pip: pip install -r requirements.txt")
        print("To install with Poetry: poetry install")
