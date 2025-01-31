import os
import dill

from collections import OrderedDict
from .AgentInteractionManager import AgentInteractionManager

# NOTE: if someone knows how to fix this, please do it :D
import warnings
warnings.filterwarnings("ignore", category=dill.PicklingWarning)



class CheckpointManager:
    """
    A singleton class for managing simulation checkpoints, allowing saving and loading of simulation states.

    This class provides functionality to:
    - Save the complete state of a simulation to disk
    - Load a previously saved simulation state
    """

    _instance = None

    def __new__(cls, name: str = None):
        """
        Create or return the singleton instance of Checkpoint.

        Args:
            name (str): Name of the checkpoint
        """
        if cls._instance is None:
            cls._instance = super(CheckpointManager, cls).__new__(cls)
            cls._instance._initialized = False
        elif name and name != cls._instance.name:
            # Allow only one instance of CheckpointManager
            raise RuntimeError(f"CheckpointManager instance already exists with a different name: {name}")
        return cls._instance

    def __init__(self, name: str = "default"):
        """
        Initialize the checkpoint manager (only runs once for the singleton).

        Args:
            name (str): Name of the checkpoint
        """

        if self._initialized:
            return

        self.name = name
        self.path = f"{self.name}.dill"

        self._interaction_manager = AgentInteractionManager()

        self._action_idx = 0
        self.recorded_actions = []

        if name and os.path.exists(self.path):
            self.load()

        self._initialized = True

    def save(self) -> None:
        """
        Save the current state of a simulation.
        """

        dill.dump({"actions": self.recorded_actions}, open(self.path, "wb"), byref=True)

    def load(self) -> None:
        """
        Load a simulation from a checkpoint.
        """

        env_data = dill.load(open(self.path, "rb"))

        self.recorded_actions = env_data["actions"]
