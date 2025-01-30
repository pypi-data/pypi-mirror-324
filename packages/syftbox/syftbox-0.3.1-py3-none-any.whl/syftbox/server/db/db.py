import sqlite3
from pathlib import Path
from typing import Optional

from syftbox.lib.permissions import PermissionRule, SyftPermission
from syftbox.server.models.sync_models import FileMetadata, RelativePath


def save_file_metadata(conn: sqlite3.Connection, metadata: FileMetadata) -> None:
    # Insert the metadata into the database or update if a conflict on 'path' occurs
    conn.execute(
        """
    INSERT INTO file_metadata (path, datasite, hash, signature, file_size, last_modified)
    VALUES (?, ?, ?, ?, ?, ?)
    ON CONFLICT(path) DO UPDATE SET
        datasite = excluded.datasite,
        hash = excluded.hash,
        signature = excluded.signature,
        file_size = excluded.file_size,
        last_modified = excluded.last_modified
    """,
        (
            str(metadata.path),
            metadata.datasite,
            metadata.hash,
            metadata.signature,
            metadata.file_size,
            metadata.last_modified.isoformat(),
        ),
    )


def delete_file_metadata(conn: sqlite3.Connection, path: str) -> None:
    cur = conn.execute("DELETE FROM file_metadata WHERE path = ?", (path,))
    # get number of changes
    if cur.rowcount != 1:
        raise ValueError(f"Failed to delete metadata for {path}.")


def get_all_metadata(conn: sqlite3.Connection, path_like: Optional[str] = None) -> list[FileMetadata]:
    query = "SELECT * FROM file_metadata"
    params: tuple = ()

    if path_like:
        if "%" in path_like:
            raise ValueError("we don't support % in paths")
        path_like = path_like + "%"
        escaped_path = path_like.replace("_", "\\_")
        query += " WHERE path LIKE ? ESCAPE '\\' "
        params = (escaped_path,)

    cursor = conn.execute(query, params)
    # would be nice to paginate
    return [FileMetadata.from_row(row) for row in cursor]


def get_one_metadata(conn: sqlite3.Connection, path: str) -> FileMetadata:
    cursor = conn.execute("SELECT * FROM file_metadata WHERE path = ?", (path,))
    rows = cursor.fetchall()
    if len(rows) == 0 or len(rows) > 1:
        raise ValueError(f"Expected 1 metadata entry for {path}, got {len(rows)}")
    row = rows[0]
    return FileMetadata.from_row(row)


def get_all_datasites(conn: sqlite3.Connection) -> list[str]:
    # INSTR(path, '/'): Finds the position of the first slash in the path.
    cursor = conn.execute(
        """SELECT DISTINCT SUBSTR(path, 1, INSTR(path, '/') - 1) AS root_folder
        FROM file_metadata;
        """
    )
    return [row[0] for row in cursor if row[0]]


def query_rules_for_permfile(cursor: sqlite3.Cursor, file: SyftPermission) -> list[sqlite3.Row]:
    cursor.execute(
        """
        SELECT * FROM rules WHERE permfile_path = ? ORDER BY priority
    """,
        (file.relative_filepath.as_posix(),),
    )
    return cursor.fetchall()


def get_rules_for_permfile(connection: sqlite3.Connection, file: SyftPermission) -> list[PermissionRule]:
    cursor = connection.cursor()
    return [PermissionRule.from_db_row(row) for row in query_rules_for_permfile(cursor, file)]


def get_all_files(cursor: sqlite3.Cursor) -> list:
    cursor.execute(
        """
        SELECT * FROM file_metadata
    """
    )
    return cursor.fetchall()


def get_all_files_under_syftperm(cursor: sqlite3.Cursor, permfile: SyftPermission) -> list[tuple[int, FileMetadata]]:
    cursor.execute(
        """
        SELECT * FROM file_metadata WHERE path LIKE ?
    """,
        (str(permfile.dir_path) + "/%",),
    )
    return [
        (
            row["id"],
            FileMetadata.from_row(row),
        )
        for row in cursor.fetchall()
    ]


def get_rules_for_path(connection: sqlite3.Connection, path: Path) -> list[PermissionRule]:
    parents = path.parents
    placeholders = ",".join("?" * len(parents))
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT * FROM rules WHERE permfile_dir in ({})
    """.format(placeholders),
        [x.as_posix() for x in parents],
    )
    return [PermissionRule.from_db_row(row) for row in cursor.fetchall()]


def set_rules_for_permfile(connection: sqlite3.Connection, file: SyftPermission) -> None:
    """
    Atomically set the rules for a permission file. Basically its just a write operation, but
    we also make sure we delete the rules that are no longer in the file.
    """
    try:
        cursor = connection.cursor()

        cursor.execute(
            """
        DELETE FROM rules
        WHERE permfile_path = ?
        """,
            (str(file.relative_filepath),),
        )

        # TODO
        files_under_dir = get_all_files_under_syftperm(cursor, file)

        rule2files = []

        for rule in file.rules:
            for _id, file_in_dir in files_under_dir:
                match, match_for_email = rule.filepath_matches_rule_path(file_in_dir.path)
                if match:
                    rule2files.append([str(rule.permfile_path), rule.priority, _id, match_for_email])

        rule_rows = [tuple(rule.to_db_row().values()) for rule in file.rules]

        cursor.executemany(
            """
        INSERT INTO rules (
            permfile_path, permfile_dir, permfile_depth, priority, path, user,
            can_read, can_create, can_write, admin, disallow
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(permfile_path, priority) DO UPDATE SET
            path = excluded.path,
            user = excluded.user,
            can_read = excluded.can_read,
            can_create = excluded.can_create,
            can_write = excluded.can_write,
            admin = excluded.admin,
            disallow = excluded.disallow
        """,
            rule_rows,
        )

        cursor.executemany(
            """
            INSERT INTO rule_files (permfile_path, priority, file_id, match_for_email) VALUES (?, ?, ?, ?)
            ON CONFLICT(permfile_path, priority, file_id) DO UPDATE SET match_for_email = excluded.match_for_email
        """,
            rule2files,
        )

    except Exception as e:
        connection.rollback()
        raise e


def get_metadata_for_file(connection: sqlite3.Connection, path: Path) -> tuple[int, FileMetadata]:
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM file_metadata WHERE path = ?", (str(path),))
    row = cursor.fetchone()
    return (
        row["id"],
        FileMetadata.from_row(row),
    )


def link_existing_rules_to_file(connection: sqlite3.Connection, path: Path) -> None:
    # 1 find all rules in that branch of the tree
    # 2 check which rules apply to the file
    # 3 link them

    perm_rules = get_rules_for_path(connection, path)

    rule2files = []
    _id, _ = get_metadata_for_file(connection, path)

    for rule in perm_rules:
        match, match_for_email = rule.filepath_matches_rule_path(path)
        if match:
            rule2files.append([str(rule.permfile_path), rule.priority, _id, match_for_email])
    cursor = connection.cursor()
    cursor.executemany(
        """
        INSERT INTO rule_files (permfile_path, priority, file_id, match_for_email) VALUES (?, ?, ?, ?)
        ON CONFLICT(permfile_path, priority, file_id) DO UPDATE SET
            match_for_email = excluded.match_for_email
    """,
        rule2files,
    )


def get_read_permissions_for_user(
    connection: sqlite3.Connection, user: str, path_like: Optional[str] = None
) -> list[sqlite3.Row]:
    """
    Get all files that the user has read access to. First we get all files, then we do a subquery for every file.
    For every file, we join all the rules that apply to it for this user. As an intermediate result, we get all those
    rules, which we reduce into a single value. To do this, we add extra columns to the table indicating rule priority.
    For all rules, later rules overwrite earlier ones, so you only need to check the
    last rule for a permission. By overwriting, we mean that if a disallow comes after an allow, you have no read
    permission. The default is no read permission.

    We use these row orderings to find if the last read is either a disallow or allow

    We do the same for admin permissions. We then compute two things:
    - The admin "bit" (indicating whether a user has admin permissions)
    - The read "bit" (indicating whether a user has read permissions)

    These bits are combined with a final OR operation.
    """
    cursor = connection.cursor()

    params: tuple = (user, user, user)
    like_clause = ""
    if path_like:
        if "%" in path_like:
            raise ValueError("we don't support % in paths")
        path_like = path_like + "%"
        escaped_path = path_like.replace("_", "\\_")
        like_clause += " WHERE path LIKE ? ESCAPE '\\' "
        params = (user, user, user, escaped_path)

    query = """
    SELECT path, hash, signature, file_size, last_modified,
    (
        SELECT COALESCE(
            max(
                CASE
                    WHEN can_read AND NOT disallow THEN rule_prio
                    ELSE 0
                END
            ) >
            max(
                CASE
                    WHEN can_read AND disallow THEN rule_prio
                    ELSE 0
                END
        ), 0)
        or
        COALESCE(
            max(
                CASE
                    WHEN admin AND NOT disallow THEN rule_prio
                    ELSE 0
                END
            ) >
            max(
                CASE
                    WHEN admin AND disallow THEN rule_prio
                    ELSE 0
                END
        ), 0)
        FROM (
            SELECT can_read, admin, disallow,
                row_number() OVER (ORDER BY rules.permfile_depth, rules.priority ASC) AS rule_prio
            FROM rule_files
            JOIN rules ON rule_files.permfile_path = rules.permfile_path and rule_files.priority = rules.priority
            WHERE rule_files.file_id = f.id and (rules.user = ? or rules.user = "*" or rule_files.match_for_email = ?)
        )
    ) OR datasite = ? AS read_permission
    FROM file_metadata f
    {}
    """.format(like_clause)
    res = cursor.execute(query, params)

    return res.fetchall()


def print_table(connection: sqlite3.Connection, table: str) -> None:
    """util function for debugging"""
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()
    for i, row in enumerate(rows):
        if i == 0:
            print("  |  ".join(dict(row).keys()))
        print("  |  ".join(str(x) for x in list(dict(row).values())))


def get_filemetadata_with_read_access(
    connection: sqlite3.Connection, user: str, path: Optional[RelativePath] = None
) -> list[FileMetadata]:
    rows = get_read_permissions_for_user(connection, user, str(path))
    res = [FileMetadata.from_row(row) for row in rows if row["read_permission"]]
    return res
