import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from model.shoe import Shoe
from utils.logger import logger

def main():
    shoe = Shoe(6, 0.75)
    logger.info("Shoe Created")
    
if __name__ == "__main__":
    main()
