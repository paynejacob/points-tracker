from points_tracker import app as App
from points_tracker.settings import get_config_for_current_environment

app = App.create_app(get_config_for_current_environment())
