import os, sqlite3

# Create directory, if applicable
if not os.path.exists("chroma/logs/"):
    os.mkdir("chroma/logs/")

# Logging setup
connection = sqlite3.connect("chroma/logs/logs.db")
cursor = connection.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS `chatbot_log` (
    `request_id` integer PRIMARY KEY AUTOINCREMENT,
    `request_time` datetime DEFAULT NULL,
    `user_prompt` text DEFAULT NULL,
    `response` text DEFAULT NULL,
    `question` varchar(150) DEFAULT NULL,
    `level_` varchar(100) DEFAULT NULL,
    `year_` varchar(100) DEFAULT NULL,
    `college` varchar(100) DEFAULT NULL,
    `time_basis` varchar(100) DEFAULT NULL,
    `campus` varchar(100) DEFAULT NULL,
    `age` varchar(100) DEFAULT NULL,
    `residency` varchar(100) DEFAULT NULL,
    `living` varchar(100) DEFAULT NULL,
    `smart_devices` varchar(100) DEFAULT NULL
);""")
