from pathlib import Path

import pandas as pd
import os

app_dir = Path(__file__).parent
df = pd.read_csv(os.path.join(app_dir, "data", "ofm-estimates.csv"))
# tips = pd.read_csv(app_dir / "tips.csv")
