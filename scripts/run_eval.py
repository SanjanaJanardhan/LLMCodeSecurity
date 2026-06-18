import sys
sys.path.insert(0, '.')

from cweval.evaluate import Evaler
import fire

if __name__ == '__main__':
    fire.Fire(Evaler)