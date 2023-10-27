# Observation Space Configuration
FIELD_LENGTH = 12
FIELD_WIDTH = 8.25

RANDOMIZE_INITIAL_POSITIONS_PLAYERS = True
RANDOMIZE_INITIAL_POSITIONS_BALL = True

RADIUS_PLAYER = 0.365
RADIUS_BALL = 0.215

# Sphero Bolt and Soccer Ball Specs - API
# Useful for scaling ENV values to API values
BOLT_MIN_SPEED = 0
BOLT_MAX_SPEED = 255
BOLT_MIN_ROTATION = 0
BOLT_MAX_ROTATION = 359
BOLT_MASS = 200

BALL_MIN_SPEED = 0
BALL_MAX_SPEED = 20000 # derived from the momentum conservation equation
BALL_MIN_ROTATION = 0
BALL_MAX_ROTATION = 359
BALL_MASS = 2.77

# Sphero Bolt Specs - MuJoCo
ENV_BOLT_MIN_SPEED = 0	# Min 0 unit/sec
ENV_BOLT_MAX_SPEED = 20 # Max 20 unit/sec
ENV_BOLT_MIN_ROTATION = 0
ENV_BOLT_MAX_ROTATION = 359
ENV_BOLT_MASS = 200

# Soccer Ball Specs - MuJoCo
ENV_BALL_MIN_SPEED = 0
ENV_BALL_MAX_SPEED = 1500 # derived from the momentum conservation equation
ENV_BALL_MIN_ROTATION = 0
ENV_BALL_MAX_ROTATION = 359
ENV_BALL_MASS = 2.77

TEAM_HOME = "HOME_TEAM"  # blue players
TEAM_AWAY = "AWAY_TEAM"  # red players
NAME_BALL = "ball"

ENV_1A_0D_0K = "Environment_1A_0D_0K"

# Goal Positions
GOAL_HOME = [-FIELD_LENGTH / 2, -FIELD_WIDTH / 2]
GOAL_AWAY = [FIELD_LENGTH / 2, FIELD_WIDTH / 2]

# Checkpoint Directories
DDPG_CHKPT_DIR = "AI/DDPG/saved_models/"