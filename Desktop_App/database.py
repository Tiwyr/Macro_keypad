import os
import sqlite3
from pathlib import Path


BUTTON_COUNT = 12
ENCODER_COUNT = 3
MAX_LAYER_COUNT = 4
ENCODER_ACTION_TYPES = ("counterclockwise", "clockwise")


def default_database_path() -> Path:
    """Return a per-user location for the application's SQLite database."""
    local_app_data = os.environ.get("LOCALAPPDATA")

    if local_app_data:
        data_folder = Path(local_app_data) / "MacroKeypad"
    else:
        data_folder = Path.home() / ".macro_keypad"

    return data_folder / "macro_keypad.db"


class Database:
    def __init__(self, path: str | Path | None = None):
        self.path = Path(path) if path is not None else default_database_path()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.initialize()

    def connect(self) -> sqlite3.Connection:
        """Open a connection with foreign-key support and named columns."""
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def initialize(self) -> None:
        """Create all tables if this is the first application launch."""
        with self.connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS profiles (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    name        TEXT NOT NULL UNIQUE,
                    created_at  TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at  TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS layers (
                    id           INTEGER PRIMARY KEY AUTOINCREMENT,
                    profile_id   INTEGER NOT NULL,
                    layer_index  INTEGER NOT NULL
                                 CHECK (layer_index BETWEEN 0 AND 3),
                    name         TEXT NOT NULL,
                    FOREIGN KEY (profile_id)
                        REFERENCES profiles(id) ON DELETE CASCADE,
                    UNIQUE (profile_id, layer_index)
                );

                CREATE TABLE IF NOT EXISTS buttons (
                    id             INTEGER PRIMARY KEY AUTOINCREMENT,
                    layer_id       INTEGER NOT NULL,
                    button_index   INTEGER NOT NULL
                                   CHECK (button_index BETWEEN 0 AND 11),
                    function_type  TEXT,
                    command        TEXT,
                    icon_data      BLOB,
                    FOREIGN KEY (layer_id)
                        REFERENCES layers(id) ON DELETE CASCADE,
                    UNIQUE (layer_id, button_index)
                );

                CREATE TABLE IF NOT EXISTS encoder_actions (
                    id             INTEGER PRIMARY KEY AUTOINCREMENT,
                    layer_id       INTEGER NOT NULL,
                    encoder_index  INTEGER NOT NULL
                                   CHECK (encoder_index BETWEEN 0 AND 2),
                    action_type    TEXT NOT NULL
                                   CHECK (
                                       action_type IN (
                                           'counterclockwise',
                                           'clockwise'
                                       )
                                   ),
                    function_type  TEXT,
                    command        TEXT,
                    FOREIGN KEY (layer_id)
                        REFERENCES layers(id) ON DELETE CASCADE,
                    UNIQUE (layer_id, encoder_index, action_type)
                );
                """
            )
            self._remove_obsolete_columns_and_actions(connection)

    def _remove_obsolete_columns_and_actions(
        self,
        connection: sqlite3.Connection,
    ) -> None:
        
        profile_columns = {
            row["name"]
            for row in connection.execute("PRAGMA table_info(profiles)")
        }


        encoder_schema_row = connection.execute(
            """
            SELECT sql
            FROM sqlite_master
            WHERE type = 'table' AND name = 'encoder_actions'
            """
        ).fetchone()
        encoder_schema = encoder_schema_row["sql"] if encoder_schema_row else ""

        if "'press'" in encoder_schema:
            connection.executescript(
                """
                DELETE FROM encoder_actions
                WHERE action_type = 'press';

                ALTER TABLE encoder_actions
                RENAME TO encoder_actions_with_press;

                CREATE TABLE encoder_actions (
                    id             INTEGER PRIMARY KEY AUTOINCREMENT,
                    layer_id       INTEGER NOT NULL,
                    encoder_index  INTEGER NOT NULL
                                   CHECK (encoder_index BETWEEN 0 AND 2),
                    action_type    TEXT NOT NULL
                                   CHECK (
                                       action_type IN (
                                           'counterclockwise',
                                           'clockwise'
                                       )
                                   ),
                    function_type  TEXT,
                    command        TEXT,
                    FOREIGN KEY (layer_id)
                        REFERENCES layers(id) ON DELETE CASCADE,
                    UNIQUE (layer_id, encoder_index, action_type)
                );

                INSERT INTO encoder_actions (
                    id,
                    layer_id,
                    encoder_index,
                    action_type,
                    function_type,
                    command
                )
                SELECT
                    id,
                    layer_id,
                    encoder_index,
                    action_type,
                    function_type,
                    command
                FROM encoder_actions_with_press;

                DROP TABLE encoder_actions_with_press;
                """
            )

        connection.execute("PRAGMA user_version = 2")

    def create_profile(self, name: str) -> int:
        """Create a profile with one empty layer and return its database ID."""
        name = name.strip()
        if not name:
            raise ValueError("A profile name cannot be empty.")

        try:
            with self.connect() as connection:
                cursor = connection.execute(
                    "INSERT INTO profiles (name) VALUES (?)",
                    (name,),
                )
                profile_id = cursor.lastrowid
                self._insert_layer(connection, profile_id, 0, "Layer 1")
        except sqlite3.IntegrityError as error:
            raise ValueError(f'A profile named "{name}" already exists.') from error

        return profile_id

    def add_layer(self, profile_id: int, name: str | None = None) -> int:
        """Add the next layer, including its empty button and encoder rows."""
        with self.connect() as connection:
            row = connection.execute(
                """
                SELECT COALESCE(MAX(layer_index), -1) + 1 AS next_index
                FROM layers
                WHERE profile_id = ?
                """,
                (profile_id,),
            ).fetchone()
            layer_index = row["next_index"]

            if layer_index >= MAX_LAYER_COUNT:
                raise ValueError(
                    f"A profile can contain at most {MAX_LAYER_COUNT} layers."
                )

            layer_name = name.strip() if name else f"Layer {layer_index + 1}"
            return self._insert_layer(
                connection,
                profile_id,
                layer_index,
                layer_name,
            )

    def delete_layer(self, layer_id: int) -> None:
        with self.connect() as connection:
            layer = connection.execute(
                """
                SELECT profile_id
                FROM layers
                WHERE id = ?
                """,
                (layer_id,),
            ).fetchone()

            if layer is None:
                raise ValueError("The requested layer does not exist.")

            profile_id = layer["profile_id"]

            layer_count = connection.execute(
                """
                SELECT COUNT(*) AS count
                FROM layers
                WHERE profile_id = ?
                """,
                (profile_id,),
            ).fetchone()["count"]

            if layer_count <= 1:
                raise ValueError("A profile must contain at least one layer.")

            connection.execute(
                "DELETE FROM layers WHERE id = ?",
                (layer_id,),
            )

            # Reassign layer_index values to 0, 1, 2...
            remaining_layers = connection.execute(
                """
                SELECT id
                FROM layers
                WHERE profile_id = ?
                ORDER BY layer_index
                """,
                (profile_id,),
            ).fetchall()

            for new_index, remaining_layer in enumerate(remaining_layers):
                connection.execute(
                    """
                    UPDATE layers
                    SET layer_index = ?
                    WHERE id = ?
                    """,
                    (new_index, remaining_layer["id"]),
                )

            connection.execute(
                """
                UPDATE profiles
                SET updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (profile_id,),
            )

    def _insert_layer(
        self,
        connection: sqlite3.Connection,
        profile_id: int,
        layer_index: int,
        name: str,
    ) -> int:
        cursor = connection.execute(
            """
            INSERT INTO layers (profile_id, layer_index, name)
            VALUES (?, ?, ?)
            """,
            (profile_id, layer_index, name),
        )
        layer_id = cursor.lastrowid

        connection.executemany(
            """
            INSERT INTO buttons (layer_id, button_index)
            VALUES (?, ?)
            """,
            ((layer_id, button_index) for button_index in range(BUTTON_COUNT)),
        )

        connection.executemany(
            """
            INSERT INTO encoder_actions (
                layer_id,
                encoder_index,
                action_type
            )
            VALUES (?, ?, ?)
            """,
            (
                (layer_id, encoder_index, action_type)
                for encoder_index in range(ENCODER_COUNT)
                for action_type in ENCODER_ACTION_TYPES
            ),
        )

        return layer_id

    def list_profiles(self) -> list[dict]:
        """Return profile summaries for the toolbar."""
        with self.connect() as connection:
            rows = connection.execute(
                """
                SELECT id, name, created_at, updated_at
                FROM profiles
                ORDER BY name COLLATE NOCASE
                """
            ).fetchall()

        return [
            {
                "id": row["id"],
                "name": row["name"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
            }
            for row in rows
        ]

    def list_configured_buttons(self) -> list[dict]:
        """Return searchable descriptions of buttons configured in profiles."""
        with self.connect() as connection:
            rows = connection.execute(
                """
                SELECT
                    buttons.id,
                    buttons.button_index,
                    buttons.function_type,
                    buttons.command,
                    buttons.icon_data IS NOT NULL AS has_icon,
                    layers.layer_index,
                    layers.name AS layer_name,
                    profiles.id AS profile_id,
                    profiles.name AS profile_name
                FROM buttons
                JOIN layers ON layers.id = buttons.layer_id
                JOIN profiles ON profiles.id = layers.profile_id
                WHERE
                    buttons.function_type IS NOT NULL
                    OR buttons.command IS NOT NULL
                    OR buttons.icon_data IS NOT NULL
                ORDER BY
                    profiles.name COLLATE NOCASE,
                    layers.layer_index,
                    buttons.button_index
                """
            ).fetchall()

        return [
            {
                "id": row["id"],
                "button_index": row["button_index"],
                "function_type": row["function_type"],
                "command": row["command"],
                "has_icon": bool(row["has_icon"]),
                "layer_index": row["layer_index"],
                "layer_name": row["layer_name"],
                "profile_id": row["profile_id"],
                "profile_name": row["profile_name"],
            }
            for row in rows
        ]

    def load_button(self, button_id: int) -> dict | None:
        """Load one button, including its image BLOB, by database ID."""
        with self.connect() as connection:
            row = connection.execute(
                """
                SELECT
                    id,
                    layer_id,
                    button_index,
                    function_type,
                    command,
                    icon_data
                FROM buttons
                WHERE id = ?
                """,
                (button_id,),
            ).fetchone()

        return dict(row) if row is not None else None

    def load_profile(self, profile_id: int) -> dict | None:
        """Load a complete profile as nested ordinary Python data."""
        with self.connect() as connection:
            profile_row = connection.execute(
                """
                SELECT id, name, created_at, updated_at
                FROM profiles
                WHERE id = ?
                """,
                (profile_id,),
            ).fetchone()

            if profile_row is None:
                return None

            layer_rows = connection.execute(
                """
                SELECT id, layer_index, name
                FROM layers
                WHERE profile_id = ?
                ORDER BY layer_index
                """,
                (profile_id,),
            ).fetchall()

            layers = []
            for layer_row in layer_rows:
                layer_id = layer_row["id"]
                button_rows = connection.execute(
                    """
                    SELECT
                        id,
                        button_index,
                        function_type,
                        command,
                        icon_data
                    FROM buttons
                    WHERE layer_id = ?
                    ORDER BY button_index
                    """,
                    (layer_id,),
                ).fetchall()
                encoder_rows = connection.execute(
                    """
                    SELECT
                        id,
                        encoder_index,
                        action_type,
                        function_type,
                        command
                    FROM encoder_actions
                    WHERE layer_id = ?
                    ORDER BY encoder_index, action_type
                    """,
                    (layer_id,),
                ).fetchall()

                encoders = [
                    {
                        "encoder_index": encoder_index,
                        "actions": {},
                    }
                    for encoder_index in range(ENCODER_COUNT)
                ]

                for row in encoder_rows:
                    encoders[row["encoder_index"]]["actions"][row["action_type"]] = {
                        "id": row["id"],
                        "function_type": row["function_type"],
                        "command": row["command"],
                    }

                layers.append(
                    {
                        "id": layer_id,
                        "layer_index": layer_row["layer_index"],
                        "name": layer_row["name"],
                        "buttons": [dict(row) for row in button_rows],
                        "encoders": encoders,
                    }
                )

        return {
            "id": profile_row["id"],
            "name": profile_row["name"],
            "created_at": profile_row["created_at"],
            "updated_at": profile_row["updated_at"],
            "layers": layers,
        }

    def update_button(
        self,
        layer_id: int,
        button_index: int,
        function_type: str | None,
        command: str | None,
        icon_data: bytes | None,
    ) -> None:
        """Save the current state of one macro button."""
        with self.connect() as connection:
            cursor = connection.execute(
                """
                UPDATE buttons
                SET function_type = ?, command = ?, icon_data = ?
                WHERE layer_id = ? AND button_index = ?
                """,
                (
                    function_type,
                    command,
                    icon_data,
                    layer_id,
                    button_index,
                ),
            )

            if cursor.rowcount == 0:
                raise ValueError("The requested button does not exist.")

    def update_encoder_action(
        self,
        layer_id: int,
        encoder_index: int,
        action_type: str,
        function_type: str | None,
        command: str | None,
    ) -> None:
        """Save one direction or press action belonging to an encoder."""
        if action_type not in ENCODER_ACTION_TYPES:
            raise ValueError(f"Invalid encoder action type: {action_type}")

        with self.connect() as connection:
            cursor = connection.execute(
                """
                UPDATE encoder_actions
                SET function_type = ?, command = ?
                WHERE
                    layer_id = ?
                    AND encoder_index = ?
                    AND action_type = ?
                """,
                (
                    function_type,
                    command,
                    layer_id,
                    encoder_index,
                    action_type,
                ),
            )

            if cursor.rowcount == 0:
                raise ValueError("The requested encoder action does not exist.")

    def rename_profile(self, profile_id: int, new_name: str) -> None:
        new_name = new_name.strip()
        if not new_name:
            raise ValueError("A profile name cannot be empty.")

        try:
            with self.connect() as connection:
                cursor = connection.execute(
                    """
                    UPDATE profiles
                    SET name = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                    """,
                    (new_name, profile_id),
                )
                if cursor.rowcount == 0:
                    raise ValueError("The requested profile does not exist.")
        except sqlite3.IntegrityError as error:
            raise ValueError(
                f'A profile named "{new_name}" already exists.'
            ) from error

    def rename_layer(self, layer_id: int, new_name: str) -> None:
        """Rename one layer and mark its profile as updated."""
        new_name = new_name.strip()
        if not new_name:
            raise ValueError("A layer name cannot be empty.")

        with self.connect() as connection:
            layer = connection.execute(
                """
                SELECT profile_id
                FROM layers
                WHERE id = ?
                """,
                (layer_id,),
            ).fetchone()

            if layer is None:
                raise ValueError("The requested layer does not exist.")

            profile_id = layer["profile_id"]
            duplicate = connection.execute(
                """
                SELECT 1
                FROM layers
                WHERE profile_id = ?
                  AND id != ?
                  AND name = ? COLLATE NOCASE
                """,
                (profile_id, layer_id, new_name),
            ).fetchone()

            if duplicate is not None:
                raise ValueError(
                    f'A layer named "{new_name}" already exists in this profile.'
                )

            connection.execute(
                """
                UPDATE layers
                SET name = ?
                WHERE id = ?
                """,
                (new_name, layer_id),
            )
            connection.execute(
                """
                UPDATE profiles
                SET updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (profile_id,),
            )

    def delete_profile(self, profile_id: int) -> None:
        with self.connect() as connection:
            cursor = connection.execute(
                "DELETE FROM profiles WHERE id = ?",
                (profile_id,),
            )

            if cursor.rowcount == 0:
                raise ValueError("The requested profile does not exist.")
