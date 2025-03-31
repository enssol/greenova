"""
Custom pylint plugin to ensure good_names attribute is available for pylint-django.
This prevents the AttributeError in pylint_django/plugin.py.
"""
from pylint.checkers import BaseChecker
<<<<<<< HEAD
=======
from pylint.interfaces import IAstroidChecker
>>>>>>> 0294b58 (refactor(project): implement comprehensive project enhancements)


def register(linter):
    """Register the plugin with pylint."""
    # This plugin needs to run before pylint_django
    linter.register_checker(GoodNamesInitializer(linter))


class GoodNamesInitializer(BaseChecker):
    """Pylint checker that ensures the good_names attribute exists."""

<<<<<<< HEAD
=======
    __implements__ = IAstroidChecker

>>>>>>> 0294b58 (refactor(project): implement comprehensive project enhancements)
    name = 'good-names-initializer'
    priority = -1  # Run early

    # Required by pylint's BaseChecker
    msgs = {}
    options = ()
<<<<<<< HEAD
=======
    reports = ()
>>>>>>> 0294b58 (refactor(project): implement comprehensive project enhancements)

    def __init__(self, linter):
        """Initialize the checker with the given linter."""
        super().__init__(linter)

        # Ensure good_names exists in the config
<<<<<<< HEAD
        if not hasattr(linter.config, 'good_names') or linter.config.good_names is None:
=======
        if not hasattr(linter.config, 'good_names'):
            linter.config.good_names = ('_',)
        elif linter.config.good_names is None:
>>>>>>> 0294b58 (refactor(project): implement comprehensive project enhancements)
            linter.config.good_names = ('_',)

    def open(self):
        """Called before visiting any modules."""
        pass

    def close(self):
        """Called after visiting all modules."""
        pass
